#! /bin/bash
# iMessage Export Script
# Save this as imessage-export.sh and make executable with: chmod +x imessage-export.sh

# Get date for filename
DATE=$(date +"%Y-%m-%d")
OUTPUT_FILE="$HOME/Documents/imessage_export_$DATE.csv"

# Create CSV header
echo "Date,Sender,Message,Is_From_Me" > "$OUTPUT_FILE"

# Run SQL query on Messages database
sqlite3 -csv ~/Library/Messages/chat.db "
SELECT
    datetime(message.date/1000000000 + strftime('%s', '2001-01-01'), 'unixepoch', 'localtime') AS message_date,
    handle.id AS contact,
    message.text AS message_text,
    message.is_from_me
FROM
    message
    LEFT JOIN handle ON message.handle_id = handle.ROWID
WHERE
    message.text IS NOT NULL
ORDER BY
    message.date DESC
LIMIT 5000;" >> "$OUTPUT_FILE"

echo "Export complete! File saved to: $OUTPUT_FILE"
open "$OUTPUT_FILE"
