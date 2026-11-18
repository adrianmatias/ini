"""The harness gate: the agent-facing files stay small, consistent with each other, and inherited.

The harness is what every agent reads before it works, so its size is a budget and its consistency
is a contract — the same compression the code is held to, applied to the instructions:

- **size** — `AGENTS.md` fits in one read (120 lines), and a learnings file is a ranked list, not a
  diary (160 lines);
- **skill** — each `SKILL.md` opens with `name` (its directory) and a `description` that starts
  «Use when» and fits one line, and stays under 150 lines: a skill that grew past that is two skills
  or a reference file;
- **skills-table** — `AGENTS.md` names every skill on disk, and every skill it names exists;
- **kickoff** — no `TODO(kickoff)` is left in an anchor: work starts after the objective is stated.
"""

import re
from dataclasses import dataclass
from pathlib import Path

from ci.core.project import Project
from ci.core.tool import Finding
from ci.gates.gate import Gate
from ci.gates.session import Session

AGENTS_LINES = 120
SKILL_LINES = 150
LEARNINGS_LINES = 160
DESCRIPTION_CHARS = 100
KICKOFF = "TODO(kickoff)"
ROW = re.compile(r"^\|\s*`(?P<name>[a-z0-9-]+)`\s*\|")


@dataclass(frozen=True, slots=True)
class Skill:
    """One `SKILL.md`: where it is, what its frontmatter says, and how long it is."""

    path: str
    directory: str
    front: dict[str, str]
    lines: int

    @classmethod
    def read(cls, project: Project, path: Path) -> Skill:
        """Parse the frontmatter between the first two `---` lines."""
        lines = path.read_text().splitlines()
        front: dict[str, str] = {}
        if lines and lines[0] == "---":
            for line in lines[1 : lines.index("---", 1) if "---" in lines[1:] else 1]:
                key, _, value = line.partition(":")
                front[key.strip()] = value.strip()
        return cls(project.relative(path), path.parent.name, front, len(lines))

    def defects(self) -> list[Finding]:
        """What the frontmatter or the size get wrong."""
        description = self.front.get("description", "")
        problems = [
            (self.front.get("name") != self.directory, f"name is not `{self.directory}`"),
            (not description.startswith("Use when"), "description does not start «Use when»"),
            (len(description) > DESCRIPTION_CHARS, f"description over {DESCRIPTION_CHARS} chars"),
            (self.lines > SKILL_LINES, f"{self.lines} lines (budget {SKILL_LINES})"),
        ]
        return [Finding(self.path, 1, "skill", why) for failed, why in problems if failed]


class Harness(Gate):
    """The instructions agents read: small, consistent, inherited, and started from an objective."""

    name = "harness"
    catches = "an oversized AGENTS.md or skill, a skill the table misses, kickoff placeholders left"
    ratchet = False

    def findings(self, session: Session) -> list[Finding]:
        """Every harness rule, in the order an agent meets the files."""
        project = session.project
        skills = self.skills(project)
        found = self.sizes(project) + [f for skill in skills for f in skill.defects()]
        return found + self.table(project, skills) + self.kickoff(project)

    @staticmethod
    def skills(project: Project) -> list[Skill]:
        """The inherited skills and the project's own."""
        roots = (project.base / "skills", project.root / "skills")
        paths = sorted(p for root in roots for p in root.glob("*/SKILL.md"))
        return [Skill.read(project, path) for path in paths]

    @staticmethod
    def sizes(project: Project) -> list[Finding]:
        """AGENTS.md and the learnings files against their budgets."""
        budgets = {
            project.agents: AGENTS_LINES,
            project.base / "learnings.md": LEARNINGS_LINES,
            project.root / "wiki" / "learnings.md": LEARNINGS_LINES,
        }
        if not project.agents.is_file():
            return [Finding(project.relative(project.agents), 1, "size", "missing")]
        return [
            Finding(project.relative(path), 1, "size", f"{n} lines (budget {budget})")
            for path, budget in budgets.items()
            if path.is_file() and (n := len(path.read_text().splitlines())) > budget
        ]

    @staticmethod
    def table(project: Project, skills: list[Skill]) -> list[Finding]:
        """Skills the `## skills` section of AGENTS.md does not name, and names no skill answers to."""
        if not project.agents.is_file():
            return []
        section = project.agents.read_text().partition("\n## skills")[2].split("\n## ")[0]
        agents = project.relative(project.agents)
        listed = {m["name"] for m in map(ROW.match, section.splitlines()) if m}
        on_disk = {skill.directory for skill in skills}
        missing = [f"`{name}` is a skill AGENTS.md does not name" for name in on_disk - listed]
        ghosts = [f"`{name}` is listed and no skill answers to it" for name in listed - on_disk]
        return [Finding(agents, 1, "skills-table", why) for why in sorted(missing + ghosts)]

    @staticmethod
    def kickoff(project: Project) -> list[Finding]:
        """Placeholders left in the anchors at the root."""
        return [
            Finding(project.relative(path), number, "kickoff", line.strip()[:90])
            for path in sorted(project.root.glob("*.md"))
            for number, line in enumerate(path.read_text().splitlines(), start=1)
            if KICKOFF in line
        ]

    def witness(self, project: Project) -> dict[str, str]:
        """A skill with no frontmatter that AGENTS.md does not list."""
        return {project.relative(project.root / "skills/witness/SKILL.md"): "# witness\n"}
