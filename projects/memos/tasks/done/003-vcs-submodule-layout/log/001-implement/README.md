# 001 — implement vcs/ submodule layout

All 8 breakdown steps implemented. Summary of what was done and verified.

## Done

- **Rules & index** — `rules/projects.md` rewritten (anatomy with
  `vcs/<repo-name>/`, `vcs:` frontmatter list, `self: true` exception, add-a-project
  snippet); `repo/` references reworded in the root `AGENTS.md`,
  `rules/tasks.md`, `rules/sdd.md`, `rules/skills.md`.
- **Skills** — `sys.project.specify` (submodule path + `vcs:` frontmatter template,
  description, Import/self body), `sys.task.finish`, and `sys.project.release`
  updated to the `vcs/<repo-name>/` layout; versions bumped; shims regenerated
  with `uv run memos shimify`.
- **Project metadata** — `projects/dotfiles/AGENTS.md` + `README.md` and
  `projects/memos/AGENTS.md` + `README.md` converted to the `vcs:` array and `vcs/`
  wording.
- **Migration** — `git mv projects/dotfiles/repo projects/dotfiles/vcs/dotfiles`;
  `.gitmodules` path **and** section name renamed to
  `projects/dotfiles/vcs/dotfiles`; pinned commit `2b334c0` (v0.0.1) and history
  intact.
- **Doctor** — added `check_project_layout` to `doctor.py` (registered in
  `_CHECKS`): flags any non-`self` project that keeps a legacy `repo/` folder or
  has a `.gitmodules` path outside `projects/<name>/vcs/`. Covered by four tests
  in `test_doctor.py` plus the smoke test.

## Verified

- `uv run memos doctor` → all checks pass (shims, rules index, project layout).
- `uv run ruff check` / `uv run mypy` / `uv run pytest` → green (15 tests).
- `git submodule status` → `projects/dotfiles/vcs/dotfiles` at `2b334c0` (v0.0.1).
- Repo-wide grep → no stale `repo/` submodule references outside the memos living
  spec (folded at Finish) and this task's own docs.

## Note

The breakdown under-scoped the documentation ripple: `repo/` also lived in
`rules/tasks.md`, `rules/sdd.md`, `rules/skills.md`, both READMEs, and three
skills' text. All were updated here so the rules and skills describe `vcs/`
consistently, as the spec requires.

## Next

Finish gate (`sys.task.finish`): fold the Target state into
`projects/memos/spec/` (`workflow.md`, `overview.md`, `cli.md`), which still
carry the `repo/` wording by design until merge-on-done.
