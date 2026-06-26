# CLI

## Purpose

The `memos` CLI is the helper tooling that maintains the OS itself — not any
single project. It owns the OS's generated outputs so they never drift from their
canonical sources.

## Behaviour

- The CLI is a `uv`-managed Python package under `scripts/memos/` (`src/` layout,
  its own `pyproject.toml`, `ruff`/`mypy`/`pytest`), exposed as a `memos` console
  script. The repo root declares a `uv` workspace whose only member is
  `scripts/memos`, so it runs from the repo root via `uv`:
  `uv run memos <command>` ([scripts.md](../../../rules/scripts.md)).
- Current commands:
  - `shimify` — regenerate every per-tool skill shim from the canonical
    `skills/<name>/SKILL.md`, for all supported tools (Claude, Cursor, Codex,
    OpenCode). Run it after adding or changing a skill, then reload skills in the
    tool ([skills.md](skills.md)).
  - `doctor` — run OS consistency checks (shims present and referencing canon;
    every `rules/*.md` indexed in `AGENTS.md` with working links). Reports every
    problem in one run and exits non-zero if any check fails. Read-only — no
    auto-fix ([ci.md](ci.md)).

## Success criteria

- `uv run memos shimify` regenerates all shims deterministically and leaves no
  diff when sources are unchanged.
- `uv run memos doctor` exits 0 on a consistent repo and non-zero when shims or
  the rules index are out of sync.
- `uv run ruff check`, `uv run mypy`, and `uv run pytest` pass for the package.
- New OS-maintenance jobs that recur are added as CLI subcommands rather than
  ad-hoc scripts.
