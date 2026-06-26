---
name: memos
vcs:
  - git@github.com:memclutter/memos.git
self: true
status: active
stack: [python]
created: 2026-06-26
---

The `memos` project is **the OS itself** — this repository. It is a
self-referential project, so it is exempt from the `vcs/` submodule rule
(`self: true`): there is no `projects/memos/vcs/` folder, and the `vcs:` entry
above is informational only. Its source lives at the OS repo root.

## What lives where (for this project)

- Source of the OS: the repo root — `rules/`, `skills/`, `scripts/`, `AGENTS.md`.
- Tasks about the OS (new rules, skills, scripts, fixes) go in
  `projects/memos/tasks/` like any other project.
- Edits to OS source are made at the root and committed directly to this repo —
  there is no submodule pointer to bump.

## Conventions

- Follow the root rules in `rules/` (this project does not override them).
- The OS CLI is the `memos` package under `scripts/memos/`, run via
  `uv run memos` (uv workspace) — see `rules/scripts.md`.
- After changing a skill, run `uv run memos shimify` and reload skills in
  your IDE/agent.
