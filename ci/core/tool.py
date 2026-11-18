"""What a gate reports, and how a maintained tool is asked for it.

Every tool runs as a module of the interpreter that runs ini, so the project's own environment
(pinned by its lock) is the one judged. The child's import path is the project's `src/` and nothing
else: a harness that exports its own `PYTHONPATH` once made a venv import a foreign `pydantic_core`
and turned five gates red on a green tree.
"""

import os
import subprocess
import sys
from dataclasses import dataclass
from importlib.util import find_spec

from ci.core.errors import IniError
from ci.core.project import Project


@dataclass(frozen=True, slots=True)
class Finding:
    """One defect: where it is, the rule it breaks, what the tool said, and the function if any."""

    path: str
    line: int
    rule: str
    message: str
    subject: str = ""

    @property
    def key(self) -> str:
        """What the ratchet counts: the file and the rule, and the function when one is named."""
        return "::".join(part for part in (self.path, self.rule, self.subject) if part)

    def __str__(self) -> str:
        return f"{self.path}:{self.line}: {self.rule} {self.message}"


@dataclass(frozen=True, slots=True)
class Outcome:
    """How a tool exited, what it printed to stdout, and what it printed to stderr."""

    code: int
    out: str
    err: str = ""

    def tail(self) -> str:
        """The end of both streams: what a refusal quotes when a tool itself broke."""
        return (self.out + self.err)[-2000:]


class Tool:
    """A maintained tool, run as `python -m <module>` from the project root in a clean environment."""

    def __init__(self, project: Project) -> None:
        self.project = project

    def env(self) -> dict[str, str]:
        """The parent's environment with the import path replaced by the project's source root."""
        env = {key: value for key, value in os.environ.items() if key != "PYTHONPATH"}
        return env | {"PYTHONPATH": str(self.project.src), "NO_COLOR": "1"}

    def run(self, module: str, *args: str) -> Outcome:
        """Run the module with the arguments; never raises on a non-zero exit, the gate reads it.
        A missing tool is a refusal: its empty failure would otherwise read as a clean verdict."""
        if find_spec(module) is None:
            raise IniError(
                f"`{module}` is not installed: `uv sync` (the dev group holds the gates)"
            )
        proc = subprocess.run(
            [sys.executable, "-m", module, *args],
            cwd=self.project.root,
            capture_output=True,
            text=True,
            env=self.env(),
            check=False,
        )
        return Outcome(proc.returncode, proc.stdout, proc.stderr)
