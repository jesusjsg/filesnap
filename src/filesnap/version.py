from importlib.metadata import PackageNotFoundError, version

import typer
from rich import print


def version_callback(value: bool):
    if value:
        try:
            pkg_version = version("filesnap")
            print(
                f":pushpin: Filesnap version [green]{pkg_version}[/green]"
            )

        except PackageNotFoundError:
            print(":error: Unknown filesnap version")

        raise typer.Exit()
