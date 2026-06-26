# CI

## Purpose

Automated enforcement keeps the OS's internal consistency invariants from drifting
silently. The same health gate runs locally before each commit and in GitHub
Actions on every push and pull request.

## Behaviour

- **`memos doctor`** is the consistency health gate. It runs read-only checks:
  shims in sync with canonical skills, the rules index in sync with `rules/`, and
  each non-`self` project's submodules under `vcs/<repo-name>/` ([cli.md](cli.md)).
- **Local pre-commit** — `.pre-commit-config.yaml` defines `repo: local` hooks
  that mirror CI: `ruff check`, `ruff format --check`, `mypy`, and `memos doctor`
  (each `always_run: true`, `pass_filenames: false`), all run from `scripts/memos`.
  Install with `pre-commit install` (documented in [README.md](../README.md)).
- **GitHub Actions** — `.github/workflows/ci.yml` runs on `push` and
  `pull_request`: lint, format check, type-check, and test the `scripts/memos`
  package, then run `memos doctor` — all from `scripts/memos`.

## Success criteria

- A clean repo passes `uv run memos doctor` (exit 0).
- With pre-commit installed, a commit that breaks a shim or rules-index invariant
  is blocked until fixed.
- A push or pull request that leaves the OS inconsistent fails the CI job on the
  doctor step.
