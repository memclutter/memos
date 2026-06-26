---
id: 002-doctor-command
status: done
created: 2026-06-26
updated: 2026-06-26
depends-on: 001-migrate-cli-to-package
---

Add a `doctor` subcommand to the `memos` CLI that runs consistency checks over
the OS and exits non-zero when any fails. Builds on the packaged CLI from task
001. Scope, success criteria, and the spec delta are in `spec.md`.

## Tasks breakdown

- [x] 1. Scaffold `src/memos/doctor.py` and wire a `doctor` subcommand in `cli.py`
  (handler returns `0`, no checks yet) — establishes the plumbing.
- [x] 2. Implement `check_shims(root) -> list[str]`: compare `compute_shims(root)`
  to disk (missing / byte-mismatch) and detect stale shim folders per `TOOLS`.
- [x] 3. Implement `check_rules_index(root) -> list[str]`: parse `AGENTS.md` for
  `rules/*.md` links; report unindexed rules and links to missing files.
- [x] 4. Fill in the `doctor` handler: run both checks, print a per-check summary
  (problems or "ok"), collect **all** problems, exit `1` if any else `0`.
- [x] 5. Add `tests/test_doctor.py`: `check_shims` and `check_rules_index` cases
  over `tmp_path` (clean → none; each violation → reported) + a smoke test that
  `doctor` on the real repo returns `0`.
- [x] 6. Add `.pre-commit-config.yaml` — `repo: local` hook `memos-doctor`
  (`entry: uv run memos doctor`, `language: system`, `pass_filenames: false`,
  `always_run: true`); note `pre-commit install` in the project README.
- [x] 7. Create `.github/workflows/ci.yml` (push + pull_request): `checkout` →
  `astral-sh/setup-uv` → lint/type/test with `working-directory: scripts/memos`
  (`uv run ruff check .`, `uv run mypy`, `uv run pytest`) → `uv run memos doctor`
  from the repo root.
- [x] 8. Green check: `uv run memos doctor` exits `0`, and ruff/mypy/pytest pass.
  ⚠️ gate — confirm a clean repo is fully green before Finish.
- [x] 9. (Finish, via `sys.task.finish`) fold the delta into `spec/`: `cli.md`
  gains `doctor`; new `spec/ci.md`; `overview.md` indexes `ci.md`; `skills.md`
  /`rules.md` note the invariant is now checkable.
