# conjectures

Deutsch's move (`foundation.md` §lenses): knowledge grows by conjecture and refutation, not by
accumulating notes. Each row is a hard-to-vary claim that could be wrong and names what would show
it wrong. State, criticise, test, then promote or destroy; a conjecture that never moves is a
belief ini pays for.

## open

| id | conjecture | refuted if | status |
|---|---|---|---|
| c1 | **deliberate redundancy via agent distillation beats linking or package deps** (`objective.md` §claim) | by `2026-12-31`, no ongoing project carries ini's gates, or refreshing an existing distillate costs more than re-distilling from scratch (`objective.md` §kill) | open (`2026-11-18`) |
| c2 | **knowledge stays readable in one sitting while compounding across projects** (`objective.md` §target 3–4) | by `2026-12-31`, no promoted lesson or skill reaches another project, or budgets must rise above 120 / 150 / 160 lines to hold real procedures | open (`2026-11-18`) |
| c3 | **shape and domain gates transfer across older-runtime repositories** (`now.md` §next) | distilling into a pre-3.14 repository fails without forcing a runtime rewrite or dropping core gates | open (`2026-11-20`) |

## promoted

| id | conjecture | evidence |
|---|---|---|
| c4 | **domain, shape, ontology and docs gates catch agent defects that style lints miss** | `ci/tests/test_gates.py`, `--prove` 13/13; active distillates hold 13–14 gates green (`log/agt.md`, `2026-11-20`) |
| c5 | **cross-family critic review catches blind spots of the author's family** | two cross-family passes on ini caught 6/6 and 11/11 accepted defects including silent missing-tool exit and `$local_sha` pre-push gap (`log/agt.md`) |

## destroyed

| id | conjecture | what killed it |
|---|---|---|
| c6 | **ini as an installable package, read-only `base/` dir, or stamped `origin` commit** | rejected `2026-11-18` (`log/agt.md`): couples projects to ini or treats deliberate project divergence as a fork |
| c7 | **enforced functional style over OO domain models** | refuted (`code-standard.md` §refuses): +42 % lines and zero defects prevented vs one domain model with enforced gates |
| c8 | **missing gate tools fail cleanly as zero findings** | refuted `2026-11-18` (`log/agt.md:26-27`, `ci/tests/test_gates.py`): missing tools now raise `IniError` instead of reading green |

## rule

A conjecture not on this page is a vibe. Every strategic, product or architecture claim gets an id
and a falsifier in the same edit that states it. Keep the id when a row moves between sections; a
kept dream (`skills/dream`) arrives here linked from both pages. Never edit a row silently.
