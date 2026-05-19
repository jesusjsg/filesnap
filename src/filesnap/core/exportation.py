import csv
import json
import re
from pathlib import Path
from typing import Iterable, Optional

from rich import print

from filesnap.utils.formatting import format_date


def export_file(
    entries: Iterable[Path],
    file_type: str,
    output: str,
    pattern: Optional[str] = None,
):
    """
    Exports file metadata from a collection of pathlib.Path entries to a file.
    Only includes files and excludes hidden files.
    """
    regex = re.compile(pattern) if pattern else None
    file_type = file_type.lower()
    output_path = Path(output)

    with open(output_path, "w", newline="", encoding="utf-8") as file:
        if file_type == "txt":
            file.write("name - full_name - modified\n")
            for entry in entries:
                if entry.is_file() and not entry.name.startswith("."):
                    name = entry.stem
                    clean_name = regex.sub("", name) if regex else name
                    full_name = entry.name
                    modified = format_date(entry.stat().st_mtime)
                    file.write(
                        f"{clean_name} - {full_name} - {modified}\n"
                    )

        elif file_type == "csv":
            writer = csv.writer(file)
            writer.writerow(["name", "full_name", "modified"])
            for entry in entries:
                if entry.is_file() and not entry.name.startswith("."):
                    name = entry.stem
                    clean_name = regex.sub("", name) if regex else name
                    full_name = entry.name
                    modified = format_date(entry.stat().st_mtime)
                    writer.writerow([clean_name, full_name, modified])

        elif file_type == "json":
            data = []
            for entry in entries:
                if entry.is_file() and not entry.name.startswith("."):
                    name = entry.stem
                    clean_name = regex.sub("", name) if regex else name
                    full_name = entry.name
                    modified = format_date(entry.stat().st_mtime)
                    data.append(
                        {
                            "name": clean_name,
                            "full_name": full_name,
                            "modified": modified,
                        }
                    )

            json.dump(data, file, indent=4)
        else:
            print(
                f"[bold red]Error:[/bold red] Unsupported file type: {file_type}"
            )
