"""The ontology as markdown, and the one block of the domain page it owns.

The page is hand-written language (what the words mean, which invariants span entities) around one
rendered block. `python -m ci domain --write` replaces the block and nothing else; the domain gate
compares it with a fresh render, so the map an agent reads is never older than the code. The block
is found by its opening tag alone, so the words after it may change without orphaning a page.
"""

from pathlib import Path

from ci.ontology.model import Ontology

OPEN = "<!-- ontology:begin"
BEGIN = f"{OPEN} — `python -m ci domain --write` renders this block; a stale block is red -->"
END = "<!-- ontology:end -->"


class Renderer:
    """Print the ontology: the component graph, then one entity table per component."""

    def __init__(self, ontology: Ontology) -> None:
        self.ontology = ontology

    def graph(self) -> list[str]:
        """The components and the imports between them, as a mermaid flowchart."""
        lines = ["```mermaid", "flowchart LR"]
        lines += [f"  {package.name}" for package in self.ontology.packages]
        lines += [f"  {a} --> {b}" for a, b in self.ontology.edges]
        return [*lines, "```"]

    def table(self, name: str) -> list[str]:
        """One component: its role, then each entity with kind, parents, relations and summary."""
        package = next(p for p in self.ontology.packages if p.name == name)
        names = self.ontology.names()
        lines = ["", f"### {package.name}", "", package.role or "(no role stated)", ""]
        if not package.entities:
            return [*lines, "No entities: a run layer or a module of pure helpers."]
        lines += ["| entity | kind | is | has | what it is |", "|---|---|---|---|---|"]
        lines += [
            f"| `{e.name}` | {e.kind} | {', '.join(e.parents)} | {', '.join(e.has(names))} "
            f"| {e.summary} |"
            for e in package.entities
        ]
        return lines

    def render(self) -> str:
        """The whole block, markers included."""
        lines = [BEGIN, "", "## ontology", "", *self.graph()]
        for package in self.ontology.packages:
            lines += self.table(package.name)
        return "\n".join([*lines, "", END])


class Page:
    """The domain page: hand-written text around the one block the renderer owns."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def text(self) -> str:
        """The page as committed; empty when it does not exist yet."""
        return self.path.read_text() if self.path.is_file() else ""

    def block(self) -> str:
        """The rendered block as committed, markers included; empty when the page has none."""
        text = self.text()
        start, end = text.find(OPEN), text.find(END)
        return text[start : end + len(END)] if 0 <= start < end else ""

    def write(self, rendered: str) -> None:
        """Replace the block in place, or append it when the page has none yet."""
        text, current = self.text(), self.block()
        if current:
            self.path.write_text(text.replace(current, rendered))
        else:
            self.path.write_text((text.rstrip() + "\n\n" + rendered + "\n").lstrip())
