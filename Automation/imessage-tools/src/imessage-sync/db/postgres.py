"""
PostgreSQL database connection and schema definitions.
"""
import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer, String,
                        Table, create_engine)
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

from imessage_sync.config import settings

# Create SQLAlchemy engine
engine = create_engine(str(settings.DATABASE_URL), echo=settings.SQLALCHEMY_ECHO)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define base class for SQLAlchemy models
Base = declarative_base()


class DBMessage(Base):
    """SQLAlchemy model for messages."""

    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    message_id = Column(Integer, nullable=False, index=True)
    text = Column(String, nullable=True)
    date = Column(DateTime, nullable=False, index=True)
    is_from_me = Column(Boolean, nullable=False)
    service = Column(String, nullable=False)
    handle_id = Column(Integer, nullable=True)
    sender_id = Column(String, nullable=True)
    conversation_id = Column(String, nullable=True, index=True)
    subject = Column(String, nullable=True)
    associated_message_id = Column(Integer, nullable=True)
    associated_message_type = Column(Integer, nullable=True)
    cache_has_attachments = Column(Boolean, nullable=True)
    cache_roomnames = Column(String, nullable=True)
    was_downgraded = Column(Boolean, nullable=True)
    is_read = Column(Boolean, nullable=True)
    is_delivered = Column(Boolean, nullable=True)
    is_sent = Column(Boolean, nullable=True)
    is_finished = Column(Boolean, nullable=True)
    is_prepared = Column(Boolean, nullable=True)
    is_from_me_original = Column(Boolean, nullable=True)
    item_type = Column(Integer, nullable=True)
    group_title = Column(String, nullable=True)
    group_action_type = Column(Integer, nullable=True)
    share_status = Column(Integer, nullable=True)
    share_direction = Column(Integer, nullable=True)
    synced_to_postgres = Column(DateTime, default=datetime.now)

    # Relationships
    handle = relationship("DBHandle", foreign_keys=[handle_id],
                        primaryjoin="DBMessage.handle_id == DBHandle.handle_id",
                        uselist=False)


class DBContact(Base):
    """SQLAlchemy model for contacts."""

    __tablename__ = "contacts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(String, nullable=False, index=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    phones = Column(ARRAY(String), nullable=False, default=[])
    emails = Column(ARRAY(String), nullable=False, default=[])
    company = Column(String, nullable=True)
    job_title = Column(String, nullable=True)
    note = Column(String, nullable=True)
    raw_data = Column(JSONB, nullable=True)  # For storing additional data
    synced_to_postgres = Column(DateTime, default=datetime.now)


class DBHandle(Base):
    """SQLAlchemy model for message handles."""

    __tablename__ = "handles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    handle_id = Column(Integer, nullable=False, unique=True)
    service = Column(String, nullable=False)
    identifier = Column(String, nullable=False, index=True)
    country = Column(String, nullable=True)
    service_center = Column(String, nullable=True)
    uncanonicalized_id = Column(String, nullable=True)
    contact_name = Column(String, nullable=True)
    synced_to_postgres = Column(DateTime, default=datetime.now)


def get_db():
    """Get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize the database schema."""
    Base.metadata.create_all(bind=engine)
