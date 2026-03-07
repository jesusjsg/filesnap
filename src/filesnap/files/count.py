from collections import defaultdict
from pathlib import Path
from typing import Annotated, List

import typer
from rich.console import Console
from rich.filesize import decimal
from rich.table import Table

from filesnap.core.filesystem import get_exclude_list, scandir
from filesnap.core.validators import validate_source_path
from filesnap.utils.formatting import task_progress

app = typer.Typer()
console = Console()


@app.command()
def count(
    path: Annotated[
        Path, typer.Argument(help="Path to count")
    ] = Path.cwd(),
    recursive: Annotated[
        bool,
        typer.Option("--recursive", "-r", help="Recursive search."),
    ] = False,
    exclude: Annotated[
        List[str],
        typer.Option(help="Exclude files/directories from counting."),
    ] = [],
):
    """Count all the files by extension in the path selected"""

    validate_source_path(path)

    scan_options = {
        "recursive": recursive,
        "exclude": get_exclude_list(exclude),
    }

    info_stats = defaultdict(lambda: {"size": 0, "count": 0})

    entries = scandir(path, **scan_options)

    track_entries = task_progress(
        entries, description="Scanning extensions..."
    )

    for entry in track_entries:
        if entry.is_file():
            ext = entry.suffix.lower() or "no-extension"
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
