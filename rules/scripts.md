# Scripts

`scripts/` holds the **helper scripts that keep the OS itself running** —
automation for this repo, not for any single project. Things like generating
skill shims, scaffolding projects/tasks, and other maintenance chores live here.

```
scripts/
└── memos          # the OS CLI (subcommands), run via uv
```

## The `memos` CLI

`scripts/memos` is the single entry point, exposing subcommands. It is a Python
tool and is **always run through `uv`**, which resolves its dependencies:

```bash
uv run scripts/memos <command> [args]

uv run scripts/memos shimify        # regenerate skill shims (see skills.md)
```

## Conventions

- Python, per [python.md](python.md): typed, `ruff`-clean.
- Run via `uv` — never assume a global interpreter or hand-managed venv.
- Each script/subcommand does one job and prints what it changed.
- Scripts are idempotent where possible (safe to re-run).
- Generated outputs (e.g. skill shim directories) are owned by the script; do
  not hand-edit them — change the source and re-run.
- English, like every other record.
