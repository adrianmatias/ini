"""The object-oriented shape: concepts are classes, the run layer is thin, every file is in scope.

Agents left alone write a pile of functions that correct one another; a class names the concept and
keeps its data and its rules together. The rules here are the deterministic part of that:

- **run layer** — `argparse`, `sys.argv` and `__main__` live in `<package>/cli/` or a `__main__.py`
  (Python's own entry point) only: source declares, run invokes, nothing else parses a command line;
- **pile** — a module outside the run layer holds at most six free functions: past that, the
  functions share a concept that wants to be a class;
- **component** — every sub-package other than the run layer defines a public class: a package of
  loose functions is a `utils` with a better name;
- **sys-path** — nothing edits the import path: the environment does that, once;
- **scope** — every Python file sits in a directory the gates read, or no gate ever looks at it.
"""

import ast
from dataclasses import dataclass
from pathlib import Path

from ci.core.project import Project, Scope
from ci.core.tool import Finding
from ci.gates.gate import Gate
from ci.gates.session import Session

PILE = 6
RUN_LAYER = "cli"


@dataclass(frozen=True, slots=True)
class Module:
    """One module's syntax tree, and whether it is domain code: in the package, outside `cli/`."""

    path: str
    tree: ast.Module
    domain: bool

    def run_layer_leaks(self) -> list[Finding]:
        """Command-line parsing in domain code."""
        if not self.domain:
            return []
        return [
            Finding(self.path, node.lineno, "run-layer", f"{what} outside `{RUN_LAYER}/`")
            for node in ast.walk(self.tree)
            if isinstance(node, ast.stmt | ast.expr) and (what := self.command_line(node))
        ]

    @staticmethod
    def command_line(node: ast.AST) -> str:
        """What makes a node command-line parsing, or empty."""
        match node:
            case ast.Import(names=names) if any(a.name == "argparse" for a in names):
                return "argparse"
            case ast.ImportFrom(module="argparse"):
                return "argparse"
            case ast.Attribute(value=ast.Name(id="sys"), attr="argv"):
                return "sys.argv"
            case ast.Compare(left=ast.Name(id="__name__")):
                return "a __main__ guard"
            case _:
                return ""

    def pile(self) -> list[Finding]:
        """Too many free functions in one domain module."""
        free = [n for n in self.tree.body if isinstance(n, ast.FunctionDef | ast.AsyncFunctionDef)]
        if not self.domain or len(free) <= PILE:
            return []
        message = f"{len(free)} free functions (budget {PILE}): name the concept they share"
        return [Finding(self.path, 1, "pile", message)]

    def sys_path(self) -> list[Finding]:
        """An edit of the import path."""
        return [
            Finding(self.path, node.lineno, "sys-path", "edits sys.path: let the environment do it")
            for node in ast.walk(self.tree)
            if isinstance(node, ast.Attribute)
            and node.attr == "path"
            and isinstance(node.value, ast.Name)
            and node.value.id == "sys"
        ]

    def classes(self) -> int:
        """Public classes at module level."""
        return sum(
            isinstance(n, ast.ClassDef) and not n.name.startswith("_") for n in self.tree.body
        )


class Shape(Gate):
    """Classes for concepts, a thin run layer, and no file outside the gates' sight."""

    name = "shape"
    catches = "parsing outside cli/, a pile of free functions, a classless package, sys.path, scope"

    def findings(self, session: Session) -> list[Finding]:
        """Module rules over every scope, package rules over the production package."""
        project = session.project
        files = project.python_files(*project.paths(Scope.ALL))
        modules = [self.module(project, path) for path in files]
        found = [f for m in modules for f in (*m.run_layer_leaks(), *m.pile(), *m.sys_path())]
        return found + self.components(project, modules) + self.out_of_scope(project)

    @staticmethod
    def module(project: Project, path: Path) -> Module:
        """A file as a module, knowing whether it is domain code."""
        outside = (project.package / RUN_LAYER, *project.excluded(Scope.PRODUCTION))
        domain = path.is_relative_to(project.package) and not any(
            path.is_relative_to(directory) for directory in outside
        )
        domain = domain and path.name != "__main__.py"
        return Module(project.relative(path), ast.parse(path.read_text()), domain)

    @staticmethod
    def components(project: Project, modules: list[Module]) -> list[Finding]:
        """Sub-packages that define no public class."""
        found: list[Finding] = []
        for init in sorted(project.package.glob("*/__init__.py")):
            if init.parent.name == RUN_LAYER or init.parent == project.nested:
                continue
            prefix = project.relative(init.parent) + "/"
            if not sum(m.classes() for m in modules if m.path.startswith(prefix)):
                message = "a package with no class: name the concept or fold it into one"
                found.append(Finding(project.relative(init), 1, "component", message))
        return found

    @staticmethod
    def out_of_scope(project: Project) -> list[Finding]:
        """Python files no gate reads."""
        scoped = (*project.paths(Scope.ALL), project.skills)
        return [
            Finding(project.relative(path), 1, "scope", "no gate reads this file: move it into "
                    "the package, the tests or a [tool.ini] scripts directory")
            for path in project.python_files()
            if not any(path.is_relative_to(root) for root in scoped)
        ]  # fmt: skip

    def witness(self, project: Project) -> dict[str, str]:
        """A domain module that parses its own command line."""
        return self.in_package(project, '"""Witness."""\n\nimport argparse\n')
