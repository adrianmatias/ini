---
name: mode
description: Use when writing or changing code. Make it work, make it right, practice — gates as proof.
---

# mode

The engineering loop: make it work, then make it right, then practice. The rules are in
`base/foundation.md` and `base/code-standard.md`; this is the order in which to apply them.

## 1. make it work

- **Shape before logic.** Name the thing first. A concept two components use lives once in
  `core/`; a closed vocabulary is a `StrEnum`. Write the type that makes the illegal state
  unconstructible — a pydantic model if it crosses a wire, a frozen dataclass if it never leaves the
  process. The logic that remains is usually short.
- **Failing test first** for a behaviour change or a bug: at the public surface (the run script's
  `main` in process, or the component's public method), seen to fail for the reason you expect.
- **Smallest edit that solves it**, in the one place the decision lives. Grep before writing a
  threshold or a rule — it probably exists.
- **Redesign from first principles** when a requirement does not fit: what would you have built had
  it been there from the start? Deliver that in pieces. Do not bolt on.
- **Attack the premise.** Two fixes that share a premise and fail the same gate mean the premise is
  the defect. Write it in one sentence before a third attempt.
- **Subtract before you add.** Look for what the change makes unnecessary and delete it first.
- **LLM steps shrink.** Where an LLM carries a step, ask each round which part of it is now
  deterministic (a parse, a lookup, a rule) and move that part into code with a test.

## 2. make it right

Never in the same diff as step 1.

- **Refactor = pin, restructure, prove.** The pins are the artifact digests and the suite; a
  refactor leaves both untouched. If a pin moves, it is a product change and carries its reason.
- **Gates**: `uv run python -m ci gates`; `--prove` after a gate or its scope changed.
  - *complexity*, *crap*: split the function, test it, or both — never raise the budget;
  - *pile*, *component*: the free functions share a concept — name it as a class;
  - *deadcode*: delete it; `ci/deadcode-whitelist.py` is only for names a framework calls;
  - *duplication*: a missing abstraction — find the concept that makes the copy unnecessary;
  - *domain*: describe the field in the field; re-render with `uv run python -m ci domain --write`;
  - *types*, *annotations*, *surface*: fix the cause, never suppress.
- **After a fix that lowered debt**, `uv run python -m ci gates --record`: a record above what the gates
  measure is red until it is lowered.
- **Tests**: would it pass if every function returned nothing? Delete it. Does a refactor that keeps
  behaviour break it? It tests the implementation — rewrite it at the surface or delete it.
- **Mutation audit before a release**, one module at a time — an audit, not a gate:
  `uv run --with mutmut mutmut run` with `paths_to_mutate` set to one module and the test
  selection set to its behaviour file. A surviving mutant is a missing behaviour test or dead code.

## 3. practice

- **Sequence into verifiable units**: finish one, run the gates, commit, start the next.
- **Commit small, in order**: each message says why, what changed and how it was proved. Push only
  when the director says so.
- **Guard the context window**: keep the main thread for decisions; send bulk reading and
  mechanical edits to a lane (`base/skills/delegate`).
- **Close the round**: gates green, `now.md` rewritten, `log/agt.md` appended, the lesson in
  `wiki/learnings.md` under the failure class it prevents, the procedure — if it will recur — in
  `skills/`. Then compress (`base/skills/compress`).

## pitfalls already paid for

- **Run the gates from a plain terminal** or let ini reset the import path; a harness that exports
  `PYTHONPATH` makes the venv import foreign compiled modules.
- **Do not edit files while the gates run**: *crap* joins coverage to source read afterwards.
- **A CLI driven through `subprocess` is invisible to coverage**: drive `main` in process.
- **A test that monkeypatches a path constant writes to the real tree** once the module stops
  reading that constant: check `git status` after touching how a module finds its files.
