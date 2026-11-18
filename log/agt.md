# 2026-11-18

> The agent's rounds of the first day, compressed before publishing: project names, paths and
> local tool state removed at the director's request; what was decided and proved is kept.

## first version: a package with thirteen gates

- Thirteen gates, each with a witness planted in a scratch copy (`--prove`): lint, docs,
  annotations, types, surface, shape, complexity, duplication, deadcode, domain, harness,
  behaviour, crap. The four no single tool holds: *domain* (wire fields describe themselves; the
  rendered ontology equals the code), *shape* (object orientation: run layer apart, at most six free
  functions per module, no classless package), the ontology render, and *docs* (self-commented
  code).
- A ratchet (`--adopt` once, `--record` to lower, a stale record is red) so an ongoing project can
  take the gates without a big-bang cleanup.
- The base: foundation, code standard, learnings, seven skills (kickoff, mode, review, delegate,
  restructure, compress, harvest). Python floor 3.14, after checking wheels for 3.15.

## publishable, a live cookiecutter, a cross-family critic

- Framed as a live cookiecutter for AI agents, with the objective sentence verbatim. Project names
  stripped from the base and the anchors; evidence keeps its date.
- Foundation 3: walking skeleton first, then distil the LLM out — each round moves a step the LLM
  carries into deterministic code, so a project grows into engineering, not a thin wrapper.
- The field-description rule stays strict.
- A critic from the other model family: six findings, all kept. The serious one: with the gate
  tools missing, three gates read an empty failure as green. A missing tool is now a refusal.

## three ongoing projects, met halfway

- Probing three ongoing projects (scratch copies) showed the common denominator: flat layouts, two
  without pydantic, none with its run layer in `cli/`, runtimes from 3.10 to 3.12, one deploying on
  a distribution's `python3`.
- Gate fixes, each a generic gap: a suite inside the package is judged as tests; a `__main__.py` is
  run layer; tests carry no annotation duty; pathlib style is not a lint rule. One probe went from
  846 findings to 231.
- One project's single-module deliverable became a package of one module per section, behaviour
  pinned by its suite, its own gates and mutations, and an identical full-run output. A same-size
  mutant restored within a second once ran from stale bytecode; its mutation gate now writes none.
- Editor state is ignored wholesale: a sweeping `git add` had carried an editor's hotkeys into a
  repository.

## restated: knowledge in the shape of a fresh repository

- ini is not installable. `base/` holds the inherited knowledge; `ci/` holds the harness, run from
  the tree with `uv run python -m ci`; the kickoff's templates hold the placeholder anchors and the
  walking skeleton. `pyproject.toml` is the starter: pydantic, the gate toolchain as the dev group.
- A new project is a copy: the kickoff's step 0 renders the templates and points `[tool.ini]` at
  the new package, with a build system so its run scripts import. An ongoing project is permeated
  by an agent (harvest *down*): harness first, then compliance until the ratchet is empty.
- The suite copies this repository and starts it as a project, so it proves a fresh copy is ready.
  End to end outside the suite: copy, start, `uv sync`, gates 13/13, the run script runs.

Proved: `uv run pytest` 12 passed; `uv run python -m ci gates` 13/13; `--prove` 13/13.

## publish

- `AGENTS.md` rewritten for the template model; the publishable rule now covers the logs too.
- Both logs compressed and stripped of project names, paths and local tool state.
- First commit of the template, pushed.
