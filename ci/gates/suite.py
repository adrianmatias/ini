"""The gates that read the behaviour suite's one run: did it pass, and is complex code exercised.

    crap(f) = complexity(f)² · (1 - coverage(f))³ + complexity(f)        budget 8

A complex function must be tested, and an untested one must be trivial. Complexity is ruff's C901
score — the complexity gate's own measure — and coverage is the share of the function's statements
the suite ran (https://dx42.github.io/gmetrics/metrics/CrapMetric.html). A function scored 2 cannot
breach (2² + 2 = 6), so ruff is asked only for those above it.
"""

import re

from ci.core.project import Project, Scope
from ci.core.tool import Finding
from ci.gates.gate import Gate
from ci.gates.ruff import Ruff, Run
from ci.gates.session import Session

BUDGET = 8.0
FAILED = re.compile(r"^(?:FAILED|ERROR) (?P<path>[^:\s]+)(?:::(?P<test>\S+))?(?: - (?P<why>.*))?$")
# pytest's exit codes that are not "tests failed": the suite itself could not run as a suite.
BROKEN = {2: "interrupted", 3: "internal error", 4: "usage error", 5: "no tests collected"}


class Behaviour(Gate):
    """The suite that drives the code through its public surface; red is red, no ratchet."""

    name = "behaviour"
    catches = "a broken contract at the public surface"
    ratchet = False

    def findings(self, session: Session) -> list[Finding]:
        """One finding per failed test, or one for a suite that could not run."""
        outcome = session.suite.outcome
        if outcome.code == 0:
            return []
        tests = session.project.relative(session.project.tests)
        if outcome.code in BROKEN:
            return [Finding(tests, 1, "suite", f"pytest: {BROKEN[outcome.code]}")]
        last = outcome.tail().strip().splitlines()[-1:] or ["pytest failed"]
        return [
            Finding(m["path"], 1, "failed", m["why"] or "failed", m["test"] or "")
            for m in map(FAILED.match, outcome.out.splitlines())
            if m
        ] or [Finding(tests, 1, "suite", last[0])]

    def witness(self, project: Project) -> dict[str, str]:
        """A test that fails."""
        text = '"""Witness."""\n\n\ndef test_planted() -> None:\n    assert 1 == 2\n'
        return {project.relative(project.tests / "test_ini_witness.py"): text}


class Crap(Gate):
    """Change risk: complexity the suite does not run."""

    name = "crap"
    catches = f"a complex function the suite does not exercise (crap > {BUDGET:g})"

    def findings(self, session: Session) -> list[Finding]:
        """Each production function scored above 2, held to the budget with its measured coverage."""
        complex_ = Run(Scope.PRODUCTION, "C901", config=("lint.mccabe.max-complexity = 2",))
        scored = Ruff(session.tool).check(complex_)
        covered = session.suite.covered
        found: list[Finding] = []
        for finding in scored:
            complexity = Ruff.score(finding)
            share = covered.get((finding.path, finding.line), 0.0)
            crap = complexity**2 * (1 - share) ** 3 + complexity
            if crap > BUDGET:
                message = f"{crap:.1f} > {BUDGET:g}: complexity {complexity}, run {share:.0%}"
                found.append(Finding(finding.path, finding.line, "crap", message, finding.subject))
        return found

    def witness(self, project: Project) -> dict[str, str]:
        """A four-way branch nothing runs."""
        branches = "".join(f"    if x == {i}:\n        return {i}\n" for i in range(4))
        text = f'"""Witness."""\n\n\ndef untested(x: int) -> int:\n{branches}    return -1\n'
        return self.in_package(project, text)
