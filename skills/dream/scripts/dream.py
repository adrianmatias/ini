"""The wiki's dream loop: sample unlinked page pairs, ground candidate links, feed verdicts back.

usage (from the repo root, or pass --root PATH):
  python skills/dream/scripts/dream.py pairs --n 24 --lanes 4 [--seed N]
  python skills/dream/scripts/dream.py check CANDIDATES.json
  python skills/dream/scripts/dream.py feed VERDICTS.json --date YYYY-MM-DD

A dream adds a link between two sourced claims, never an unverified fact. A kept dream becomes a
conjecture in `wiki/conjectures.md` and one line under `## Dream links` on both pages. Every pair,
kept or killed, goes to `wiki/dreams/pairs.tsv` so it is never sampled again.
"""

import argparse
import datetime
import json
import random
import re
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Self

from pydantic import BaseModel, ConfigDict, model_validator

SECTION = "## Dream links"
WIKILINK = re.compile(r"\[\[([^\]|#\\]+)(?:#[^\]|]*)?(?:\\?\|([^\]]*))?\]\]")
MDLINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
PROVENANCE = re.compile(r"\^\[[^\]]*\]")
NOISE = re.compile(r"[*_`\"'\u201c\u201d\u2018\u2019\u2026\u00ab\u00bb]|\.\.\.")


class Decision(StrEnum):
    """Whether a candidate pair survived cross-family judging."""

    KEPT = "kept"
    KILLED = "killed"


class Rules(BaseModel):
    """Which pages dream: the steering, ledger and index pages stay out, and so do stubs."""

    model_config = ConfigDict(frozen=True, use_attribute_docstrings=True)

    out_of_pool: frozenset[str] = frozenset({"index", "SCHEMA", "learnings", "conjectures"})
    """Root wiki pages excluded from random pairing."""
    out_of_tree: frozenset[str] = frozenset({"dreams", "sources", "_archive"})
    """Wiki subdirectories excluded from random pairing."""
    min_bytes: int = 2000
    """Minimum page byte size eligible for pairing."""
    max_uses: int = 3
    """Maximum times one page may appear in a single night's sample."""
    min_quote: int = 20
    """Minimum normalized character length for a verbatim grounding quote."""


RULES = Rules()


class Pair(BaseModel):
    """One sampled pair of unlinked wiki pages."""

    model_config = ConfigDict(frozen=True, use_attribute_docstrings=True)

    id: str
    """Sampled pair identifier (e.g. `p01`)."""
    a: str
    """First page key relative to `wiki/` without `.md`."""
    b: str
    """Second page key relative to `wiki/` without `.md`."""


class Candidate(BaseModel):
    """A generator's proposed link: non-`none` candidates require verbatim quotes in both pages."""

    model_config = ConfigDict(frozen=True, use_attribute_docstrings=True)

    id: str
    """Sampled pair identifier (e.g. `p01`)."""
    a: str
    """First page key relative to `wiki/` without `.md`."""
    b: str
    """Second page key relative to `wiki/` without `.md`."""
    kind: str = ""
    """Candidate relation kind (`transfer`, `pattern`, `contradiction`, `story`, `gap`, `none`)."""
    quote_a: str = ""
    """Verbatim quote supporting the claim in page `a`."""
    quote_b: str = ""
    """Verbatim quote supporting the claim in page `b`."""


class Verdict(BaseModel):
    """The judge's call on one sampled pair; a `kept` verdict requires a non-empty `claim`."""

    model_config = ConfigDict(frozen=True, use_attribute_docstrings=True)

    a: str
    """First page key relative to `wiki/` without `.md`."""
    b: str
    """Second page key relative to `wiki/` without `.md`."""
    verdict: Decision
    """Judge decision: `kept` or `killed`."""
    note: str
    """One-line reason recorded in the pair ledger."""
    claim: str = ""
    """One-line claim appended under `## Dream links` on both pages when kept."""
    conjecture: str = ""
    """Conjecture id on `wiki/conjectures.md` (e.g. `c12`) when kept."""

    @model_validator(mode="after")
    def kept_requires_claim(self) -> Self:
        """Refuse a kept verdict that carries no claim to attach to both pages."""
        if self.verdict == Decision.KEPT and not self.claim.strip():
            raise ValueError("a kept verdict requires a non-empty claim")
        return self


