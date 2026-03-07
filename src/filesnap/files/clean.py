from pathlib import Path
from typing import Annotated, List

import typer
from rich import print

from filesnap.core.filesystem import (
    get_exclude_list,
    get_extension_list,
    scandir,
)
from filesnap.core.validators import validate_source_path
from filesnap.utils.formatting import task_progress

app = typer.Typer()


@app.command()
def clean(
    path: Annotated[
        Path, typer.Argument(help="Path to clean")
    ] = Path.cwd(),
    recursive: Annotated[
        bool,
        typer.Option("--recursive", "-r", help="Recursive cleaning."),
    ] = False,
    contain: Annotated[
        str,
        typer.Option(
            "--contain",
            "-c",
            help="Clean only files containing this string.",
        ),
    ] = "",
    extensions: Annotated[
        List[str],
        typer.Option(
            "--ext",
            "-e",
            help="Clean only files with these extensions.",
        ),
    ] = [],
    exclude: Annotated[
        List[str],
        typer.Option(help="Exclude files/directories from cleaning."),
    ] = [],
    force: Annotated[
        bool,
        typer.Option(
            "--force", "-f", help="Force deletion without confirmation."
        ),
    ] = False,
    dry_run: Annotated[
        bool,
        typer.Option(
            "--dry-run",
            help="Simulate cleaning without deleting files.",
        ),
    ] = False,
):
    """Clean the content of the path"""
    validate_source_path(path)

    if not dry_run and not force:
        typer.confirm(
            f"Are you sure you want to delete content in {path} matching your filters?",
            abort=True,
        )

    scan_options = {
        "extensions": get_extension_list(extensions),
        "exclude": get_exclude_list(exclude),
        "contain": contain,
        "recursive": recursive,
    }

    entries = list(scandir(path, **scan_options))
    track_entries = task_progress(
        entries, description="Cleaning content..."
    )

    count = 0
    for entry in track_entries:
        try:
            if dry_run:
                print(
                    f"[yellow][DRY RUN][/yellow] Would remove: [white]{entry}[/white]"
                )
                count += 1
                continue

            if entry.is_file() or entry.is_symlink():
                entry.unlink()
                count += 1
            elif entry.is_dir() and not any(entry.iterdir()):
                entry.rmdir()
                count += 1
        except OSError as e:
            print(f"[red]Error removing {entry}: {e}[/red]")

    message = (
        f"Dry run completed! {count} total items would be affected"
        if dry_run
        else f"Cleaned {count} items successfully!"
    )
    print(f"[green]{message}[/green]")
