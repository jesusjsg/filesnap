import os
import shutil
from typing import Annotated, List, Optional

import typer
from rich import print

from filesnap.utils.filesystem import (
    get_exclude_list,
    get_extension_list,
    scandir,
    validate_path_exist,
)
from filesnap.utils.formatting import task_progress

app = typer.Typer()


@app.command()
def clean(
    path: str,
    recursive: Annotated[
        bool, typer.Option("--recursive", "-r")
    ] = False,
    pattern: Annotated[
        Optional[str], typer.Option("--pattern", "-p")
    ] = None,
    extensions: Annotated[
        Optional[List[str]], typer.Option("--ext", "-e")
    ] = None,
    exclude: Annotated[Optional[List[str]], typer.Option()] = None,
    force: Annotated[bool, typer.Option("--force", "-f")] = False,
):
    """Clean the content of the path"""
    validate_path_exist(path)

    if force:
        if typer.confirm(
            f"Are you sure you want to delete the entire {path}?",
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

    scan_options = {
        "exclude": get_exclude_list(exclude),
        "extensions": get_extension_list(extensions),
    }

    entries = scandir(path, recursive, **scan_options)

    track_entries = task_progress(
        entries, description="Cleaning content..."
    )

    for entry in track_entries:
        if pattern and pattern not in entry.name:
            continue

        try:
            if entry.is_file() or entry.is_symlink():
                os.remove(entry)
            elif entry.is_dir():
                if not pattern:
                    os.rmdir(entry.path)
        except OSError:
            pass

    print(
        "[green]The content of the path was removed successfully![/green]"
    )
