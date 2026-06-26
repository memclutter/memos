# memos — Product spec

The "product" of the `memos` project is **the OS itself**: a personal operating
system for running open-source projects under
[github.com/memclutter](https://github.com/memclutter). It ships no application
code — only the rules, the agent skills, the helper scripts, and the project/task
structure that make work across projects consistent and agent-friendly.

This is the living spec: what the OS does **now**. It references the rules in
[rules/](../../../rules/) instead of restating them — the rules are the detailed
договор, this spec is the product-level view of current capabilities.

## Vision

Give the owner and AI agents a single, version-controlled home where every
project is run the same way: written rules as the source of truth, reusable
skills for recurring procedures, and Spec-Driven Development so the spec — not
chat history — is what's authoritative. The OS manages itself as a project too
(`self: true`), so it improves through its own workflow.

## Capabilities

- [rules.md](rules.md) — the rules corpus and its index (`AGENTS.md` → `rules/`).
- [skills.md](skills.md) — canonical agent skills and the per-tool shims.
- [workflow.md](workflow.md) — projects, tasks, and the two-level SDD loop.
- [cli.md](cli.md) — the `memos` CLI that maintains the OS.

## Product-wide success criteria

- `AGENTS.md` indexes every file in `rules/` with one paragraph and a link; the
  index and `rules/` stay in sync. `CLAUDE.md` points at `AGENTS.md`.
- Every canonical skill in `skills/` has generated shims for all supported tools
  (Claude, Cursor, Codex, OpenCode), regenerable with one command and never
  hand-edited.
- Every project lives under `projects/<name>/` with `README.md`, `AGENTS.md`,
  `spec/`, `tasks/`, and `docs/` (plus a `repo/` submodule unless `self: true`).
- Work flows through SDD; each project's `spec/` reflects **only shipped
  reality** (merge-on-done).
- All on-disk artifacts are in English; conversation with the owner is in
  Russian ([language.md](../../../rules/language.md)).

## Boundaries

Reference the global rules; recorded here is only the OS-wide delta.

- ✅ **Always** — Conventional Commits ([git.md](../../../rules/git.md)); regenerate
  shims after changing a skill; keep the rules index in sync with `rules/`.
- ⚠️ **Ask first** — creating a new public GitHub repo; adding a tool outside the
  [base stack](../../../rules/stack.md).
- 🚫 **Never** — hand-edit generated shims; commit secrets; keep a manual work
  journal (git history is the log, [history.md](../../../rules/history.md)).
