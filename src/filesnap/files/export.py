from pathlib import Path
from typing import Annotated, Optional

import typer
from rich.console import Console

from filesnap.utils.filesystem import scandir, validate_path_exist
from filesnap.utils.formatting import task_progress

app = typer.Typer()

console = Console()


@app.command()
def export(
    path: str,
    recursive: Annotated[
        bool, typer.Option("--recursive", "-r")
    ] = False,
    output: Annotated[
        Optional[str], typer.Option("--output", "-o")
    ] = None,
    # TODO: Apply logic to generate the file in multiples formats (csv, json, txt, etc...). Actually only txt
    type: Annotated[Optional[str], typer.Option("--type", "-t")] = None,
):
    validate_path_exist(path)

    if output is None:
        output = f"{Path(path).name}.txt"  # Using path to get more easily the last folder name

    entries = scandir(path, recursive)
    track_entries = task_progress(
        entries, description="Generating file..."
    )

    with open(output, "w") as file:
        file.write("codigo_articulos\n")
        for entry in track_entries:
            file_name = entry.name.split(".")[0]
            file.write(file_name + "\n")
    file.close()

    console.print("[green]File generated successfully[/green] :star:")
