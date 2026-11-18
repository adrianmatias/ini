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

## redundancy vs decoupling: distil, don't link

- The director's contradiction: shared knowledge is either a copy in every project (redundant, and
  it drifts) or one central source (and the projects depend on it). The resolution is his, an agent
  distilling into each project, and it is now the model. A project owns its distillate and stays
  whole without ini; `[tool.ini] origin` records the ini commit it read. *Again* reads
  `git log <origin>..` and brings in what applies, rather than diffing trees, because the trees are
  meant to diverge.
- Evidence: the first ongoing project to take ini did this already. It kept `ci/` as its own, added
  a product gate to it and left `base/` out of the tree. The old harvest text ("never edited in
  place") would have marked that as a fork.
- Changed: foundation (header; "Distil, don't link"), harvest (down rewritten, "what never
  crosses"), the headers of code-standard, learnings and base README, the kickoff's step 0 and
  AGENTS template, objective (claim, target 2, kill), README, AGENTS, domain words (distil, origin),
  `Settings.origin`.

Proved: gates 13/13, `--prove` 13/13, `uv run pytest` 12 passed.

## no base, no origin

- The director, on the two open decisions: no dependency and no registered commit; no `base/` in
  ini or in a project.
- `base/` dissolved into the root, where a project keeps its knowledge: `foundation.md`,
  `code-standard.md`, `wiki/learnings.md`, `skills/`. A copy keeps them and owns them. The
  kickoff's foundation and learnings templates are gone, so a project's invariants go in a section
  at the end of `foundation.md`, and a new copy carries six kickoff placeholders instead of seven.
- `Settings.base` and `Settings.origin` were removed; the harness reads `skills/` and
  `wiki/learnings.md` only. *Again* in harvest means reading ini as it is now (its log and `now.md`
  say what moved) and comparing with the project by meaning.

Proved: gates 13/13, `--prove` 13/13, `uv run pytest` 12 passed.

## harvest up: three fixes from the first distillate

- The fruit-salad example was reverted by the director; `ci/` is again the package the gates judge.
- **Data link**: `Replica.link` symlinks whatever the replica did not copy, and descends into the
  copied directories. Without it, a suite that reads project data at collection errored in the
  scratch copy; the error was not located in the planted file, so the behaviour witness looked inert.
  Test: a conftest that reads `data/` at import, with `--prove --only behaviour` green.
- **Every suite**: the behaviour gate runs pytest without a path, so it collects what `testpaths`
  names. Before, it ran only `[tool.ini] tests`. Test: a failing test in a second `testpaths`
  folder turns the gate red.
- Both tests fail on the previous harness and pass on this one.
- **Field docstrings as prose**: this fix lives in a project's own literal-counting gate, and ini
  has no gate that counts literals. It came up as a lesson instead (`wiki/learnings.md` §1).

Proved: gates 13/13, `--prove` 13/13, `uv run pytest` 14 passed.
