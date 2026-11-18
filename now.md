# now

What is true today; rewritten every round.

## state

- 2026-11-18: ini 0.2.0 is a repository of knowledge in the shape of a fresh repository, not an
  installable package. `base/` holds the inherited knowledge; `ci/` holds the harness (13 gates,
  ratchet, ontology), run from the tree with `uv run python -m ci`; the kickoff's templates hold
  the placeholder anchors and the walking skeleton. Committed and pushed; the repository is still
  private.
- Proved: 12 behaviour tests, gates 13/13, `--prove` 13/13. End to end outside the suite: a copy,
  started by the kickoff's mechanical steps, with its own `uv sync`, was 13/13 and its run script
  ran.
- Inheritance is an agent's job: harvest *down*, in two steps (harness, then compliance).
- No project, client or employer names anywhere in the repository, logs included.

## next

1. Permeate an ongoing project (harvest *down*, step 1), then a second one with an older runtime.
2. Open: the harness code needs Python 3.14; a project whose runtime is older runs the gates under
   3.14 only if its code imports there.
3. Make the repository public when the director decides.
