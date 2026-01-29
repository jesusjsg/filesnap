import typer

from filesnap.files import app as files_app
from filesnap.version import app as version_app

app = typer.Typer(no_args_is_help=True)

app.add_typer(version_app)
app.add_typer(files_app)

if __name__ == "__main__":
    app()
