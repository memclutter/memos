# Spec — 003-vcs-submodule-layout

## Problem

Every project pins its git submodule at the same fixed path:
`projects/<name>/repo/`. Two problems follow:

1. **Ambiguity in an AI-IDE.** As more projects come under the OS, the editor
   shows many folders all named `repo` — there's no way to tell which project's
   repository is which at a glance.
2. **One repo per project only.** Some projects are not a single repository (e.g.
   an API repo plus a web repo). A single `repo/` slot can't represent them.

The current rule ([projects.md](../../../rules/projects.md)) hardcodes the single
`repo/` folder, so the layout can't express these cases.

## Goal

Replace the fixed `repo/` submodule with a `vcs/` (version control system)
container: each submodule lives at `projects/<name>/vcs/<repo-name>/`, named after
its GitHub repository. This makes every checkout self-identifying and lets a
project hold one *or several* repositories. The OS-self project (`self: true`)
still has no submodule folder.

## User journeys

- **Identify a repo in the IDE:** the owner opens the workspace, expands a
  project, and sees `vcs/<repo-name>/` — the folder name says exactly which GitHub
  repo it is, even with many projects open at once.
- **Single-repo project:** `dotfiles` keeps its one repository, now at
  `projects/dotfiles/vcs/dotfiles/`. There is no special-case shorter path for
  single-repo projects — the layout is uniform.
- **Multi-repo project:** a project made of several repositories gets one
  subfolder per repo under `vcs/` (e.g. `vcs/<name>-api/`, `vcs/<name>-web/`),
  each an independent submodule pinned by the OS.
- **Start a new project:** `sys.project.specify` adds the submodule under
  `vcs/<repo-name>/` instead of `repo/`, and records the repo(s) in the project's
  `AGENTS.md` metadata.

## Success criteria

- Submodules live at `projects/<name>/vcs/<repo-name>/`; no project uses a `repo/`
  folder. `<repo-name>` equals the GitHub repository name.
- A project may declare one or more repositories, each its own submodule under
  `vcs/`; the project's `AGENTS.md` metadata represents them (one or many).
- `self: true` projects have no `vcs/` folder (source is the OS repo root).
- `sys.project.specify` scaffolds new submodules under `vcs/<repo-name>/`.
- The rules, the root `AGENTS.md` index, and the memos living spec all describe
  the `vcs/` layout consistently — no lingering reference to a `repo/` submodule.
- The existing `dotfiles` submodule is migrated to
  `projects/dotfiles/vcs/dotfiles/` with its history and pinned commit intact.
- `uv run memos doctor` passes against the new layout.

## Affected spec sections

- spec/workflow.md — modify: the **Projects** subsection and its success criterion
  describe submodules under `vcs/<repo-name>/` (one or many) instead of `repo/`;
  the `self: true` note still says "no submodule folder".
- spec/overview.md — modify: the product-wide success criterion that lists project
  anatomy replaces "(plus a `repo/` submodule unless `self: true`)" with the
  `vcs/<repo-name>/` form.

## Target state

After this task ships, the memos living spec describes project VCS as: each
project keeps its repositories as git submodules under
`projects/<name>/vcs/<repo-name>/`, where `<repo-name>` matches the GitHub repo
name; a project may have one or several such repos; `self: true` projects have no
`vcs/` folder. `spec/workflow.md`'s Projects subsection, its success criteria, and
`spec/overview.md`'s anatomy success criterion all use this `vcs/<repo-name>/`
wording with no remaining mention of a fixed `repo/`.

## Out of scope

- Changing how submodule commits are pinned or how source changes are committed —
  only the *location/naming* of the submodule changes, not the workflow.
- Introducing tooling to manage multiple repos beyond what plain git submodules
  already provide.
- Migrating any project other than `dotfiles` (it is the only one with a
  submodule today).

## Boundaries

- ✅ Always: keep submodule history and pinned commits intact during migration;
  keep the rules, the `AGENTS.md` index, and the living spec in sync; verify with
  `uv run memos doctor`.
- ⚠️ Ask first: changing the project `AGENTS.md` frontmatter shape in a way that
  affects existing metadata conventions (the exact key for one-or-many repos is a
  Plan decision — confirm before locking it in).
- 🚫 Never: lose a submodule's git history or its pinned commit; leave the rules
  and spec disagreeing about the layout; hand-edit generated skill shims
  ([skills.md](../../../rules/skills.md)). Reference the global rules
  ([git.md](../../../rules/git.md), [projects.md](../../../rules/projects.md)).
