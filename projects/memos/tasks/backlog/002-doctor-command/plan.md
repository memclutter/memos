# Plan — 002-doctor-command

> Depends on **001-migrate-cli-to-package**: assumes `memos` is a proper
> `src/`-layout package with `pyproject.toml`, `ruff`/`mypy`/`pytest`, invoked as
> `uv run memos <command>`. Do not start until 001 is done.

## Approach

Add a `doctor` subcommand to the packaged CLI, reusing the path/skill helpers the
package already exposes (from `shimify`). Each check is a pure function that takes
the repo root and returns a list of problem strings; `doctor` runs them all,
prints every problem, and exits non-zero if any are found. Then wire `doctor` into
a local `pre-commit` hook and a GitHub Actions workflow.

## Stack

- The `memos` package ([python.md](../../../../rules/python.md)): `src/` layout,
  `pyproject.toml`, `uv`, `ruff`, `mypy`, `pytest` — all in place from task 001.
- `pre-commit` for the local hook; GitHub Actions for CI (`astral-sh/setup-uv`).

## Architecture

### `doctor` command

- New `doctor` subcommand module/handler registered next to `shimify` in the
  package's CLI entry point.
- Reuse the package's existing helpers: skills discovery, the `SKILLS_DIR`/`TOOLS`
  constants, and the canonical shim-path helper. ⚠️ spec boundary: reuse, don't
  fork, `shimify`'s path logic — factor the canonical-path computation into a
  shared function if it isn't already.
- Two pure checks, each `(root: Path) -> list[str]`:

  **`check_shims(root)`**
  - For every `skills/*/` folder and every tool in `TOOLS`, expect
    `<root>/<dirname>/skills/<name>/SKILL.md` to exist and its body to reference
    the canonical `skills/<name>/SKILL.md`.
  - Report missing shims, shims not referencing canon, and **stale** shim folders
    with no matching canonical skill.

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

- Extend the CI workflow from task 001 (`.github/workflows/ci.yml`) with a step
  `uv run memos doctor`, alongside the existing lint/type/test steps, on push and
  pull request.

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
- The shim check must reuse `shimify`'s path computation; divergence would make
  `doctor` and `shimify` disagree.
- CI must install `uv` before invoking the CLI; pin `setup-uv` to a major version.

## Testing strategy

`pytest` (configured by task 001) over `tmp_path` fixtures:

- `check_shims`: clean fixture → no problems; remove a shim → reported; shim
  without the canon reference → reported; stale shim folder → reported.
- `check_rules_index`: clean fixture → no problems; unindexed `rules/x.md` →
  reported; `AGENTS.md` link to a missing rule → reported.
- Smoke test: `uv run memos doctor` on the real repo exits `0`.
- CI runs `doctor` plus the suite, so a regression turns the check red.
