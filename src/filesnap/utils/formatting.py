import time
from typing import Iterable

from rich.progress import Progress, SpinnerColumn, TextColumn


def format_date(date: int | float) -> str:
    return str(time.ctime(date))


def task_progress(
    iterable: Iterable, description: str = "Processing..."
) -> Iterable:
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task(description=description, total=None)

        for item in iterable:
            yield item
            progress.update(task, advance=1)
