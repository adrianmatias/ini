"""The ratchet: recorded debt that may shrink and never grow.

An existing project adopts a gate by recording what it finds today (`--adopt`, once, visible in
review); from then on a key — file, rule, and function when there is one — may not exceed its count,
a new key is red, and a record above what the gate measures is red too until `--record` lowers it.
That last rule is what makes the ceiling move: a fix that is not recorded fails the run.
"""

from collections import Counter
from collections.abc import Sequence
from pathlib import Path

from pydantic import TypeAdapter

from ci.core.tool import Finding

RECORD = TypeAdapter(dict[str, dict[str, int]])


class Ceilings:
    """The ratchet's record: per gate, per finding key, how many findings are tolerated."""

    def __init__(self, path: Path, label: str) -> None:
        self.path = path
        self.label = label
        self.table = RECORD.validate_json(path.read_text()) if path.is_file() else {}

    def judge(self, gate: str, findings: Sequence[Finding]) -> list[Finding]:
        """The findings that make the gate red: every finding of a key over its record, plus one per
        record the gate no longer measures in full."""
        recorded = self.table.get(gate, {})
        counts = Counter(finding.key for finding in findings)
        over = [
            finding for finding in findings if counts[finding.key] > recorded.get(finding.key, 0)
        ]
        stale = [
            Finding(self.label, 1, "ratchet-stale", f"{key}: recorded {n}, measured {counts[key]}")
            for key, n in sorted(recorded.items())
            if counts[key] < n
        ]
        return over + stale

    def record(self, gate: str, findings: Sequence[Finding]) -> None:
        """Lower every record to what the gate measures; never raise one, never add one."""
        counts = Counter(finding.key for finding in findings)
        recorded = self.table.get(gate, {})
        self.table[gate] = {key: min(n, counts[key]) for key, n in recorded.items() if counts[key]}

    def adopt(self, gate: str, findings: Sequence[Finding]) -> None:
        """Record what the gate measures today as the debt the project starts from."""
        self.table[gate] = dict(Counter(finding.key for finding in findings))

    def save(self) -> None:
        """Write the record, gates with no debt left out."""
        table = {gate: dict(sorted(keys.items())) for gate, keys in self.table.items() if keys}
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_bytes(RECORD.dump_json(dict(sorted(table.items())), indent=2) + b"\n")
