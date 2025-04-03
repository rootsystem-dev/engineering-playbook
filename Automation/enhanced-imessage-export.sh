#!/bin/bash
# Enhanced iMessage Export Script with Contact Names
# Save this as enhanced-imessage-export.sh and make executable with: chmod +x enhanced-imessage-export.sh

# variables for messages limit and date range for the query
MESSAGES_LIMIT=1000

START_DATE="2023-01-01"
END_DATE="2023-12-31"

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

# Create a temporary AppleScript file to get contact information
TEMP_SCRIPT="/tmp/get_contacts.scpt"
cat > "$TEMP_SCRIPT" << 'EOF'
on run
    tell application "Contacts"
        set allContacts to {}
        repeat with eachContact in every person
            set phoneNumbers to {}
            set emailAddresses to {}

            -- Get phone numbers
            repeat with eachPhone in phone values of eachContact
                set phoneNumbers to phoneNumbers & eachPhone
            end repeat

            -- Get email addresses
            repeat with eachEmail in email values of eachContact
                set emailAddresses to emailAddresses & eachEmail
            end repeat

            -- Create a record with name, phones, and emails
            set contactName to name of eachContact
            set end of allContacts to {name:contactName, phones:phoneNumbers, emails:emailAddresses}
        end repeat

        return allContacts
    end tell
end run
EOF

# Run the AppleScript to get contacts data and store it in a temporary JSON file
CONTACTS_JSON="/tmp/contacts_data.json"
osascript -l "JavaScript" -e "
    function run() {
        const contacts = Application('Contacts');
        const people = contacts.people();

        let contactsData = [];
        people.forEach(person => {
            let phones = [];
            let emails = [];

            // Get phone numbers
            if (person.phoneNumbers) {
                person.phoneNumbers().forEach(phone => {
                    phones.push(phone.value());
                });
            }

            // Get email addresses
            if (person.emailAddresses) {
                person.emailAddresses().forEach(email => {
                    emails.push(email.value());
                });
            }

            contactsData.push({
                name: person.name(),
                phones: phones,
                emails: emails
            });
        });

        return JSON.stringify(contactsData);
    }
" > "$CONTACTS_JSON"

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
    message.text IS NOT NULL AND message.date >= $START_DATE AND message.date <= $END_DATE
ORDER BY
    message.date DESC
LIMIT $MESSAGES_LIMIT;" > /tmp/messages.csv

# Process the results and look up contact names
python3 -c "
import csv
import json
import re

# Load contacts data
with open('$CONTACTS_JSON', 'r') as f:
    contacts_data = json.load(f)

# Create a lookup dictionary for faster matching
contact_lookup = {}
for contact in contacts_data:
    # Normalize and add phone numbers
    for phone in contact['phones']:
        # Remove all non-digit characters for comparison
        normalized = re.sub(r'\\D', '', phone)
        # Store different lengths for better matching chances
        if len(normalized) >= 10:
            contact_lookup[normalized[-10:]] = contact['name']  # Last 10 digits
        if normalized:
            contact_lookup[normalized] = contact['name']

    # Add email addresses
    for email in contact['emails']:
        contact_lookup[email.lower()] = contact['name']

# Process messages and add contact names
with open('/tmp/messages.csv', 'r') as infile, open('$OUTPUT_FILE', 'a') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    for row in reader:
        message_date, sender_id, message_text, is_from_me = row

        # Skip if any required field is missing
        if not all([message_date, sender_id, is_from_me]):
            continue

        # Look up contact name
        contact_name = 'Unknown'

        # Try exact match first
        if sender_id in contact_lookup:
            contact_name = contact_lookup[sender_id]
        else:
            # Try normalizing phone number
            normalized = re.sub(r'\\D', '', sender_id)
            if normalized in contact_lookup:
                contact_name = contact_lookup[normalized]
            # Try last 10 digits for US numbers
            elif len(normalized) >= 10 and normalized[-10:] in contact_lookup:
                contact_name = contact_lookup[normalized[-10:]]

        # Write the row with the contact name
        writer.writerow([message_date, sender_id, contact_name, message_text, is_from_me])
"

# Clean up temporary files
# if cleanup succeeds, echo message
if rm /tmp/messages.csv "$CONTACTS_JSON" "$TEMP_SCRIPT"; then
    echo "Temporary files cleaned up successfully."
else
    echo "Failed to clean up temporary files."
fi

echo "Enhanced export complete! File saved to: $OUTPUT_FILE"
open "$OUTPUT_FILE"
