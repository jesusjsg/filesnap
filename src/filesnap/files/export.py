import csv
import json
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
    column: Annotated[
        str, typer.Option("--column", "-c")
    ] = "file_name",
):
    """Export the filename to a txt file"""
    validate_path_exist(path)

    if output is None:
        output = f"{Path(path).name}.{type}"

    entries = scandir(path, recursive)
    track_entries = task_progress(
        entries, description=f"Generating {type.upper()} file..."
    )

    # TODO: add the another types files and refactor to a function
    with open(output, "w", newline="") as file:
        if type == "txt":
            file.write(f"{column}\n")
            for entry in track_entries:
                if not entry.is_file() or entry.name.startswith("."):
                    continue
                file_name = Path(entry.name).stem
                if format:
                    file_name = re.sub(format, "", file_name)
                file.write(f"{file_name}\n")

        if type == "csv":
            writer = csv.writer(file)
            writer.writerow(f"{column}\n")
            for entry in track_entries:
                if not entry.is_file() or entry.name.startswith("."):
                    continue
                file_name = Path(entry.name).stem
                if format:
                    file_name = re.sub(format, "", file_name)
                file.write(f"{file_name}\n")

        if type == "json":
            file.write("[\n")
            first = True
            for entry in track_entries:
                if not entry.is_file() or entry.name.startswith("."):
                    continue
                file_name = Path(entry.name).stem
                if format:
                    file_name = re.sub(format, "", file_name)
                if not first:
                    file.write(",\n")
                json.dump({column: file_name}, file, indent=4)
                first = False
            file.write("\n]")

    print(
        f"[green]{type.upper()} file generated successfully[/green] :star:"
    )
