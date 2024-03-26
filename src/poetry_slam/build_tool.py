import logging
import subprocess
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger("slam.build_tool")


class BuildError(Exception):
    """
    Thrown when a subprocess command fails.
    """


@dataclass
class BuildTool:
    """
    Thin wrapper around poetry and some dev tools.
    """

    poetry: Path = Path("poetry")
    verbose: bool = False

    def do(self, *command_line) -> bool:
        """
        Execute a poetry subprocess.
        """
        cmdline = [str(self.poetry)] + list(command_line)
        logger.info(" ".join(cmdline))
        if self.verbose:
            result = subprocess.run(cmdline)
            return result.returncode

        result = subprocess.run(cmdline, capture_output=True)
        logger.debug(f"{result = }")
        if result.stdout:
            # log the output and optional print it
            logger.info(result.stdout)
            if self.verbose:
                print(result.stdout.decode("utf-8"))
        if result.stderr:
            # log the error and optionally print it
            if self.verbose:
                print(result.stderr.decode("utf-8"))
            if result.returncode != 0:
                logger.error(result.stderr)
                raise BuildError(f"Command Failed: {cmdline}")
            logger.info(result.stderr)
        return result.returncode

    def run(self, *command_line):
        """
        Same as do(), but prepend a 'run' subcommand.
        """
        return self.do("run", *command_line)

    def install(self) -> bool:
        return self.do("install")

    def auto_format(self) -> bool:
        self.run("isort", "src", "test")
        self.run("autoflake", "src", "test")
        self.run("black", "src", "test")
        return 0

    def test(self, args) -> bool:
        return self.run("pytest", *args)

    def build(self) -> bool:
        print("Formatting...")
        success = self.auto_format()
        print("Testing...")
        success += self.test([])
        print("Installing...")
        success += self.install()
        print("Building...")
        success += self.do("build")
        return success
