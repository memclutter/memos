# Spec — 001-migrate-cli-to-package

## Problem

The OS CLI is a single-file PEP-723 script ([scripts/memos](../../../../scripts/memos))
with inline dependencies. It works for `shimify`, but it has hit a ceiling:

- No conventional test setup — testing it means importing a no-extension,
  shebang script via `importlib` and pulling deps in by hand.
- No `ruff`/`mypy` wiring, no dependency lock, no editor/tooling affordances.
- It diverges from the OS's own Python rule, which prescribes a `src/` layout
  with `pyproject.toml` managed by `uv` ([python.md](../../../../rules/python.md)).

This makes the CLI harder to extend (the upcoming `doctor` command, task 002) and
less familiar to contributors.

## Goal

Turn the CLI into a conventional `uv`-managed Python package — `src/` layout,
`pyproject.toml`, `ruff`, `mypy`, `pytest` — invoked as `uv run memos <command>`,
**without changing what `shimify` does**.

## User journeys

- A contributor opens the repo and finds a familiar `pyproject.toml` + `src/memos/`
  package instead of a lone script.
- A developer runs `uv run memos shimify` and gets exactly the same shims as
  before (byte-identical output).
- A developer runs `uv run pytest`, `uv run ruff check`, and `uv run mypy` and all
  pass, with the tooling configured in `pyproject.toml`.

## Success criteria

- `pyproject.toml` exists with project metadata, a `memos` console script entry
  point, the runtime dependency (`pyyaml`), and dev dependencies (`pytest`,
  `ruff`, `mypy`).
- The CLI lives under `src/memos/`; the `shimify` logic is moved over unchanged in
  behaviour.
- `uv run memos shimify` regenerates the existing shims with **no git diff**.
- `uv run pytest` passes (includes at least a test asserting `shimify` output is
  stable), `uv run ruff check` and `uv run mypy` pass.
- The single-file `scripts/memos` no longer holds the logic (removed, or reduced
  to nothing that duplicates the package).
- `rules/scripts.md` and the root `AGENTS.md` scripts entry are updated to the new
  invocation and location.

## Affected spec sections

- `spec/cli.md` — modify: the CLI is now a `uv`-managed package (`src/` layout,
  `pyproject.toml`, `ruff`/`mypy`/`pytest`), invoked as `uv run memos <command>`;
  `shimify` behaviour unchanged.

(Implementation also edits the OS source `rules/scripts.md` and root `AGENTS.md` —
these are договор/source changes for the self-project, not `spec/` deltas; they
land in the same task.)

## Target state

After this task, `spec/cli.md` describes the `memos` CLI as a conventional
`uv`-managed Python package: `src/memos/` layout with `pyproject.toml`, dev
tooling (`ruff`/`mypy`/`pytest`), invoked via `uv run memos <command>`. The
`shimify` command is documented exactly as today (same behaviour), now as part of
the package.

## Out of scope

- No new commands — `doctor` is task 002.
- No change to `shimify`'s behaviour or output.
- No change to skill/shim formats.

## Boundaries

- ✅ Always: keep `shimify` output byte-identical; run `ruff`/`mypy`/`pytest`
  before finishing; follow [python.md](../../../../rules/python.md).
- ⚠️ Ask first: changing the command invocation name or the shim output format.
- 🚫 Never: alter generated shims to make anything pass; break the existing
  `shimify` contract.
