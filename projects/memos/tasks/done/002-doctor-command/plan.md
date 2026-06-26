# Plan — 002-doctor-command

> Builds on **001-migrate-cli-to-package** (done): `memos` is a `src/`-layout
> package under `scripts/memos/` with `pyproject.toml` + `ruff`/`mypy`/`pytest`,
> invoked as `uv run memos <command>`, exposing `memos.shims` (incl.
> `compute_shims`, `find_repo_root`, `TOOLS`).

## Approach

Add a `doctor` subcommand to the packaged CLI, reusing the helpers `shimify`
already exposes in `memos.shims` — in particular `compute_shims(root)`, which
already maps every expected shim path to its exact content. Each check is a pure
function that takes the repo root and returns a list of problem strings; `doctor`
runs them all, prints every problem, and exits non-zero if any are found. Then
wire `doctor` into a local `pre-commit` hook and a new GitHub Actions workflow.

## Stack

- The `memos` package ([python.md](../../../../rules/python.md)): `src/` layout,
  `pyproject.toml`, `uv`, `ruff`, `mypy`, `pytest` — all in place from task 001.
- `pre-commit` for the local hook; GitHub Actions for CI (`astral-sh/setup-uv`).

## Architecture

### `doctor` command

- New module `scripts/memos/src/memos/doctor.py` holding the checks; wired as a
  `doctor` subcommand in `cli.py` next to `shimify`. Tests in
  `scripts/memos/tests/`.
- Reuse the actual `memos.shims` API: `find_repo_root()`, `compute_shims(root)`,
  and `TOOLS`. (There is no `SKILLS_DIR` constant — the skills dir is `root /
  "skills"` inside the helpers.) ⚠️ spec boundary: reuse, don't fork, `shimify`'s
  path logic — `compute_shims` **is** that shared logic.
- Two pure checks, each `(root: Path) -> list[str]`:

  **`check_shims(root)`**
  - Call `compute_shims(root)` for the expected `{path: content}` map. For each:
    report if the file is missing, or if its bytes differ from the expected
    content (this subsumes both "missing shim" and "doesn't reference canon",
    since the canonical pointer line is part of the expected content).
  - Detect **stale** shims: for each tool in `TOOLS`, list `<root>/<dir>/skills/*`
    folders and report any whose name has no canonical skill (i.e. not among the
    expected paths' skill names).

  **`check_rules_index(root)`**
  - Parse `AGENTS.md` for Markdown links to `rules/*.md`.
  - Report any `rules/*.md` with no linking entry, and any `rules/*.md` link in
    `AGENTS.md` pointing to a missing file.

- The `doctor` handler concatenates results, prints a per-check summary (problems
  or "ok"), returns `1` if the combined list is non-empty else `0`.

### pre-commit hook

- Commit `.pre-commit-config.yaml` with a `repos: - repo: local` hook:
  `id: memos-doctor`, `entry: uv run memos doctor`, `language: system`,
  `pass_filenames: false`, `always_run: true`. Document `pre-commit install`.

### GitHub Actions

- **Create** `.github/workflows/ci.yml` (none exists yet — 001 left CI to this
  task). Triggers `on: [push, pull_request]`, job on `ubuntu-latest`:
  `actions/checkout` → `astral-sh/setup-uv` (pinned to a major) → the check steps.
- Invocation context matters: `ruff`/`mypy`/`pytest` config lives in
  `scripts/memos/pyproject.toml`, and `mypy`/`pytest` discover config from the
  cwd. So run the lint/type/test step with `working-directory: scripts/memos`
  (`uv run ruff check .`, `uv run mypy`, `uv run pytest`) — the verified pattern
  from task 001. `doctor` runs from the repo root: `uv run memos doctor`.

## Trade-offs & alternatives

- **Unit checks** (chosen): pure functions taking `root` are tested directly with
  `tmp_path` fixtures — fast and precise. Now that the CLI is a real package,
  tests just `import` the module; the `importlib`-from-path workaround the old
  single-file script would have needed is gone with task 001. One happy-path
  smoke test still runs the real `uv run memos doctor`.
- **`repo: local` system hook** (chosen) vs. a published pre-commit hook repo:
  local keeps the hook in lockstep with the CLI and needs no release.

## Constraints & risks

- `doctor` stays **read-only** (spec boundary) — never writes or fixes.
- The shim check reuses `compute_shims`; this guarantees `doctor` and `shimify`
  can't disagree about what a correct shim is.
- CI must install `uv` before invoking the CLI; pin `setup-uv` to a major version.
- The lint/type/test step must use `working-directory: scripts/memos`; running
  those tools from the repo root would miss their config.

## Testing strategy

`pytest` (configured by task 001) over `tmp_path` fixtures:

- `check_shims`: clean fixture → no problems; remove a shim → reported; mutate a
  shim's bytes (e.g. drop the canon pointer) → reported; stale shim folder →
  reported.
- `check_rules_index`: clean fixture → no problems; unindexed `rules/x.md` →
  reported; `AGENTS.md` link to a missing rule → reported.
- Smoke test: `uv run memos doctor` on the real repo exits `0`.
- CI runs `doctor` plus the suite, so a regression turns the check red.
