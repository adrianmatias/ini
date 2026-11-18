"""Run the gates: hold each to its ratchet, print one line per gate, end with the tally.

`--prove` runs each gate against its witness instead of the tree: the project's gate inputs are
copied into a scratch directory, the witness is planted there — never in the working tree — and the
gate must turn red with a finding in a planted file. Green under a witness means the gate is inert.
"""

import shutil
from collections.abc import Sequence
from pathlib import Path
from tempfile import TemporaryDirectory

from ci.core.errors import IniError
from ci.core.project import Project
from ci.core.tool import Finding
from ci.gates.gate import Gate
from ci.gates.ratchet import Ceilings
from ci.gates.session import Session
from ci.gates.table import GATES

SHOWN = 12
# What a replica needs beyond the Python scopes: the anchors and records the harness reads. Root
# files above a megabyte (a PDF dropped at the root of a vault) are no gate's input.
INPUTS = ("ci", "skills", "wiki")
ROOT_FILE_BYTES = 1_000_000
IGNORED = shutil.ignore_patterns(".git", ".venv", "__pycache__", "*.pyc", "node_modules", ".tmp")


class Replica:
    """A scratch copy of the project's gate inputs, where a witness can be planted safely."""

    def __init__(self, project: Project, into: Path) -> None:
        self.project = project
        self.into = into

    def build(self) -> Project:
        """Copy the small root files, the Python scopes, the base and the harness directories."""
        source = self.project.root
        for path in source.iterdir():
            if path.is_file() and path.stat().st_size <= ROOT_FILE_BYTES:
                shutil.copy2(path, self.into / path.name)
        top = {source / name for name in INPUTS} | {self.project.package, self.project.tests}
        top |= {*self.project.scripts, self.project.base}
        for directory in sorted(p for p in top if p.is_dir() and p.is_relative_to(source)):
            target = self.into / directory.relative_to(source)
            if not target.exists():
                shutil.copytree(directory, target, ignore=IGNORED)
        return Project(self.into, self.project.settings)

    def plant(self, files: dict[str, str]) -> Project:
        """Build the copy and write the witness files into it."""
        replica = self.build()
        for relative, text in files.items():
            target = self.into / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text)
        return replica


class Runner:
    """The gates over one project: check, prove, record, adopt, describe."""

    def __init__(self, project: Project, gates: Sequence[Gate] = GATES) -> None:
        self.project = project
        self.gates = {gate.name: gate for gate in gates}

    def select(self, names: Sequence[str]) -> list[Gate]:
        """The named gates in table order, or all of them."""
        unknown = set(names) - self.gates.keys()
        if unknown:
            raise IniError(
                f"no gate named {', '.join(sorted(unknown))}: `python -m ci gates --list`"
            )
        return [gate for name, gate in self.gates.items() if not names or name in names]

    def describe(self) -> int:
        """Each gate's name and the defect class it catches."""
        for gate in self.gates.values():
            print(f"{gate.name:12s} {gate.catches}")
        return 0

    def check(self, names: Sequence[str] = (), record: bool = False, adopt: bool = False) -> int:
        """Run the gates; red is any finding past the ratchet. `record` lowers the ceilings to what
        was measured; `adopt` records today's debt as the starting point."""
        session = Session(self.project)
        label = self.project.relative(self.project.ceilings)
        ceilings = Ceilings(self.project.ceilings, label)
        results: dict[str, bool] = {}
        for gate in self.select(names):
            findings = gate.findings(session)
            if gate.ratchet and adopt:
                ceilings.adopt(gate.name, findings)
            elif gate.ratchet and record:
                ceilings.record(gate.name, findings)
            red = ceilings.judge(gate.name, findings) if gate.ratchet else findings
            results[gate.name] = not red
            self.report(gate, red, len(findings) - len(red))
        if record or adopt:
            ceilings.save()
        return self.tally(results, "green")

    def prove(self, names: Sequence[str] = ()) -> int:
        """Plant each gate's witness in a replica; a gate passes only if the witness turns it red."""
        results: dict[str, bool] = {}
        for gate in self.select(names):
            with TemporaryDirectory(prefix="ini-prove-") as scratch:
                witness = gate.witness(self.project)
                replica = Replica(self.project, Path(scratch)).plant(witness)
                ceilings = Ceilings(replica.ceilings, "ceilings")
                findings = gate.findings(Session(replica))
                red = ceilings.judge(gate.name, findings) if gate.ratchet else findings
            caught = [f for f in red if f.path in witness]
            results[gate.name] = bool(caught)
            line = f"rejected: {caught[0]}" if caught else "witness ACCEPTED — the gate is inert"
            print(f"{'ok  ' if caught else 'FAIL'}  {gate.name:12s} {line}")
        return self.tally(results, "proofs passed")

    @staticmethod
    def report(gate: Gate, red: list[Finding], held: int) -> None:
        """One line per gate, then the first findings that make it red."""
        debt = f" ({held} held by the ratchet)" if held else ""
        print(f"{'FAIL' if red else 'ok  '}  {gate.name:12s} {len(red)} red{debt}")
        for finding in red[:SHOWN]:
            print(f"      {finding}")
        if len(red) > SHOWN:
            print(f"      … {len(red) - SHOWN} more")

    @staticmethod
    def tally(results: dict[str, bool], label: str) -> int:
        """The closing line; 1 when any gate is not green."""
        failed = [name for name, ok in results.items() if not ok]
        print(f"\n{label}: {len(results) - len(failed)}/{len(results)}")
        if failed:
            print("not green: " + ", ".join(failed))
        return 1 if failed else 0
