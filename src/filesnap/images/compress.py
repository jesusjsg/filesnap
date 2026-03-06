from pathlib import Path
from typing import Annotated

import typer
from PIL import Image
from rich import print

from filesnap.core.validators import validate_destination_path

app = typer.Typer()


def compress_images(
    source_path: Path, destination_path: Path, quality: int
) -> None:
    with Image.open(source_path) as img:
        if img.mode != "RGB":
            img = img.convert("RGB")
        img.save(destination_path, optimize=True, quality=quality)


@app.command()
def compress(
    source_path: Annotated[Path, typer.Argument()],
    destination_path: Annotated[Path, typer.Argument()],
    current_format: Annotated[
        str, typer.Option("--current-format", "-c")
    ] = "png",
    new_format: Annotated[
        str, typer.Option("--new-format", "-n")
    ] = "jpg",
    quality: Annotated[int, typer.Option("--quality", "-q")] = 80,
):
    """Compress all the images in the path selected with different formats"""
    if quality > 100:
        print(
            "[bold red]Error:[/bold red] Quality must be between 60 and 100"
        )
        raise typer.Exit(code=1)

    count = 0

    validate_destination_path(destination_path)

    for entry in source_path.glob(f"*.{current_format}"):
        compress_images(
            entry,
            destination_path / entry.with_suffix(f".{new_format}").name,
            quality,
        )
        count += 1

    print(
        f"[bold green]A total of [yellow]{count}[/yellow] files were compressed[/bold green] :rocket:"
    )
