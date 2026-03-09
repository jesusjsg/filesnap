from pathlib import Path
from typing import Annotated, List

import typer
from rich import print

from filesnap.core.filesystem import (
    compress_images,
    get_extension_list,
    scandir,
)
from filesnap.core.validators import (
    validate_destination_path,
    validate_quality,
    validate_source_path,
)
from filesnap.utils.formatting import task_progress

app = typer.Typer()


@app.command()
def compress(
    source_path: Annotated[
        Path, typer.Argument(help="Path to images to compress")
    ],
    destination_path: Annotated[
        Path, typer.Argument(help="Path to save compressed images")
    ],
    current_format: Annotated[
        List[str],
        typer.Option(
            "--current-format",
            "-f",
            help="The format of the images to compress.",
        ),
    ] = [],
    new_format: Annotated[
        str,
        typer.Option(
            "--new-format",
            "-t",
            help="The format to convert the images to.",
        ),
    ] = "jpg",
    quality: Annotated[
        int,
        typer.Option(
            "--quality",
            "-q",
            help="The quality of the compressed images (0-100).",
        ),
    ] = 80,
):
    """Compress all the images in the path selected with different formats"""

    validate_source_path(source_path)
    validate_quality(quality)
    validate_destination_path(destination_path)

    scan_options = {
        "extensions": get_extension_list(current_format),
    }

    entries = scandir(source_path, **scan_options)

    track_entries = task_progress(
        entries, description="Compressing images..."
    )

    count = 0
    for entry in track_entries:
        output_file = (
            destination_path
            / entry.with_suffix(f".{new_format.lstrip('.')}").name
        )
        compress_images(entry, output_file, quality)

        if entry.resolve() != output_file.resolve():
            entry.unlink()

        count += 1

    print(
        f"[bold green]A total of [yellow]{count}[/yellow] files were compressed[/bold green] :rocket:"
    )
