import typer

from filesnap.files import app as files_app
from filesnap.version import app as version_app

app = typer.Typer(
    no_args_is_help=True,
    add_completion=False,
    add_help_option=False,
    help="A simple CLI to handle your files",
)

app.add_typer(version_app)
app.add_typer(files_app)

if __name__ == "__main__":
    app()
