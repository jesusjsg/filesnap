import os
from typing import Annotated, Optional

import typer
from rich.console import Console
from rich.filesize import decimal
from rich.table import Table

from filesnap.constants import DEFAULT_LIST_IGNORED
from filesnap.utils.decorators import benchmark
from filesnap.utils.filesystem import (
    get_ignore_list,
    scandir,
    validate_path_exist,
)
from filesnap.utils.formatting import format_date, task_progress

app = typer.Typer()
console = Console()

MAX_TABLE_ROWS = 1000


@app.command()
@benchmark
def scan(
    path: Annotated[
        str,
        typer.Argument(
            help="Path to scan.",
        ),
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
            help="Pretty table to show all the files. Note: this take more time if the path have a lot files.",
        ),
    ] = False,
    ignore: Annotated[
        Optional[str],
        typer.Option(
            "--ignore",
            "-i",
            help=f"Folders to ignore. By the default are those {', '.join(DEFAULT_LIST_IGNORED)}. Use commas to separate each folder.",
        ),
    ] = None,
):
    """
    Scan all the files in the path
    """

    validate_path_exist(path)
    ignore_list = get_ignore_list(ignore)

    entries = scandir(path, recursive, ignore_list)
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
                console.print(
                    f"\n:warning:[yellow]Warning[/yellow]: Table output truncated. Showing first {MAX_TABLE_ROWS}"
                )

    console.print(f"{count} files found in [green]{path}[/green]")
