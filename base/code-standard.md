# code standard

Inherited from ini; do not edit here. Tier 4: it derives from `foundation.md`, and a rule is kept
because a gate fails without it — or it says here why nothing can enforce it. Compact on purpose: a
standard that takes ten minutes to read is paraphrased, not followed.

## environment

- **uv owns the environment.** One `pyproject.toml`, one `uv.lock`, every command through `uv run`
  (`--frozen` in CI). A dependency is declared, locked and earns its place by deleting a class of
  code. The gate toolchain is the `dev` group, pinned as in ini's starter `pyproject.toml`.
- **Python 3.14 is the floor**: deferred annotations (no `from __future__`, no quoted forward
  references), template strings, supported free-threading. Move to 3.15 (`frozendict`, lazy
  imports, UTF-8 by default) when every dependency ships a `cp315` wheel — on 2026-11-18
  `onnxruntime` and langgraph's `pyyaml` did not.
- **Near-native first.** Standard library and the language before a dependency; `pydantic` is the
  one default, because the wire needs a validator and a JSON schema the stdlib does not have.
  `beartype` only at a seam where a library hands back `Any` and a wrong runtime type would corrupt
  the domain (a float into a `Decimal` ledger) — ty is silent there by construction.

## shape

1. **One package, absolute imports.** `src/<package>/<component>/` in a new project, flat in an old
   one (`[tool.ini] src = "."`), is the map in `domain.md`; dependencies point down it. Nothing
   edits `sys.path`.
2. **Source declares, run invokes.** A component is a class that owns its constants, entities and
   steps; a free function is a pure helper, at most six to a module. A command is a run script in
   `<package>/cli/` or a `__main__.py`: it parses arguments, calls one method and returns an exit
   code. `argparse`, `sys.argv` and `__main__` appear nowhere else.
3. **Pydantic at the wire, plain classes inside.** A record that crosses a wire — a file, an HTTP
   body, an LLM's typed output — is a `BaseModel`, frozen where it travels, and each field says what
   it is (`Field(description=...)` or a docstring under it with `use_attribute_docstrings=True`).
   A value that never leaves the process is a frozen `@dataclass(slots=True)`. A closed vocabulary
   is a `StrEnum`. No `TypedDict`, no dict-as-record. A rule that reads one record is its method.
4. **Decode at the boundary, then trust.** Outside data is parsed once, where it enters. No `Any` in
   a signature; every function outside the tests states its parameters and its return. The checker
   is never silenced.
5. **Declarative over imperative.** Complexity ≤ 6 in code, ≤ 15 in a test; past that, the data
   wants to be a table and the code its interpreter.
6. **Constants are a tree.** A number or phrase with a domain meaning is a frozen field under one
   `CONST` in the module that owns the rule, never retyped.
7. **Errors are typed.** One base error per project; a refusal the caller must tell apart gets its
   own class. `ValueError` is for programmer error.
8. **A renderer prints what it is handed.** No template or formatter derives a number or a
   classification. Review keeps this one: a derivation reads like any other expression.
9. **No stringly code.** No `eval`, `exec` or `pickle`; no regex where a typed decoder exists.
10. **Self-commented code.** Names state the rule. A module docstring states the domain rule it
    enforces; a class docstring states what it is — the ontology prints both. A comment states a
    *why* the code cannot: a source, a measured incident, a rejected alternative. No commented-out
    code: git keeps it.

## invariants

- **One decision lives in one place.** Grep before writing a rule or a threshold; on the second use,
  extract it to one home, switch the callers green, then build the new use.
- **Refactor first, then change.** A move and a behaviour change never share a diff.
- **A rule that is never called is not a rule.** Every predicate that matters is called from the
  real entry point, and a test proves the wiring.
- **A behaviour change starts as a failing test**, seen to fail for the expected reason.

## tests

- **Behaviour at the public surface.** A test calls the code the way its user does — the run
  script's `main`, in process, or the component's public method — and checks what that user sees.
  If it would still pass with every function returning nothing, delete it.
- **One behaviour file per component, plus the end-to-end flows.** Cases are parametrised tables.
- **A golden is a pinned value** that moves only with a written reason.
- **Do not test the implementation.** A refactor that keeps behaviour must not rewrite the suite.
- **Mutation testing is an audit**, run before a release one module at a time; a surviving mutant is
  a missing behaviour test or dead code (`base/skills/mode`).

## gates

`uv run python -m ci gates` — red blocks the change. `--prove` plants a defect per gate in a scratch copy
and fails if any gate lets it through: a gate you have not seen fail is not a gate. `--adopt`
records an existing project's debt once; from then on the ratchet (`ci/ceilings.json`) only
shrinks, and `--record` lowers it after a fix.

| gate | catches |
|---|---|
| lint | defects, relative imports, globals, data clumps, unidiomatic code, layout (ruff, ruff format) |
| docs | a module, package or class that does not say what it is; commented-out code (ruff D, ERA) |
| annotations | an unstated contract, `Any` in a signature (ruff ANN) |
| types | a wrong type, an unguarded `None` (ty) |
| surface | `TypedDict`, `eval`/`exec`, `pickle` (ruff banned-api, bandit) |
| shape | parsing outside `cli/`, a pile of free functions, a classless package, `sys.path`, a file out of scope |
| complexity | a function over budget (ruff C901) |
| duplication | a block of six lines copied twice (pylint symilar) |
| deadcode | a name written and never wired (vulture; tests excluded on purpose) |
| domain | an undescribed wire field; a `domain.md` ontology older than the code |
| harness | an oversized `AGENTS.md` or skill, a skill the table misses, kickoff left |
| behaviour | the pytest suite |
| crap | a complex function the suite does not run (`complexity²·(1−coverage)³ + complexity > 8`) |

## refuses

- Blanket ignores, raised thresholds, `--exit-zero`, `cast` or `type: ignore` to reach green.
- More enforcement than the repo keeps green: an aspirational red gate blocks nothing.
- DI containers, repositories, service layers, a class per verb: a class exists because the domain
  names the thing.
- Enforced functional style: in the ledger experiment it cost 42 % more lines and prevented no
  defect. Shape — one domain model and enforced gates — is what paid.
- A language migration on safety grounds; the same experiment found no case for it.
