"""The gate table: every gate in the order a run reports them — fast and local first, the suite last."""

from ci.gates.domain import Domain
from ci.gates.gate import Gate
from ci.gates.harness import Harness
from ci.gates.ruff import Annotations, Complexity, Docs, Lint, Surface
from ci.gates.shape import Shape
from ci.gates.suite import Behaviour, Crap
from ci.gates.tools import Deadcode, Duplication, Types

GATES: tuple[Gate, ...] = (
    Lint(),
    Docs(),
    Annotations(),
    Types(),
    Surface(),
    Shape(),
    Complexity(),
    Duplication(),
    Deadcode(),
    Domain(),
    Harness(),
    Behaviour(),
    Crap(),
)
