import os
from collections import defaultdict
from typing import Annotated, List, Optional

import typer
from rich.console import Console
from rich.filesize import decimal
from rich.table import Table

from filesnap.utils.filesystem import (
    get_exclude_list,
    get_extension,
    scandir,
    validate_path_exist,
)
from filesnap.utils.formatting import task_progress

app = typer.Typer()
console = Console()


@app.command()
def count(
    path: Annotated[
        str, typer.Argument(help="Path to count")
    ] = os.getcwd(),
    recursive: Annotated[
        bool,
        typer.Option("--recursive", "-r", help="Recursive search."),
    ] = False,
    exclude: Annotated[Optional[List[str]], typer.Option()] = None,
):
    """Count all the files by extension in the path selected"""

    validate_path_exist(path)

    scan_options = {
        "exclude": get_exclude_list(exclude),
    }

    info_stats = defaultdict(lambda: {"size": 0, "count": 0})

    entries = scandir(path, recursive, **scan_options)

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
