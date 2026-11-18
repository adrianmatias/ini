"""The gates that are other maintained tools: ty for types, vulture for dead code, symilar for copies.

Each one is asked once and its text output read by one pattern; nothing here re-implements a rule.
"""

import re
import sys
from itertools import takewhile
from pathlib import Path
from tempfile import TemporaryDirectory

from ci.core.errors import IniError
from ci.core.project import Project, Scope
from ci.core.tool import Finding
from ci.gates.gate import Gate
from ci.gates.session import Session
from ci.ontology.model import Kind

TY = re.compile(r"^(?P<path>[^:\s]+):(?P<line>\d+):\d+: \w+\[(?P<rule>[^\]]+)\] (?P<message>.*)$")
VULTURE = re.compile(r"^(?P<path>[^:]+):(?P<line>\d+): unused (?P<what>\w+) '(?P<name>[^']+)'")
SIMILAR = re.compile(r"^(?P<count>\d+) similar lines in \d+ files$")
LOCATED = re.compile(r"^==(?P<path>.+):\[(?P<start>\d+):(?P<end>\d+)\]$")
# Methods a framework calls by decoration; vulture cannot see the call.
FRAMEWORK = "@field_validator,@model_validator,@field_serializer,@model_serializer,@computed_field"
MIN_DUPLICATE = 6


class Types(Gate):
    """ty over every scope: wrong types and unguarded `None` are defects, never style."""

    name = "types"
    catches = "a wrong type, an unguarded None, an unresolved import"

    def findings(self, session: Session) -> list[Finding]:
        """ty's concise diagnostics, against the interpreter that runs ini."""
        paths = [str(p) for p in session.project.paths(Scope.ALL)]
        args = ("check", "--output-format", "concise", "--python", sys.executable, *paths)
        outcome = session.tool.run("ty", *args)
        if outcome.code not in (0, 1):
            raise IniError(f"ty failed: {outcome.tail()}")
        return [
            Finding(session.project.relative(m["path"]), int(m["line"]), m["rule"], m["message"])
            for m in map(TY.match, outcome.out.splitlines())
            if m
        ]

    def witness(self, project: Project) -> dict[str, str]:
        """A function that returns what it says it does not."""
        return self.in_package(project, '"""Witness."""\n\n\ndef name() -> str:\n    return 1\n')


class Deadcode(Gate):
    """vulture over production code; tests excluded, because a helper only its test calls is dead."""

    name = "deadcode"
    catches = "a name written and never wired"

    def findings(self, session: Session) -> list[Finding]:
        """vulture at 60 % confidence — its floor for an unused function; a higher bar reports none."""
        project = session.project
        with TemporaryDirectory() as scratch:
            fields = Path(scratch) / "wire_fields.py"
            fields.write_text(self.wire_fields(session))
            whitelist = project.root / "ci" / "deadcode-whitelist.py"
            extra = [str(whitelist)] if whitelist.is_file() else []
            extra += [f"--exclude={p}" for p in project.excluded(Scope.PRODUCTION)]
            outcome = session.tool.run(
                "vulture", str(project.package), str(fields), *extra,
                "--min-confidence", "60", "--ignore-decorators", FRAMEWORK,
            )  # fmt: skip
        return [
            Finding(project.relative(m["path"]), int(m["line"]), f"unused-{m['what']}",
                    f"unused {m['what']} '{m['name']}'", m["name"])
            for m in map(VULTURE.match, outcome.out.splitlines())
            if m
        ]  # fmt: skip

    @staticmethod
    def wire_fields(session: Session) -> str:
        """A whitelist of what a wire model's serialiser reads: its fields and `model_config`."""
        names = {"model_config"} | {
            a.name for e in session.ontology.entities() if e.kind is Kind.WIRE for a in e.attributes
        }
        return "".join(f"{name}\n" for name in sorted(names))

    def witness(self, project: Project) -> dict[str, str]:
        """A documented function nothing calls."""
        text = '"""Witness."""\n\n\ndef never_wired() -> None:\n    """Nothing calls this."""\n'
        return self.in_package(project, text)


class Duplication(Gate):
    """pylint's `symilar` over production code: a block copied twice is a missing abstraction."""

    name = "duplication"
    catches = f"a block of {MIN_DUPLICATE}+ lines copied twice"

    def findings(self, session: Session) -> list[Finding]:
        """One finding per copy, at its first location, pointing at the other."""
        project = session.project
        files = [str(p) for p in project.python_files(project.package)]
        outcome = session.tool.run(
            "pylint.checkers.symilar", "--duplicates", str(MIN_DUPLICATE),
            "--ignore-imports", "--ignore-docstrings", "--ignore-signatures", *files,
        )  # fmt: skip
        return self.parse(project, outcome.out.splitlines())

    @staticmethod
    def parse(project: Project, lines: list[str]) -> list[Finding]:
        """symilar's report: a count line, then one `==path:[start:end]` line per copy."""
        found: list[Finding] = []
        for index, line in enumerate(lines):
            header = SIMILAR.match(line)
            following = map(LOCATED.match, lines[index + 1 :])
            places = list(takewhile(bool, following)) if header else []
            if not header or not places:
                continue
            first, *others = [m for m in places if m]
            elsewhere = ", ".join(f"{project.relative(m['path'])}:{m['start']}" for m in others)
            message = f"{header['count']} lines also at {elsewhere}"
            path = project.relative(first["path"])
            found.append(Finding(path, int(first["start"]) + 1, "duplicate", message))
        return found

    def witness(self, project: Project) -> dict[str, str]:
        """The same eight-line function in two modules."""
        body = "".join(f"    total = total * {i} + {i}\n" for i in range(2, 10))
        text = f'"""Witness."""\n\n\ndef twin(total: int) -> int:\n{body}    return total\n'
        return self.in_package(project, text) | self.in_package(project, text, "ini_witness_2.py")
