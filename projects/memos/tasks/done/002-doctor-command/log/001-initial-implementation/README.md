# Log 001 — initial implementation

Added the `doctor` consistency command and wired it into pre-commit and CI.

## What was done

- `scripts/memos/src/memos/doctor.py`: `check_shims(root)` (reuses
  `compute_shims` — reports missing / out-of-date shims and stale shim folders)
  and `check_rules_index(root)` (parses `AGENTS.md` for `rules/*.md` links; reports
  unindexed rules and links to missing files). `run_doctor` runs both, prints a
  per-check summary, collects all problems, returns non-zero if any.
- Wired `doctor` as a subcommand in `cli.py`.
- `scripts/memos/tests/test_doctor.py`: tmp-repo cases for both checks (clean +
  each violation) and a smoke test that the real repo is healthy.
- `.pre-commit-config.yaml`: local `memos-doctor` hook (`uv run memos doctor`).
- `.github/workflows/ci.yml`: on push/PR — lint/type/test with
  `working-directory: scripts/memos`, then `uv run memos doctor` from the root.
- Noted `pre-commit install` in `projects/memos/README.md`.

## Verification

- `uv run memos doctor` → both checks ok, exit 0.
- `uv run memos shimify` → no shim diff (doctor and shimify agree).
- From `scripts/memos`: `ruff check .`, `ruff format --check .`, `mypy`, `pytest`
  all pass (11 tests).

## Deferred to Finish (merge-on-done)

Fold the delta into `spec/` via `sys.task.finish`: `cli.md` gains `doctor`; new
`spec/ci.md`; `overview.md` indexes `ci.md`; `skills.md`/`rules.md` note the
invariant is now checkable with `memos doctor`.
