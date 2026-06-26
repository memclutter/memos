# Spec — 001-doctor-command

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
the OS.

## User journeys

- The owner (or CI) runs `uv run scripts/memos doctor`. On a clean repo it prints
  an OK summary and exits 0.
- After adding a skill but forgetting `shimify`, `doctor` lists the missing shims
  per tool and exits non-zero.
- After adding `rules/foo.md` without an `AGENTS.md` entry, `doctor` reports the
  unindexed rule and exits non-zero. A broken `rules/*.md` link in the index is
  reported the same way.

## Success criteria

- `uv run scripts/memos doctor` exits 0 on the current (clean) repo.
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

## Affected spec sections

- `spec/cli.md` — add `doctor` to the list of current commands (modify).
- `spec/skills.md` — note that the "shims in sync, never hand-edited" success
  criterion is now verifiable via `memos doctor` (modify).
- `spec/rules.md` — note that the "index ↔ rules/ in sync" success criterion is
  now verifiable via `memos doctor` (modify).

## Target state

After this task:

- `spec/cli.md` lists `doctor` alongside `shimify`, describing it as the
  consistency-check command (shims present & referencing canon; rules indexed with
  working links) that exits non-zero on any failure.
- `spec/skills.md` success criteria mention that shim-sync is checkable with
  `memos doctor`.
- `spec/rules.md` success criteria mention that index↔rules sync is checkable with
  `memos doctor`.

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
