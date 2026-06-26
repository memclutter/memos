# Spec — 002-doctor-command

## Problem

The OS has two consistency invariants that are easy to break silently:

- Skill shims under `.claude/`, `.cursor/`, `.codex/`, `.opencode/` must exist for
  every canonical skill and point back to `skills/<name>/SKILL.md`. A skill added
  without running `shimify`, or a deleted skill leaving stale shims, drifts
  unnoticed.
- Every rule file in `rules/` must be retold in the `AGENTS.md` index with a link
  to the full rule. A new/renamed rule with no index entry (or a broken link)
  breaks the "index ↔ rules/" guarantee.

Today nothing checks these; you find out only when something is already wrong.

## Goal

A `memos doctor` subcommand that runs both consistency checks, reports every
problem it finds, and exits non-zero if any check fails — a single health gate for
the OS. The gate is wired in **two places**: a local `pre-commit` hook that runs
`doctor` before each commit, and a GitHub Actions workflow that runs it on push
and pull request.

## User journeys

- The owner (or CI) runs `uv run memos doctor`. On a clean repo it prints
  an OK summary and exits 0.
- After adding a skill but forgetting `shimify`, `doctor` lists the missing shims
  per tool and exits non-zero.
- After adding `rules/foo.md` without an `AGENTS.md` entry, `doctor` reports the
  unindexed rule and exits non-zero. A broken `rules/*.md` link in the index is
  reported the same way.
- The owner tries to commit a change that breaks an invariant; the `pre-commit`
  hook runs `doctor`, fails, and blocks the commit until it's fixed.
- A push or pull request triggers the GitHub Actions workflow, which runs
  `doctor`; a red check signals the OS is inconsistent.

## Success criteria

- `uv run memos doctor` exits 0 on the current (clean) repo.
- **Shim check:** for every folder in `skills/`, a shim exists in each of
  `.claude/skills/<name>/`, `.cursor/skills/<name>/`, `.codex/skills/<name>/`,
  `.opencode/skills/<name>/`, and each shim references the canonical
  `skills/<name>/SKILL.md`. Missing or non-referencing shims are reported and
  cause a non-zero exit. (Stale shims with no canonical skill are reported too.)
- **Rules check:** every `rules/*.md` file has at least one linking entry in
  `AGENTS.md`, and every `rules/*.md` link in `AGENTS.md` resolves to an existing
  file. Violations are reported and cause a non-zero exit.
- All problems are collected and printed in one run (checks don't stop at the
  first failure).
- The command is covered by tests.
- **pre-commit:** a committed `.pre-commit-config.yaml` defines a hook that runs
  `uv run memos doctor`; with pre-commit installed, a commit that breaks
  an invariant is blocked.
- **CI:** a committed GitHub Actions workflow runs `uv run memos doctor`
  on push and pull request, and fails the job on a non-zero exit.

## Affected spec sections

- `spec/cli.md` — add `doctor` to the list of current commands (modify).
- `spec/skills.md` — note that the "shims in sync, never hand-edited" success
  criterion is now verifiable via `memos doctor` (modify).
- `spec/rules.md` — note that the "index ↔ rules/ in sync" success criterion is
  now verifiable via `memos doctor` (modify).
- `spec/ci.md` — NEW capability: automated enforcement (pre-commit hook + GitHub
  Actions) that runs `doctor`.
- `spec/overview.md` — add `ci.md` to the capabilities index (modify).

## Target state

After this task:

- `spec/cli.md` lists `doctor` alongside `shimify`, describing it as the
  consistency-check command (shims present & referencing canon; rules indexed with
  working links) that exits non-zero on any failure.
- `spec/skills.md` success criteria mention that shim-sync is checkable with
  `memos doctor`.
- `spec/rules.md` success criteria mention that index↔rules sync is checkable with
  `memos doctor`.
- `spec/ci.md` exists and describes: the local `pre-commit` hook running `doctor`,
  the GitHub Actions workflow running `doctor` on push and PR, and the success
  criterion that the OS is consistent on every commit and green in CI.
- `spec/overview.md` lists `ci.md` in its capabilities index.

## Out of scope

- No auto-fixing — `doctor` only reports (a `--fix` flag may be a later task).
- No checks beyond the two above (e.g. frontmatter validation, link-checking
  inside rule bodies) — future additions.

## Boundaries

- ✅ Always: run `doctor` and `pytest` before finishing; follow
  [python.md](../../../../rules/python.md).
- ⚠️ Ask first: changing how `shimify` computes shim paths (doctor should reuse,
  not fork, that logic).
- 🚫 Never: have `doctor` modify files; never hand-edit shims to make the check
  pass.

---

**Assumptions to confirm at the gate** (chosen as defaults, not specified by the
owner): read-only (report, no fix); exits non-zero on any failure; collects all
problems rather than failing fast; "references canon" means the shim body links to
`skills/<name>/SKILL.md`.
