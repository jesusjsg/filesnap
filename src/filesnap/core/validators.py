from pathlib import Path

import typer
from rich import print


def validate_source_path(source_path: Path) -> None:
    if not source_path.exists():
        print(
            f"[bold red]Error:[/bold red] The path [yellow]{source_path}[/yellow] doesn't exist!"
        )
        raise typer.Exit(code=1)


def validate_destination_path(destination_path: Path) -> None:
    if not destination_path.exists():
        destination_path.mkdir(parents=True)


def validate_quality(quality: int) -> None:
    if quality > 100:
        print(
            "[bold red]Error:[/bold red] Quantity cannot be greater than 100!"
        )
        raise typer.Exit(code=1)
