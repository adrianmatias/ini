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

# 2026-11-20

## harvest up: dream loop, push gate, AST call-site sweep and multi-family routing

Phase: expand (harvest candidates across active projects since 2026-11-18) then compress.

- **Field evidence (2026-11-18..20)**: harvested from two ongoing projects carrying ini distillates
  (the first running 14 gates with a product gate and pre-push hook; a second newly distilled onto
  all 13 gates with `--prove` 13/13), one new project started from a copy of 0.3.0 (13/13 green
  after kickoff), and a non-code knowledge vault.
- **Dream & Deutsch conjectures** (`skills/dream/SKILL.md`, `foundation.md` §lenses, `AGENTS.md`,
  `skills/kickoff/templates/AGENTS.md.tmpl`): promoted the two-phase consolidation loop — replay
  logs before sampling, cross-family daydream with verbatim machine-grounded quotes, and a
  falsifiable `wiki/conjectures.md` register.
- **Pre-push gate for `main`** (`.githooks/pre-push`, `code-standard.md`, `README.md`,
  `skills/kickoff/SKILL.md`, `skills/kickoff/templates/AGENTS.md.tmpl`, `ci/tests/test_gates.py`):
  gates the exact `$local_sha` pushed to `refs/heads/main` (using a detached worktree when not at
  a clean `HEAD`), skipping branch pushes and all-zero deletions.
- **Restructure & parallel lanes** (`skills/restructure/SKILL.md`,
  `skills/restructure/scripts/sweep_callsites.py`, `ci/tests/test_skills.py`): added AST call-site
  rewriting (handling split imports, refusing shadowing locals and local imports), per-package
  `GATES`/`Session` debt dumping, base-first kernel reshaping, `@staticmethod`-pile spot-checks,
  import-only conflict auto-resolution, and `rsync` residue cleanup after `git mv`.
- **Billing-aware routing, review & recovery** (`AGENTS.md`, `AGENTS.md.tmpl`,
  `skills/delegate/SKILL.md`, `skills/review/SKILL.md`): added three-family rotation (plan-backed vs
  pay-per-token complement vs cheap API volume), harness-neutral pre-dispatch model checks, immediate
  override cleanup, no subprocess LLM CLI calls, explicit finding dispositions, and resuming
  interrupted lane worktrees.
- **Standards & learnings** (`foundation.md` §engineering 7–8, `code-standard.md` §shape 4,
  `wiki/learnings.md`): tightened wire-model/ledger rules, noted `object` narrowing at decode seams,
  folded 8 lessons (6 new, 2 merged into existing rules) and dropped 4 intra-repo duplicates
  (`wiki/learnings.md` 87 → 92/160 lines; `AGENTS.md` 74 → 75/120; all skills 56–90/150).
- **Critic (`claude-opus-5-5`, cross-family)**: found 1 blocker (pre-push gated working tree
  instead of `$local_sha`), 7 should-fix (split-import bug in `sweep_callsites.py`, `.git`
  dependency in `test_gates.py`, stale redaction notes, unlogged field evidence in `now.md`,
  learnings budget and 4 intra-repo duplicates, harness-specific `list`/`pin` terms in `delegate`)
  and 3 notes (count mismatch, SHA-256 zero oid, non-existent `wiki/conjectures.md` citation). All
  11 accepted and resolved, with tests added in `ci/tests/test_gates.py` and `ci/tests/test_skills.py`.

Proved: `uv run pytest` 16 passed; `uv run python -m ci domain --write` unchanged;
`uv run python -m ci gates` 13/13; `--prove` 13/13.

# 2026-11-23

## harvest up: knowledge management from the Deutsch lenses

Phase: expand (harvest Deutsch-lens knowledge structures from active projects) then compress.

- **Conjecture register & starter template** (`wiki/conjectures.md`,
  `skills/kickoff/templates/wiki/conjectures.md.tmpl`, `domain.md`, `README.md`, `AGENTS.md`,
  `skills/kickoff/templates/AGENTS.md.tmpl`): added `ini`'s own live Deutsch board (`c1`–`c3` open,
  `c4`–`c5` promoted, `c6`–`c8` destroyed with permanent ids) and a rendered starter template for new
  copies, defined `conjecture` in `domain.md`, and wired `wiki/conjectures.md` into `AGENTS.md` /
  `AGENTS.md.tmpl` entry, close, and `dream` triggers without conflating `ini`'s own bets with the
  universal knowledge projects merge.
- **Deterministic dream tool** (`skills/dream/scripts/dream.py`, `skills/dream/SKILL.md`,
  `ci/tests/test_skills.py`): harvested and hardened `pairs`, `check`, and `feed` (`Decision`
  `StrEnum`, `Pair`/`Candidate`/`Verdict` wire models, `--root` flag, `kind: "none"` skip,
  self-link and path-qualified link checks, section-aware `## Dream links` insertion, and idempotent
  `pairs.tsv` ledger appends).
- **Epistemology & lifecycle alignment** (`foundation.md`, `wiki/learnings.md`,
  `skills/kickoff/SKILL.md`, `skills/compress/SKILL.md`, `skills/harvest/SKILL.md`): recorded the
  negative-knowledge rule (`learnings.md` + `destroyed` conjectures), tightened the Deutsch lens
  around hard-to-vary falsifiable claims, and folded the field lesson that standalone conjecture
  boards stall unless paired with log replay and falsifiers (`wiki/learnings.md` 96 → 99/160 lines;
  `AGENTS.md` 75 → 76/120; all skills 56–89/150).
- **Critic (`claude-opus-5-5`, cross-family)**: found 0 blockers, 6 should-fix (`check` rejecting
  `kind: "none"` rows, `Verdict.verdict` plain `str` + empty `claim`, non-idempotent `pairs.tsv`
  append, `## Dream links` inserting at EOF when another heading follows, `wiki/conjectures.md`
  mixed classification across `domain.md`/`README.md`/`harvest`, and unsourced `cD3` / circular
  `cP3` evidence) and 5 notes (permanent conjecture ids, weak template assertion in `test_gates.py`,
  repeated destroyed-bet rule, stray `wiki/SCHEMA.md` line, and `E501` / dict-as-record /
  path-collision / self-link bugs in `dream.py`). All 11 accepted and resolved with failing tests
  written first.

Proved: `uv run pytest` 18 passed; `ruff check` (with `E501`) and `ty check` clean on
`skills/dream/scripts/dream.py`; `uv run python -m ci domain --write` clean; `uv run python -m ci
gates` 13/13; `--prove` 13/13.

- 2026-11-26: ACDC GitHub PR webhook probe for n8n gate verification.

- 2026-11-26: DeepSeek critic endpoint probe commit.

- 2026-11-26: Verified updated DeepSeek ACDC workflow webhook probe.
