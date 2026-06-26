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

## Tasks breakdown

- [ ] 1. Add `pyproject.toml`: `[project]` (name, version, `requires-python
  >=3.11`, `pyyaml>=6`), `[project.scripts] memos = "memos.cli:main"`,
  `hatchling` build backend with `packages = ["src/memos"]`, dev group
  (`pytest`/`ruff`/`mypy`), and `[tool.ruff]` / `[tool.mypy]` config.
- [ ] 2. Scaffold `src/memos/`: `__init__.py`, `__main__.py` (`python -m memos`),
  and an empty `cli.py` with an `argparse` `main()` (no subcommands yet).
- [ ] 3. Add `find_repo_root(start)` (ascend to a marker: `AGENTS.md` + `rules/`)
  and the path constants (`SKILLS_DIR`, `TOOLS`, tool shim dirs) hanging off it.
- [ ] 4. Port `shimify` into `shims.py` as `compute_shims(root) -> {path: content}`
  (pure) + `write_shims(root)` (I/O), keeping behaviour identical (frontmatter
  split, skill loading, shim text).
- [ ] 5. Wire the `shimify` subcommand in `cli.py` to call `write_shims` and print
  the same summary line.
- [ ] 6. Verify byte-identical output: `uv run memos shimify` leaves **no git
  diff**.  ⚠️ gate — headline acceptance criterion; ask owner if any diff appears.
- [ ] 7. Remove the old single-file `scripts/memos`.
- [ ] 8. Rename `uv run scripts/memos` → `uv run memos` and fix "where the CLI
  lives" wording across `rules/scripts.md`, root `AGENTS.md`, `rules/skills.md`,
  `projects/memos/AGENTS.md`, `projects/memos/spec/{cli,skills}.md`, `README.md`;
  regenerate shims; `grep -r "scripts/memos"` comes back clean.
- [ ] 9. Add `tests/test_shims.py`: stability (`compute_shims(root)` == bytes on
  disk) and round-trip in `tmp_path` (mutated shim detected as different).
- [ ] 10. `uv run ruff check`, `uv run mypy`, and `uv run pytest` all pass.
