# Log 001 — initial implementation

Migrated the `memos` CLI from the single-file `scripts/memos` PEP-723 script to a
`uv`-workspace Python package, with `shimify` behaviour preserved exactly.

## What was done

- Removed the old single-file `scripts/memos`.
- Added a virtual `uv` workspace root `pyproject.toml`
  (`members = ["scripts/memos"]`) and the package manifest
  `scripts/memos/pyproject.toml` (hatchling, `memos` console script, `pyyaml`,
  dev group `pytest`/`ruff`/`mypy`/`types-PyYAML`, ruff + mypy config).
- Created `scripts/memos/src/memos/`: `__init__.py`, `__main__.py`, `cli.py`
  (argparse, `shimify` subcommand), and `shims.py`.
- `shims.py` adds `find_repo_root()` (ascends to an `AGENTS.md` + `rules/` marker,
  replacing the old `__file__.parent.parent`) and splits shim generation into pure
  `compute_shims(root)` and side-effecting `write_shims(root)`.
- Updated doctrine references `uv run scripts/memos …` → `uv run memos …` in
  `rules/scripts.md`, `rules/skills.md`, root `AGENTS.md`, `projects/memos/AGENTS.md`,
  and fixed task 002's README forward-reference.
- Added `tests/test_shims.py`; added tool caches to `.gitignore`.

## Verification

- **Gate (byte-identical):** `uv run memos shimify` → `7 skill(s) -> 28 shim(s)`,
  **no git diff** on `.claude/.cursor/.codex/.opencode`.
- `uv run ruff check scripts/memos` — all checks passed.
- `mypy` (strict) — no issues in 4 source files.
- `pytest` — 3 passed (disk-stability + round-trip + drift detection).

## Deferred to Finish (merge-on-done)

Per SDD, the living spec is updated at the Finish gate, not during implement. Left
for `sys.task.finish`:

- `projects/memos/spec/cli.md` and `spec/skills.md` still say `uv run scripts/memos`
  — these fold to the new invocation (and `cli.md` gains the package/workspace
  description) when the delta is merged.
