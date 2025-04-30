# iMessage Sync

A Python application to sync iMessage and Contacts data from macOS to PostgreSQL.

## Structure
imessage-sync/
├── pyproject.toml
├── .gitignore
├── README.md
├── src/
│   ├── imessage_sync/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── models.py
│   │   ├── db/
│   │   │   ├── __init__.py
│   │   │   ├── postgres.py
│   │   ├── sync/
│   │   │   ├── __init__.py
│   │   │   ├── messages.py
│   │   │   ├── contacts.py
│   │   ├── utils/
│   │   │   ├── __init__.py
│   │   │   ├── apple_utils.py
├── scripts/
│   ├── sync_contacts.py
│   ├── sync_messages.py
├── tests/
│   ├── __init__.py
│   ├── test_messages.py
│   ├── test_contacts.py

## Features

- Export iMessage conversations to PostgreSQL
- Export macOS Contacts to PostgreSQL
- Match contacts with messages for better analytics
- Supports periodic syncing

## Prerequisites

- macOS (for access to Messages.app and Contacts.app)
- Python 3.10+
- PostgreSQL database
- UV package manager (recommended)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/imessage-sync.git
   cd imessage-sync
   ```

2. Set up a virtual environment with UV:
   ```bash
   uv venv
   source .venv/bin/activate
   ```

3. Install the package in development mode:
   ```bash
   uv pip install -e ".[dev]"
   ```

4. Create a `.env` file with your PostgreSQL credentials:
   ```
   DATABASE_URL=postgresql://username:password@localhost:5432/imessage_db
   ```

## Usage

### Sync Contacts

```bash
python scripts/sync_contacts.py
```

### Sync Messages

```bash
python scripts/sync_messages.py
```

## Permissions

This application requires access to:

1. Your macOS Contacts database
2. Your iMessage database (~/Library/Messages/chat.db)

You may need to grant "Full Disk Access" to Terminal or your Python interpreter in System Preferences > Security & Privacy > Privacy.

## Database Schema

### Messages Table
- id (UUID, primary key)
- message_id (from iMessage)
- sender_id
- text
- date_sent
- is_from_me
- conversation_id
- service
- handle_id
- ...

### Contacts Table
- id (UUID, primary key)
- contact_id (from Contacts)
- first_name
- last_name
- full_name
- phones (array)
- emails (array)
- ...

## License

MIT