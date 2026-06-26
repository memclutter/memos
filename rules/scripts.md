# Scripts

`scripts/` holds the **helper scripts that keep the OS itself running** —
automation for this repo, not for any single project. Things like generating
skill shims, scaffolding projects/tasks, and other maintenance chores live here.

```
scripts/
├── pyproject.toml   # uv workspace root (keeps .venv/.cache under scripts/)
├── uv.lock
└── memos/           # the OS CLI — a uv-managed Python package (src/ layout)
    ├── pyproject.toml
    └── src/memos/
```

## The `memos` CLI

The CLI is a proper Python package under `scripts/memos/` (`src/` layout, its own
`pyproject.toml`), exposed as a `memos` console script. The **uv workspace root**
(`[tool.uv.workspace]`) lives at `scripts/pyproject.toml` with `memos` as its only
member, so uv keeps the virtualenv (`scripts/.venv`) and tool caches
(`scripts/.cache`) under `scripts/` rather than scattering them at the repo root.

Run the CLI from inside the workspace, or from the repo root with `--directory`:

```bash
# from scripts/memos
uv run memos <command> [args]

# from the repo root
uv run --directory scripts/memos memos <command> [args]

uv run memos shimify        # regenerate skill shims (see skills.md)
```

## Conventions

- Python, per [python.md](python.md): typed, `ruff`-clean.
- Run via `uv` — never assume a global interpreter or hand-managed venv.
- Each script/subcommand does one job and prints what it changed.
- Scripts are idempotent where possible (safe to re-run).
- Generated outputs (e.g. skill shim directories) are owned by the script; do
  not hand-edit them — change the source and re-run.
- English, like every other record.
