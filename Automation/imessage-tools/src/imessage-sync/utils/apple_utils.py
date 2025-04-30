"""
Utility functions for working with Apple's databases and services.
"""
import re
import subprocess
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Union


def convert_apple_timestamp(timestamp: Union[int, float]) -> datetime:
    """
    Convert Apple's timestamp format to Python datetime.

    Args:
        timestamp: Timestamp in Apple's format (nanoseconds since 2001-01-01)

    Returns:
        datetime: Corresponding datetime object
    """
    from datetime import datetime, timedelta

    # Handle None or 0
    if not timestamp:
        return datetime.now()

    # Convert from nanoseconds to seconds since 2001-01-01
    seconds_since_apple_epoch = timestamp / 1000000000

    # Add seconds to Apple epoch to get datetime
    return datetime(2001, 1, 1) + timedelta(seconds=seconds_since_apple_epoch)


def convert_datetime_to_apple_timestamp(dt: datetime) -> int:
    """
    Convert Python datetime to Apple's timestamp format.

    Args:
        dt: Python datetime object

    Returns:
        int: Timestamp in Apple's format (nanoseconds since 2001-01-01)
    """
    from datetime import datetime, timedelta

    # Calculate seconds since Apple's epoch (2001-01-01)
    seconds_since_apple_epoch = (dt - datetime(2001, 1, 1)).total_seconds()

    # Convert to nanoseconds
    return int(seconds_since_apple_epoch * 1000000000)


def normalize_phone_number(phone: str) -> str:
    """
    Normalize a phone number by removing non-digits.

    Args:
        phone: Phone number string

    Returns:
        str: Normalized phone number (digits only)
    """
    return re.sub(r'\D', '', phone)


def run_applescript(script: str) -> str:
    """
    Run an AppleScript and return its output.

    Args:
        script: AppleScript code to run

    Returns:
        str: Output from the AppleScript

    Raises:
        subprocess.CalledProcessError: If the AppleScript execution fails
    """
    try:
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing AppleScript: {e}")
        print(f"Error output: {e.stderr}")
        raise


def check_accessibility_permissions() -> bool:
    """
    Check if the Terminal has required accessibility permissions.

    Returns:
        bool: True if permissions are granted, False otherwise
    """
    script = """
    tell application "System Events"
        try
            set frontmost of process "Terminal" to true
            return true
        on error
            return false
        end try
    end tell
    """

    try:
        result = run_applescript(script)
        return result.lower() == "true"
    except:
        return False


def check_full_disk_access() -> bool:
    """
    Check if the Terminal has Full Disk Access permissions.

    Returns:
        bool: True if permissions are granted, False otherwise
    """
    import os

    # Try to access a protected file that requires Full Disk Access
    try:
        # Test access to the Messages database
        test_path = os.path.expanduser("~/Library/Messages/chat.db")
        with open(test_path, "rb") as f:
            # Just read a few bytes to test access
            f.read(1)
        return True
    except:
        return False


def prompt_for_permissions() -> None:
    """
    Prompt the user to grant necessary permissions.
    """
    permissions_script = """
    tell application "System Preferences"
        activate
        set current pane to pane "com.apple.preference.security"
        reveal anchor "Privacy_AllFiles" of pane "com.apple.preference.security"
    end tell

    display dialog "This script needs Full Disk Access permissions to access your Messages and Contacts databases. Please add Terminal to the list of applications with Full Disk Access in the System Preferences window that just opened." buttons {"OK"} default button "OK"
    """

    run_applescript(permissions_script)
