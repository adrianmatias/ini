"""Behaviour of bundled skill scripts: AST call-site rewrite."""

import ast
import importlib.util

import pytest

from ci.tests.conftest import ROOT

SCRIPT = ROOT / "skills/restructure/scripts/sweep_callsites.py"


def load_sweep():
    spec = importlib.util.spec_from_file_location("sweep_callsites", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_sweep_callsites_handles_multiple_imports_and_refuses_local(tmp_path) -> None:
    mod = load_sweep()
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
