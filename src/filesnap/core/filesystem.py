import fnmatch
from pathlib import Path
from typing import Generator, List, Set

from PIL import Image

from filesnap.core.constants import DEFAULT_LIST_IGNORED


def scandir(path: Path, **kwargs) -> Generator[Path, None, None]:
    recursive: bool = kwargs.get("recursive", False)
    valid_extensions: Set[str] = kwargs.get("extensions", set())
    exclude_names: Set[str] = kwargs.get("exclude", set())
    pattern: str = kwargs.get("pattern", "")
    contain: str = kwargs.get("contain", "").lower()

    def _scan_directory(current_path: Path):
        try:
            for entry in current_path.iterdir():
                if pattern and not fnmatch.fnmatch(entry.name, pattern):
                    continue

                if contain and contain not in entry.name.lower():
                    continue

                if entry.name in exclude_names:
                    continue

                if entry.is_file() and valid_extensions:
                    if entry.suffix.lower() not in valid_extensions:
                        continue

                yield entry

                if recursive and entry.is_dir():
                    yield from _scan_directory(entry)

        except PermissionError:
            pass
        except FileNotFoundError:
            pass

    yield from _scan_directory(path)


def get_extension(path: Path) -> str:
    if not path.is_file():
        return ""
    return path.suffix.lower()


def get_extension_list(extensions: List[str]) -> Set[str]:
    if not extensions:
        return set()

    final_extensions = set()
    for item in extensions:
        parts = [i.strip() for i in item.split(",") if i.strip()]
        for ext in parts:
            final_extensions.add(f".{ext.lstrip('.')}".lower())
    return final_extensions


def get_exclude_list(exclude_names: List[str]) -> Set[str]:
    final_ignores = set(DEFAULT_LIST_IGNORED)

    if exclude_names:
        for item in exclude_names:
            parts = [
                name.strip() for name in item.split(",") if name.strip()
            ]
            final_ignores.update(parts)

    return final_ignores


def compress_images(
    source_path: Path, destination_path: Path, quality: int
) -> None:
    with Image.open(source_path) as img:
        if img.mode != "RGB":
            img = img.convert("RGB")
        img.save(destination_path, optimize=True, quality=quality)
