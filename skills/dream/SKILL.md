---
name: dream
description: Use when logs outpace docs or wiki, or conjectures stall. Replay, pair, judge.
---

# dream

Consolidation sleep for the repository: **replay** brings anchors, learnings and conjectures up to
the logs; **daydream** pairs unlinked artifacts across time or pages to catch silent breaks, stale
thresholds and missing links; **compress** folds what survived and drops dead weight.

Tool: `skills/dream/scripts/dream.py` (`pairs`, `check`, `feed`). Ledger: `wiki/dreams/pairs.tsv`.

## the rule that protects the record

**A dream adds a link or a conjecture, never an unverified fact.** Every kept link joins two
existing claims with verbatim quotes. Never invent a number into a ledger, never rewrite `log/`,
and never edit frozen evidence. A conjecture not on `wiki/conjectures.md` is a vibe.

## 1 · replay (logs since last consolidation)

1. Find the last consolidation (`wiki/dreams/dream-*.md`, or the last `log/agt.md` round that ran
   it). Compare every newer `log/` entry against `now.md`, `README.md`, `foundation.md`, `domain.md`,
   `code-standard.md`, `wiki/learnings.md` and `wiki/conjectures.md`.
2. Fix stale status lines, tier contradictions and renamed module/file paths in place.
3. Fold costly new failure classes into `wiki/learnings.md` (budget 160 lines; rank and prune
   before adding).
4. Update `wiki/conjectures.md` (`open`, `promoted`, `destroyed`; keep permanent ids): promote
   verified claims with evidence, move refuted ones to `destroyed` with dated evidence, and
   register new open bets with hard-to-vary claims and falsifiers.
5. **Replay finishes before daydream starts.** A link judged against a stale page is judged wrong.

## 2 · daydream (cross-family)

1. **Sample.** In a wiki-backed repo, run `uv run python skills/dream/scripts/dream.py pairs --n 24
   --lanes 4 > $TMPDIR/pairs.json` (skips steering/ledger pages, stubs `< 2 kB`, linked pairs and
   pairs in `wiki/dreams/pairs.tsv`). In a code-only repo, sample 15–25 unlinked pairs between
   recent updates (`now.md`, plans, code) and older anchors, baselines and skills in `$TMPDIR`.
2. **Generate** — read-only lane(s) in a **different model family** from the judge (`skills/delegate`),
   returning `output_schema` fields `id, a, b, kind, link, mechanism, quote_a, quote_b, use`
   (`kind`: `transfer | pattern | contradiction | story | gap | none`) and writing the full JSON to
   `$TMPDIR` so transcripts do not truncate. Tell generators that `none` is expected for most pairs
   and quotes must be verbatim (≥ 20 chars).
3. **Ground.** Run `uv run python skills/dream/scripts/dream.py check $TMPDIR/candidates.json`
   (skips `kind: "none"` rows automatically; in a code-only repo, match verbatim against disk). A
   failed quote kills the candidate immediately — no repair, no benefit of the doubt.
4. **Judge** — the session, from a different family than the generator. Keep only if all four hold
   after reading lines around both quotes:
   - *true*: the mechanism survives reading the context in both files (narrow if only part holds);
   - *new*: not already stated or settled (grep the key noun in both pages and `wiki/conjectures.md`);
   - *useful*: changes a concrete file, threshold, gate, conjecture or next move today;
   - *not a topic match*: hard to vary — would not hold for any two files sharing a tag.
   Kill rejected candidates with a one-line reason. Expect roughly one keep in six to ten.
5. **Feed back.** Put every verdict (`a, b, verdict, note, claim, conjecture`) in one JSON list
   covering all sampled pairs, assign the next `cNN` id with a falsifier on `wiki/conjectures.md`,
   and run `uv run python skills/dream/scripts/dream.py feed $TMPDIR/verdicts.json --date
   YYYY-MM-DD` (idempotent on both `pairs.tsv` and `## Dream links`). Write
   `wiki/dreams/dream-YYYY-MM-DD.md` (replay summary, kept dreams with quotes/use/`cNN`, kills by
   reason) and apply verified fixes to code, docs or `now.md`.

## 3 · close

Run `skills/compress`, `uv run python -m ci domain --write` (if package code changed), `uv run
python -m ci gates` and `--prove`, rewrite `now.md`, and append the round to `log/agt.md`.
