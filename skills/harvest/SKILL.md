---
name: harvest
description: Use when a lesson holds beyond one project, or a project takes in ini. Down and up.
---

# harvest

ini is how projects inherit each other's learning without depending on each other. Shared knowledge
has two bad homes: copies that drift, or one source every project links to. ini takes neither. An
agent **distils**: it reads ini and writes the knowledge into the project, in the project's own
words and layout. The project owns the result outright; nothing records where it came from. Two
directions: **down** (a project takes in ini) and **up** (a project's lesson or skill joins ini).

## down — distil

From a local clone of ini (`git clone`, or `git -C <ini> pull` to refresh), on demand.

1. **Harness**, one round with no behaviour change:
   - `ci/` without `ci/tests/`, adapted where the project needs it (a product gate of its own
     belongs there);
   - the knowledge, merged into the project's own `foundation.md`, `code-standard.md`,
     `wiki/learnings.md` and `skills/`. Keep what the project obeys, drop what it never meets, and
     use its domain's words. Where the project already says it, its line wins;
   - a `[tool.ini]` that fits the layout: `src` (`"."` when flat), `package`, `tests` (it may sit
     inside the package), `scripts` (every directory of hand-run `.py` files; not notebooks);
   - the gate tools from ini's dev group into the project's (`uv add --dev`), and the skill rows in
     its `AGENTS.md`;
   - `uv run python -m ci gates --adopt` records today's debt in `ci/ceilings.json`; `--prove` is
     green.
   The harness needs Python 3.14. When the project's runtime is older, run the gates under 3.14
   only if its code imports there; otherwise stop and tell the director.
2. **Compliance**, in later rounds: fix, then `--record`, until the ratchet is empty, or let the
   director drop a rule that does not fit the project.
3. **Again**, when ini has moved: read ini as it is now (its `log/agt.md` and `now.md` say what
   moved) and compare it with the project by meaning, not by `diff`, because the two differ on
   purpose. Bring in what applies; fix or `--adopt` a new rule meeting old code. Say what came in
   and what was declined in `log/agt.md`.

## up — promote

A candidate holds in at least two projects, or it names no project-specific file, number or tool.
Where a project departs from ini, the departure is either local fit or a lesson ini lacks.

1. **Generalise**: restate it as the class of failure or the procedure, with the incidents as
   evidence (dated). Strip project names a public repository should not carry.
2. **Place it**: a principle in `foundation.md`, an enforceable rule in `code-standard.md` (and a
   gate, if a machine can hold it), a lesson in `wiki/learnings.md`, a procedure in
   `skills/<name>/SKILL.md`. Prefer extending an existing section to adding one.
3. **Edit ini**. A gate change ships with its witness and `uv run python -m ci gates --prove` green
   in ini.
4. **Budget**: every agent in every project reads this. A promotion that adds lines removes some:
   merge, rank, delete the weakest (`skills/compress`).
5. Commit in ini with the evidence in the message. The project keeps its own version.

## what never crosses

A project never imports, links, submodules, pins or reads ini at run time or gate time. If ini
disappeared, every project would stay green. ini never names a project. Within one repository a
fact has one home; between repositories the redundancy is deliberate.
