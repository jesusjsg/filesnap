from pathlib import Path
from typing import Annotated

import typer
from rich import print

from filesnap.core.filesystem import compress_images
from filesnap.core.validators import (
    validate_destination_path,
    validate_quality,
    validate_source_path,
)

app = typer.Typer()


@app.command()
def compress(
    source_path: Annotated[Path, typer.Argument(help="Path to images to compress")],
    destination_path: Annotated[Path, typer.Argument(help="Path to save compressed images")],
    current_format: Annotated[
        str, typer.Option("--current-format", "-f", help="The format of the images to compress.")
    ] = "png",
    new_format: Annotated[
        str, typer.Option("--new-format", "-t", help="The format to convert the images to.")
    ] = "jpg",
    quality: Annotated[
        int, typer.Option("--quality", "-q", help="The quality of the compressed images (0-100).")
    ] = 80,
):
    """Compress all the images in the path selected with different formats"""

    validate_source_path(source_path)
    validate_quality(quality)
    validate_destination_path(destination_path)

    count = 0
    # Use glob for efficiency if we only care about files in source_path
    for entry in source_path.glob(f"*.{current_format.lstrip('.')}"):
        if entry.is_file():
            output_file = destination_path / entry.with_suffix(f".{new_format.lstrip('.')}").name
            compress_images(entry, output_file, quality)
            count += 1

    print(
        f"[bold green]A total of [yellow]{count}[/yellow] files were compressed[/bold green] :rocket:"
    )
