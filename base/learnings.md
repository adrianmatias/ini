# learnings

Inherited from ini; do not edit here. Lessons that held in more than one project, one imperative
rule per line with the evidence that bought it. A project's own lessons live in its
`wiki/learnings.md`; one that holds twice moves here (`base/skills/harvest`). Grouped by the class
of failure it prevents; budget 160 lines.

## 1. Boundaries own the defects

- **Name every seam with its shape, its invariant and the gate that keeps it.** A defect reached a
  buyer twice through a boundary nobody owned (2026-09).
- **Wire every predicate through the real entry point, then test the wiring.** A key check existed
  and silently dropped the nine items it found (2026-09-21).
- **Test the check, not the clean tree.** A release needle spelled «gmail..com» was green by
  construction until it was fixed and fired on its first run.
- **Parse a ship-blocking artifact by its contract.** A hand-written check accepted five of six
  corruptions — `must_fix: "none"` iterates per character.
- **Derive the gate scope from the repository, not from a sentence.** A second package passed every
  gate for weeks because no gate looked at it (2026-11-05).
- **A diagram is a claim; render it from the code.** A hand-drawn package map kept two edges for
  weeks after both were gone (2026-11-11).

## 2. Requirements and agents

- **Encode the requirements as a verifiable artifact before steering agents.** Agents built a
  hallucinated mixed scoring mode; the oversized unit suite and AGENTS.md both pinned the wrong
  shape and refused the correction until the quoted requirements were in the repo (2026).
- **Shape beats style.** One domain model and enforced gates paid; enforced functional style cost
  42 % more lines and caught nothing (a ledger benchmark, 2026-09).
- **A declarative schema tames agent sprawl.** Typed models constrained an LLM from raw text to the
  expected artifact and kept the codebase from a pile of functions correcting one another (2026).
- **Name the metric the reader judges by before choosing by it.** A take-home failed on modularity
  (one file in twelve sections), missing tests, and a primary metric the reviewers did not share —
  calibration over PR-AUC (2026-10-29).

## 3. Generated artifacts are claims

- **A fix is done when the generator changed and the artifact was rebuilt.** The commit said
  removed; the page still served the item (2026-11-05).
- **A count a reader sees is derived or a bound, and a test owns it.** «482 questions» drifted from
  the bank in one round.
- **A byte-identity pin is a review gate.** When a shared renderer changes, keep the others identical
  or call it a product change with a reason — never edit the pin to get green.
- **Before deleting a producer, find what proves its output.** A generator was the only proof of half
  the data it froze (2026-11-12).

## 4. Tests freeze contracts, not structure

- **Bind tests to the public surface, or a coverage gate breeds a private-helper suite.** 41 unit
  files reached 367 private names and doubled the suite (2026-11-06).
- **Size is a contract.** 74 files / 13 525 lines became 45 / 7 000 by deleting structure tests, not
  coverage.
- **Mutation parity is a sample, not a proof.** It missed a dropped retry on the money path; an
  adversarial reader found it (2026-11-06).
- **A facade kept alive only by a test is dead code with a caller.** Delete it, drive the component.
- **A scan that skips a missing input proves nothing.** Require every input to exist.
- **Drive a CLI's `main` in process.** A suite that switched to subprocesses left 49 complex
  functions at 0 % coverage; the CRAP gate caught it, the green suite did not.

## 5. Delegation

- **Probe the exact route with one tool call before a fan-out.** A text-only probe passed while every
  real lane died; an all-null result is a route failure, never «finished» (2026-11-05).
- **The integrator accepts only the whole tree.** Lanes were green alone while the merge lost a
  `__main__` guard.
- **The reviewer is another family, and a finding is a failing case.** A cross-family read of the
  deleted tests found what sampled mutation did not (2026-11-06).
- **Lanes run on a different quota than the integrator.** Four parallel lanes on one plan exhausted
  its rate limit in three minutes, twice (2026-11-11).
- **Package lanes compress packages; concepts that span packages need one lane per concept.** Eight
  package lanes took 5 % out; the cross-package concepts went in a second wave (2026-11-12).
- **Put the size budget in the brief.** Two lanes returned a faithful, twice larger file.
- **A brief by objective beats a checklist.** A lane given a ticket list mirrors the list.

## 6. Environment

- **One dependency home.** Declared in `pyproject.toml`, pinned in `uv.lock`, installed everywhere
  the code runs from that one declaration (2026-11-10).
- **Run the gates from a clean shell.** A harness that exported `PYTHONPATH` made the venv import a
  foreign `pydantic_core` and turned five gates red on a green tree (2026-11-11). ini's tools
  run with the import path reset for this reason.
- **Ignore editor state wholesale.** A sweeping `git add` in a restructure commit carried an editor's
  hotkeys file into the repository (2026-11-10); `.obsidian/`, `.idea/` belong in `.gitignore`.
- **Check wheels before raising the floor.** On 2026-11-18 Python 3.15 resolved pydantic, torch and
  polars but not onnxruntime or langgraph's pyyaml (ini).