def normalized(text: str) -> str:
    """Text as a quote check compares it: links unwrapped, provenance and noise dropped."""
    text = PROVENANCE.sub("", text)
    text = WIKILINK.sub(lambda m: m.group(2) or m.group(1).split("/")[-1], text)
    text = MDLINK.sub(lambda m: m.group(1), text)
    return re.sub(r"\s+", " ", NOISE.sub("", text)).strip().lower()


def links_to(text: str, target: str) -> bool:
    """Whether `text` contains a wikilink or markdown link pointing to `target`."""
    stem = target.split("/")[-1]
    wiki_refs = {ref.strip().removesuffix(".md") for ref, _ in WIKILINK.findall(text)}
    md_refs = {
        url.split("#")[0].strip().removesuffix(".md")
        for _, url in MDLINK.findall(text)
        if url.split("#")[0].endswith(".md")
    }
    return any(ref == target if "/" in ref else ref == stem for ref in wiki_refs | md_refs)


@dataclass
class Wiki:
    """The dreamable pages, keyed by their path under `wiki/` without `.md`."""

    pages: dict[str, Path] = field(default_factory=dict)

    @classmethod
    def load(cls, root: Path, min_bytes: int = RULES.min_bytes) -> Wiki:
        """Every page big enough to hold a claim, outside the steering and ledger pages."""
        wiki_dir = root / "wiki"
        if not wiki_dir.is_dir():
            return cls({})
        pages: dict[str, Path] = {}
        for path in sorted(wiki_dir.rglob("*.md")):
            key = path.relative_to(wiki_dir).as_posix()[:-3]
            if key in RULES.out_of_pool or key.split("/")[0] in RULES.out_of_tree:
                continue
            if path.stat().st_size >= min_bytes:
                pages[key] = path
        return cls(pages)

    def text(self, key: str) -> str:
        """One page's UTF-8 text."""
        return self.pages[key].read_text(encoding="utf-8")

    def linked(self, a: str, b: str) -> bool:
        """Whether either page links the other (self-links in `a` or `b` ignored)."""
        return links_to(self.text(a), b) or links_to(self.text(b), a)

    def grounded(self, key: str, quote: str) -> bool:
        """A quote long enough to mean something, found verbatim in its page."""
        q = normalized(quote)
        return key in self.pages and len(q) >= RULES.min_quote and q in normalized(self.text(key))

    def attach(self, here: str, there: str, line: str, date: str) -> bool:
        """Insert one dream line inside `## Dream links`; idempotent per target page."""
        text = self.text(here).rstrip("\n")
        if SECTION in text:
            head, _, tail = text.partition(SECTION)
            body, sep, rest = tail.partition("\n## ")
            if f"[[{there}]] —" in body:
                return False
            new_body = body.rstrip("\n") + f"\n{line}\n"
            text = f"{head}{SECTION}{new_body}" + (f"\n## {rest}" if sep else "")
        else:
            text += (
                f"\n\n{SECTION}\n\nConjectures, not record: each joins two sourced claims."
                f"\n{line}\n"
            )
        updated = re.sub(r"^updated:.*$", f"updated: {date}", text, count=1, flags=re.M)
        self.pages[here].write_text(updated.rstrip("\n") + "\n", encoding="utf-8")
        return True


class Ledger:
    """`wiki/dreams/pairs.tsv`: every pair ever judged, so a pair dreams once."""

    HEADER = "date\ta\tb\tverdict\tnote\n"

    @staticmethod
    def seen(ledger: Path) -> set[frozenset[str]]:
        """The pairs already judged."""
        if not ledger.is_file():
            return set()
        rows = ledger.read_text(encoding="utf-8").splitlines()[1:]
        return {frozenset(r.split("\t")[1:3]) for r in rows if r.strip()}

    @classmethod
    def append(cls, ledger: Path, date: str, verdicts: list[Verdict]) -> None:
        """Append unseen verdicts idempotently; write the header once."""
        known = cls.seen(ledger)
        rows: list[str] = []
        for v in verdicts:
            pair = frozenset((v.a, v.b))
            if pair in known:
                continue
            known.add(pair)
            rows.append("\t".join((date, v.a, v.b, v.verdict.value, v.note.replace("\t", " "))))
        if not rows and ledger.is_file():
            return
        ledger.parent.mkdir(parents=True, exist_ok=True)
        needs_header = not ledger.is_file() or ledger.stat().st_size == 0
        head = cls.HEADER if needs_header else ""
        with ledger.open("a", encoding="utf-8") as out:
            out.write(head + ("\n".join(rows) + "\n" if rows else ""))


