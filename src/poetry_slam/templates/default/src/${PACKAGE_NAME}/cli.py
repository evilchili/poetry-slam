import io
import logging
from pathlib import Path
from typing import Optional

import typer
from dotenv import load_dotenv
from rich.logging import RichHandler


CONFIG_DEFAULTS = """
# ${PROJECT_NAME} Defaults

LOG_LEVEL=INFO
"""

app = typer.Typer()
app_state = dict(
    config_file=Path("~/.config/${PROJECT_NAME}.conf").expanduser(),
)

logger = logging.getLogger("${PACKAGE_NAME}.cli")


@app.callback(invoke_without_command=True)
def main(
    context: typer.Context,
    verbose: bool = typer.Option(False, help="Enable verbose output."),
    log_level: str = typer.Option("error", help=" Set the log level."),
    config_file: Optional[Path] = typer.Option(
        app_state["config_file"],
        help="Path to the ${PACKAGE_NAME} configuration file",
    ),
):
    """
    Configure the execution environment with global parameters.
    """
    app_state["config_file"] = config_file
    load_dotenv(stream=io.StringIO(CONFIG_DEFAULTS))
    load_dotenv(app_state["config_file"])

    logging.basicConfig(
        format="%(message)s",
        level=getattr(logging, log_level.upper()),
        handlers=[RichHandler(rich_tracebacks=True, tracebacks_suppress=[typer])],
    )
    app_state["verbose"] = verbose

    if context.invoked_subcommand is None:
        logger.debug("No command specified; invoking default handler.")
        run(context)


def run(context: typer.Context):
    """
    The default CLI entrypoint is ${PACKAGE_NAME}.cli.run().
    """
    raise NotImplementedError("Please define ${PACKAGE_NAME}.cli.run().")
