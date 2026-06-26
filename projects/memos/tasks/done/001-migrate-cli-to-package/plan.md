# Plan — 001-migrate-cli-to-package

## Approach

Lift the existing single-file CLI into a `src/`-layout package with a
`pyproject.toml`, a `memos` console-script entry point, and `ruff`/`mypy`/`pytest`
configured — moving the `shimify` logic across **unchanged in behaviour**. Split
shim generation into a pure "compute" step and a thin "write" step so it becomes
testable (and reusable by the later `doctor` command). Finally, update every
reference to the old `uv run scripts/memos …` invocation to `uv run memos …`.

## Stack

Per [python.md](../../../../rules/python.md): CPython ≥3.11, `uv`, `src/` layout,
`pyproject.toml`, `ruff` (format+lint), `mypy` (types), `pytest`. Runtime dep:
`pyyaml`. Build backend: `hatchling`.

## Architecture

### Layout

The package lives entirely under `scripts/memos/`; the repo root carries only a
**virtual uv workspace** declaration so `uv run memos` works from the root.

```
pyproject.toml                 # virtual workspace root: [tool.uv.workspace] members = ["scripts/memos"]
scripts/memos/
├── pyproject.toml             # the memos package (hatchling, entry point, deps, ruff/mypy)
├── src/memos/
│   ├── __init__.py
│   ├── __main__.py            # python -m memos
│   ├── cli.py                 # argparse: main() + subcommand wiring
│   └── shims.py               # shim model: load skills, compute + write shims
└── tests/
    └── test_shims.py
```

- The old single-file `scripts/memos` (a **file**) is replaced by the
  `scripts/memos/` package **directory**. A file and directory can't share a name,
  so the file is `git rm`'d before the directory is created.
- Invocation is `uv run memos <command>` from the repo root, resolved through the
  workspace.

### `pyproject.toml` (two files)

- **Root** (`pyproject.toml`): virtual workspace only — `[tool.uv.workspace]`
  `members = ["scripts/memos"]`, no `[project]` table.
- **Package** (`scripts/memos/pyproject.toml`):
  - `[project]`: `name = "memos"`, `version`, `requires-python = ">=3.11"`,
    `dependencies = ["pyyaml>=6"]`.
  - `[project.scripts]`: `memos = "memos.cli:main"`.
  - `[build-system]`: `hatchling`; `[tool.hatch.build.targets.wheel]`
    `packages = ["src/memos"]`.
  - Dev deps via `[dependency-groups] dev = ["pytest", "ruff", "mypy",
    "types-PyYAML"]`.
  - `[tool.ruff]`, `[tool.mypy]` configured (mypy `strict` over `src`).

### Repo-root resolution (key change)

The script currently uses `ROOT = Path(__file__).parent.parent`, which breaks once
the code sits under `scripts/memos/src/memos/`. Replace with a
`find_repo_root(start)` that ascends until it finds a marker (`AGENTS.md` +
`rules/`), raising a clear error if not found. All path logic (`SKILLS_DIR`,
`TOOLS`, tool shim dirs) hangs off that.

### `shims.py` (refactor of `shimify`)

- Keep `_split_frontmatter`, `_load_skills`, `GENERAL_KEYS`, `TOOLS`, and the
  shim-text builder, behaviour identical.
- Split into:
  - `compute_shims(root) -> dict[Path, str]` — pure: maps each shim file path to
    its exact content (no I/O).
  - `write_shims(root)` — removes each tool's `skills/` dir, writes the computed
    mapping, returns counts. `cmd_shimify` calls this and prints the same summary.
- Identical output is the contract: the same files with the same bytes as today.

### Reference updates (runtime rename)

Replace `uv run scripts/memos` → `uv run memos` everywhere it appears, and fix the
"where the CLI lives" wording:

- `rules/scripts.md` and the root `AGENTS.md` Scripts entry (договор).
- `rules/skills.md` (the `shimify` instructions).
- `projects/memos/AGENTS.md` and `projects/memos/spec/{cli,skills}.md`.
- `README.md` if it mentions the CLI.

(The canonical skill SKILL.md files only reference `shimify` in prose pointing to
`scripts/memos`; update those too, then regenerate shims so the change is
self-consistent.)

## Trade-offs & alternatives

- **Remove `scripts/memos`** (chosen) vs. keep it as a thin shim calling the
  package. A leftover wrapper would just be a second invocation path to keep in
  sync; the console script (`uv run memos`) replaces it cleanly.
- **`hatchling`** (chosen) — simplest standards-based backend for a `src/` package;
  no need for setuptools config.
- **Marker-based `find_repo_root`** (chosen) vs. assuming `cwd`. A marker makes the
  CLI work regardless of where it's invoked from, matching today's behaviour.
- **compute/write split** (chosen) vs. leaving `shimify` monolithic. The split is
  what makes shim output testable without filesystem churn and seeds the `doctor`
  shim check (task 002).

## Constraints & risks

- **Byte-identical shims** is the headline acceptance criterion: after migration,
  `uv run memos shimify` must leave **no git diff**. The compute/write split plus a
  stability test guard this.
- The reference rename is broad; a missed `scripts/memos` mention would be stale.
  Task 002's `doctor` will later catch index/shim drift, but for this task verify
  with a repo-wide grep for `scripts/memos`.
- `requires-python` and `pyyaml` must match the old inline metadata so nothing
  about resolution changes.

## Testing strategy

`pytest` over the real repo plus `tmp_path`:

- **Stability:** `compute_shims(repo_root)` output equals the bytes currently on
  disk for every shim — proves the migration changed nothing.
- **Round-trip:** in a `tmp_path` fixture with a fake skill, `write_shims` then
  `compute_shims` agree, and a hand-mutated shim is detected as different.
- `uv run ruff check`, `uv run mypy`, `uv run pytest` all green; a CI workflow is
  added in task 002 (here we just ensure the commands pass locally).
