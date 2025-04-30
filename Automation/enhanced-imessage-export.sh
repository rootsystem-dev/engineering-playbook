#!/bin/bash
# Enhanced iMessage Export Script with Contact Names
# Save this as enhanced-imessage-export.sh and make executable with: chmod +x enhanced-imessage-export.sh

# variables for messages limit and date range for the query
MESSAGES_LIMIT=5000

#default start date to 8 years ago
START_DATE=$(date -v-8y +"%Y-%m-%d")
#default end date to today
END_DATE=$(date +"%Y-%m-%d")

# convert dates to timestamps for queries
# Convert date strings to Apple's timestamp format (seconds since 2001-01-01 × 1000000000)
START_TIMESTAMP=$(date -j -f "%Y-%m-%d" "$START_DATE" "+%s")
START_TIMESTAMP=$((($START_TIMESTAMP - $(date -j -f "%Y-%m-%d" "2001-01-01" "+%s")) * 1000000000))

END_TIMESTAMP=$(date -j -f "%Y-%m-%d" "$END_DATE" "+%s")
# Add 86400 seconds (1 day) to include the full end date
END_TIMESTAMP=$((($END_TIMESTAMP + 86400 - $(date -j -f "%Y-%m-%d" "2001-01-01" "+%s")) * 1000000000))

# Get date for filename
DATE=$(date +"%Y-%m-%d")
OUTPUT_FILE="$HOME/Desktop/imessage_export_enhanced_$DATE.csv"

# Create contacts data using AppleScript
CONTACTS_FILE="/tmp/contacts_data.txt"

# Fixed AppleScript to get contacts
osascript <<EOT > "$CONTACTS_FILE"
tell application "Contacts"
    set contactsList to ""
    repeat with eachPerson in every person
        set personName to name of eachPerson
        
        -- Get phone numbers
        set phoneList to ""
        set phoneItems to {}
        try
            set phoneItems to phones of eachPerson
        end try
        
        repeat with phoneItem in phoneItems
            try
                set phoneValue to value of phoneItem
                set phoneList to phoneList & phoneValue & "|"
            end try
        end repeat
        
        -- Get email addresses
        set emailList to ""
        set emailItems to {}
        try
            set emailItems to emails of eachPerson
        end try
        
        repeat with emailItem in emailItems
            try
                set emailValue to value of emailItem
                set emailList to emailList & emailValue & "|"
            end try
        end repeat
        
        -- Add contact to the list
        set contactsList to contactsList & personName & "§" & phoneList & "§" & emailList & return
    end repeat
    
    return contactsList
end tell
EOT

# Create CSV header
echo "Date,Sender ID,Sender Name,Message,Is From Me" > "$OUTPUT_FILE"

# Run SQL query on Messages database to get message data
sqlite3 -csv ~/Library/Messages/chat.db "
SELECT
    datetime(message.date/1000000000 + strftime('%s', '2001-01-01'), 'unixepoch', 'localtime') AS message_date,
    handle.id AS sender_id,
    message.text AS message_text,
    message.is_from_me
FROM
    message
    LEFT JOIN handle ON message.handle_id = handle.ROWID
WHERE
    message.text IS NOT NULL AND message.date >= $START_TIMESTAMP AND message.date <= $END_TIMESTAMP
ORDER BY
    message.date DESC
LIMIT $MESSAGES_LIMIT;" > /tmp/messages.csv

# Process the results and look up contact names
python3 -c "
import csv
import re
import os

# Debug information
print('Python processing started')
print(f'Messages file size: {os.path.getsize(\"/tmp/messages.csv\")} bytes')
print(f'Contacts file size: {os.path.getsize(\"$CONTACTS_FILE\")} bytes')

# Load contacts data using a simpler format
contact_lookup = {}
with open('$CONTACTS_FILE', 'r') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        
        # Use a different delimiter to avoid issues with commas in names
        parts = line.split('§')
        if len(parts) < 3:
            print(f'Skipping malformed contact entry: {line[:30]}...')
            continue
            
        name, phones_str, emails_str = parts
        
        # Process phones
        phones = phones_str.split('|')
        for phone in phones:
            if not phone:
                continue
                
            # Remove all non-digit characters for comparison
            normalized = re.sub(r'\\D', '', phone)
            
            # Store different lengths for better matching chances
            if len(normalized) >= 10:
                contact_lookup[normalized[-10:]] = name  # Last 10 digits
            if normalized:
                contact_lookup[normalized] = name
        
        # Process emails
        emails = emails_str.split('|')
        for email in emails:
            if not email:
                continue
            contact_lookup[email.lower()] = name

print(f'Loaded {len(contact_lookup)} contact identifiers')

# Process messages and add contact names
matched_count = 0
total_count = 0

with open('/tmp/messages.csv', 'r') as infile, open('$OUTPUT_FILE', 'a') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    
    for row in reader:
        if len(row) < 4:
            print(f'Skipping incomplete row: {row}')
            continue
            
        message_date, sender_id, message_text, is_from_me = row
        total_count += 1
        
        # Skip if any required field is missing
        if not all([message_date, sender_id, is_from_me]):
            continue
            
        # Look up contact name
        contact_name = 'Unknown'
        
        # Try exact match first
        if sender_id.lower() in contact_lookup:
            contact_name = contact_lookup[sender_id.lower()]
            matched_count += 1
        else:
            # Try normalizing phone number
            normalized = re.sub(r'\\D', '', sender_id)
            if normalized in contact_lookup:
                contact_name = contact_lookup[normalized]
                matched_count += 1
            # Try last 10 digits for US numbers
            elif len(normalized) >= 10 and normalized[-10:] in contact_lookup:
                contact_name = contact_lookup[normalized[-10:]]
                matched_count += 1
        
        # Write the row with the contact name
        writer.writerow([message_date, sender_id, contact_name, message_text, is_from_me])

print(f'Matched {matched_count} out of {total_count} messages with contact names')
"

# Clean up temporary files
if rm /tmp/messages.csv "$CONTACTS_FILE"; then
    echo "Temporary files cleaned up successfully."
else
    echo "Failed to clean up temporary files."
fi

echo "Enhanced export complete! File saved to: $OUTPUT_FILE"
open "$OUTPUT_FILE"