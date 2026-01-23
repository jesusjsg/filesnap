import os
import time
from typing import Generator, Iterable, Optional

from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn

from filesnap.constants import DEFAULT_LIST_IGNORED


def format_date(date: int | float) -> str:
    return str(time.ctime(date))


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


def task_progress(
    iterable: Iterable, description: str = "Processing..."
) -> Iterable:
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=40),
        transient=True,
    ) as progress:
        task = progress.add_task(description=description, total=None)

        for item in iterable:
            yield item
            progress.update(task, advance=1)
