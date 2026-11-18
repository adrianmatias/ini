"""The ontology's own vocabulary: kinds of class, attributes, entities, packages and the whole map.

A class's kind is read from its lineage, not declared: a pydantic model crosses a wire, a dataclass
is a value, an enum is a closed vocabulary, an exception is a refusal, anything else is a component
that owns behaviour. The kind decides which rules apply to it (a wire model must describe its
fields, because its schema is what a model or a client reads).
"""

from dataclasses import dataclass
from enum import StrEnum


class Kind(StrEnum):
    """The role a class plays in the domain, read from what it extends or how it is decorated."""

    WIRE = "wire"
    VALUE = "value"
    VOCABULARY = "vocabulary"
    ERROR = "error"
    COMPONENT = "component"


@dataclass(frozen=True, slots=True)
class Attribute:
    """An annotated attribute declared in a class body, and how it says what it is."""

    name: str
    line: int
    mentions: frozenset[str]
    described: bool
    docstring: bool


@dataclass(frozen=True, slots=True)
class Entity:
    """A public class: where it lives, what it says it is, its kind, parents and attributes."""

    name: str
    package: str
    path: str
    line: int
    summary: str
    kind: Kind
    parents: tuple[str, ...]
    attributes: tuple[Attribute, ...]
    attribute_docs: bool

    def undescribed(self) -> tuple[Attribute, ...]:
        """Wire attributes whose schema tells a reader nothing: no description, no docstring that
        pydantic would turn into one."""
        if self.kind is not Kind.WIRE:
            return ()
        return tuple(
            a for a in self.attributes if not (a.described or (a.docstring and self.attribute_docs))
        )

    def has(self, names: frozenset[str]) -> tuple[str, ...]:
        """The other entities its attributes mention: the composition edges of the domain."""
        mentioned = {name for attribute in self.attributes for name in attribute.mentions}
        return tuple(sorted((mentioned & names) - {self.name}))


@dataclass(frozen=True, slots=True)
class Package:
    """A component: one sub-package of the project, the role its `__init__` states, its entities."""

    name: str
    role: str
    entities: tuple[Entity, ...]


@dataclass(frozen=True, slots=True)
class Ontology:
    """The domain as the code declares it: components, the imports between them, their entities."""

    root: str
    packages: tuple[Package, ...]
    edges: tuple[tuple[str, str], ...]

    def entities(self) -> tuple[Entity, ...]:
        """Every entity, package by package."""
        return tuple(entity for package in self.packages for entity in package.entities)

    def names(self) -> frozenset[str]:
        """The entity names: what an attribute must mention to count as a relation."""
        return frozenset(entity.name for entity in self.entities())
