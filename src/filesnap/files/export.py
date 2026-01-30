import csv
import re
from pathlib import Path
from typing import Annotated, Optional

import typer
from rich import print

from filesnap.utils.filesystem import scandir, validate_path_exist
from filesnap.utils.formatting import task_progress

app = typer.Typer()


@app.command()
def export(
    path: str,
    # TODO: Apply logic to generate the file in multiples formats (csv, json, txt, etc...). Actually only txt
    type: Annotated[str, typer.Option("--type", "-t")],
    recursive: Annotated[
        bool, typer.Option("--recursive", "-r")
    ] = False,
    output: Annotated[
        Optional[str], typer.Option("--output", "-o")
    ] = None,
    format: Annotated[
        Optional[str], typer.Option("--format", "-f")
    ] = None,
):
    """Export the filename to a txt file"""
    validate_path_exist(path)

    if output is None:
        output = f"{Path(path).name}.{type}"

    entries = scandir(path, recursive)
    track_entries = task_progress(
        entries, description=f"Generating {type} file..."
    )

    # TODO: add the another types files and refactor to a function
    with open(output, "w", newline="") as file:
        for entry in track_entries:
            if type == "txt":
                file.write("file_name\n")
                for entry in track_entries:
                    if not entry.is_file() or entry.name.startswith(
                        "."
                    ):
                        continue
                    file_name = Path(entry.name).stem
                    if format:
                        file_name = re.sub(format, "", file_name)
                    file.write(f"{file_name}\n")

            if type == "csv":
                writer = csv.writer(file)
                writer.writerow(["file_name"])
                for entry in track_entries:
                    if not entry.is_file() or entry.name.startswith(
                        "."
                    ):
                        continue
                    file_name = Path(entry.name).stem
                    if format:
                        file_name = re.sub(format, "", file_name)
                    writer.writerow([file_name])

    print(
        f"[green]{type.upper()} file generated successfully[/green] :star:"
    )
