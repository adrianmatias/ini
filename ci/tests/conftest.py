"""Shared fixtures: a copy of this repository, started as a new project the way the kickoff does."""

import shutil
from pathlib import Path

import pytest

from ci.cli.main import main

ROOT = Path(__file__).resolve().parents[2]
TEMPLATES = ROOT / "base/skills/kickoff/templates"
IGNORED = shutil.ignore_patterns(".git", ".venv", "__pycache__", "*.pyc", ".obsidian", ".*_cache")
HARNESS = 'src = "."\npackage = "ci"\ntests = "ci/tests"\n'
PROJECT = 'src = "src"\npackage = "demo"\ntests = "tests"\nscripts = ["ci"]\n'
BUILD = '[build-system]\nrequires = ["uv_build>=0.13.5,<0.14.0"]\nbuild-backend = "uv_build"\n'
VALUES = {"project": "demo", "package": "demo", "owner": "director", "date": "2026-11-18"}


def render(text: str) -> str:
    """Replace every `{{key}}` the templates use."""
    for key, value in VALUES.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def start(copy: Path) -> None:
    """The kickoff's mechanical part: the templates replace ini's own anchors, logs and suite, and
    `[tool.ini]` points at the new package."""
    shutil.rmtree(copy / "ci/tests")
    shutil.rmtree(copy / "log")
    for template in TEMPLATES.rglob("*.tmpl"):
        target = copy / render(str(template.relative_to(TEMPLATES).with_suffix("")))
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render(template.read_text()))
    pyproject = copy / "pyproject.toml"
    text = pyproject.read_text().replace('name = "ini"', 'name = "demo"').replace(HARNESS, PROJECT)
    text = text.replace('["ci/tests"]', '["tests"]').replace('["."]', '["src"]')
    start_, end = text.index("\n[tool.uv]\n"), text.index("\n[tool.ini]\n")
    pyproject.write_text(text[: start_ + 1] + BUILD + text[end:])
    assert main(["domain", "--root", str(copy), "--write"]) == 0


@pytest.fixture
def project(tmp_path: Path) -> Path:
    """A fresh copy of ini, started as `demo`, its kickoff placeholders not yet answered."""
    copy = tmp_path / "demo"
    shutil.copytree(ROOT, copy, ignore=IGNORED)
    start(copy)
    return copy


@pytest.fixture
def kicked_off(project: Path) -> Path:
    """The same project after a kickoff that answered every placeholder."""
    for page in project.glob("*.md"):
        page.write_text(page.read_text().replace("TODO(kickoff)", "stated"))
    return project
