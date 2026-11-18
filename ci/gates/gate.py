"""The gate: a deterministic check that reports findings and carries the defect it must reject.

A gate you have not seen fail is not a gate. Each one returns a witness — files that, written into a
copy of the project, must turn it red with a finding located in one of them — and `python -m ci gates
--prove` plants every witness. A gate whose witness passes is inert, and that is a red run.
"""

from abc import ABC, abstractmethod
from typing import ClassVar

from ci.core.project import Project
from ci.core.tool import Finding
from ci.gates.session import Session

WITNESS = "ini_witness.py"


class Gate(ABC):
    """A deterministic check: the findings it reports, and the planted defect that proves it."""

    name: ClassVar[str]
    catches: ClassVar[str]
    ratchet: ClassVar[bool] = True

    @abstractmethod
    def findings(self, session: Session) -> list[Finding]:
        """Every defect of this gate's class in the project, recorded debt included."""

    @abstractmethod
    def witness(self, project: Project) -> dict[str, str]:
        """Files (project-relative path to text) that must make this gate red."""

    @staticmethod
    def in_package(project: Project, text: str, name: str = WITNESS) -> dict[str, str]:
        """A witness module planted in the production package."""
        return {project.relative(project.package / name): text}
