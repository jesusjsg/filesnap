import typer

from filesnap.files.clean import app as clean_app
from filesnap.files.count import app as count_app
from filesnap.files.scan import app as scan_app

app = typer.Typer()

app.add_typer(scan_app)
app.add_typer(count_app)
app.add_typer(clean_app)
