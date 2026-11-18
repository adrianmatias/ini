"""Read a project's package into its ontology, from the syntax tree alone — nothing is imported.

Deterministic by construction: the same tree gives the same ontology, so the rendered page can be
compared byte for byte and a stale page is a gate failure, not a review comment.
"""

import ast
import re
from collections.abc import Iterator, Sequence
from dataclasses import dataclass

from ci.core.project import Project
from ci.ontology.model import Attribute, Entity, Kind, Ontology, Package

# The roots a lineage ends in when it leaves the project.
KNOWN = {
    "BaseModel": Kind.WIRE,
    "RootModel": Kind.WIRE,
    "BaseSettings": Kind.WIRE,
    "Enum": Kind.VOCABULARY,
    "StrEnum": Kind.VOCABULARY,
    "IntEnum": Kind.VOCABULARY,
    "Flag": Kind.VOCABULARY,
    "IntFlag": Kind.VOCABULARY,
    "NamedTuple": Kind.VALUE,
    "Exception": Kind.ERROR,
    "BaseException": Kind.ERROR,
}
IDENTIFIER = re.compile(r"[A-Za-z_]\w*")


def _name(node: ast.expr) -> str:
    """The name an expression ends in: `pydantic.BaseModel` and `RootModel[int]` alike."""
    match node:
        case ast.Name(id=name) | ast.Attribute(attr=name):
            return name
        case ast.Subscript(value=value) | ast.Call(func=value):
            return _name(value)
        case _:
            return ""


def _mentions(annotation: ast.expr) -> frozenset[str]:
    """Every identifier an annotation names, forward references in strings included."""
    found: set[str] = set()
    for node in ast.walk(annotation):
        match node:
            case ast.Name(id=name) | ast.Attribute(attr=name):
                found.add(name)
            case ast.Constant(value=str(text)):
                found.update(IDENTIFIER.findall(text))
    return frozenset(found)


def _describes(node: ast.expr | None) -> bool:
    """Whether a value or annotation carries `Field(description=...)`."""
    return node is not None and any(
        isinstance(call, ast.Call)
        and _name(call.func) == "Field"
        and any(k.arg == "description" for k in call.keywords)
        for call in ast.walk(node)
    )


@dataclass(frozen=True, slots=True)
class Declaration:
    """A class statement as written, with the module facts the lineage pass needs."""

    node: ast.ClassDef
    package: str
    path: str

    @property
    def bases(self) -> tuple[str, ...]:
        """The names of what it extends."""
        return tuple(name for name in map(_name, self.node.bases) if name)

    @property
    def decorated_value(self) -> bool:
        """Whether a `@dataclass` makes it a value."""
        return any(_name(d) == "dataclass" for d in self.node.decorator_list)

    @property
    def sets_attribute_docs(self) -> bool:
        """Whether its own config turns attribute docstrings into schema descriptions."""
        return any(
            isinstance(node, ast.keyword)
            and node.arg == "use_attribute_docstrings"
            and isinstance(node.value, ast.Constant)
            and node.value.value is True
            for node in ast.walk(self.node)
        )

    def attributes(self) -> tuple[Attribute, ...]:
        """The public annotated attributes of its body; `ClassVar`s and `model_config` are not data."""
        body = self.node.body
        found: list[Attribute] = []
        for index, statement in enumerate(body):
            if not isinstance(statement, ast.AnnAssign) or not isinstance(
                statement.target, ast.Name
            ):
                continue
            name = statement.target.id
            if name.startswith("_") or name == "model_config":
                continue
            if _name(statement.annotation) == "ClassVar":
                continue
            following = body[index + 1] if index + 1 < len(body) else None
            docstring = isinstance(following, ast.Expr) and isinstance(
                following.value, ast.Constant
            )
            described = _describes(statement.value) or _describes(statement.annotation)
            mentions = _mentions(statement.annotation)
            found.append(Attribute(name, statement.lineno, mentions, described, docstring))
        return tuple(found)


