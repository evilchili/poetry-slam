import logging
from pathlib import Path
from typing import Optional

import typer
from rich.logging import RichHandler

from poetry_slam.build_tool import BuildTool

app = typer.Typer()
app_state = dict()

logger = logging.getLogger("slam.cli")


@app.callback(invoke_without_command=True)
def main(
    context: typer.Context,
    verbose: bool = typer.Option(False, help="Enable verbose output."),
    log_level: str = typer.Option("error", help=" Set the log level."),
    poetry: Optional[Path] = typer.Option(
        "poetry",
        help="Path to the poetry executable; defaults to the first in your path.",
    ),
):
    logging.basicConfig(
        format="%(message)s",
        level=getattr(logging, log_level.upper()),
        handlers=[RichHandler(rich_tracebacks=True, tracebacks_suppress=[typer])],
    )
    app_state["build_tool"] = BuildTool(poetry=poetry, verbose=verbose)
    if context.invoked_subcommand is None:
        logger.debug("No command specified; defaulting to build.")
        build()


@app.command()
def format():
    """
    Run isort, autoflake, and black on the src/ and test/ directories.
    """
    returncode = app_state["build_tool"].auto_format()
    print(f"slam format: {'SUCCESS' if returncode == 0 else 'ERROR'}")
    return returncode


@app.command()
def build():
    """
    Calls format, test, and install before invoking 'poetry build'.
    """
    returncode = app_state["build_tool"].build()
    print(f"slam build: {'SUCCESS' if returncode == 0 else 'ERROR'}")
    return returncode


@app.command()
def install():
    """
    Synonym for 'poetry install'
    """
    returncode = app_state["build_tool"].install()
    print(f"slam install: {'SUCCESS' if returncode == 0 else 'ERROR'}")
    return returncode


@app.command(context_settings={"allow_extra_args": True, "ignore_unknown_options": True})
def test(context: typer.Context):
    """
    Synonym for 'poetry run pytest' Output is always verbose.
    """
    app_state["build_tool"].verbose = True
    returncode = app_state["build_tool"].test(context.args)
    print(f"slam test: {'SUCCESS' if returncode == 0 else 'ERROR'}")
    return returncode