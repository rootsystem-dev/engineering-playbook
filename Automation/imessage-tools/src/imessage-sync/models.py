"""
Pydantic models for the iMessage Sync application.
"""
from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Message(BaseModel):
    """Representation of an iMessage message."""

    id: UUID = Field(default_factory=uuid4)
    message_id: int
    text: Optional[str] = None
    date: datetime
    is_from_me: bool
    service: str
    handle_id: Optional[int] = None
    sender_id: Optional[str] = None
    conversation_id: Optional[str] = None
    subject: Optional[str] = None
    associated_message_id: Optional[int] = None
    associated_message_type: Optional[int] = None
    cache_has_attachments: Optional[bool] = None
    cache_roomnames: Optional[str] = None
    was_downgraded: Optional[bool] = False
    is_read: Optional[bool] = None
    is_delivered: Optional[bool] = None
    is_sent: Optional[bool] = None
    is_finished: Optional[bool] = None
    is_prepared: Optional[bool] = None
    is_from_me_original: Optional[bool] = None
    item_type: Optional[int] = None
    group_title: Optional[str] = None
    group_action_type: Optional[int] = None
    share_status: Optional[int] = None
    share_direction: Optional[int] = None
    synced_to_postgres: datetime = Field(default_factory=datetime.now)

    class Config:
        """Model configuration."""

        from_attributes = True


class Contact(BaseModel):
    """Representation of a macOS Contact."""

    id: UUID = Field(default_factory=uuid4)
    full_name: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phones: List[str] = Field(default_factory=list)
    emails: List[str] = Field(default_factory=list)
    company: Optional[str] = None
    job_title: Optional[str] = None
    note: Optional[str] = None
    synced_to_postgres: datetime = Field(default_factory=datetime.now)

    class Config:
        """Model configuration."""

        from_attributes = True


class Handle(BaseModel):
    """Representation of an iMessage handle (chat recipient)."""

    id: UUID = Field(default_factory=uuid4)
    handle_id: int
    service: str
    identifier: str  # phone number or email
    country: Optional[str] = None
    service_center: Optional[str] = None
    uncanonicalized_id: Optional[str] = None
    contact_name: Optional[str] = None  # Derived from Contact lookup
    synced_to_postgres: datetime = Field(default_factory=datetime.now)

    class Config:
        """Model configuration."""

        from_attributes = True
