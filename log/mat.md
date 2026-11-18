# 2026-11-18

> The director's prompts of the first day. Project names, paths and private links were removed at
> the director's request before publishing; the wording is otherwise his.

## prompt

distill the recent learnings across my projects for an agent harness
create a template repo to condense them into a ready to start generic agent
principles, standards, gates, top skills, pattern/model/effort/delegation, hierarchy of steering agents, objective-placeholder must be part of it and ready
no reliance on a specific agent harness: skills better than plugins, skills as refining sub-product should be part of the template
included in the deterministic gate:
- domain-driven-design as expressed in recent projects
- object orientation for conceptual abstraction
- ontology render
- self-commented code
expand/compress cycle should be present in the harness
include starter toml for basic uv-env control
- gate deps
- basic standard deps: pydantic
- consider python version, latest versions have extra support for typing and concurrency. consider support for deps vs the near-native approach
the objective is to distill current and future learning/best-pratices as a dep for inheriting them at ongoing and new projects
i will consider to opensource it later
we can name it [ini](https://github.com/adrianmatias/ini)


## prompt

mention as mental model this is a live cookiecutter for ai agents
do not mention specific projects or context. this should be publishable beyond these projects.
the objective of ini is stated in the prev prompt:
> the objective is to distill current and future learning/best-practices as a dep for inheriting them at ongoing and new projects

python dependencies for gates should be in a toml.dev.group

the evolution of a project is to strip away functions from and llm into deterministic implementation to produce a piece of engineering instead of an llm shallow wrapper

decisions for me
1. "approved" Review the base text
2. "not yet" Commit and push ini?
3. "after the changes i request" Run a review from the other model family? The delegation pin is Opus, the same family that wrote it. Say ok and I'll switch the pin to DeepSeek for one critic pass.
4. "do it on another project" Make a project the first adoption (--adopt, Python floor to 3.14)?
5. Keep the field-description rule strict?
> 	enforce, not pussy-later-will-do-now-is-hard

## prompt

> python dependencies for gates should be in a toml.dev.group

this might be wrong and cause issues on the usage of ini, revert it if more useful or conflicts with the objective
about obsidian, that should be outside gh. in fact, i have been having issues and lost hotkeys
we can split that project's single-module deliverable, that is not a requirement anymore
be flexible with prev projects. some others are not even using pydantic, or find the common denominator
try to apply ini to a third project to learn how this should be applied to more projects before commiting to a common shape.
i would accept the installation could be in 2 steps: first install the harness and then propagate across the project until compliance.
new and old projects can take ini differently, keep the ini as core

## prompt

restate the objective: ini as a repository of knowledge in the shape of a fresh repo template
it is not installable as a package, but an agent could inherit and permeate into a project harness on demand from ini. that should address the decisions on me

## prompt

i approve the agents edit
remove specifics about the projects here. remove entries in /log if needed
the commit/push
