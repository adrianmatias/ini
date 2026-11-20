# ini — agent contract

ini is a live cookiecutter for AI agents: a repository of knowledge in the shape of a fresh
repository. It is its own first project: the knowledge it carries is the knowledge it obeys, and
its product is the harness in `ci/`.

## entry (every session)

1. Read the tiers in order: `objective.md` → `foundation.md` → `domain.md` →
   `code-standard.md`.
2. Read `now.md` and the **latest prompt at the bottom of `log/mat.md`**: that is the task.
3. Read the skill whose trigger matches (table below), then only the files the task needs.
4. Close the round: `uv run python -m ci gates` and `--prove` green, `now.md` rewritten,
   `log/agt.md` appended.

Steering: `objective > foundation > domain > code-standard > gates and behaviour tests >
implementation`.

## what is special here

- **Three audiences.** `foundation.md`, `code-standard.md`, `wiki/learnings.md` and `skills/` are
  read by every agent in every project that carries them, so each line costs context everywhere. `skills/kickoff/templates/` becomes a new project's anchors. `ci/`
  becomes every project's harness. ini's own anchors (this file, `objective.md`, `now.md`,
  `domain.md`, `log/`) are replaced in a copy.
- **A gate change ships with its witness**, and `--prove` stays 13/13 (or N/N): a gate that cannot
  be seen to fail is not merged.
- **Projects distil ini; they never link to it.** No dependency, no submodule, no recorded commit.
  A change here reaches a project only when an agent reads ini and brings it in, in that project's
  terms. Say in the commit what a project must do (a new skill row, a new rule meeting old code).
- **Promotions arrive from projects** (`harvest`): generalise, strip project names a public
  repository should not carry, and pay for added lines by removing weaker ones.
- Templates carry `.tmpl` so no tool reads them as code; `{{key}}` is the only placeholder syntax.
- **Publishable.** No project, client or employer names anywhere in the repository, logs included;
  evidence keeps its date and loses its source.

## roles and models

| role | model (2026-11) | effort |
|---|---|---|
| director | mat | — |
| integrator | `claude-opus` (plan, fixed cost) or `gemini-4` (pay-per-token complement) | high |
| lane | `deepseek-v4.1-flash` on the DeepSeek API | max |
| critic | distinct family from author (`claude-opus` ↔ `gemini-4` ↔ `deepseek-v4.1-flash`) | high |

## skills

The skills every copy keeps:

| skill | use when |
|---|---|
| `kickoff` | a project starts or its bet changes |
| `mode` | writing or changing code: make it work, make it right, practice |
| `review` | a change, plan or artifact needs a critic from another family |
| `delegate` | work could fan out: roles, patterns, briefs, integration |
| `restructure` | reshaping code without changing behaviour |
| `compress` | a round ends, or code, docs or skills have grown |
| `dream` | logs outpace docs or wiki: replay, pair, judge |
| `harvest` | a lesson holds beyond one project, or a project takes in ini |

## don't

- Don't add a gate without a witness, or a skill without trimming one when the knowledge is near budget.
- Don't make ini depend on a harness (Hermes, Claude Code, pi) or become an installable package:
  skills are plain files, and the gates run from the tree.
- Don't commit or push unless mat says so.

## commands

```
uv sync
uv run python -m ci gates             # ini judged by itself
uv run python -m ci gates --prove     # every witness rejected
uv run pytest                         # the behaviour suite (starts copies in tmp and gates them)
uv run python -m ci domain --write    # re-render domain.md
```
