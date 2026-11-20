---
name: dream
description: Use when logs outpace docs or wiki. Replay, pair, judge.
---

# dream

Consolidation sleep for the repository: **replay** brings anchors, learnings and conjectures up to
the logs; **daydream** pairs unlinked artifacts across time or pages to catch silent breaks, stale
thresholds and missing links; **compress** folds what survived and drops dead weight.

## the rule that protects the record

**A dream adds a link or a conjecture, never an unverified fact.** Every kept link joins two
existing claims with verbatim quotes. Never invent a number into a ledger, never rewrite `log/`,
and never edit frozen evidence.

## 1 · replay (logs since last consolidation)

1. Find the last consolidation (`wiki/dreams/dream-*.md`, or the last `log/agt.md` round that ran
   it). Compare every newer `log/` entry against `now.md`, `README.md`, `foundation.md`, `domain.md`,
   `code-standard.md`, `wiki/learnings.md` and `wiki/conjectures.md`.
2. Fix stale status lines, tier contradictions and renamed module/file paths in place.
3. Fold costly new failure classes into `wiki/learnings.md` (budget 160 lines; rank and prune
   before adding).
4. Update (or create) `wiki/conjectures.md` (`id | claim | falsifier | status`): promote verified
   claims, mark refuted ones destroyed with dated evidence, and register every open strategic or
   architecture bet with what would refute it.
5. **Replay finishes before daydream starts.** A link judged against a stale page is judged wrong.

## 2 · daydream (cross-family)

1. **Sample.** Pick 15–25 unlinked pairs in `$TMPDIR` (keep helper scripts out of `wiki/` so the
   `shape` gate stays green). In a wiki-heavy repo, sample unlinked pages ≥ 2 kB; in a code repo,
   pair recent updates (`now.md`, plans, code) against older anchors, baselines and skills. Skip
   pairs already recorded in `wiki/dreams/pairs.tsv`.
2. **Generate** — read-only lane(s) in a **different model family** from the judge (`skills/delegate`),
   returning `output_schema` fields `id, a, b, kind, link, mechanism, quote_a, quote_b, use`
   (`kind`: `transfer | pattern | contradiction | story | gap | none`) and writing the full JSON to
   `$TMPDIR` so transcripts do not truncate. Tell generators that `none` is expected for most pairs
   and quotes must be verbatim (≥ 20 chars).
3. **Ground.** Verify every `quote_a` and `quote_b` verbatim against disk with a scratch script. A
   failed quote kills the candidate immediately — no repair, no benefit of the doubt.
4. **Judge** — the session, from a different family than the generator. Keep only if all four hold
   after reading lines around both quotes:
   - *true*: the mechanism survives reading the context in both files (narrow if only part holds);
   - *new*: not already stated or settled (grep the key noun first);
   - *useful*: changes a concrete file, threshold, gate, conjecture or next move today;
   - *not a topic match*: would not hold for any two files sharing a tag.
   Kill rejected candidates with a one-line reason. Expect roughly one keep in six to ten.
5. **Feed back.** Append every sampled pair (`kept` or `killed`) to `wiki/dreams/pairs.tsv` once per
   night (a missing verdict gets resampled), write `wiki/dreams/dream-YYYY-MM-DD.md` (replay summary,
   kept dreams with quotes and use, kills by reason), add kept conjectures to `wiki/conjectures.md`
   (and `## Dream links` on wiki pages if used), and apply verified fixes to code, docs or `now.md`.

## 3 · close

Run `skills/compress`, `uv run python -m ci domain --write` (if package code changed), `uv run
python -m ci gates` and `--prove`, rewrite `now.md`, and append the round to `log/agt.md`.
