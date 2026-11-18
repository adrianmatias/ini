# foundation

Inherited from ini; do not edit here — improve it upstream (`base/skills/harvest`). Tier 2 of
`objective > foundation > domain > code-standard > gates and behaviour tests > implementation`. A
project adds its own invariants in its `foundation.md`; where the two disagree, the project's
objective decides and the conflict goes upstream.

**Simplicity leads. Compression is the core of intelligence.** Redundancy is what a wrong concept
looks like from outside: two files that say the same thing, two functions that derive the same
value, a test per function. When something is said twice, find the concept that makes the second
statement unnecessary.

## direction

1. **The objective is a loss.** State a target a machine or a stranger can check — a metric with a
   threshold, a sale, a pass/fail — and spend tokens on closing the gap. Work that moves no target
   is expansion without contraction.
2. **Requirements are an artifact, not a memory.** Quote them from their source, index them, version
   them, and surface their contradictions to the person who owns them. An agent that paraphrases a
   requirement into its own notes will build the paraphrase.
3. **Walking skeleton first, then distil the LLM out.** One thin path from input to output that
   runs end to end, then depth. An LLM may carry every step of the first skeleton; each round moves
   a step it carries into deterministic code — typed, tested, cheap, repeatable — and the LLM keeps
   only the judgement nothing else can make. A project grows into engineering, not a thin wrapper
   around a model.
4. **Measure with the uncertainty.** A number without its spread is an anecdote; 7/10 is not 70/100.
   Decide on the metric the decision uses, not on the one that is easy to report.

## engineering

5. **Model the domain first.** Name the things, then make the illegal state impossible to construct.
   The names come from `domain.md`; the map of what exists is rendered from the code, never drawn.
6. **A concept is a class; a component is a package.** The class owns its data, its rules and its
   workflow; the package states its role. Agents left alone write piles of functions that correct
   one another — a named class is where that stops.
7. **The schema is the prompt.** A model that crosses a wire — to a file, a client or an LLM —
   describes each field once, in the field. Prompts are rendered from the domain, so the words an
   LLM reads cannot drift from the types the code checks.
8. **Declarative over imperative.** Describe the data — tables, specs, section lists — and let one
   interpreter walk it. Artifacts are projections of the model: regenerated, never hand-edited.
9. **Proof over prose.** A rule is a gate that has been seen to fail, or it says why nothing can
   enforce it. Tests pin behaviour at the public surface; a narrow test is micromanagement.
10. **Root cause always.** Reproduce, fix the cause, wire the check through the real entry point. A
    guard that hides the failure is not a fix.
11. **Pragmatic dependencies.** A maintained library that deletes a class of code is welcome,
    declared and locked; a framework where a typed renderer and a static file suffice is not.
12. **Operations are idempotent.** Run twice, or resumed after a crash, the end state is the same.

## rhythm

- **Expand, then compress.** Work breathes. *Expand*: generate paths toward the objective, build,
  make it work. *Compress*: judge every thread against the objective, kill with reasons, fold what
  survived into fewer concepts, lines and files, and name the one next move. A round that only
  expands leaves debt; one that only compresses ships nothing. Every round ends compressed.
- **Make it work, then make it right** — never in the same diff.
- **Subtract before you add.** Two fixes that share a premise and fail the same gate mean the
  premise is the defect.
- **Build the lever.** If a change is not obvious at a glance, do one unit by hand, then write the
  tool that does the rest.
- **Trust the agent, verify the tree.** Give it the objective, the invariants and the gates, not a
  checklist; accept only the whole tree green. Agents overestimate how long a task takes and divert
  into partial fixes — hold them to the whole change.

## the harness compounds

- **Skills are the by-product of the work.** A procedure done twice becomes a skill; a lesson that
  cost a round becomes one line in `learnings.md`. Both are compressed like code, on a budget, or
  they exhaust the context they were meant to save and overfit the harness to yesterday's task.
- **Skills over plugins.** Plain files any agent reads on demand travel across harnesses, vendors
  and years; a plugin binds the method to one tool.
- **What generalises goes upstream.** A skill or lesson that holds in two projects moves into ini,
  and every project takes it in the next time an agent brings ini down.

## sovereignty

Open-source first, local-first, portable across harnesses and model vendors. The repository is the
memory: anchors, domain, skills and logs are plain files. The director's attention is the
bottleneck — what he reads is concise and complete, and his hours go to direction and judgement.

## lenses

Constraints distilled from people, kept only where they decide something the rules above do not.

- **Taleb** — antifragile: an outage of one model, one vendor or one host degrades, never stops.
- **Deutsch** — conjectures and refutations: a claim is kept until a test kills it, not until it
  feels settled.
- **Karpathy** — compile knowledge once into a wiki; do not re-retrieve the same sources each session.
- **Chollet** — generalisation is the score; a benchmark the work was tuned on proves nothing.
