---
name: kickoff
description: Use when a project starts or its bet changes. State the objective as a checkable loss.
---

# kickoff

The first round of a project, and the round to repeat when the bet changes. The harness gate stays
red while any kickoff placeholder is left in an anchor: work starts after the objective is stated.

## 0. from a copy of ini (skip when the bet of a running project changes)

1. Every `templates/**/*.tmpl` goes to the same path at the root, suffix dropped, with `{{project}}`,
   `{{package}}` (an importable name), `{{owner}}` (the director: `log/<owner>.md`) and `{{date}}`
   replaced. ini's own `log/` and `ci/tests/` go; `foundation.md`, `code-standard.md`,
   `wiki/learnings.md` and `skills/` stay, and the project owns them from now on.
2. `pyproject.toml`: the project's name and description; `[tool.ini]` becomes `src = "src"`,
   `package = "<package>"`, `tests = "tests"`, `scripts = ["ci"]`; pytest's `testpaths` becomes
   `["tests"]` and its `pythonpath` `["src"]`; `[tool.uv]` gives way to a `[build-system]` of
   `uv_build`, so `uv sync` installs the package and its run scripts resolve.
3. `git config core.hooksPath .githooks`, `uv run python -m ci domain --write`, then
   `uv run python -m ci gates`: red only on the kickoff placeholders, which the steps below answer.

## 1. the objective (`objective.md`)

Ask the director, in one message, only what the files cannot answer. Then write:

- **The claim** — one sentence: what will be true when this works, for whom.
- **The target** — a loss a stranger can check: a metric with a threshold and a direction, a count
  of paying users by a date, a pass/fail against a public benchmark. Not «improve», not «explore».
  If the director's goal is fuzzy, propose two targets and let him pick.
- **Success scenarios** — three at most, each observable.
- **Kill criteria** — what result, by when, stops or reframes the project. A project without a kill
  criterion is a hobby; say so if that is what it is.
- **What it is not** — the tempting adjacent product this project refuses to become.

Register the project's open strategic or product bets in `wiki/conjectures.md` with their
refutation conditions (`c1`, `c2`, …): a claim without a falsifier is a vibe.

Mirror the target in code: `core/objective.py` holds a `Target` whose `loss(measured)` is zero
when the objective is met. Keep it if the target is a metric; replace it with the project's own
first entity if not. The behaviour test that pins it is the project's first contract.

## 2. the foundation (`foundation.md`)

A section at the end, named after the project, with only what it adds: product invariants (pricing, privacy, dignity),
domain invariants (point-in-time data, money in `Decimal`), and the one or two rules that would be
fatal to forget. Five lines is a good section; thirty is a second objective. A general line that
does not fit the project is edited or deleted, and the reason goes in `log/agt.md`.

## 3. the domain (`domain.md`)

The words: each term the objective uses, what it means here, what it is not. The ontology block
below them is rendered (`uv run python -m ci domain --write`); never type into it.

## 4. requirements, when someone else owns them

Put the source documents under `requirements/` as quoted text with ids, one file per source, and
an index. Contradictions between sources go to the director as a list, never resolved silently.
Agents cite requirement ids; they never paraphrase a requirement into `AGENTS.md`.

## 5. the walking skeleton

One thin path from the real input to the real output, end to end, through the `cli/` run script and
one behaviour test. An LLM may carry any step at first; name which steps it carries in `now.md`, so
the next rounds can move them into deterministic code.

## close

`uv run python -m ci gates` green — the harness gate included — then `now.md` (what is true, the one next
move), and the round in `log/agt.md`. Commit when the director says so.
