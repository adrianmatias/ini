---
name: review
description: Use when a change, plan or artifact needs a critic before it ships. Another family reads it.
---

# review

The author's model family shares its blind spots: self-review confirms. One independent pass by a
different family, over a precisely cut context, finds what the author cannot.

## what the critic gets

- **The contract**: the objective's relevant lines, the requirement ids, the acceptance checks, the
  invariants from `base/foundation.md` that apply.
- **The artifact**: the diff, or the document, whole.
- **The test delta**: what tests were added, changed or deleted.
- **Not** the author's reasoning, plan or conversation: fresh context is the point.

## what the critic returns

Findings, each one checkable without trusting the critic:

- `severity`: blocks / should-fix / note;
- `claim`: one sentence;
- `evidence`: a quote with `path:line`, or a failing input and the output it produces;
- `fix`: the smallest change that would resolve it, or «unknown».

Tell the critic that «no finding» is an acceptable answer, that a finding without evidence is
discarded, and that style preferences are not findings unless a rule in `base/code-standard.md`
names them.

## judge the findings

The integrator judges; the critic does not merge.

1. **Reproduce** each blocking finding: run the failing input, read the quoted lines. A finding that
   does not reproduce is killed with its reason.
2. **A kept finding becomes a failing test** (or a gate witness) before the fix, so it cannot come
   back.
3. **Narrow, do not inflate**: a finding may be true of one case and false as stated in general;
   keep the true part.
4. When several findings share a premise, fix the premise once.

## record

In `log/agt.md`: the critic's model, how many findings, kept and killed with one-line reasons. A
pattern that recurs across reviews is a lesson for `wiki/learnings.md`, or a gate.

## when not to review

A one-line change with a failing-then-passing test, a rename the gates prove, a scratch
experiment. Review is for what ships, what the director will repeat to someone else, and anything
whose error is expensive to undo.
