"""
Functions for syncing iMessage data to PostgreSQL.
"""
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from sqlalchemy.orm import Session

from imessage_sync.config import settings
from imessage_sync.db.postgres import DBHandle, DBMessage, init_db
from imessage_sync.models import Handle, Message


def get_imessage_db_connection() -> sqlite3.Connection:
    """
    Establish a connection to the iMessage SQLite database.

    Returns:
        sqlite3.Connection: Connection to the iMessage database

    Raises:
        FileNotFoundError: If the iMessage database file doesn't exist
        PermissionError: If the script doesn't have permission to access the database
    """
    db_path = settings.MESSAGES_DB_PATH

    if not db_path.exists():
        raise FileNotFoundError(f"iMessage database not found at {db_path}")

    try:
        # Use URI mode to open read-only
        conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.OperationalError as e:
        if "unable to open database file" in str(e):
            raise PermissionError(
                f"Unable to access iMessage database at {db_path}. "
                "Make sure Terminal has Full Disk Access permissions in "
                "System Preferences > Security & Privacy > Privacy."
            ) from e
        raise


def get_messages(days: int = None) -> List[Message]:
    """
    Retrieve messages from the iMessage database.

    Args:
        days: Number of days to look back for messages. If None, gets all messages.

    Returns:
        List[Message]: List of messages from the iMessage database
    """
    conn = get_imessage_db_connection()

    # Build query with optional date filter
    query = """
    SELECT
        message.ROWID as message_id,
        message.text,
        message.date,
        message.is_from_me,
        message.service,
        message.handle_id,
        handle.id as sender_id,
        message.cache_roomnames,
        message.was_downgraded,
        message.subject,
        message.is_read,
        message.is_delivered,
        message.is_sent,
        message.item_type,
        message.group_title
    FROM
        message
    LEFT JOIN handle ON message.handle_id = handle.ROWID
    WHERE
        message.text IS NOT NULL
    """

    params = []
    if days is not None:
        # Apple's epoch starts at 2001-01-01
        apple_epoch = datetime(2001, 1, 1)
        start_date = datetime.now() - timedelta(days=days)
        # Convert to Apple's timestamp format (seconds since 2001-01-01 × 1000000000)
        start_timestamp = int((start_date - apple_epoch).total_seconds() * 1000000000)

        query += " AND message.date >= ?"
        params.append(start_timestamp)

    query += " ORDER BY message.date DESC"

    if settings.MESSAGE_BATCH_SIZE:
        query += f" LIMIT {settings.MESSAGE_BATCH_SIZE}"

    # Execute query
    cursor = conn.execute(query, params)

    # Process results
    messages = []
    for row in cursor:
        # Convert Apple's timestamp to Python datetime
        date_value = row["date"]
        if date_value:
            # Convert from nanoseconds to seconds since 2001-01-01
            seconds_since_apple_epoch = date_value / 1000000000
            # Add seconds to Apple epoch to get datetime
            message_date = datetime(2001, 1, 1) + timedelta(seconds=seconds_since_apple_epoch)
        else:
            message_date = datetime.now()

        # Create Message object
        messages.append(
            Message(
                message_id=row["message_id"],
                text=row["text"],
                date=message_date,
                is_from_me=bool(row["is_from_me"]),
                service=row["service"] or "iMessage",
                handle_id=row["handle_id"],
                sender_id=row["sender_id"],
                conversation_id=row["cache_roomnames"],
                subject=row["subject"],
                was_downgraded=bool(row["was_downgraded"]) if row["was_downgraded"] is not None else None,
                is_read=bool(row["is_read"]) if row["is_read"] is not None else None,
                is_delivered=bool(row["is_delivered"]) if row["is_delivered"] is not None else None,
                is_sent=bool(row["is_sent"]) if row["is_sent"] is not None else None,
                item_type=row["item_type"],
                group_title=row["group_title"],
            )
        )

    conn.close()
    return messages


def get_handles() -> List[Handle]:
    """
    Retrieve handles (chat recipients) from the iMessage database.

    Returns:
        List[Handle]: List of handles from the iMessage database
    """
    conn = get_imessage_db_connection()

    query = """
    SELECT
        ROWID as handle_id,
        id as identifier,
        service,
        country,
        service_center,
        uncanonicalized_id
    FROM
        handle
    """

    cursor = conn.execute(query)

    handles = []
    for row in cursor:
        handles.append(
            Handle(
                handle_id=row["handle_id"],
                identifier=row["identifier"],
                service=row["service"] or "iMessage",
                country=row["country"],
                service_center=row["service_center"],
                uncanonicalized_id=row["uncanonicalized_id"],
            )
        )

    conn.close()
    return handles


def sync_messages_to_postgres(db: Session, days: Optional[int] = None) -> Tuple[int, int]:
    """
    Sync messages from iMessage database to PostgreSQL.

    Args:
        db: SQLAlchemy database session
        days: Number of days to look back for messages. If None, uses settings.MESSAGE_SYNC_DAYS

    Returns:
        Tuple[int, int]: Tuple of (number of messages synced, number of handles synced)
    """
    if days is None:
        days = settings.MESSAGE_SYNC_DAYS

    # First sync handles to make sure we have all the references
    handles = get_handles()
    handle_count = sync_handles_to_postgres(db, handles)

    # Get handle_id to database id mapping for faster lookups
    handle_mapping = {h.handle_id: h.id for h in db.query(DBHandle.handle_id, DBHandle.id).all()}

    # Now sync messages
    messages = get_messages(days)

    # Check which message IDs already exist in the database
    existing_message_ids = {
        m[0] for m in db.query(DBMessage.message_id).filter(
            DBMessage.message_id.in_([m.message_id for m in messages])
        ).all()
    }

    # Filter out messages that already exist
    new_messages = [m for m in messages if m.message_id not in existing_message_ids]

    # Insert new messages
    for message in new_messages:
        db_message = DBMessage(
            message_id=message.message_id,
            text=message.text,
            date=message.date,
            is_from_me=message.is_from_me,
            service=message.service,
            handle_id=message.handle_id,
            sender_id=message.sender_id,
            conversation_id=message.conversation_id,
            subject=message.subject,
            was_downgraded=message.was_downgraded,
            is_read=message.is_read,
            is_delivered=message.is_delivered,
            is_sent=message.is_sent,
            item_type=message.item_type,
            group_title=message.group_title,
            synced_to_postgres=datetime.now(),
        )
        db.add(db_message)

    db.commit()
    return len(new_messages), handle_count


def sync_handles_to_postgres(db: Session, handles: List[Handle] = None) -> int:
    """
    Sync handles from iMessage database to PostgreSQL.

    Args:
        db: SQLAlchemy database session
        handles: Optional list of handles. If None, will fetch from iMessage database.

    Returns:
        int: Number of new handles synced
    """
    if handles is None:
        handles = get_handles()

    # Check which handles already exist
    existing_handle_ids = {
        h[0] for h in db.query(DBHandle.handle_id).filter(
            DBHandle.handle_id.in_([h.handle_id for h in handles])
        ).all()
    }

    # Filter out handles that already exist
    new_handles = [h for h in handles if h.handle_id not in existing_handle_ids]

    # Insert new handles
    for handle in new_handles:
        db_handle = DBHandle(
            handle_id=handle.handle_id,
            identifier=handle.identifier,
            service=handle.service,
            country=handle.country,
            service_center=handle.service_center,
            uncanonicalized_id=handle.uncanonicalized_id,
            contact_name=handle.contact_name,
            synced_to_postgres=datetime.now(),
        )
        db.add(db_handle)

    db.commit()
    return len(new_handles)
