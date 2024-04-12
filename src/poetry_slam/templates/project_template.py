import logging

from dataclasses import dataclass, field
from pathlib import Path
from string import Template


TEMPLATE_ROOT = Path(__file__).parent

logger = logging.getLogger("slam.templates")


@dataclass
class ProjectTemplate:
    root: Path = TEMPLATE_ROOT / "default"
    values: field(default_factory=dict) = None

    @property
    def paths(self) -> list:
        def walk(path):
            files = []
            for path in path.iterdir():
                if path.is_dir():
                    files += walk(path)
                else:
                    files.append(path)
            return files
        return walk(self.root)

    def render(self, path) -> tuple:
        """
        Return a tuple of the formatted destination path name and the file contents, if any.
        """
        if path.is_dir():
            body = None
        else:
            body = Template((TEMPLATE_ROOT / path).read_text()).substitute(self.values)

        relpath = path.relative_to(self.root)
        path_template = Template(str(relpath)).substitute(self.values)
        return Path(path_template), body

    def apply(self):
        """
        Apply the template to the current directory, creating any missing files and directories.
        """
        if not Path(".git").exists():
            raise RuntimeError("Cannot apply a template outside of a project root (no .git present here).")
        if Path("pyproject.toml").exists():
            raise RuntimeError(
                "Cannot apply a template to an existing project. "
                "Maybe you meant slam init, to apply defaults to your pyproject.toml?"
            )
        for path in self.paths:
            logger.debug(f"Processing {path}...")
            target, body = self.render(path)
            if not target.parent.exists():
                target.parent.mkdir(parents=True, exist_ok=True)
            if not target.exists():
                target.write_text(body)
                logger.info(f"Created {target}")
            else:
                logger.warn(f"Skipping existing file {target}")

    def __repr__(self):
        return f"{self.root}: {self.values}"
