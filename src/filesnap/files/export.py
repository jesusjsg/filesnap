from pathlib import Path
from typing import Annotated, Optional

import typer
from rich import print

from filesnap.core.exportation import export_file
from filesnap.core.filesystem import scandir
from filesnap.core.validators import validate_source_path
from filesnap.utils.formatting import task_progress

app = typer.Typer()


@app.command()
def export(
    path: Annotated[
        Path, typer.Argument(help="Path to scan for filenames")
    ] = Path.cwd(),
    type: Annotated[
        str,
        typer.Option(
            "--type",
            "-t",
            help="The type of file to export to (e.g., txt, csv, json).",
        ),
    ] = "txt",
    recursive: Annotated[
        bool,
        typer.Option("--recursive", "-r", help="Recursive scanning."),
    ] = False,
    output: Annotated[
        Optional[str],
        typer.Option("--output", "-o", help="The output file name."),
    ] = None,
    format: Annotated[
        Optional[str],
        typer.Option(
            "--format",
            "-f",
            help="The format of the output (regex to remove).",
        ),
    ] = None,
    column: Annotated[
        str,
        typer.Option(
            "--column", "-c", help="The column/header to export."
        ),
    ] = "file_name",
):
    """Export the filename to a file (txt, csv, or json)"""
    validate_source_path(path)

    if output is None:
        output = f"{path.name}.{type}"

    entries = scandir(path, recursive=recursive)
    track_entries = task_progress(
        entries, description=f"Generating {type.upper()} file..."
    )

    export_file(
        entries=track_entries,
        file_type=type,
        output=output,
        column_name=column,
        pattern=format,
    )

    print(
        f"[green]{type.upper()} file generated successfully: {output}[/green] :star:"
    )
