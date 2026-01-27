import os
from typing import Generator, Optional

import typer
from rich import print

from filesnap.constants import DEFAULT_LIST_IGNORED


def get_extension(file_name: str) -> str:
    _, ext = os.path.splitext(file_name)
    return ext.lower() if ext else "Invalid extension"


def get_ignore_list(ignore_name: Optional[str]) -> list[str]:
    final_ignores = DEFAULT_LIST_IGNORED

    if ignore_name:
        user_list = [item.strip() for item in ignore_name.split(",")]
        final_ignores = list(set(final_ignores + user_list))
    return final_ignores


def scandir(
    path: str, recursive: bool = False, ignore_list: list = None
) -> Generator[os.DirEntry, None, None]:
    if ignore_list is None:
        ignore_list = DEFAULT_LIST_IGNORED

    try:
        for entry in os.scandir(path):
            if entry.is_dir() and entry.name in ignore_list:
                continue
            if entry.is_dir():
                if recursive:
                    yield from scandir(
                        entry.path, recursive, ignore_list
                    )
            else:
                yield entry
    except PermissionError:
        pass


def validate_path_exist(path: str) -> None:
    if not os.path.isdir(path):
        print(
            f"[bold red]Error:[/bold red] The path [yellow]{path}[/yellow] donsn't exist!"
        )
        raise typer.Exit(code=1)
