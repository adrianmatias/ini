"""Behaviour of bundled skill scripts: AST call-site rewrite and dream loop."""

import ast
import importlib.util
import json
import subprocess
import sys

import pytest
from pydantic import ValidationError

from ci.tests.conftest import ROOT

SWEEP_SCRIPT = ROOT / "skills/restructure/scripts/sweep_callsites.py"
DREAM_SCRIPT = ROOT / "skills/dream/scripts/dream.py"


def load_module(path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_sweep_callsites_handles_multiple_imports_and_refuses_local(tmp_path) -> None:
    mod = load_module(SWEEP_SCRIPT, "sweep_callsites")
    spec = mod.Spec(
        module="pkg.doc",
        receiver={"read_text": ["Document", "read_text"], "write_text": ["Document", "write_text"]},
    )
    caller = tmp_path / "caller.py"
    caller.write_text(
        "from pkg.doc import read_text\n"
        "from pkg.doc import write_text\n\n"
        "x = read_text(p)\n"
        "write_text(p, x)\n"
    )
    assert mod.Source(caller, spec).sweep() is True
    rewritten = caller.read_text()
    ast.parse(rewritten)
    assert "from pkg.doc import Document\n\n" in rewritten
    assert "Document(p).read_text()" in rewritten
    assert "Document(p).write_text(x)" in rewritten

    local = tmp_path / "local.py"
    local.write_text("def f() -> None:\n    from pkg.doc import read_text\n    read_text(p)\n")
    with pytest.raises(SystemExit, match="local import"):
        mod.Source(local, spec)


def test_dream_pairs_respects_self_links_paths_and_skips_none(tmp_path, capsys) -> None:
    mod = load_module(DREAM_SCRIPT, "dream")
    wiki = tmp_path / "wiki"
    (wiki / "x").mkdir(parents=True)
    (wiki / "y").mkdir(parents=True)
    pad = " " + ("padding sentence for minimum byte threshold. " * 50)
    (wiki / "conjectures.md").write_text("# conjectures\n" + pad)
    (wiki / "alpha.md").write_text(
        "Claim about [[alpha#self]] and [[other|aliases]] with provenance^[log/mat.md:1] "
        "and [[x/note]].\n" + pad
    )
    (wiki / "x/note.md").write_text("X note linked from alpha.\n" + pad)
    (wiki / "y/note.md").write_text("Y note unlinked from alpha.\n" + pad)

    loaded = mod.Wiki.load(tmp_path)
    assert sorted(loaded.pages) == ["alpha", "x/note", "y/note"]
    night = mod.Night(loaded)
    lanes = night.pairs(set(), n=10, lanes=2, seed=20261123)
    sampled = {frozenset((p.a, p.b)) for lane in lanes for p in lane}
    assert sampled == {frozenset(("alpha", "y/note")), frozenset(("x/note", "y/note"))}

    good = mod.Candidate(
        id="p01",
        a="alpha",
        b="y/note",
        kind="gap",
        quote_a="Claim about alpha and aliases with provenance",
        quote_b="Y note unlinked from alpha.",
    )
    none_row = mod.Candidate.model_validate({"id": "p02", "a": "x/note", "b": "y/note", "kind": "none"})
    bad = mod.Candidate(id="p03", a="alpha", b="y/note", quote_a="short", quote_b="missing quote")
    assert night.check([good, none_row]) == 0
    assert night.check([bad]) == 1
    capsys.readouterr()


def test_dream_feeds_idempotently_and_validates_verdicts(tmp_path) -> None:
    mod = load_module(DREAM_SCRIPT, "dream")
    wiki = tmp_path / "wiki"
    wiki.mkdir()
    pad = " " + ("padding sentence for minimum byte threshold. " * 50)
    (wiki / "alpha.md").write_text(
        "---\nupdated: 2026-11-01\n---\nBody.\n\n## Dream links\n\n- existing\n\n## Sources\n\n- s\n"
        + pad
    )
    (wiki / "beta.md").write_text("---\nupdated: 2026-11-01\n---\nBeta body.\n" + pad)
    (wiki / "gamma.md").write_text("Gamma body.\n" + pad)

    with pytest.raises(ValidationError):
        mod.Verdict(a="alpha", b="beta", verdict="keep", note="typo", claim="x")
    with pytest.raises(ValidationError):
        mod.Verdict(a="alpha", b="beta", verdict="kept", note="empty claim", claim="")

    night = mod.Night(mod.Wiki.load(tmp_path))
    ledger = wiki / "dreams/pairs.tsv"
    verdicts = [
        mod.Verdict(
            a="alpha",
            b="beta",
            verdict=mod.Decision.KEPT,
            note="kept",
            claim="Alpha and beta share a boundary.",
            conjecture="c1",
        ),
        mod.Verdict(a="beta", b="gamma", verdict=mod.Decision.KILLED, note="topic match"),
    ]
    assert night.feed(verdicts, ledger, "2026-11-23") == 2
    assert night.feed(verdicts, ledger, "2026-11-23") == 0
    alpha_text = (wiki / "alpha.md").read_text()
    dream_sec = alpha_text.split("## Dream links")[1].split("## Sources")[0]
    assert "[[beta]] — Alpha and beta share a boundary. ([[conjectures]] c1)" in dream_sec
    assert "updated: 2026-11-23" in alpha_text
    assert len(ledger.read_text().splitlines()) == 3

    cli = subprocess.run(
        [sys.executable, str(DREAM_SCRIPT), "pairs", "--root", str(tmp_path), "--n", "4"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert len(json.loads(cli.stdout)) == 4
