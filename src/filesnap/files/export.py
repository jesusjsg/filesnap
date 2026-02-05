from pathlib import Path
from typing import Annotated, Optional

import typer
from rich import print

from filesnap.utils.filesystem import (
    export_file,
    scandir,
    validate_path_exist,
)
from filesnap.utils.formatting import task_progress

app = typer.Typer()


@app.command()
def export(
    path: str,
    type: Annotated[str, typer.Option("--type", "-t")],
    recursive: Annotated[
        bool, typer.Option("--recursive", "-r")
    ] = False,
    output: Annotated[
        Optional[str], typer.Option("--output", "-o")
    ] = None,
    format: Annotated[
        Optional[str], typer.Option("--format", "-f")
    ] = None,
    column: Annotated[
        str, typer.Option("--column", "-c")
    ] = "file_name",
):
    """Export the filename to a txt file"""
    validate_path_exist(path)

    if output is None:
        output = f"{Path(path).name}.{type}"

    entries = scandir(path, recursive)
    track_entries = task_progress(
        entries, description=f"Generating {type.upper()} file..."
    )

    export_file(track_entries, type, output, column, format)

    print(
        f"[green]{type.upper()} file generated successfully[/green] :star:"
    )
