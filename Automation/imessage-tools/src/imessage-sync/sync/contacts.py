"""
Functions for syncing macOS Contacts to PostgreSQL.
"""
import json
import re
import subprocess
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from sqlalchemy.orm import Session

from imessage_sync.db.postgres import DBContact, DBHandle
from imessage_sync.models import Contact


def get_contacts_from_applescript() -> List[Contact]:
    """
    Retrieve contacts from macOS Contacts app using AppleScript.
    
    Returns:
        List[Contact]: List of contacts from the macOS Contacts app
    
    Raises:
        subprocess.CalledProcessError: If the AppleScript execution fails
    """
    # Create AppleScript to extract contacts
    applescript = """
    tell application "Contacts"
        set allContacts to {}
        repeat with eachPerson in every person
            set personProps to {}
            
            -- Basic information
            copy {name:name of eachPerson} to personProps
            
            try
                copy {firstName:first name of eachPerson} to end of personProps
            on error
                copy {firstName:""} to end of personProps
            end try
            
            try
                copy {lastName:last name of eachPerson} to end of personProps
            on error
                copy {lastName:""} to end of personProps
            end try
            
            try
                copy {company:organization of eachPerson} to end of personProps
            on error
                copy {company:""} to end of personProps
            end try
            
            try
                copy {jobTitle:job title of eachPerson} to end of personProps
            on error
                copy {jobTitle:""} to end of personProps
            end try
            
            try
                copy {note:note of eachPerson} to end of personProps
            on error
                copy {note:""} to end of personProps
            end try
            
            -- Get phone numbers
            set phoneNumbers to {}
            set phoneItems to {}
            try
                set phoneItems to phones of eachPerson
            end try
            
            repeat with phoneItem in phoneItems
                try
                    set phoneValue to value of phoneItem
                    set end of phoneNumbers to phoneValue
                end try
            end repeat
            
            -- Get email addresses
            set emailAddresses to {}
            set emailItems to {}
            try
                set emailItems to emails of eachPerson
            end try
            
            repeat with emailItem in emailItems
                try
                    set emailValue to value of emailItem
                    set end of emailAddresses to emailValue
                end try
            end repeat
            
            -- Add all values to the contact
            copy {phones:phoneNumbers} to end of personProps
            copy {emails:emailAddresses} to end of personProps
            
            -- Add contact to result list
            set end of allContacts to personProps
        end repeat
        
        -- Convert to JSON
        return allContacts
    end tell
    """
    
    # Execute AppleScript
    try:
        result = subprocess.run(
            ["osascript", "-e", applescript],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Parse the output from AppleScript (which is in a specialized format)
        # This is a bit complex because the output isn't pure JSON
        contacts_data = result.stdout.strip()
        
        # Convert AppleScript record format to Python dict 
        # Replace AppleScript syntax with JSON syntax
        contacts_data = contacts_data.replace("{", "[").replace("}", "]")
        contacts_data = re.sub(r'([a-zA-Z]+):(.*?)(?=,\s*[a-zA-Z]+:|$|\])', r'["\1", \2]', contacts_data)
        
        # Now parse with Python
        parsed_data = eval(contacts_data)  # Using eval for AppleScript output
        
        # Convert to Contact objects
        contacts = []
        for contact_record in parsed_data:
            # Convert list of [key, value] pairs to dict
            contact_dict = {item[0]: item[1] for item in contact_record}
            
            contacts.append(
                Contact(
                    full_name=contact_dict.get("name", ""),
                    first_name=contact_dict.get("firstName", ""),
                    last_name=contact_dict.get("lastName", ""),
                    phones=contact_dict.get("phones", []),
                    emails=contact_dict.get("emails", []),
                    company=contact_dict.get("company", ""),
                    job_title=contact_dict.get("jobTitle", ""),
                    note=contact_dict.get("note", ""),
                )
            )
        
        return contacts
        
    except subprocess.CalledProcessError as e:
        print(f"Error executing AppleScript: {e}")
        print(f"Error output: {e.stderr}")
        raise


def sync_contacts_to_postgres(db: Session) -> int:
    """
    Sync contacts from macOS Contacts app to PostgreSQL.
    
    Args:
        db: SQLAlchemy database session
    
    Returns:
        int: Number of new contacts synced
    """
    contacts = get_contacts_from_applescript()
    
    # Check which contacts (by full name and phone/email) might already exist
    existing_contacts = {}
    for contact in db.query(DBContact).all():
        key = f"{contact.full_name}:{','.join(contact.phones)}:{','.join(contact.emails)}"
        existing_contacts[key] = contact
    
    # Filter out contacts that appear to be the same
    new_contacts = []
    for contact in contacts:
        key = f"{contact.full_name}:{','.join(contact.phones)}:{','.join(contact.emails)}"
        if key not in existing_contacts:
            new_contacts.append(contact)
    
    # Insert new contacts
    for contact in new_contacts:
        db_contact = DBContact(
            full_name=contact.full_name,
            first_name=contact.first_name,
            last_name=contact.last_name,
            phones=contact.phones,
            emails=contact.emails,
            company=contact.company,
            job_title=contact.job_title,
            note=contact.note,
            synced_to_postgres=datetime.now(),
        )
        db.add(db_contact)
    
    db.commit()
    
    # Now update handles with contact names
    update_handles_with_contact_names(db)
    
    return len(new_contacts)


def update_handles_with_contact_names(db: Session) -> int:
    """
    Update handles in the database with contact names based on phone/email matching.
    
    Args:
        db: SQLAlchemy database session
    
    Returns:
        int: Number of handles updated with contact names
    """
    # Get all contacts and create lookup dictionaries for phone and email
    phone_lookup = {}
    email_lookup = {}
    
    for contact in db.query(DBContact).all():
        for phone in contact.phones:
            # Normalize phone number (remove non-digits)
            normalized = re.sub(r'\D', '', phone)
            if normalized:
                phone_lookup[normalized] = contact.full_name
                # Also add the last 10 digits for better US number matching
                if len(normalized) >= 10:
                    phone_lookup[normalized[-10:]] = contact.full_name
        
        for email in contact.emails:
            email_lookup[email.lower()] = contact.full_name
    
    # Get all handles without contact names
    handles_to_update = db.query(DBHandle).filter(
        (DBHandle.contact_name.is_(None)) | (DBHandle.contact_name == "")
    ).all()
    
    # Update handles with contact names
    update_count = 0
    for handle in handles_to_update:
        contact_name = None
        
        # Check if identifier is an email
        if '@' in handle.identifier:
            contact_name = email_lookup.get(handle.identifier.lower())
        else:
            # Assume it's a phone number
            normalized = re.sub(r'\D', '', handle.identifier)
            if normalized:
                contact_name = phone_lookup.get(normalized)
                # Try last 10 digits
                if not contact_name and len(normalized) >= 10:
                    contact_name = phone_lookup.get(normalized[-10:])
        
        if contact_name:
            handle.contact_name = contact_name
            update_count += 1
    
    db.commit()
    return update_count