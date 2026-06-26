---
id: 003-vcs-submodule-layout
status: done
created: 2026-06-26
updated: 2026-06-26
---

Change the project structure rule so git submodules no longer live at a fixed
`projects/<name>/repo/` but under `projects/<name>/vcs/<repo-name>/`, where
`<repo-name>` is the GitHub repository name. This disambiguates submodules in an
AI-IDE (no more many folders all called `repo`) and lets one project hold several
repositories. `self: true` projects keep having no submodule folder.

Touches the rules (`rules/projects.md`, `rules/repo-structure.md`), the root
`AGENTS.md` index, the `sys.project.specify` skill, project `AGENTS.md` metadata
(one-or-many repos), and `memos doctor` if it checks layout. Includes migrating
the existing `projects/dotfiles/repo` submodule to `projects/dotfiles/vcs/dotfiles`.
Acceptance: no `repo/` submodule remains, new projects scaffold under
`vcs/<repo-name>/`, spec and rules agree, and `uv run memos doctor` passes.

## Tasks breakdown

- [x] 1. Rewrite `rules/projects.md`: anatomy diagram and prose use
  `projects/<name>/vcs/<repo-name>/` (one or many repos), the `vcs:` frontmatter
  list, the `self: true` exception (no `vcs/` folder), and the "Add a project"
  snippet `git submodule add <url> projects/<name>/vcs/<repo-name>`.
- [x] 2. Reword the `repo/` references in `rules/repo-structure.md` and the
  **Projects** paragraph of the root `AGENTS.md` to the `vcs/<repo-name>/` layout.
- [x] 3. Update the `sys.project.specify` skill: step 2 submodule path →
  `vcs/<repo-name>/` and the frontmatter template `repo:` → `vcs:` list; bump its
  `version`. Then run `uv run memos shimify` (never hand-edit shims).
- [x] 4. Convert project metadata to the `vcs:` array: `projects/dotfiles/AGENTS.md`
  (+ `README.md` `repo/` refs) and `projects/memos/AGENTS.md` (self note: `vcs:`
  URL but no `vcs/` folder).
- [x] 5. Migrate the submodule: `git mv projects/dotfiles/repo
  projects/dotfiles/vcs/dotfiles`; verify `.gitmodules` path **and** section name
  are updated and `git submodule status` shows the same pinned commit (`2b334c0`).
- [x] 6. Add `check_project_layout` to `scripts/memos/src/memos/doctor.py` and
  register it in `_CHECKS`: every non-`self` project has no `repo/` and all its
  `.gitmodules` paths sit under `projects/<name>/vcs/`.
- [x] 7. Cover the check in `scripts/memos/tests/test_doctor.py` (healthy `vcs/`
  passes, a `repo/` path fails); run `uv run ruff check`, `uv run mypy`,
  `uv run pytest` green.
- [x] 8. Verify end to end: repo-wide grep finds no stale `repo/` submodule
  references; `uv run memos doctor` passes; `git submodule update --init` (fresh)
  populates `vcs/dotfiles/`.
