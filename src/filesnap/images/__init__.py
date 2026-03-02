import typer

from filesnap.images.compress import app as compress_app

app = typer.Typer()

app.add_typer(compress_app)
