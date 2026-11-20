"""Move free functions of one module onto a class and rewrite every caller, by AST positions.

usage: python sweep_callsites.py SPEC.json FILE...      (run on callers only, not on the module)
SPEC: {"module": "pkg.core.document",
       "receiver":  {"read_text": ["Document", "read_text"]},   # f(*r) -> Document(a).read_text
       "attribute": {"render": ["TEMPLATES", "render"]}}        # f -> TEMPLATES.render
Rewrites the `from <module> import ...` line to the class names, prints each file it changed, and
refuses a file where a moved name is also a parameter or an assignment target (shadowing: the
sweep would rewrite the local too). Then: ruff check --fix --select I,F401; ruff format; the suite.
"""

import ast
import sys
from pathlib import Path

from pydantic import BaseModel

Edit = tuple[int, int, bytes]


class Spec(BaseModel):
    """Which names leave the module, and the expression each becomes."""

    module: str
    receiver: dict[str, list[str]] = {}
    attribute: dict[str, list[str]] = {}

    @property
    def moved(self) -> set[str]:
        """Every name the module loses."""
        return set(self.receiver) | set(self.attribute)

    def owner(self, name: str) -> str:
        """The class (or instance) a moved name now lives on."""
        return (self.receiver.get(name) or self.attribute[name])[0]


class Source:
    """One caller file: its bytes, its tree, and the edits that move its calls onto the class."""

    def __init__(self, path: Path, spec: Spec) -> None:
        self.path, self.spec = path, spec
        self.data = path.read_bytes()
        self.tree = ast.parse(self.data)
        self.starts = [0] + [i + 1 for i, b in enumerate(self.data) if b == 10]
        self.imports = [
            n for n in self.tree.body if isinstance(n, ast.ImportFrom) and n.module == spec.module
        ]
        nested = [
            n
            for n in ast.walk(self.tree)
            if isinstance(n, ast.ImportFrom) and n.module == spec.module and n not in self.imports
        ]
        if nested:
            raise SystemExit(
                f"{self.path}:{nested[0].lineno}: local import from {spec.module}: edit by hand"
            )
        self.names = {
            a.asname or a.name: a.name
            for n in self.imports
            for a in n.names
            if a.name in spec.moved
        }

    def at(self, node: ast.stmt | ast.expr | ast.keyword, end: bool = False) -> int:
        """A node's start (or end) as a byte offset; `col_offset` is a byte offset already."""
        line, col = (
            (node.end_lineno, node.end_col_offset) if end else (node.lineno, node.col_offset)
        )
        assert line is not None and col is not None
        return self.starts[line - 1] + col

    def shadowed(self) -> set[str]:
        """Moved names the file also binds locally: the sweep would rewrite the local too."""
        bound = {a.arg for a in ast.walk(self.tree) if isinstance(a, ast.arg)}
        bound |= {
            n.id
            for n in ast.walk(self.tree)
            if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store)
        }
        return set(self.names) & bound

    def calls(self) -> tuple[list[Edit], set[int]]:
        """`f(a, *rest)` becomes `Class(a).method(*rest)`; returns edits and consumed names."""
        edits: list[Edit] = []
        done: set[int] = set()
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                original = self.names.get(node.func.id)
                if original in self.spec.receiver:
                    edits.append(self.receiver_call(node, *self.spec.receiver[original]))
                    done.add(id(node.func))
        return edits, done

    def receiver_call(self, node: ast.Call, cls: str, method: str) -> Edit:
        """One call rewritten so its first argument constructs the receiver."""
        if not node.args or isinstance(node.args[0], ast.Starred):
            raise SystemExit(
                f"{self.path}:{node.lineno}: a moved call without a positional first arg"
            )
        first = node.args[0]
        arg = self.data[self.at(first) : self.at(first, end=True)]
        rest = sorted([*node.args[1:], *node.keywords], key=lambda r: (r.lineno, r.col_offset))
        end = self.at(rest[0]) if rest else self.at(node, end=True) - 1
        return self.at(node.func), end, f"{cls}(".encode() + arg + f").{method}(".encode()

    def references(self, done: set[int]) -> list[Edit]:
        """Other uses of a moved name become `Owner.method`; bare receiver names refuse."""
        edits: list[Edit] = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Name) and node.id in self.names and id(node) not in done:
                original = self.names[node.id]
                if original not in self.spec.attribute:
                    raise SystemExit(f"{self.path}:{node.lineno}: bare reference to {node.id}")
                cls, method = self.spec.attribute[original]
                start = self.at(node)
                edits.append((start, start + len(node.id.encode()), f"{cls}.{method}".encode()))
        return edits

    def import_lines(self) -> list[Edit]:
        """The module's import line names the owners instead of the moved functions."""
        owners = sorted({self.spec.owner(n) for n in self.names.values()})
        edits: list[Edit] = []
        for node in self.imports:
            kept = [a.name if not a.asname else f"{a.name} as {a.asname}" for a in node.names
                    if a.name not in self.spec.moved]  # fmt: skip
            names = sorted(set(kept + owners))
            owners = []
            start, end = self.at(node), self.at(node, end=True)
            if not names:
                if end < len(self.data) and self.data[end : end + 1] == b"\n":
                    end += 1
                edits.append((start, end, b""))
            else:
                text = f"from {self.spec.module} import {', '.join(names)}"
                edits.append((start, end, text.encode()))
        return edits

    def sweep(self) -> bool:
        """Apply every edit back to front; write the file when it changed."""
        if not self.names:
            return False
        if clash := self.shadowed():
            raise SystemExit(f"{self.path}: {sorted(clash)} also bound locally: edit by hand")
        calls, done = self.calls()
        out, last = self.data, len(self.data) + 1
        for start, end, new in sorted(
            calls + self.references(done) + self.import_lines(), key=lambda e: e[0], reverse=True
        ):
            if end > last:
                raise SystemExit(f"{self.path}: overlapping edits at byte {start}")
            out, last = out[:start] + new + out[end:], start
        if out == self.data:
            return False
        self.path.write_bytes(out)
        return True


if __name__ == "__main__":
    spec = Spec.model_validate_json(Path(sys.argv[1]).read_text())
    for name in sys.argv[2:]:
        if Source(Path(name), spec).sweep():
            print(name)
