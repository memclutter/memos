# 002 — `memos doctor` command

Add a `doctor` subcommand to the `memos` CLI that checks the OS's internal
consistency and reports problems.

## Goal

One command that verifies the OS is healthy and fails loudly when it isn't.

## Scope

Two checks:

1. **Shims in sync** — every canonical skill in `skills/` has a shim in each
   native tool directory (`.claude`, `.cursor`, `.codex`, `.opencode`) that points
   back to the canonical `SKILL.md`.
2. **Rules indexed** — every rule file in `rules/` is retold in `AGENTS.md` with a
   working link to the full rule.

Plus automated enforcement: run `doctor` from a `pre-commit` hook and from a
GitHub Actions workflow.

## Acceptance criteria

- `uv run scripts/memos doctor` reports all problems found and exits non-zero if
  any check fails; exits zero on a clean repo.
- Both checks above are implemented and covered by tests.
- A committed `.pre-commit-config.yaml` runs `doctor`; a committed GitHub Actions
  workflow runs `doctor` on push and pull request.
