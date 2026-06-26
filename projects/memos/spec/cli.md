# CLI

## Purpose

The `memos` CLI is the helper tooling that maintains the OS itself — not any
single project. It owns the OS's generated outputs so they never drift from their
canonical sources.

## Behaviour

- The CLI lives in `scripts/` and is run through `uv`:
  `uv run scripts/memos <command>` ([scripts.md](../../../rules/scripts.md)).
- Current commands:
  - `shimify` — regenerate every per-tool skill shim from the canonical
    `skills/<name>/SKILL.md`, for all supported tools (Claude, Cursor, Codex,
    OpenCode). Run it after adding or changing a skill, then reload skills in the
    tool ([skills.md](skills.md)).

## Success criteria

- `uv run scripts/memos shimify` regenerates all shims deterministically and
  leaves no diff when sources are unchanged.
- New OS-maintenance jobs that recur are added as CLI subcommands rather than
  ad-hoc scripts.