@dataclass
class Night:
    """One night of the loop over the current wiki."""

    wiki: Wiki

    def pairs(self, seen: set[frozenset[str]], n: int, lanes: int, seed: int) -> list[list[Pair]]:
        """Random unlinked pairs never judged before, each page in at most `max_uses` pairs."""
        keys = sorted(self.wiki.pages)
        if len(keys) < 2 or n <= 0 or lanes <= 0:
            return [[] for _ in range(max(lanes, 1))]
        rng, taken, uses, out = random.Random(seed), set(seen), {}, []
        for _ in range(200 * n):
            if len(out) == n:
                break
            a, b = rng.sample(keys, 2)
            pair = frozenset((a, b))
            if pair in taken or self.wiki.linked(a, b):
                continue
            if max(uses.get(a, 0), uses.get(b, 0)) >= RULES.max_uses:
                continue
            taken.add(pair)
            uses[a], uses[b] = uses.get(a, 0) + 1, uses.get(b, 0) + 1
            out.append(Pair(id=f"p{len(out) + 1:02d}", a=a, b=b))
        return [out[i::lanes] for i in range(lanes)]

    def check(self, candidates: list[Candidate]) -> int:
        """Verify quotes on non-`none` candidates; return the count of failed candidates."""
        bad = 0
        for c in candidates:
            if c.kind.lower() == "none":
                print(f"{'skip':8} {c.id}  {c.a} x {c.b}")
                continue
            missing = [
                side
                for side, key, quote in (("a", c.a, c.quote_a), ("b", c.b, c.quote_b))
                if not self.wiki.grounded(key, quote)
            ]
            bad += bool(missing)
            status = "FAIL " + "+".join(missing) if missing else "ok"
            print(f"{status:8} {c.id}  {c.a} x {c.b}")
        print(f"{bad} ungrounded")
        return bad

    def feed(self, verdicts: list[Verdict], ledger: Path, date: str) -> int:
        """Ledger rows for unseen verdicts, and one dream line on both pages of each kept pair."""
        fed = 0
        for v in (item for item in verdicts if item.verdict == Decision.KEPT):
            ref = f"[[conjectures]] {v.conjecture}" if v.conjecture else f"dream-{date}"
            for here, there in ((v.a, v.b), (v.b, v.a)):
                if here in self.wiki.pages:
                    line = f"- [[{there}]] — {v.claim} ({ref})"
                    fed += self.wiki.attach(here, there, line, date)
        Ledger.append(ledger, date, verdicts)
        return fed


def arguments() -> argparse.Namespace:
    """Parse the three verbs of a dream night."""
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--root", type=Path, default=Path("."), help="Repository root.")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sp = sub.add_parser("pairs", parents=[common])
    sp.add_argument("--n", type=int, default=24)
    sp.add_argument("--lanes", type=int, default=4)
    sp.add_argument("--seed", type=int, default=int(datetime.date.today().strftime("%Y%m%d")))
    sp.add_argument("--min-bytes", type=int, default=RULES.min_bytes)
    sc = sub.add_parser("check", parents=[common])
    sc.add_argument("file", type=Path)
    sc.add_argument("--min-bytes", type=int, default=RULES.min_bytes)
    sf = sub.add_parser("feed", parents=[common])
    sf.add_argument("file", type=Path)
    sf.add_argument("--date", default=datetime.date.today().isoformat())
    sf.add_argument("--min-bytes", type=int, default=RULES.min_bytes)
    return ap.parse_args()


if __name__ == "__main__":
    args = arguments()
    night = Night(Wiki.load(args.root, min_bytes=args.min_bytes))
    ledger_path = args.root / "wiki" / "dreams" / "pairs.tsv"
    if args.cmd == "pairs":
        lanes = night.pairs(Ledger.seen(ledger_path), args.n, args.lanes, args.seed)
        print(json.dumps([[p.model_dump() for p in lane] for lane in lanes], indent=1))
    elif args.cmd == "check":
        rows = json.loads(args.file.read_text(encoding="utf-8"))
        raise SystemExit(1 if night.check([Candidate.model_validate(r) for r in rows]) else 0)
    else:
        rows = json.loads(args.file.read_text(encoding="utf-8"))
        fed = night.feed([Verdict.model_validate(r) for r in rows], ledger_path, args.date)
        print(f"pages fed {fed}")
