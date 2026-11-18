---
name: compress
description: Use when a round ends, or code, docs or skills have grown. Judge, kill, fold, measure.
---

# compress

The contraction half of every round. Expansion builds; compression is where the project learns.
It applies to three things at once — the code, the documents, and the harness itself — because a
harness that only grows exhausts the context it was meant to save and overfits to yesterday's task.

## the cycle

1. **Name the phase.** Say at the start of a round whether it expands or compresses. A round may do
   both, but it ends compressed.
2. **Judge against the objective.** List the threads the round opened. For each: does it move the
   target in `objective.md`? Keep, kill with a one-line reason, or park it in `now.md`.
3. **Fold what survived** into fewer concepts, lines and files (below).
4. **Measure.** Before and after: lines of code, number of public classes and free functions, test
   lines, `AGENTS.md` and skills lines, learnings lines. Report the delta honestly — a compression
   that grew the line count says why (a kernel concept often does, before the waves that use it).
5. **Name the one next move** in `now.md`.

## code

- **Redundancy is the signal.** The same literal, status string, dict shape or file-reading idiom
  in several places is a concept without a home. Survey it (grep, or an AST count), give it one home
  in `core/`, switch the callers green, ratchet the count.
- **A table for a cascade**, a library call for hand-rolled code, a dataclass for a pydantic model
  nothing serialises, a dead path deleted.
- Deleting docstrings or squeezing lines is not compression.
- Ratchets: after the fold, `uv run python -m ci gates --record`.

## documents

- One fact, one home. A fact in two pages is moved to the one that owns it and linked from the
  other.
- `now.md` holds what is true today; it is rewritten, not appended.
- Logs are append-only and never compressed: they are the record compression is judged against.

## the harness (skills, AGENTS.md, learnings)

The harness gate holds the budgets; this is how to stay under them with more knowledge, not less.

- **Replay**: read the round's `log/agt.md` entries since the last compression. What procedure was
  done twice? What failed twice for the same reason?
- **Promote**: a procedure done twice becomes a skill or a section of one; a lesson becomes one line
  in `wiki/learnings.md`, under the failure class it prevents, with its evidence.
- **Merge**: two skills whose triggers overlap become one; a skill section nobody followed in the
  last rounds is deleted; detail that is read rarely moves to the skill's `references/`.
- **Rank**: learnings are ordered by the cost of the failure they prevent; the bottom of a full
  list is the first to go.
- **Generalise or keep local**: a skill or lesson that held in two projects goes upstream to ini
  (`base/skills/harvest`); one that names this project's files stays here.
- **Overfitting test**: a rule that mentions a single incident's file names or numbers in its
  imperative is a log entry pretending to be a rule. Restate it as the class of failure, keep the
  incident as its evidence.

## close

Gates green, the deltas in `log/agt.md`, the next move in `now.md`.
