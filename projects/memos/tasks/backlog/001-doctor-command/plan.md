# Plan — 001-doctor-command

## Approach

Add a `doctor` subcommand to the existing single-file CLI [scripts/memos](../../../../scripts/memos),
reusing the constants and path logic that `shimify` already defines, then wire
`doctor` into a local `pre-commit` hook and a GitHub Actions workflow. Each check
is a pure function that takes the repo root and returns a list of problem strings;
`doctor` runs them all, prints every problem, and exits non-zero if any are found.
This keeps checks unit-testable and lets `doctor` collect all failures in one run.

## Stack

- Python ([python.md](../../../../rules/python.md)), run via `uv` as the existing
  PEP-723 inline-dependency script — **no packaging change**, stays one file with
  `pyyaml` as its only dep.
- `pytest` for tests, run without a project install via
  `uv run --with pytest --with pyyaml pytest`.
- `pre-commit` for the local hook; GitHub Actions for CI (`astral-sh/setup-uv`).

## Architecture

### `doctor` command

- New `cmd_doctor(args)` + subparser registered in `main()` next to `shimify`.
- Reuse module-level `ROOT`, `SKILLS_DIR`, `TOOLS`, and `_load_skills()`. Factor
  the canonical shim path out of `_shim_text` into a small helper so both
  `shimify` and the shim check compute the same path (⚠️ spec boundary: reuse, do
  not fork, that logic).
- Two pure checks, each `(...) -> list[str]` of human-readable problems:

  **`check_shims(root) -> list[str]`**
  - For every `skills/*/` folder and every tool in `TOOLS`, expect
    `<root>/<dirname>/skills/<name>/SKILL.md` to exist and its body to reference
    the canonical `skills/<name>/SKILL.md` (the pointer line shims already carry).
  - Report missing shims, shims that don't reference canon, and **stale** shim
    folders present under a tool dir with no matching canonical skill.

  **`check_rules_index(root) -> list[str]`**
  - Parse `AGENTS.md` for Markdown links to `rules/*.md` (regex over link
    targets).
  - Report any `rules/*.md` file with no linking entry, and any `rules/*.md` link
    in `AGENTS.md` that points to a non-existent file.

- `cmd_doctor` concatenates results, prints a per-check summary (problems or
  "ok"), returns `1` if the combined list is non-empty else `0`.

### pre-commit hook

- Commit `.pre-commit-config.yaml` with a `repos: - repo: local` hook:
  - `id: memos-doctor`, `name: memos doctor`,
    `entry: uv run scripts/memos doctor`, `language: system`,
    `pass_filenames: false`, `always_run: true`.
- Document `pre-commit install` in the project README (hook runs on `git commit`).

### GitHub Actions

- Commit `.github/workflows/ci.yml`, triggers `on: [push, pull_request]`.
- Job on `ubuntu-latest`: `actions/checkout` → `astral-sh/setup-uv` →
  `uv run scripts/memos doctor` → `uv run --with pytest --with pyyaml pytest`.

## Trade-offs & alternatives

- **Unit checks importing the module** (chosen) vs. end-to-end subprocess tests.
  Pure functions taking `root` let tests build tiny fixture repos in `tmp_path`
  and assert on returned problems — fast and precise. The script is imported via
  `importlib.util` from its path (the `# /// script` header is just a comment).
  Subprocess tests would re-run the whole CLI but can't easily point `ROOT` at a
  fixture, so they're kept only as one happy-path smoke test.
- **Keep single-file script** (chosen) vs. promoting `scripts/memos` to a `src/`
  package with `pyproject.toml`. Packaging is heavier than this one command
  warrants; revisit if the CLI keeps growing.
- **`repo: local` system hook** (chosen) vs. a published pre-commit hook repo.
  Local keeps the hook in lockstep with the CLI and needs no release.

## Constraints & risks

- `doctor` must stay **read-only** (spec boundary) — it never writes or fixes.
- The shim check must reuse `shimify`'s path computation; divergence would make
  `doctor` and `shimify` disagree.
- Importing a no-extension, shebang script via `importlib` needs an explicit
  spec/loader; verify in tests. `pyyaml` must be present in the test env (hence
  `--with pyyaml`).
- CI must install `uv` before invoking the script; pin `setup-uv` to a major
  version.

## Testing strategy

Prove the spec's success criteria with `pytest` over `tmp_path` fixtures:

- `check_shims`: clean fixture → no problems; remove a shim → reported; shim
  without the canon reference → reported; stale shim folder → reported.
- `check_rules_index`: clean fixture → no problems; add a `rules/x.md` with no
  `AGENTS.md` entry → reported; add an `AGENTS.md` link to a missing rule →
  reported.
- One smoke test: `uv run scripts/memos doctor` on the real repo exits `0`.
- CI runs both `doctor` and the test suite, so a regression turns the check red.
