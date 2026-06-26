# CI

## Purpose

Automated enforcement keeps the OS's internal consistency invariants from drifting
silently. The same health gate runs locally before each commit and in GitHub
Actions on every push and pull request.

## Behaviour

- **`memos doctor`** is the single health gate. It runs two read-only checks:
  shims in sync with canonical skills, and the rules index in sync with
  `rules/` ([cli.md](cli.md)).
- **Local pre-commit** — `.pre-commit-config.yaml` defines a `repo: local` hook
  (`memos-doctor`) that runs `uv run memos doctor` on every commit
  (`always_run: true`, `pass_filenames: false`). Install with `pre-commit install`
  (documented in [README.md](../README.md)).
- **GitHub Actions** — `.github/workflows/ci.yml` runs on `push` and
  `pull_request`: lint, format check, type-check, and test the `scripts/memos`
  package, then run `uv run memos doctor` from the repo root.

## Success criteria

- A clean repo passes `uv run memos doctor` (exit 0).
- With pre-commit installed, a commit that breaks a shim or rules-index invariant
  is blocked until fixed.
- A push or pull request that leaves the OS inconsistent fails the CI job on the
  doctor step.
