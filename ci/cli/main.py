"""The harness command: gates and domain. Each verb parses its arguments and calls one method.

uv run python -m ci gates                 # every gate; red blocks the change
uv run python -m ci gates --prove         # plant each witness in a scratch copy: it must turn red
uv run python -m ci gates --record        # lower the ratchet to what the gates measure now
uv run python -m ci gates --adopt         # an existing project records today's debt, once
uv run python -m ci domain --write        # render the ontology into the domain page
"""

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from ci.core.errors import IniError
from ci.core.project import Project
from ci.gates.runner import Runner
from ci.gates.table import GATES
from ci.ontology.reader import Reader
from ci.ontology.render import Page, Renderer


def gates(args: argparse.Namespace) -> int:
    """Check, prove, record, adopt or list."""
    runner = Runner(Project.load(args.root))
    if args.list:
        return runner.describe()
    if args.prove:
        return runner.prove(args.only)
    return runner.check(args.only, record=args.record, adopt=args.adopt)


def domain(args: argparse.Namespace) -> int:
    """Print the rendered ontology, or write it into the domain page."""
    project = Project.load(args.root)
    rendered = Renderer(Reader(project).read()).render()
    if args.write:
        Page(project.domain).write(rendered)
    else:
        print(rendered)
    return 0


def parser() -> argparse.ArgumentParser:
    """The verbs and their options."""
    root = argparse.ArgumentParser(prog="python -m ci", description="the deterministic gates")
    verbs = root.add_subparsers(dest="verb", required=True)
    check = verbs.add_parser("gates", help="run the deterministic gates")
    check.add_argument("--only", action="append", default=[], choices=[g.name for g in GATES])
    for flag, text in (
        ("prove", "plant each witness"),
        ("record", "lower the ratchet"),
        ("adopt", "record today's debt"),
        ("list", "describe the gates"),
    ):
        check.add_argument(f"--{flag}", action="store_true", help=text)  # fmt: skip
    render = verbs.add_parser("domain", help="render the ontology")
    render.add_argument("--write", action="store_true", help="into the domain page")
    for verb in (check, render):
        verb.add_argument("--root", type=Path, default=Path.cwd(), help="the project root")
    return root


def main(argv: Sequence[str] | None = None) -> int:
    """Parse, dispatch, and turn a refusal into exit code 2."""
    args = parser().parse_args(argv)
    try:
        return {"gates": gates, "domain": domain}[args.verb](args)
    except IniError as refusal:
        print(f"ini: {refusal}", file=sys.stderr)
        return 2
