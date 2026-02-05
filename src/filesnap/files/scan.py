import os
from typing import Annotated, List, Optional

import typer
from rich import print
from rich.console import Console
from rich.filesize import decimal
from rich.table import Table

from filesnap.utils.filesystem import (
    get_exclude_list,
    get_extension_list,
    scandir,
    validate_path_exist,
)
from filesnap.utils.formatting import format_date, task_progress

app = typer.Typer()
console = Console()

MAX_TABLE_ROWS = 1000


@app.command()
def scan(
    path: Annotated[
        str, typer.Argument(help="Path to count")
    ] = os.getcwd(),
    recursive: Annotated[
        bool,
        typer.Option("--recursive", "-r", help="Recursive search."),
    ] = False,
    pretty: Annotated[
        bool,
        typer.Option(
            "--pretty",
            "-p",
        ),
    ] = False,
    exclude: Annotated[Optional[List[str]], typer.Option()] = None,
    extensions: Annotated[
        Optional[List[str]], typer.Option("--ext", "-e")
    ] = None,
):
    """
    Scan all the files in the path
    """

    validate_path_exist(path)

    scan_options = {
        "exclude": get_exclude_list(exclude),
        "extensions": get_extension_list(extensions),
    }

    entries = scandir(path, recursive, **scan_options)
    count = 0

    table = Table("Name", "Size", "Created") if pretty else None

    track_entries = task_progress(
        entries, description="Scanning path..."
    )

    for entry in track_entries:
        count += 1
        if pretty and table is not None:
            if count <= MAX_TABLE_ROWS:
                file_info = entry.stat()
                table.add_row(
                    entry.name,
                    decimal(file_info.st_size),
                    format_date(file_info.st_ctime),
                )

    if pretty and table:
        with console.pager(styles=True):
            console.print(table)

            if count > MAX_TABLE_ROWS:
                print(
                    f"\n:warning:[yellow]Warning[/yellow]: Table output truncated. Showing first {MAX_TABLE_ROWS}"
                )

    print(f"{count} files found in [green]{path}[/green]")
