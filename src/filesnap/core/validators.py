from pathlib import Path

import typer
from rich import print


def validate_source_path(source_path: Path) -> None:
    """Validates that a path exists and is a directory."""
    if not source_path.exists():
        print(
            f"[bold red]Error:[/bold red] The path [yellow]{source_path}[/yellow] doesn't exist!"
        )
        raise typer.Exit(code=1)

    if not source_path.is_dir():
        print(
            f"[bold red]Error:[/bold red] The path [yellow]{source_path}[/yellow] is not a directory!"
        )
        raise typer.Exit(code=1)


def validate_destination_path(destination_path: Path) -> None:
    """Ensures the destination directory exists, creating it if necessary."""
    if not destination_path.exists():
        destination_path.mkdir(parents=True)


def validate_quality(quality: int) -> None:
    """Validates image compression quality."""
    if not (0 <= quality <= 100):
        print(
            "[bold red]Error:[/bold red] Quality must be between 0 and 100"
        )
        raise typer.Exit(code=1)
