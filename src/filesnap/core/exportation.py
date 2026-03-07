import csv
import json
import re
from pathlib import Path
from typing import Iterable, Optional

from rich import print


def export_file(
    entries: Iterable[Path],
    file_type: str,
    output: str,
    column_name: str,
    pattern: Optional[str] = None,
):
    """
    Exports filenames from a collection of pathlib.Path entries to a file.
    Only includes files and excludes hidden files.
    """
    regex = re.compile(pattern) if pattern else None
    file_type = file_type.lower()
    output_path = Path(output)

    with open(output_path, "w", newline="", encoding="utf-8") as file:
        if file_type == "txt":
            file.write(f"{column_name}\n")
            for entry in entries:
                if entry.is_file() and not entry.name.startswith("."):
                    file_name = entry.stem
                    clean_name = (
                        regex.sub("", file_name) if regex else file_name
                    )
                    file.write(f"{clean_name}\n")

        elif file_type == "csv":
            writer = csv.writer(file)
            writer.writerow([column_name])
            for entry in entries:
                if entry.is_file() and not entry.name.startswith("."):
                    file_name = entry.stem
                    clean_name = (
                        regex.sub("", file_name) if regex else file_name
                    )
                    writer.writerow([clean_name])

        elif file_type == "json":
            data = []
            for entry in entries:
                if entry.is_file() and not entry.name.startswith("."):
                    file_name = entry.stem
                    clean_name = (
                        regex.sub("", file_name) if regex else file_name
                    )
                    data.append({column_name: clean_name})

            json.dump(data, file, indent=4)
        else:
            print(
                f"[bold red]Error:[/bold red] Unsupported file type: {file_type}"
            )
