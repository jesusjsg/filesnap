import typer
from rich.console import Console

app = typer.Typer()
console = Console()


@app.command()
def version():
    console.print(":pushpin: Filesnap version [green]0.1.0[/green]")
