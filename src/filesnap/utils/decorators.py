import functools
import time

from rich.console import Console

console = Console()


def benchmark(func):
    """Decorator to get the execution time of a function"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()

        result = func(*args, **kwargs)

        end_time = time.perf_counter()
        duration = end_time - start_time

        console.print(
            f"\n[bold magenta]Time:[/bold magenta] [cyan]{func.__name__}[/cyan] took [bold]{duration:.4f}[/bold] seconds."
        )
        return result

    return wrapper
