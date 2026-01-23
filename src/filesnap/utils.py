import os
import time
from typing import Generator, Iterable

from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn


def format_date(date: int | float) -> str:
    return str(time.ctime(date))


def get_extension(file_name: str) -> str:
    _, ext = os.path.splitext(file_name)
    return ext.lower() if ext else "Invalid extension"


def scandir(
    path: str, recursive: bool = False
) -> Generator[os.DirEntry, None, None]:
    try:
        for entry in os.scandir(path):
            if entry.is_dir():
                if recursive:
                    yield from scandir(entry.path, recursive)
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
