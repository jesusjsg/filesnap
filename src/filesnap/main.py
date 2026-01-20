import os
from typing import Annotated

import typer
from rich.console import Console
from rich.filesize import decimal
from rich.table import Table

console = Console()
app = typer.Typer()


@app.command()
def scan(path: Annotated[str, typer.Argument()] = os.getcwd()):
    """
    Scan all the files in the path
    """
    table = Table("Name", "Size")
    if os.path.isdir(path):
        for file in os.scandir(path):
            # TODO: validate the file extension and other directories
            if file.is_file():
                table.add_row(file.name, decimal(file.stat().st_size))

    console.print(table)


@app.command()
def sync():
    pass
