from typing import Annotated

import typer

from filesnap.files import app as files_app
from filesnap.version import version_callback

app = typer.Typer(
    no_args_is_help=True,
    add_completion=False,
    help="A simple CLI to handle your files",
)

app.add_typer(files_app)


@app.callback()
def main(
    version: Annotated[
        bool | None,
        typer.Option(
            "--version",
            "-v",
            is_eager=True,
            callback=version_callback,
            help="Show the current version",
        ),
    ] = None,
):
    "Callback to show the package version"
    pass


if __name__ == "__main__":
    app()
