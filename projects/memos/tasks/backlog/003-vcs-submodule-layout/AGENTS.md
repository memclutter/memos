---
id: 003-vcs-submodule-layout
status: backlog
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
