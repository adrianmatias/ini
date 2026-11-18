"""The gates that are ruff rules: one maintained tool, asked through one seam, with ini's selections.

ini owns the rule selection — each gate passes its own `--select` — so a project inherits the
rules when it upgrades ini, and its `pyproject.toml` keeps only what is the project's to decide
(line length, target version). A per-file ignore in the project is visible in review; a blanket
ignore or a raised budget is refused by the standard, not by this code.
"""

import re
from dataclasses import dataclass
from typing import ClassVar

from pydantic import BaseModel, TypeAdapter

from ci.core.errors import IniError
from ci.core.project import Project, Scope
from ci.core.tool import Finding, Tool
from ci.gates.gate import Gate
from ci.gates.session import Session

# ruff's C901 message: "`name` is too complex (7 > 6)". The score is the tool's.
COMPLEX = re.compile(r"`(?P<name>[^`]+)` is too complex \((?P<score>\d+) > \d+\)")
BANNED = (
    "lint.flake8-tidy-imports.banned-api = {"
    " 'typing.TypedDict' = { msg = 'a dict-as-record: declare a pydantic model or a dataclass' },"
    " 'typing_extensions.TypedDict' = { msg = 'a dict-as-record: declare a model' },"
    " 'pickle' = { msg = 'executable data: serialise a model with model_dump_json' } }"
)


class _Location(BaseModel):
    row: int


class _Diagnostic(BaseModel):
    code: str | None
    message: str
    filename: str
    location: _Location


DIAGNOSTICS = TypeAdapter(list[_Diagnostic])


@dataclass(frozen=True, slots=True)
class Run:
    """One ruff invocation: the scope it reads, the rules it selects, the settings it overrides."""

    scope: Scope
    select: str
    ignore: str = ""
    config: tuple[str, ...] = ()


class Ruff:
    """ruff, asked for findings in JSON and decoded once."""

    def __init__(self, tool: Tool) -> None:
        self.tool = tool

    def check(self, run: Run) -> list[Finding]:
        """The findings of one run; a ruff error (exit 2) is the gate's hard stop."""
        paths = [str(path) for path in self.tool.project.paths(run.scope)]
        if not paths:
            return []
        args = ["check", "--no-cache", "--output-format", "json", "--select", run.select]
        args += ["--ignore", run.ignore] if run.ignore else []
        for excluded in self.tool.project.excluded(run.scope):
            args += ["--force-exclude", "--extend-exclude", self.tool.project.relative(excluded)]
        args += [flag for setting in run.config for flag in ("--config", setting)]
        outcome = self.tool.run("ruff", *args, *paths)
        if outcome.code not in (0, 1):
            raise IniError(f"ruff failed: {outcome.tail()}")
        return [self.finding(d) for d in DIAGNOSTICS.validate_json(outcome.out)]

    def finding(self, diagnostic: _Diagnostic) -> Finding:
        """A diagnostic as a finding; a complexity finding also names its function."""
        found = COMPLEX.match(diagnostic.message)
        return Finding(
            path=self.tool.project.relative(diagnostic.filename),
            line=diagnostic.location.row,
            rule=diagnostic.code or "syntax",
            message=diagnostic.message,
            subject=found["name"] if found else "",
        )

    @staticmethod
    def score(finding: Finding) -> int:
        """The complexity a C901 finding states; 0 for any other finding."""
        found = COMPLEX.match(finding.message)
        return int(found["score"]) if found else 0

    def unformatted(self, scope: Scope) -> list[Finding]:
        """Files `ruff format` would rewrite: layout is the formatter's, never a review topic."""
        paths = [str(path) for path in self.tool.project.paths(scope)]
        outcome = self.tool.run("ruff", "format", "--check", "--no-cache", *paths)
        return [
            Finding(self.tool.project.relative(line.removeprefix("Would reformat: ")), 1, "format",
                    "not formatted: `uv run ruff format`")
            for line in outcome.out.splitlines()
            if line.startswith("Would reformat: ")
        ]  # fmt: skip


class RuffGate(Gate):
    """A gate that is a set of ruff runs."""

    runs: ClassVar[tuple[Run, ...]]

    def findings(self, session: Session) -> list[Finding]:
        """Every run's findings, in order."""
        ruff = Ruff(session.tool)
        return [finding for run in self.runs for finding in ruff.check(run)]


class Lint(RuffGate):
    """Defects, unclear code and layout."""

    name = "lint"
    catches = "defects (F, B), relative imports, globals, data clumps, unidiomatic code, layout"
    # E501 is the formatter's: what `ruff format` leaves long is a string or a docstring line.
    runs = (
        Run(
            Scope.ALL,
            "E,F,I,B,UP,SIM,RUF,TID252,PLW0603,PLR0913",
            ignore="E501",
            config=("lint.flake8-tidy-imports.ban-relative-imports = 'all'",),
        ),
    )

    def findings(self, session: Session) -> list[Finding]:
        """The rules, then the formatter."""
        return super().findings(session) + Ruff(session.tool).unformatted(Scope.ALL)

    def witness(self, project: Project) -> dict[str, str]:
        """An unused import."""
        return self.in_package(project, '"""Witness: an unused import."""\n\nimport os\n')


class Annotations(RuffGate):
    """Every function states what it takes and returns; `Any` never appears in a signature. A test
    has no caller to state a contract to, so the suite is left out."""

    name = "annotations"
    catches = "an unstated contract, or Any in a signature"
    runs = (Run(Scope.CODE, "ANN"),)

    def witness(self, project: Project) -> dict[str, str]:
        """A function with neither parameter nor return annotated."""
        return self.in_package(project, '"""Witness."""\n\n\ndef echo(value):\n    return value\n')


class Docs(RuffGate):
    """Self-commented code: modules, packages and classes say what they are; no commented-out code."""

    name = "docs"
    catches = "a module, package or class that does not say what it is; commented-out code"
    runs = (Run(Scope.CODE, "D100,D101,D104,D419"), Run(Scope.ALL, "ERA001"))

    def witness(self, project: Project) -> dict[str, str]:
        """A public module with no docstring and a line of dead code."""
        return self.in_package(project, "# value = compute()\nVALUE = 1\n")


class Complexity(RuffGate):
    """A function over budget wants its data as a table and its code as the interpreter."""

    name = "complexity"
    catches = "a function over the complexity budget (6 in code, 15 in a test)"
    runs = (
        Run(Scope.CODE, "C901", config=("lint.mccabe.max-complexity = 6",)),
        Run(Scope.TESTS, "C901", config=("lint.mccabe.max-complexity = 15",)),
    )

    def witness(self, project: Project) -> dict[str, str]:
        """A cascade of seven branches."""
        branches = "".join(f"    if x == {i}:\n        return {i}\n" for i in range(7))
        text = f'"""Witness."""\n\n\ndef cascade(x: int) -> int:\n{branches}    return -1\n'
        return self.in_package(project, text)


class Surface(RuffGate):
    """Shapes that are refused outright: dict-as-record, executable strings, executable data."""

    name = "surface"
    catches = "TypedDict, eval/exec, pickle"
    runs = (Run(Scope.ALL, "TID251,S102,S307,S301", config=(BANNED,)),)

    def witness(self, project: Project) -> dict[str, str]:
        """A TypedDict record."""
        return self.in_package(project, '"""Witness."""\n\nfrom typing import TypedDict\n')
