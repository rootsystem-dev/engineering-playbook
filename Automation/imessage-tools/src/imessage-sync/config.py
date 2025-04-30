"""
Configuration settings for the iMessage Sync application.
"""
import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    """Application settings."""

    # Database settings
    DATABASE_URL: PostgresDsn

    # macOS paths
    MESSAGES_DB_PATH: Path = Path.home() / "Library" / "Messages" / "chat.db"
    CONTACTS_DB_PATH: Optional[Path] = None  # Will use AppleScript to access contacts

    # Sync settings
    MESSAGE_BATCH_SIZE: int = 5000
    MESSAGE_SYNC_DAYS: int = 365 * 8  # Last 8 years by default

    # SQLAlchemy settings
    SQLALCHEMY_ECHO: bool = False

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True
    )


# Create a global settings instance
settings = Settings()
