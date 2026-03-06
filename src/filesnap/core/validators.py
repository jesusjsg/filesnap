from pathlib import Path

import typer


def validate_source_path(source_path: Path) -> None:
    if not source_path.exists():
        print(
            f"[bold red]Error:[/bold red] The path [yellow]{source_path}[/yellow] dosen't exist!"
        )
        raise typer.Exit(code=1)


def validate_destination_path(destination_path: Path) -> None:
    if not destination_path.exists():
        destination_path.mkdir(parents=True)
