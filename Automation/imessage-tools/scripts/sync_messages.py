#!/usr/bin/env python3
"""
Script to sync iMessage data with PostgreSQL database.
"""
import sys
import time
from pathlib import Path

import typer
from rich.console import Console
from sqlalchemy.orm import Session

# Add the src directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from imessage_sync.config import settings
from imessage_sync.db.postgres import SessionLocal, init_db
from imessage_sync.sync.messages import sync_messages_to_postgres
from imessage_sync.utils.apple_utils import check_full_disk_access, prompt_for_permissions

app = typer.Typer()
console = Console()


@app.command()
def sync(
    days: int = typer.Option(
        None, "--days", "-d", help="Number of days to look back for messages"
    ),
    force: bool = typer.Option(
        False, "--force", "-f", help="Force sync even if permissions are missing"
    ),
):
    """
    Sync iMessage data to PostgreSQL database.
    """
    # Check permissions
    if not check_full_disk_access() and not force:
        console.print("[bold red]Missing Full Disk Access permissions![/bold red]")
        console.print("This script needs Full Disk Access to read your Messages database.")

        # Ask if user wants to open System Preferences
        if typer.confirm("Open System Preferences to grant permissions?"):
            prompt_for_permissions()
            console.print("[yellow]Please run this script again after granting permissions.[/yellow]")
            return
        elif not typer.confirm("Continue anyway? (This may fail)"):
            return

    # Initialize database if needed
    console.print("[bold blue]Initializing database...[/bold blue]")
    init_db()

    # Start sync
    days_text = f"last {days} days" if days else f"last {settings.MESSAGE_SYNC_DAYS} days"
    console.print(f"[bold blue]Starting iMessage sync for {days_text}...[/bold blue]")

    try:
        # Get database session
        db = SessionLocal()

        # Sync messages
        with console.status("[bold green]Syncing messages...[/bold green]"):
            start_time = time.time()
            messages_synced, handles_synced = sync_messages_to_postgres(db, days)
            end_time = time.time()

        # Report results
        console.print(f"[bold green]Sync completed successfully![/bold green]")
        console.print(f"Synced {messages_synced} new messages and {handles_synced} new handles in {end_time - start_time:.2f} seconds")

    except Exception as e:
        console.print(f"[bold red]Error during sync:[/bold red] {str(e)}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    app()
