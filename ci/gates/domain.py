"""Domain-driven design, the part a machine can hold: the ontology is complete and current.

- **field-description** — a wire model's schema is what a model, a client or the next agent reads,
  so each field says what its name cannot: a `Field(description=...)`, or a docstring under the
  field with `use_attribute_docstrings=True`. The schema is the prompt; a field that says nothing
  makes the prompt say nothing.
- **ontology-stale** — the domain page's rendered block equals a fresh render of the code: the map
  an agent reads before it changes anything is never older than the code it describes.

The rest of DDD — names from the domain, illegal states unconstructible — is review's, and the
standard says so.
"""

from ci.core.project import Project
from ci.core.tool import Finding
from ci.gates.gate import Gate
from ci.gates.session import Session
from ci.ontology.render import Page, Renderer


class Domain(Gate):
    """Wire fields that describe themselves, and an ontology page that matches the code."""

    name = "domain"
    catches = "an undescribed wire field; an ontology page older than the code"

    def findings(self, session: Session) -> list[Finding]:
        """Every undescribed wire field, then the page if it drifted."""
        ontology = session.ontology
        found = [
            Finding(entity.path, attribute.line, "field-description",
                    f"`{entity.name}.{attribute.name}` crosses a wire and does not say what it is")
            for entity in ontology.entities()
            for attribute in entity.undescribed()
        ]  # fmt: skip
        page = Page(session.project.domain)
        if page.block() != Renderer(ontology).render():
            path = session.project.relative(session.project.domain)
            found.append(
                Finding(path, 1, "ontology-stale", "run `uv run python -m ci domain --write`")
            )
        return found

    def witness(self, project: Project) -> dict[str, str]:
        """A wire model whose field says nothing."""
        text = (
            '"""Witness."""\n\nfrom pydantic import BaseModel\n\n\n'
            'class Planted(BaseModel):\n    """A record that crosses a wire."""\n\n    value: int\n'
        )
        return self.in_package(project, text)
