"""Behaviour of the gates on a started copy: verdicts, proofs and the ratchet."""

from pathlib import Path

import pytest

from ci.cli.main import main
from ci.core.errors import IniError
from ci.core.project import Project
from ci.core.tool import Tool

CASCADE = "".join(f"    if x == {i}:\n        return {i}\n" for i in range(7))
DEBT = f'"""Debt."""\n\n\ndef cascade(x: int) -> int:\n{CASCADE}    return -1\n'


def gates(root: Path, *args: str) -> int:
    return main(["gates", "--root", str(root), *args])


def test_a_new_project_is_red_only_until_its_objective_is_stated(project, capsys) -> None:
    assert gates(project) == 1
    out = capsys.readouterr().out
    assert "green: 12/13" in out
    assert "not green: harness" in out
    assert out.count(" kickoff ") == 7
    for page in project.glob("*.md"):
        page.write_text(page.read_text().replace("TODO(kickoff)", "stated"))
    assert gates(project) == 0


def test_every_gate_rejects_its_witness(kicked_off, capsys) -> None:
    assert gates(kicked_off, "--prove") == 0
    assert "proofs passed: 13/13" in capsys.readouterr().out
    assert not list(kicked_off.rglob("ini_witness*.py")), "a witness leaked into the real tree"


def test_the_ratchet_holds_debt_and_only_shrinks(kicked_off, capsys) -> None:
    debt = kicked_off / "src/demo/debt.py"
    debt.write_text(DEBT)
    assert gates(kicked_off, "--only", "complexity") == 1
    assert gates(kicked_off, "--only", "complexity", "--adopt") == 0
    (kicked_off / "src/demo/more.py").write_text(DEBT)
    assert gates(kicked_off, "--only", "complexity") == 1, "new debt is red"
    for path in (debt, kicked_off / "src/demo/more.py"):
        path.unlink()
    assert gates(kicked_off, "--only", "complexity") == 1, "a stale record is red"
    assert gates(kicked_off, "--only", "complexity", "--record") == 0
    assert "complexity" not in (kicked_off / "ci/ceilings.json").read_text()
    assert "ratchet-stale" in capsys.readouterr().out


@pytest.mark.parametrize(
    ("source", "rule"),
    [
        ('"""Run layer leak."""\n\nimport sys\n\nARGS = sys.argv\n', "run-layer"),
        ('"""Path edit."""\n\nimport sys\n\nsys.path.insert(0, ".")\n', "sys-path"),
        ("".join(f"def f{i}() -> None:\n    pass\n\n\n" for i in range(7)), "pile"),
    ],
)
def test_shape_refuses_what_a_pile_of_functions_needs(kicked_off, capsys, source, rule) -> None:
    (kicked_off / "src/demo/core/leak.py").write_text(source)
    assert gates(kicked_off, "--only", "shape") == 1
    assert f" {rule} " in capsys.readouterr().out


def test_a_missing_tool_is_a_refusal_not_a_clean_verdict(kicked_off) -> None:
    with pytest.raises(IniError, match="not installed"):
        Tool(Project.load(kicked_off)).run("ini_absent_tool")


UNITTEST = '''"""A unittest suite kept inside the package."""

import unittest


class TestNested(unittest.TestCase):
    def test_runs(self) -> None:
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
'''


def test_a_package_main_is_run_layer(kicked_off) -> None:
    main_module = '"""Run the package."""\n\nif __name__ == "__main__":\n    print("run")\n'
    (kicked_off / "src/demo/__main__.py").write_text(main_module)
    assert gates(kicked_off, "--only", "shape") == 0


def test_tests_inside_the_package_are_judged_as_tests(kicked_off, capsys) -> None:
    nested = kicked_off / "src/demo/tests"
    (kicked_off / "tests").rename(nested)
    (nested / "__init__.py").write_text('"""The behaviour suite."""\n')
    (nested / "test_nested.py").write_text(UNITTEST)
    pyproject = kicked_off / "pyproject.toml"
    pyproject.write_text(
        pyproject.read_text().replace('tests = "tests"', 'tests = "src/demo/tests"')
    )
    for gate in ("docs", "annotations", "shape", "deadcode", "duplication", "domain"):
        assert gates(kicked_off, "--only", gate) == 0, capsys.readouterr().out


def test_an_unknown_gate_is_refused(kicked_off) -> None:
    with pytest.raises(SystemExit):
        gates(kicked_off, "--only", "style")
