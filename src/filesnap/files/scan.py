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
def scan(
    path: Annotated[
        Path, typer.Argument(help="Path to scan.")
    ] = Path.cwd(),
    recursive: Annotated[
        bool,
        typer.Option("--recursive", "-r", help="Recursive search."),
    ] = False,
    exclude: Annotated[
        List[str],
        typer.Option(help="Exclude files/directories from scanning."),
    ] = [],
    extensions: Annotated[
        List[str],
        typer.Option(
            "--ext", "-e", help="Scan only files with these extensions."
        ),
    ] = [],
):
    """
    Scan all the files in the path
    """

    validate_source_path(path)

    scan_options = {
        "exclude": get_exclude_list(exclude),
        "extensions": get_extension_list(extensions),
    }

    entries = scandir(path, recursive=recursive, **scan_options)
    track_entries = task_progress(
        entries, description="Scanning path..."
    )

    count = 0
    for entry in track_entries:
        count += 1

    print(f"{count} files found in [green]{path}[/green]")