class Lineage:
    """Resolve a class's kind and config through its bases: project classes first, then roots."""

    def __init__(self, declarations: Sequence[Declaration]) -> None:
        self.by_name = {d.node.name: d for d in declarations}

    def kind(self, name: str) -> Kind:
        """A dataclass is a value; otherwise the first base that resolves decides; else a component."""
        return self.resolve(name, frozenset()) or Kind.COMPONENT

    def resolve(self, name: str, seen: frozenset[str]) -> Kind | None:
        """The kind a name's lineage reaches, or None when it ends in nothing known."""
        declaration = self.by_name.get(name)
        if declaration is None or name in seen:
            error = name.endswith(("Error", "Exception"))
            return KNOWN.get(name) or (Kind.ERROR if error else None)
        if declaration.decorated_value:
            return Kind.VALUE
        for base in declaration.bases:
            if (kind := self.resolve(base, seen | {name})) is not None:
                return kind
        return None

    def attribute_docs(self, name: str, seen: frozenset[str] = frozenset()) -> bool:
        """Whether the class or a project ancestor sets `use_attribute_docstrings=True`."""
        declaration = self.by_name.get(name)
        if declaration is None or name in seen:
            return False
        return declaration.sets_attribute_docs or any(
            self.attribute_docs(base, seen | {name}) for base in declaration.bases
        )

    def parents(self, declaration: Declaration) -> tuple[str, ...]:
        """The bases that are project classes."""
        return tuple(base for base in declaration.bases if base in self.by_name)


class Reader:
    """Read the project's package — modules, classes, imports — into an `Ontology`."""

    def __init__(self, project: Project) -> None:
        self.project = project
        self.root = project.package.name

    def package_of(self, module: str) -> str:
        """The component a dotted module belongs to: its first sub-package, or the root."""
        parts = module.split(".")
        directory = self.project.package / parts[1] if len(parts) > 1 else None
        return parts[1] if directory is not None and directory.is_dir() else self.root

    def modules(self) -> Iterator[tuple[str, str, ast.Module]]:
        """Each module as (component, project-relative path, syntax tree)."""
        for path in self.project.python_files(self.project.package):
            dotted = path.relative_to(self.project.src).with_suffix("").parts
            module = ".".join(part for part in dotted if part != "__init__")
            yield self.package_of(module), self.project.relative(path), ast.parse(path.read_text())

    def read(self) -> Ontology:
        """The whole map: roles, entities with resolved kinds, and the import edges between packages."""
        declarations: list[Declaration] = []
        edges: set[tuple[str, str]] = set()
        roles: dict[str, str] = {}
        for package, path, tree in self.modules():
            if path.endswith("__init__.py") and package not in roles:
                roles[package] = (ast.get_docstring(tree) or "").strip().split("\n")[0]
            declarations += [
                Declaration(node, package, path)
                for node in tree.body
                if isinstance(node, ast.ClassDef)
            ]
            edges |= {(package, target) for target in self.imports(tree)} - {(package, package)}
        lineage = Lineage(declarations)
        entities = [
            self.entity(d, lineage) for d in declarations if not d.node.name.startswith("_")
        ]
        packages = tuple(
            Package(name, roles[name], tuple(e for e in entities if e.package == name))
            for name in sorted(roles)
        )
        return Ontology(self.root, packages, tuple(sorted(edges)))

    def imports(self, tree: ast.Module) -> set[str]:
        """The project components a module imports from."""
        names = {node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)}
        names |= {a.name for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names}
        return {self.package_of(n) for n in names if n and n.split(".")[0] == self.root}

    def entity(self, declaration: Declaration, lineage: Lineage) -> Entity:
        """One declaration resolved against the lineage of every class in the project."""
        node = declaration.node
        return Entity(
            name=node.name,
            package=declaration.package,
            path=declaration.path,
            line=node.lineno,
            summary=(ast.get_docstring(node) or "").strip().split("\n")[0],
            kind=lineage.kind(node.name),
            parents=lineage.parents(declaration),
            attributes=declaration.attributes(),
            attribute_docs=lineage.attribute_docs(node.name),
        )
