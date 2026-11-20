---
name: delegate
description: Use when work could fan out to other agents. Roles, patterns, effort, briefs, integration.
---

# delegate

Delegation is a trade: focus against fragmentation, speed against cost. **The default is one
session, direct.** This skill names the roles, the few patterns worth their overhead, and how a
lane's work comes back. Concrete models are machine-local facts: the project's `AGENTS.md` maps
each role to a model; this file speaks in roles only.

## the hierarchy

| role | who | does | never |
|---|---|---|---|
| director | the human | sets the objective, decides, judges taste, approves pushes | is asked what the files already say |
| integrator | the session, strong model (plan-backed or pay-per-token complement), high effort | plans, writes what the director reads, merges, judges | runs parallel lanes on a plan quota or burns paid tokens on bulk |
| lane | cheap API model, maximum effort, fresh context | one bounded slice: ingest, extraction, a package, a draft | decides a design, edits a file outside its list |
| critic | a different model family, high effort | reads the contract and the diff, returns failing cases | sees the author's reasoning |

Effort and billing follow the role: a cheap model is slow and weak below maximum effort, so lanes
run at max; never run parallel lanes on a plan quota, never burn pay-per-token strong models on
bulk, and never run two strong families on the same job. Steering flows down the tiers
(`objective > foundation > domain > code-standard > gates > implementation`); evidence flows up as
findings, never as summaries taken on trust.

## patterns

- **direct** (default) — the session does it. A task it closes in about ten tool calls is never
  delegated: the brief costs more than the work.
- **sandwich** — plan (integrator) → execute (lanes, parallel only for disjoint files) → validate
  (critic or a fresh context that writes nothing). For a change too big for one context.
- **fan-out** — one question or one package per lane, read-only or on disjoint files; the
  integrator distils. Worth it from three lanes up.
- **adversarial** — one critic pass by another family over the contract, the diff and the test
  delta (`skills/review`). For anything that ships or that the director will repeat.
- **cascade** — try the cheap role, verify mechanically, escalate one tier only on a proven
  failure, carrying the failure forward.
- **expand / compress** — a lane may expand (drafts, options, a survey); compression is the
  integrator's (`skills/compress`).

Never split one decision or one document's argument across lanes.

## before a fan-out

- **Confirm the model before dispatching.** Check which model and family a lane or critic will
  actually run on; if a session policy blocks the route or a critic would share the author's family,
  stop and ask or switch once — never spawn a call that dies, never report a same-family pass as
  cross-family, and never shell out to another LLM CLI inside a session.
- **Undo temporary model overrides at once**: verify the active child's model after dispatching and
  restore the default right after spawning, before children finish.
- **Decide the cross-cutting things first** and commit them on the base: a changed rule, a new
  dependency, a convention. Left open, they come back as N incompatible guesses.
- **Snapshot or worktree**: on a dirty tree, archive what lanes may touch; on a clean one, one git
  worktree per write lane.
- All lanes of a round go out in one call unless one lane's output is another's input; spend the
  wait on disjoint work or end the turn (background results arrive between turns — never poll).

## the brief

A lane knows nothing. Give absolute paths, the objective, the invariants, the boundary and what to
return — by objective, not a checklist.

- **Write lanes get an exact file list**; everything else is read-only to them. Shared files —
  `AGENTS.md`, `now.md`, `log/*`, ratchets, the lock — belong to the integrator; a lane reports the
  line it needs.
- **Read-only lanes return structured output** and also write it to one scratch file: transcripts
  truncate.
- **Put the size budget in the brief.** A lane told to rework a file returns a faithful, larger one
  unless «fewer lines, fewer concepts» is part of its objective.
- Say what to do when the source is silent: «omit and report the gap; do not invent».
- Ask for evidence the integrator can check without rereading the source: quotes, `path:line`.
- A brief leaves the machine: no credentials, no `.env`, no private material the project keeps out
  of its prompts.
- **A long lane is timeboxed** and writes its report before its final answer; an interrupted lane
  returns partial output, never its report.

## integrate

- **A lane's report is a claim.** Merge the tree, run every gate on the merge, read the diff, check a
  handful of its citations. Recompute any count it proposes.
- **An interrupted lane leaves a worktree, not nothing.** After a stop or model switch, inspect its
  worktree (`git log`, `git status`); staged renames and uncommitted edits are usually sound, so
  finish stragglers instead of re-dispatching from scratch.
- **A failed lane is retried tighter, not repeated**: a smaller sample, a shorter brief, its partial
  output as context. If a route stalls, replace the family once or absorb inline — no retry loops.
- **The integrator accepts only the whole tree green**, never a lane's own green.
- Record in `log/agt.md` which lanes ran, on which model, and what was rejected.
