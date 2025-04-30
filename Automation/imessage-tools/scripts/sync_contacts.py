#!/usr/bin/env python3
"""
Script to sync macOS Contacts with PostgreSQL database.
"""
import sys
import time
from pathlib import Path

import typer
from rich.console import Console
from sqlalchemy.orm import Session

# Add the src directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from imessage_sync.db.postgres import SessionLocal, init_db
from imessage_sync.sync.contacts import sync_contacts_to_postgres
from imessage_sync.utils.apple_utils import check_full_disk_access, prompt_for_permissions

app = typer.Typer()
console = Console()


@app.command()
def sync(force: bool = typer.Option(False, "--force", "-f", help="Force sync even if permissions are missing")):
    """
    Sync macOS Contacts to PostgreSQL database.
    """
    # Check permissions
    if not check_full_disk_access() and not force:
        console.print("[bold red]Missing Full Disk Access permissions![/bold red]")
        console.print("This script needs Full Disk Access to read your Contacts.")

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
    console.print("[bold blue]Starting Contacts sync...[/bold blue]")

    try:
        # Get database session
        db = SessionLocal()

        # Sync contacts
        with console.status("[bold green]Syncing contacts...[/bold green]"):
            start_time = time.time()
            new_contacts = sync_contacts_to_postgres(db)
            end_time = time.time()

        # Report results
        console.print(f"[bold green]Sync completed successfully![/bold green]")
        console.print(f"Synced {new_contacts} new contacts in {end_time - start_time:.2f} seconds")

    except Exception as e:
        console.print(f"[bold red]Error during sync:[/bold red] {str(e)}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    app()
