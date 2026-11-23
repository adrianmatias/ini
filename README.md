# ini

A live cookiecutter for AI agents: a repository of knowledge in the shape of a fresh repository.

Its objective is to distil current and future learnings and best practices into something ongoing
and new projects inherit: the principles, the code standard, the lessons, the skills, and thirteen
deterministic gates that hold agent-written Python to them, each gate proven able to fail. A
project shaped by them starts with an LLM carrying its steps and moves those steps, round by round,
into deterministic code: a piece of engineering, not a thin wrapper around a model.

Nothing is installed and nothing is linked. A new project is a copy of this repository. In an
ongoing project, an agent reads ini and writes what the project needs into it, in the project's own
terms. Either way the project owns what it took, keeps no tie back, and would stay green if ini
vanished.

Shared knowledge usually ends up as copies that drift or as a dependency that couples every project
to one source. ini picks deliberate redundancy and leaves the refresh to an agent.

## start a project

```
git clone --depth 1 https://github.com/adrianmatias/ini my-project
cd my-project && rm -rf .git && git init && uv sync
```

Then ask your agent to run the kickoff (`skills/kickoff`). It replaces ini's own anchors, logs
and suite with the templates, names the package, points `[tool.ini]` at it, and asks you for the
objective. `uv run python -m ci gates` stays red until the objective states a target someone else
can check.

## bring ini into an ongoing project

Point an agent at ini and at the project, and ask for the harvest skill (`skills/harvest`,
*down*). It works in two steps:

1. **Harness**: `ci/`; the knowledge merged into the project's own foundation, code standard,
   learnings and skills; a `[tool.ini]` table that fits the project's layout; the gate tools in its
   dev group; the skill rows in its `AGENTS.md`; and `python -m ci gates --adopt` to record
   today's debt.
2. **Compliance**: round by round the debt in `ci/ceilings.json` goes down, until it is empty.

The agent takes what fits and adapts it: a flat layout, a suite inside the package and a
`__main__.py` entry point are all supported. A project keeps its Python, its tools and its history.

## what is here

| path | what | in a copy |
|---|---|---|
| `foundation.md`, `code-standard.md`, `wiki/learnings.md`, `skills/` | the knowledge: principles, rules, lessons, eight skills | kept, and owned by the project |
| `skills/kickoff/templates/` | the anchors with kickoff placeholders, starter `wiki/conjectures.md`, and the walking skeleton | rendered by the kickoff |
| `ci/` | the gates, the ratchet and the ontology renderer, run with `uv run python -m ci` | kept, as the project's own harness |
| `.githooks/pre-push` | blocks pushes to `main` when gates are red (`git config core.hooksPath .githooks`) | kept, opt-in per clone |
| `pyproject.toml` | the starter: Python ≥ 3.14, pydantic, the gate toolchain in the dev group | renamed; then the project's |
| `objective.md`, `now.md`, `domain.md`, `AGENTS.md`, `wiki/conjectures.md`, `log/` | ini's own anchors and bets | replaced by the templates |

The steering ladder every project shares:
`objective > foundation > domain > code-standard > gates and behaviour tests > implementation`.

## the gates

`uv run python -m ci gates` runs them; red blocks the change. `--prove` copies the project's gate
inputs to a scratch directory and links the rest, so a suite that reads data runs there as in the
tree. It plants one defect per gate in that directory and fails if any gate lets its
defect through. `--adopt` records an existing project's debt once; from then on `ci/ceilings.json`
only shrinks (`--record` lowers it after a fix; a record above what the gate measures is red).

| gate | catches | tool |
|---|---|---|
| lint | defects, relative imports, globals, data clumps, layout | ruff, ruff format |
| docs | a module, package or class that does not say what it is; commented-out code | ruff D, ERA |
| annotations | an unstated contract, `Any` in a signature (tests excepted) | ruff ANN |
| types | a wrong type, an unguarded `None` | ty |
| surface | `TypedDict`, `eval`/`exec`, `pickle` | ruff banned-api, bandit |
| shape | parsing outside `cli/` or `__main__.py`, more than six free functions in a module, a classless package, `sys.path` edits, a file no gate reads | AST |
| complexity | a function over 6 (15 in a test) | ruff C901 |
| duplication | a six-line block copied twice | pylint symilar |
| deadcode | a name written and never wired | vulture |
| domain | a wire-model field that does not describe itself; a `domain.md` ontology older than the code | AST |
| harness | an `AGENTS.md` over 120 lines, a skill over 150 or with bad frontmatter, a skill the table misses, kickoff placeholders left | files |
| behaviour | the pytest suite, every folder `testpaths` names | pytest |
| crap | complexity the suite does not run: `c²·(1−cov)³ + c > 8` | ruff + coverage |

Four of them are what agent-written code needs most and no single tool holds: **domain-driven
design** (wire models describe their fields: the schema is the prompt), **object orientation**
(concepts are classes, the run layer is thin), the **ontology** (`python -m ci domain --write`
renders components, entities, kinds and relations from the syntax tree into `domain.md`; a stale
page is red), and **self-commented code** (modules and classes say what they are; no commented-out
code).

## learning flows both ways

- **Up**: a lesson or skill that held in two projects is generalised and moved into ini
  (`skills/harvest`, *up*), with project names stripped.
- **Down**: an agent reads ini as it is now, compares it with the project by meaning and distils
  what applies; a new rule meeting old code is fixed or recorded as debt. Where the project departs from ini, the
  departure either fits the project and stays, or is a lesson that goes up.
- **Expand / compress**: every round ends compressed (`skills/compress`), and the harness gate
  holds the budgets that keep skills and lessons from exhausting the context they exist to save.

## why Python 3.14

The floor is 3.14: deferred annotations, template strings, supported free-threading. On
2026-11-18, 3.15 resolved pydantic, torch, polars and numpy, but not onnxruntime or langgraph's
pyyaml (no `cp315` wheels). Near-native is the default: the standard library first, pydantic at the
wire, frozen dataclasses inside, beartype only at a seam that hands back `Any`.

ini is its own first project: `uv run python -m ci gates` and `--prove` hold it to the knowledge it
carries.
