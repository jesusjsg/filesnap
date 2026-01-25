import os
from collections import defaultdict
from typing import Annotated, Optional

import typer
from rich.console import Console
from rich.filesize import decimal
from rich.table import Table

from filesnap.constants import DEFAULT_LIST_IGNORED
from filesnap.utils.decorators import benchmark
from filesnap.utils.filesystem import (
    get_extension,
    get_ignore_list,
    scandir,
)
from filesnap.utils.formatting import format_date, task_progress

console = Console()
app = typer.Typer(no_args_is_help=True)


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
        typer.Option(
            "--recursive",
            "-r",
            help="Recursive search to list files in subfolders.",
        ),
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
    table = Table("Name", "Size", "Created")

    ignore_list = get_ignore_list(ignore)
    count = 0

    if os.path.isdir(path):
        entries = scandir(path, recursive, ignore_list)
        track_entries = task_progress(
            entries, description="Scanning path..."
        )

        for entry in track_entries:
            if pretty:
                file_info = entry.stat()
                table.add_row(
                    entry.name,
                    decimal(file_info.st_size),
                    format_date(file_info.st_ctime),
                )
            count += 1

    if pretty:
        with console.pager():
            console.print(table)

    console.print(f"Total files found: [bold]{count}[/bold]")


@app.command()
def count(
    path: Annotated[
        str, typer.Argument(help="Path to count")
    ] = os.getcwd(),
    recursive: Annotated[
        bool, typer.Option("--recursive", "-r")
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
    """Count all the files by extension in the path selected"""
    ignore_list = get_ignore_list(ignore)
    info_stats = defaultdict(lambda: {"size": 0, "count": 0})

    if os.path.isdir(path):
        entries = scandir(path, recursive, ignore_list)

        track_entries = task_progress(
            entries, description="Scanning extensions..."
        )

        for entry in track_entries:
            if entry.is_file():
                ext = get_extension(entry.name)
                file_info = entry.stat()

                info_stats[ext]["size"] += file_info.st_size
                info_stats[ext]["count"] += 1

    table = Table(title=f"File statistics for {path}")
    table.add_column("Extension", style="cyan")
    table.add_column("Size", style="magenta", justify="right")
    table.add_column("Count", style="green", justify="right")

    sorted_stats = sorted(
        info_stats.items(),
        key=lambda item: item[1]["size"],
        reverse=True,
    )

    for ext, info in sorted_stats:
        table.add_row(ext, decimal(info["size"]), str(info["count"]))

    console.print(table)
