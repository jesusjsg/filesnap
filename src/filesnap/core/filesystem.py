import fnmatch
from pathlib import Path
from typing import Generator, Set

import typer
from rich import print


# TODO: Implement new scandir with pathlib nad yield Path objects
def scandir(path: Path, **kwargs) -> Generator[Path, None, None]:
    recursive: bool = kwargs.get("recursive", False)
    valid_extensions: Set[str] = kwargs.get("extensions", set())
    exclude_names: Set[str] = kwargs.get("exclude", set())
    pattern: str = kwargs.get("pattern", "")

    def _scan_directory(current_path: Path):
        try:
            for entry in current_path.iterdir():
                if pattern and not fnmatch.fnmatch(entry.name, pattern):
                    continue

                if valid_extensions and entry.is_file():
                    if entry.suffix.lower() not in valid_extensions:
                        continue

                if entry.name in exclude_names:
                    continue

                yield entry

                if recursive and entry.is_dir():
                    yield from _scan_directory(entry)

        except PermissionError:
            pass
        except FileNotFoundError:
            pass

    yield from _scan_directory(path)


def validate_path_exist(path: Path) -> None:
    if not path.exists():
        print(
            f"[bold red]Error:[/bold red] The path [yellow]{path}[/yellow] dosen't exist!"
        )
        raise typer.Exit(code=1)
