# Rules

## Purpose

The rules are the OS's single source of truth for conventions — language, repo
structure, stack, project/task layout, SDD, skills, scripts, history, git, and
the per-language/tooling standards. Agents read the relevant rule before acting
on its topic, so behaviour stays consistent across every project.

## Behaviour

- `AGENTS.md` at the repo root is the **index of the rules**: one paragraph per
  file in `rules/`, each ending with a `Details → rules/<file>.md` link.
  `CLAUDE.md` is a thin pointer to `AGENTS.md`.
- `rules/` holds one focused file per topic. The index and `rules/` are kept in
  sync: when a file is added, removed, or renamed, its `AGENTS.md` entry changes
  too.
- Current rule files: `language`, `repo-structure`, `stack`, `projects`, `tasks`,
  `sdd`, `skills`, `scripts`, `history`, `workflow`, `git`, `go`, `python`,
  `vue`, `docker`, `data`.
- Rules describe conventions, not events; the commit history records when things
  happened ([history.md](../../../rules/history.md)).

## Success criteria

- Every file in `rules/` has exactly one matching entry in `AGENTS.md`, and every
  entry links to an existing file.
- A reader can find the rule for any topic from the index in one hop.
- Rules are written in English ([language.md](../../../rules/language.md)).
