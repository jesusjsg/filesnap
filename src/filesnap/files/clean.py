import os
import shutil
from typing import Annotated, Optional

import typer
from rich.console import Console

from filesnap.utils.filesystem import (
    get_ignore_list,
    scandir,
    validate_path_exist,
)
from filesnap.utils.formatting import task_progress

app = typer.Typer()
console = Console()


@app.command()
def clean(
    path: str,
    recursive: Annotated[
        bool, typer.Option("--recursive", "-r")
    ] = False,
    ignore: Annotated[
        Optional[str], typer.Option("--ignore", "-i")
    ] = None,
    all: Annotated[bool, typer.Option("-all", "-a")] = False,
):
    """Clean the path entered"""
    validate_path_exist(path)

    if all:
        if typer.confirm(
            f"Are you sure you want to delete {path}?",
            abort=True,
        ):
            shutil.rmtree(path)
        print(
            f"[green]The directory {path} was removed successfully![/green]"
        )
        raise typer.Exit()

    typer.confirm(
        "Are you sure you want to delete the content of the path?",
        abort=True,
    )
    ignore_list = get_ignore_list(ignore)

    entries = scandir(path, recursive, ignore_list)

    track_entries = task_progress(
        entries, description="Cleaning content..."
    )
    for entry in track_entries:
        if entry.is_file() or entry.is_symlink():
            os.remove(entry)
        elif entry.is_dir():
            try:
                os.rmdir(entry.path)
            except OSError:
                pass

    print(
        "[green]The content of the path was removed successfully![/green]"
    )
