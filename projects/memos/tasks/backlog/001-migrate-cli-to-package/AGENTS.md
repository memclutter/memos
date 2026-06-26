---
id: 001-migrate-cli-to-package
status: backlog
created: 2026-06-26
updated: 2026-06-26
blocks: 002-doctor-command
---

Migrate the `memos` CLI from the single-file `scripts/memos` PEP-723 script to a
proper `uv`-managed Python package (`src/` layout, `pyproject.toml`,
`ruff`/`mypy`/`pytest`), preserving `shimify` behaviour exactly. Prerequisite for
the `doctor` command (002). Scope, success criteria, and the spec delta are in
`spec.md`.
