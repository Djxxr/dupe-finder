import os
from pathlib import Path
from collections import defaultdict
import hashlib
import pyfiglet
import psutil
import questionary
from rich.console import Console
from rich.table import Table
from rich.progress import Progress

# --- Helper Functions ---

def clear_screen():
    """Clears the console screen for a cleaner UI."""
    os.system('cls' if os.name == 'nt' else 'clear')

def format_size(size_in_bytes):
    """Formats a size in bytes into KB, MB, GB, etc."""
    if size_in_bytes < 1024:
        return f"{size_in_bytes} B"
    for unit in ['KB', 'MB', 'GB', 'TB']:
        size_in_bytes /= 1024
        if size_in_bytes < 1024:
            return f"{size_in_bytes:.2f} {unit}"
    return f"{size_in_bytes:.2f} PB"

def hash_file(path):
    """Calculates the SHA-256 hash of a file, returning None on error."""
    sha256 = hashlib.sha256()
    try:
        with open(path, 'rb') as f:
            # Read in chunks to handle large files efficiently
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()
    except (IOError, PermissionError):
        return None

# --- Core Logic & UI ---

def handle_deletion(confirmed_dupes, console):
    """Handles the interactive deletion process with a 'select all but oldest' feature."""
    console.print("\n[bold yellow]--- Deletion Module ---[/bold yellow]")
    proceed = questionary.confirm("Do you want to proceed with deleting duplicate files?").ask()

    if not proceed:
        console.print("[cyan]Deletion process skipped.[/cyan]")
        return

    deleted_files = []
    failed_to_delete = []

    for i, group in enumerate(confirmed_dupes):
        files_in_group = [Path(f) for f in group]
        console.print(f"\n[bold]Processing duplicate group {i+1}/{len(confirmed_dupes)} ({len(files_in_group)} identical files):[/bold]")
        
        try:
            oldest_file = min(files_in_group, key=lambda f: f.stat().st_mtime)
        except FileNotFoundError:
            console.print("[red]Error: One of the files was deleted during processing. Skipping group.[/red]")
            continue
            
        SELECT_ALL_BUT_OLDEST_CHOICE = f"✨ Mark all for deletion (keeps oldest: {oldest_file.name})"
        
        selected_for_action = questionary.checkbox(
            "Select files to DELETE. Use spacebar to toggle.",
            choices=[SELECT_ALL_BUT_OLDEST_CHOICE, *[str(f) for f in files_in_group]]
        ).ask()

        if selected_for_action is None:
            console.print("[yellow]Skipping this group.[/yellow]")
            continue
        
        files_to_delete_paths = []
        if SELECT_ALL_BUT_OLDEST_CHOICE in selected_for_action:
            files_to_delete_paths = [str(f) for f in files_in_group if f != oldest_file]
            user_deselected = [f for f in selected_for_action if f != SELECT_ALL_BUT_OLDEST_CHOICE]
            files_to_delete_paths = [f for f in files_to_delete_paths if f not in user_deselected]
        else:
            files_to_delete_paths = selected_for_action

        if not files_to_delete_paths:
            console.print("[yellow]No files selected for deletion in this group.[/yellow]")
            continue
            
        console.print("\n[bold]You have selected the following files for deletion:[/bold]")
        for f in files_to_delete_paths:
            console.print(f"  - [red]{f}[/red]")
        
        confirm_deletion = questionary.confirm("Are you sure you want to permanently delete these files?").ask()

        if confirm_deletion:
            for file_path_str in files_to_delete_paths:
                try:
                    os.remove(file_path_str)
                    deleted_files.append(file_path_str)
                except OSError as e:
                    failed_to_delete.append((file_path_str, e))
            console.print(f"[green]Deletion for this group complete.[/green]")
        else:
            console.print("[yellow]Deletion cancelled for this group.[/yellow]")
    
    console.print("\n[bold]--- Deletion Summary ---[/bold]")
    if deleted_files:
        console.print(f"[green]Successfully deleted {len(deleted_files)} file(s).[/green]")
    if failed_to_delete:
        console.print(f"[red]Failed to delete {len(failed_to_delete)} file(s) due to errors.[/red]")
    if not deleted_files and not failed_to_delete:
        console.print("[cyan]No files were marked for deletion.[/cyan]")


