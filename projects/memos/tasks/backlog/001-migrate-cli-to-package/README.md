# 001 — Migrate the `memos` CLI to a packaged project

Replace the single-file `scripts/memos` PEP-723 script with a proper
`uv`-managed Python package (`src/` layout, `pyproject.toml`, `ruff`, `mypy`,
`pytest`), preserving `shimify` behaviour exactly.

## Goal

The OS CLI is a conventional, familiar Python package — easy to test, lint, and
extend — without changing what `shimify` does.

## Scope

- `pyproject.toml` with project metadata, a `memos` console script, runtime dep
  (`pyyaml`), and dev tooling (`pytest`, `ruff`, `mypy`).
- `src/memos/` package holding the CLI; `shimify` logic moved over unchanged.
- `ruff`/`mypy` configured and passing; `pytest` set up with a test for `shimify`.
- Update `rules/scripts.md` and the root `AGENTS.md` scripts entry to the new
  invocation (`uv run memos <command>`).

## Acceptance criteria

- `uv run memos shimify` regenerates the existing shims with **no diff**.
- `uv run pytest`, `uv run ruff check`, and `uv run mypy` all pass.
- The old single-file `scripts/memos` no longer carries the logic.
