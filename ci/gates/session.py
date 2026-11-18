"""One gate run: the project, its tools, and what several gates share — measured once.

The behaviour suite runs once, under coverage: the behaviour gate reads how it exited and the CRAP
gate reads how much of each function it executed. Running it twice would double the slowest gate
and let the two readings disagree.
"""

from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from tempfile import TemporaryDirectory

from pydantic import BaseModel

from ci.core.project import Project
from ci.core.tool import Outcome, Tool
from ci.ontology.model import Ontology
from ci.ontology.reader import Reader


class _Summary(BaseModel):
    percent_covered: float


class _Function(BaseModel):
    start_line: int
    summary: _Summary


class _File(BaseModel):
    functions: dict[str, _Function] = {}


class _Report(BaseModel):
    """The part of coverage.py's JSON report the CRAP gate reads; the rest is the tool's own."""

    files: dict[str, _File]


@dataclass(frozen=True, slots=True)
class Suite:
    """One run of the behaviour suite under coverage: its exit, and the share of each function run."""

    outcome: Outcome
    covered: dict[tuple[str, int], float]

    @classmethod
    def measure(cls, tool: Tool) -> Suite:
        """Run pytest under coverage over the production package and read the per-function report.
        pytest collects what `testpaths` names, so a project with more than one suite runs them all."""
        project = tool.project
        with TemporaryDirectory() as scratch:
            data, report = Path(scratch) / ".coverage", Path(scratch) / "coverage.json"
            outcome = tool.run(
                "coverage", "run", f"--data-file={data}", f"--source={project.package}",
                "-m", "pytest", "-p", "no:cacheprovider",
            )  # fmt: skip
            tool.run("coverage", "json", f"--data-file={data}", "-o", str(report), "-q")
            covered = cls.read(project, report) if report.is_file() else {}
        return cls(outcome, covered)

    @staticmethod
    def read(project: Project, report: Path) -> dict[tuple[str, int], float]:
        """(file, line of the `def`) to the share of the function's statements the suite ran."""
        parsed = _Report.model_validate_json(report.read_text())
        return {
            (project.relative(path), function.start_line): function.summary.percent_covered / 100
            for path, measured in parsed.files.items()
            for function in measured.functions.values()
        }


class Session:
    """The shared state of one gate run over one project."""

    def __init__(self, project: Project) -> None:
        self.project = project
        self.tool = Tool(project)

    @cached_property
    def ontology(self) -> Ontology:
        """The domain read from the package, once."""
        return Reader(self.project).read()

    @cached_property
    def suite(self) -> Suite:
        """The behaviour suite's single run."""
        return Suite.measure(self.tool)
