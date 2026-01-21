import os
from typing import Annotated, Generator

import typer
from rich.console import Console
from rich.filesize import decimal
from rich.table import Table

from filesnap.decorators import benchmark
from filesnap.utils import format_date

console = Console()
app = typer.Typer()


def scandir(path: str, recursive: bool = False) -> Generator[os.DirEntry, None, None]:
    try:
        for entry in os.scandir(path):
            if entry.is_dir():
                if recursive:
                    yield from scandir(entry.path, recursive)
            else:
                yield entry
    except PermissionError:
        pass


@app.command()
@benchmark
def scan(
    path: Annotated[str, typer.Argument(help="Path to scan.")] = os.getcwd(),
    recursive: Annotated[
        bool, typer.Option(help="Recursive search to list files in subfolders.")
    ] = False,
    pretty: Annotated[
        bool,
        typer.Option(
            help="Pretty table to show all the files. Note: this take more time if the path have a lot files."
        ),
    ] = False,
):
    """
    Scan all the files in the path
    """
    table = Table("Name", "Size", "Created")
    count = 0

    if os.path.isdir(path):
        entries = scandir(path, recursive)

        for entry in entries:
            if pretty:
                file_info = entry.stat()
                table.add_row(
                    entry.name,
                    decimal(file_info.st_size),
                    format_date(file_info.st_ctime),
                )
            count += 1

    if pretty:
        console.print(table)

    console.print(f"Total files found: [bold]{count}[/bold]")
