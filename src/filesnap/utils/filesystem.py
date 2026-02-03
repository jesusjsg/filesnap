import os
from typing import Generator, List, Optional

import typer
from rich import print

from filesnap.constants import DEFAULT_LIST_IGNORED


def get_extension(file_name: str) -> str:
    _, ext = os.path.splitext(file_name)
    return ext.lower() if ext else "Invalid extension"


def get_exclude_list(exclude_names: Optional[List[str]]) -> set[str]:
    final_ignores = set(DEFAULT_LIST_IGNORED)

    if exclude_names:
        for item in exclude_names:
            user_list = [
                file.strip() for file in item.split(",") if item.strip()
            ]
        final_ignores.update(user_list)
    return final_ignores


def get_extension_list(extensions: Optional[List[str]]) -> set[str]:
    if not extensions:
        return set()

    final_extensions = set()
    for item in extensions:
        parts = [i.strip() for i in item.split(",") if i.strip()]
        for ext in parts:
            final_extensions.add(f".{ext.lstrip('.')}")
    return final_extensions


def scandir(
    path: str, recursive: bool = False, **kwargs
) -> Generator[os.DirEntry, None, None]:
    exclude_names = kwargs.get("exclude", set())
    valid_extensions = kwargs.get("extensions", set())
    contain = kwargs.get("contain", str)

    try:
        for entry in os.scandir(path):
            if entry.name in exclude_names:
                continue

            if contain and contain.lower() not in entry.name.lower():
                continue

            if entry.is_file():
                if valid_extensions:
                    _, ext = os.path.splitext(entry.name)
                    if ext.lower() in valid_extensions:
                        yield entry
                else:
                    yield entry

            elif entry.is_dir():
                if recursive:
                    yield from scandir(entry.path, recursive, **kwargs)
                yield entry
    except PermissionError:
        pass


def validate_path_exist(path: str) -> None:
    if not os.path.isdir(path):
        print(
            f"[bold red]Error:[/bold red] The path [yellow]{path}[/yellow] donsn't exist!"
        )
        raise typer.Exit(code=1)
