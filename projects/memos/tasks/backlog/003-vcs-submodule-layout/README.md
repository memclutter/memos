# 003 — vcs/ submodule layout

**Goal:** stop putting every project's git submodule at a fixed `repo/`. Move
submodules under a `vcs/` folder, each in a subfolder named after its GitHub
repository, so multiple submodules are unambiguous in an AI-IDE and a project can
hold more than one repository.

**As-is:** one submodule per project at `projects/<name>/repo/`.

**To-be:** submodules live at `projects/<name>/vcs/<repo-name>/`, where
`<repo-name>` is the GitHub repo name. One or more repos per project; `self: true`
projects (the OS itself) have no `vcs/`.

**Scope:**
- Rewrite the rule (`rules/projects.md`) and update every place that names
  `repo/` (`rules/repo-structure.md`, root `AGENTS.md`, `skills/sys.project.specify`).
- Update project `AGENTS.md` metadata to describe one-or-many repos.
- Update `memos doctor` if it validates project layout.
- Migrate the existing project: `projects/dotfiles/repo` → `projects/dotfiles/vcs/dotfiles`.

**Acceptance:**
- `projects/dotfiles/vcs/dotfiles/` is the submodule; no `repo/` remains.
- `sys.project.specify` creates new submodules under `vcs/<repo-name>/`.
- The memos living spec and rules consistently describe the `vcs/` layout.
- `uv run memos doctor` passes.
