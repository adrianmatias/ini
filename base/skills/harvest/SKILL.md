---
name: harvest
description: Use when a lesson holds beyond one project, or a project takes in ini. Down and up.
---

# harvest

ini is how projects inherit each other's learning. Nothing is installed: an agent carries it. Two
directions: **down** (a project takes in ini) and **up** (a project's lesson or skill joins ini).

## down — permeate

From a local clone of ini (`git clone`, or `git -C <ini> pull` to refresh), on demand.

1. **Harness**, one round with no behaviour change:
   - copy `base/` whole and `ci/` without `ci/tests/`;
   - a `[tool.ini]` that fits the layout: `src` (`"."` when flat), `package`, `tests` (it may sit
     inside the package), `scripts` (every directory of hand-run `.py` files; not notebooks);
   - the gate tools from ini's dev group into the project's (`uv add --dev`), and the skill rows in
     its `AGENTS.md`;
   - `uv run python -m ci gates --adopt` records today's debt in `ci/ceilings.json`; `--prove` is
     green.
   The harness needs Python 3.14. When the project's runtime is older, run the gates under 3.14
   only if its code imports there; otherwise stop and tell the director.
2. **Compliance**, in later rounds: fix, then `--record`, until the ratchet is empty. A rule that
   does not fit the project goes to the director as a proposal for ini, never as a local edit.
3. **Again**, when ini has moved: `diff -r <ini>/base base` and the same for `ci/`, bring the
   difference in, and fix or `--adopt` a new rule meeting old code. Say which in `log/agt.md`.

## up — promote

A candidate holds in at least two projects, or it names no project-specific file, number or tool.

1. **Generalise**: restate it as the class of failure or the procedure, with the incidents as
   evidence (project, date). Strip project names a public repository should not carry.
2. **Place it**: a principle in `base/foundation.md`, an enforceable rule in
   `base/code-standard.md` (and a gate, if a machine can hold it), a lesson in `base/learnings.md`,
   a procedure in `base/skills/<name>/SKILL.md`. Prefer extending an existing section to adding one.
3. **Edit ini, not the copy**: in the ini repository, under `base/` (or `ci/` for a gate). A gate
   change ships with its witness and `uv run python -m ci gates --prove` green in ini.
4. **Budget**: the base is read by every agent in every project. A promotion that adds lines removes
   some — merge, rank, delete the weakest (`base/skills/compress`).
5. Commit in ini with the evidence in the message; then run *down* in the project that proposed it.
   Its local copy of the lesson is deleted in the same round: one fact, one home.

## what stays local

The project's objective, product invariants, domain words, its own skills that name its files, and
its learnings until they hold twice. `base/` and `ci/` are never edited in place: a local fork turns
the next *down* into a merge.
