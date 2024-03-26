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

    project_root: Path = Path(".")
    poetry: Path = Path("poetry")
    verbose: bool = False

    def _exec(self, *command_line) -> bool:
        """
        Execute a subprocess.
        """
        cmd = " ".join(command_line)
        logger.info(f"Executing: '{cmd}'")
        if self.verbose:
            result = subprocess.run(cmd, shell=True)
            return result.returncode

        result = subprocess.run(cmd, capture_output=True, shell=True)
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
                raise BuildError(f"Command Failed: {command_line}")
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
        src = str((self.project_root / "src").absolute())
        test = str((self.project_root / "test").absolute())
        self._exec("isort", src, test)
        self._exec("autoflake", src, test)
        self._exec("black", src, test)
        return 0

    def test(self, args) -> bool:
        old_v = self.verbose
        self.verbose = True
        returncode = self.run("pytest", *args)
        self.verbose = old_v
        return returncode

    def build(self) -> bool:
        print("Formatting...")
        success = self.auto_format()
        print("Installing...")
        success += self.install()
        print("Testing...")
        success += self.test([])
        print("Building...")
        success += self.run_with_poetry("build")
        return success
