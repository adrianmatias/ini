"""Behaviour of a copy of ini started as a project, and of `domain`: it starts and maps itself."""

from ci.cli.main import main

MODELS = '''"""A domain with every kind of class."""

from dataclasses import dataclass
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class Wired(BaseModel):
    """A base that turns attribute docstrings into descriptions."""

    model_config = ConfigDict(use_attribute_docstrings=True)


class Colour(StrEnum):
    """A closed vocabulary."""

    RED = "red"


@dataclass(frozen=True, slots=True)
class Point:
    """A value."""

    x: int


class Shape(Wired):
    """A wire model that inherits the docstring config."""

    colour: Colour
    """What it looks like."""
    corner: Point = Field(description="Where it starts.")


class Refused(Exception):
    """A refusal."""
'''


def test_a_copy_starts_with_the_skeleton_and_the_base(project) -> None:
    for path in ("AGENTS.md", "objective.md", "log/director.md", "src/demo/core/objective.py"):
        assert (project / path).is_file(), path
    assert (project / "base/skills/kickoff/SKILL.md").is_file()
    assert not (project / "ci/tests").exists(), "ini's own suite stays in ini"
    rendered = [p for p in project.rglob("*{{*") if not p.is_relative_to(project / "base")]
    assert not rendered, "a placeholder is left in a path"


def test_the_ontology_reads_kinds_and_relations_from_the_code(kicked_off, capsys) -> None:
    (kicked_off / "src/demo/core/shapes.py").write_text(MODELS)
    assert main(["gates", "--root", str(kicked_off), "--only", "domain"]) == 1, "stale page"
    assert main(["domain", "--root", str(kicked_off), "--write"]) == 0
    page = (kicked_off / "domain.md").read_text()
    for row in ("`Colour` | vocabulary", "`Point` | value", "`Refused` | error",
                "`Shape` | wire | Wired | Colour, Point"):  # fmt: skip
        assert row in page
    assert main(["domain", "--root", str(kicked_off), "--write"]) == 0
    assert (kicked_off / "domain.md").read_text() == page, "rendering is deterministic"
    capsys.readouterr()
    assert main(["gates", "--root", str(kicked_off), "--only", "domain"]) == 0
