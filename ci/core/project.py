"""The project a command judges: its root, its `[tool.ini]` settings and the paths they name.

Settings are outside data (a TOML file a person edits), so they are decoded once, here, into a
frozen model; every other module asks `Project` for a path and never reads `pyproject.toml` again.
"""

import tomllib
from enum import StrEnum
from pathlib import Path

from pydantic import BaseModel, ConfigDict

from ci.core.errors import IniError

# Directories no gate reads and no scope rule asks about: tool state, not project code.
SKIPPED = frozenset({".git", ".venv", "node_modules", "__pycache__", ".tmp", "dist", "build"})


class Scope(StrEnum):
    """Which of the project's Python directories a check reads."""

    PRODUCTION = "production"
    CODE = "code"
    TESTS = "tests"
    ALL = "all"


class Settings(BaseModel):
    """The `[tool.ini]` table: where the project keeps what the gates read. Every key is optional."""

    model_config = ConfigDict(frozen=True, extra="forbid", use_attribute_docstrings=True)

    src: str = "src"
    """Directory that holds the package and goes on the import path; `.` for a flat layout."""
    package: str = ""
    """Import name of the package under `src`; empty means the one package found there."""
    tests: str = "tests"
    """Directory of the behaviour suite."""
    scripts: tuple[str, ...] = ()
    """Directories of hand-run scripts: linted, typed and annotated, never measured for coverage."""
    domain: str = "domain.md"
    """Page that holds the rendered ontology."""
    agents: str = "AGENTS.md"
    """The project's agent contract."""
    ceilings: str = "ci/ceilings.json"
    """Recorded debt the ratchet holds: per gate, per file and rule, a count that only shrinks."""


class Project:
    """A repository the gates judge: its root, its settings and every path they name."""

    def __init__(self, root: Path, settings: Settings) -> None:
        self.root = root.resolve()
        self.settings = settings

    @classmethod
    def load(cls, root: Path) -> Project:
        """Read `[tool.ini]` from the root's `pyproject.toml`; absent table, default settings."""
        pyproject = root / "pyproject.toml"
        if not pyproject.is_file():
            raise IniError(f"no pyproject.toml in {root}: ini judges uv projects")
        table = tomllib.loads(pyproject.read_text()).get("tool", {}).get("ini", {})
        return cls(root, Settings.model_validate(table))

    @property
    def src(self) -> Path:
        """The source root, the one entry the tools put on the import path."""
        return self.root / self.settings.src

    @property
    def package(self) -> Path:
        """The production package: named in settings, or the only one under `src/`."""
        if self.settings.package:
            return self.src / self.settings.package
        found = sorted(p.parent for p in self.src.glob("*/__init__.py"))
        if len(found) != 1:
            raise IniError(f"{len(found)} packages under {self.src}: name one in [tool.ini]")
        return found[0]

    @property
    def tests(self) -> Path:
        """The behaviour suite."""
        return self.root / self.settings.tests

    @property
    def scripts(self) -> tuple[Path, ...]:
        """Hand-run script directories that exist."""
        return tuple(p for p in (self.root / s for s in self.settings.scripts) if p.is_dir())

    @property
    def skills(self) -> Path:
        """The procedures agents read when their trigger matches, one directory per skill."""
        return self.root / "skills"

    @property
    def domain(self) -> Path:
        """The page the ontology is rendered into."""
        return self.root / self.settings.domain

    @property
    def agents(self) -> Path:
        """The agent contract."""
        return self.root / self.settings.agents

    @property
    def ceilings(self) -> Path:
        """The ratchet's record."""
        return self.root / self.settings.ceilings

    @property
    def nested(self) -> Path | None:
        """The suite when it lives inside the package: there it is tests, never production."""
        tests, package = self.tests, self.package
        return tests if tests != package and tests.is_relative_to(package) else None

    def excluded(self, scope: Scope) -> tuple[Path, ...]:
        """What a scope's directories contain but the scope does not judge."""
        code = scope in {Scope.PRODUCTION, Scope.CODE}
        return (self.nested,) if code and self.nested is not None else ()

    def paths(self, scope: Scope) -> tuple[Path, ...]:
        """The existing directories a scope names."""
        named = {
            Scope.PRODUCTION: (self.package,),
            Scope.CODE: (self.package, *self.scripts),
            Scope.TESTS: (self.tests,),
            Scope.ALL: (self.package, self.tests, *self.scripts),
        }[scope]
        return tuple(path for path in named if path.is_dir())

    def relative(self, path: Path | str) -> str:
        """A path as the project names it: relative to the root, forward slashes."""
        located = Path(path)
        located = located if located.is_absolute() else self.root / located
        return located.resolve().relative_to(self.root).as_posix()

    def python_files(self, *dirs: Path) -> list[Path]:
        """Every `.py` file under the given directories (all of the project when none), tool state
        and hidden directories skipped, in a stable order. The package read alone leaves out a suite
        nested in it."""
        roots = dirs or (self.root,)
        nested = self.excluded(Scope.PRODUCTION)
        return sorted(
            path
            for root in roots
            for path in root.rglob("*.py")
            if not any(
                part in SKIPPED or part.startswith(".")
                for part in path.relative_to(self.root).parts
            )
            and not (root == self.package and any(path.is_relative_to(n) for n in nested))
        )
