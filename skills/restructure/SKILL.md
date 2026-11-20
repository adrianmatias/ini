---
name: restructure
description: Use when reshaping code without changing behaviour. Pins first, slices, lanes, merge.
---

# restructure

A refactor at repository scale: nothing a user or an operator sees may change. The proof comes
before anything moves.

## the proof

1. **Baseline**: `uv run python -m ci gates` green on the starting commit.
2. **The pins are the contract**: artifact digests in the suite, committed generated files, each
   command's stdout and exit code. A slice is done when all of them are unchanged — or a pin moved
   for a reason written next to it (a path inside a message is a reason; a different number is a
   defect).
3. **Every entry point something outside the suite runs** (deploy scripts, a worker, the commands
   in `AGENTS.md` and in skills) is driven by a test through its run script. A move once deleted a
   deployed build step while every gate stayed green, because the worker's tests faked the
   subprocess.

## one slice (a module becomes a component)

1. Name the class from `domain.md`; its methods are the workflow, not its helpers.
2. Move the workflow in, keeping every message and refusal word for word.
3. The run script `cli/<verb>.py` owns argument parsing and calls one method.
4. Update callers, tests (drive `main` or the public method) and every doc that names the entry.
5. Prove: stdout and exit codes identical, gates green, pins unchanged. One revertible commit.

## a mechanical sweep (renames, moves)

Write the script, do not hand-edit: a mapping table, `git mv`, rewrites for every form a name takes
(`from pkg import x`, dotted `pkg.x.attr`, the string `"pkg.x"` of a `-m` target, file paths in
prose). Let the suite list what the script missed; fix the class, not the instance. Re-pin digests
only after proving only path strings moved (map the new spelling back; the old digest returns).

Moving free functions onto a class (`read_text(p)` → `Document(p).read_text()`) is an AST rewrite,
not a regex: `skills/restructure/scripts/sweep_callsites.py` rewrites calls and imports by byte
offset and refuses shadowing locals for hand editing.

## parallel lanes

- **Cut along the import graph as it is**: read it from `domain.md`'s rendered block. A wave is one
  layer of it, leaves first; two packages that import each other are one lane.
- **Dump debt per package first**: when findings exceed the CLI summary, read `ci.gates.table.GATES`
  with `ci.gates.session.Session` before fanning out.
- **A lane owns a package**, its run scripts and its behaviour file — never another lane's call
  sites; it reports the edit it needed. List any symbols cross-component tests import from each
  package so lanes keep them importable.
- **Decide cross-cutting things and reshape shared kernel APIs on the base first**: a rule change, a
  dependency (`uv add`), a convention, or an API every package imports.
- **One worktree per lane** from the committed base; the lane commits there.
- **Package lanes only compress inside packages.** With cross-package APIs frozen, each lane finds
  its best move outside its boundary. The redundancy left is a concept restated across packages
  (status strings, ids, count dicts, file I/O): give each concept one home in `core/` and run one
  lane per concept across all packages. Make string concepts `StrEnum`s: they compare and serialise
  as the old strings, so adoption is incremental.
- **Tell the lane what to do when the data is wrong**: leave it failing and report the ids and the
  false statement; the data decision is the integrator's.

## merge

- **Merge on a clean tree**: commit or stash the director's uncommitted notes first — a botched
  merge is undone with `git reset --hard`, which destroys them.
- One lane at a time, `--no-ff`; every gate on each merge, `--prove` on the result. Spot-check
  merged lanes for `@staticmethod` piles or file-splitting meant only to pass `pile`.
- **Auto-resolve only top-level `import`/`from` conflicts** (`ruff check --fix --select I`), and
  audit with `git show --remerge-diff`; resolve indented code by hand. When lane A renamed a call
  inside code lane B restructured, keep B's structure, replay A's diff, and let `types` find any
  missed call sites.
- Ratchet conflicts take every lane's lowered entry; `uv.lock` is regenerated with `uv lock`.
- **Expect red from the merged toolchain**, not from the code: a lane that changed shared config
  makes other lanes' code fail rules they never ran under. Fix on the merge commit.
- **`git mv` carries only tracked files**: ignored or untracked directories stay at the old path, so
  use `rsync -a` + `rm -rf` when moving data or state trees.
- Clean up: `git worktree remove`, delete merged branches, `git worktree prune`.
