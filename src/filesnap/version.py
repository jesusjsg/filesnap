import typer
from rich import print

app = typer.Typer()


@app.command()
def version():
    """Get the current version"""
    print(":pushpin: Filesnap version [green]0.1.0[/green]")
