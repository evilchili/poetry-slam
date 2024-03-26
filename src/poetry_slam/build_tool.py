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

    def _exec(self, *command_line) -> bool:
        """
        Execute a subprocess.
        """
        cmdline = [str(self.poetry)] + list(command_line)
        logger.info(" ".join(cmdline))
        if self.verbose:
            result = subprocess.run(cmdline, shell=True)
            return result.returncode

        result = subprocess.run(cmdline, capture_output=True, shell=True)
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

    def run_with_poetry(self, *command_line):
        return self._exec(str(self.poetry), *command_line)

    def run(self, *command_line):
        """
        Same as run_with_poetry(), but prepend a 'run' subcommand.
        """
        return self.run_with_poetry("run", *command_line)

    def install(self) -> bool:
        return self.run_with_poetry("install")

    def auto_format(self) -> bool:
        self._exec("isort", "src", "test")
        self._exec("autoflake", "src", "test")
        self._exec("black", "src", "test")
        return 0

    def test(self, args) -> bool:
        return self._exec("pytest", *args)

    def build(self) -> bool:
        print("Formatting...")
        success = self.auto_format()
        print("Testing...")
        success += self.test([])
        print("Installing...")
        success += self.install()
        print("Building...")
        success += self.run_with_poetry("build")
        return success