def run_scanner(directory_path_str):
    """Scans for duplicates and then triggers the deletion handler."""
    console = Console()
    directory = Path(directory_path_str)

    if not directory.is_dir():
        console.print(f"[bold red]Error: Invalid directory path '{directory}'[/bold red]")
        return

    console.print("\n[bold cyan]Scanning directory: [/bold cyan]", end="")
    console.print(str(directory))

    files_by_size = defaultdict(list)
    all_files = [f for f in directory.rglob('*') if f.is_file()]

    with console.status("[bold green]Phase 1/2: Analyzing file sizes...[/bold green]"):
        for file_path in all_files:
            try:
                size = file_path.stat().st_size
                # Ignore empty files, as they are all identical by content anyway.
                if size > 0:
                    files_by_size[size].append(file_path)
            except FileNotFoundError:
                continue
    
    potential_dupe_groups = [files for files in files_by_size.values() if len(files) > 1]
    
    if not potential_dupe_groups:
        console.print("\n[bold yellow]No files with matching sizes found. No duplicates.[/bold yellow]")
        return
        
    console.print(f"\n[bold cyan]Found {len(potential_dupe_groups)} groups of files with matching sizes. Now verifying content...[/bold cyan]")
    
    confirmed_dupes = []
    with Progress(console=console) as progress:
        task = progress.add_task("[green]Phase 2/2: Hashing files...", total=len(potential_dupe_groups))
        for group in potential_dupe_groups:
            hashes = defaultdict(list)
            for file_path in group:
                file_hash = hash_file(file_path)
                if file_hash:
                    hashes[file_hash].append(file_path)
            
            for file_list in hashes.values():
                if len(file_list) > 1:
                    confirmed_dupes.append(file_list)
            progress.update(task, advance=1)

    console.print("\n[bold green]Scan complete.[/bold green]")

    if not confirmed_dupes:
        console.print("[bold yellow]No content-identical duplicates found.[/bold yellow]")
        return

    table = Table(title="[bold]Confirmed Duplicate Files[/bold]")
    table.add_column("File Size", justify="right", style="cyan", no_wrap=True)
    table.add_column("SHA-256 Hash", justify="center", style="magenta")
    table.add_column("File Paths", style="green")

    for group in confirmed_dupes:
        first_file = group[0]
        size = first_file.stat().st_size
        file_hash = hash_file(first_file) 
        
        paths_str = "\n".join([str(f) for f in group])
        table.add_row(format_size(size), f"{file_hash[:12]}...", paths_str)
        table.add_section()

    console.print(table)
    
    handle_deletion(confirmed_dupes, console)


def select_path_from_drives():
    """Interactive prompt to select a drive and then a folder."""
    console = Console()
    try:
        partitions = psutil.disk_partitions()
        drives = [p.device for p in partitions]
        
        selected_drive = questionary.select(
            "Which drive do you want to scan?",
            choices=[*drives, "[ Back ]"]
        ).ask()
        
        if not selected_drive or selected_drive == "[ Back ]": return None

        drive_path = Path(selected_drive)
        try:
            folders = [f.name for f in drive_path.iterdir() if f.is_dir()]
        except PermissionError:
            console.print(f"[bold red]Could not access folders in {drive_path}. Try running as administrator.[/bold red]")
            return None

        choices = ["[SCAN ENTIRE DRIVE]", *folders, "[ Back ]"]
        selected_folder = questionary.select("Which folder do you want to scan?", choices=choices).ask()

        if not selected_folder or selected_folder == "[ Back ]": return None
        if selected_folder == "[SCAN ENTIRE DRIVE]": return str(drive_path)
        
        return str(drive_path / selected_folder)
    except Exception as e:
        console.print(f"An error occurred while Browse drives: {e}", style="bold red")
        return None

def main():
    """Main entry point. Handles the interactive menu and user choices."""
    console = Console()
    try:
        while True:
            clear_screen()
            ascii_banner = pyfiglet.figlet_format("benz")
            console.print(f"[bold green]{ascii_banner}[/bold green]")
            console.print("[bold]Welcome to Dupe-Finder![/bold] A tool to find duplicate files.\n")
    
            main_choice = questionary.select(
                "What would you like to do?",
                choices=["Enter a custom path to scan", "Select a drive to browse", "Exit"]
            ).ask()

            if main_choice == "Enter a custom path to scan":
                while True:
                    path_input = questionary.text("Please enter the directory path (or type 'back' to return):").ask()
                    if path_input is None or path_input.lower() in ['back', 'exit', '[back]']: break
                    if Path(path_input).is_dir():
                        run_scanner(path_input)
                        break
                    else:
                        questionary.print(f"Error: The path '{path_input}' is not a valid directory. Please try again.", style="bold red")
            
            elif main_choice == "Select a drive to browse":
                path_to_scan = select_path_from_drives()
                if path_to_scan:
                    run_scanner(path_to_scan)
            
            elif main_choice == "Exit" or main_choice is None:
                break
    
            console.print("\n[bold]Press Enter to return to the main menu...[/bold]")
            input()

    except KeyboardInterrupt:
        clear_screen()
        console.print("\n[bold cyan]Operation cancelled by user. Goodbye![/bold cyan]")
    
    clear_screen()


if __name__ == "__main__":
    main()