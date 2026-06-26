# Skills

`skills/` holds **agent skills** — reusable, named procedures the agent can
invoke instead of re-deriving steps each time. `skills/` is the **canonical**
home; per-tool copies are generated shims (see below).

```
skills/
└── <category>.<entity>.<action>/
    └── SKILL.md      # canonical skill: frontmatter + instructions
```

## Naming

A skill name is `{category}.{entity}.{action}` (lowercase, dot-separated). The
folder is named exactly the same.

- `category` — area the skill belongs to. `sys` = managing this OS itself.
- `entity` — the thing it acts on (`project`, `task`, …).
- `action` — what it does (`create`, …).

Examples:

- `sys.project.specify` — create a project in the OS (folder, `README.md`,
  `AGENTS.md`, `repo/` submodule, `tasks/`, `docs/`) and write its living
  product spec under `spec/`.
- `sys.task.specify` — create a task inside a project and write its `spec.md`.

New categories/entities are added as the OS grows; keep the three-part shape.

## Project-scoped skills resolve the project

A skill that acts on a project (e.g. `sys.task.specify`) takes the project as an
argument. **If it is not provided, the skill scans `projects/` and asks the
owner to pick one** via the available user-question tool before continuing. It
never guesses the project.

## Canonical `SKILL.md` frontmatter

The canonical file carries only **general** metadata — nothing tool-specific:

```markdown
---
name: sys.project.specify
description: Create a new project in the OS — scaffold its folder, README,
  AGENTS.md, repo submodule, tasks, docs, and living product spec.
category: sys
entity: project
action: specify
version: 0.2.0
---

Step-by-step instructions for the agent…
```

The `description` is what an agent matches against to decide relevance — make it
specific. Supporting files (scripts, templates) live alongside `SKILL.md` in the
skill folder.

## Shims for AI IDEs / agents

Different tools discover skills in their own directories. We do **not** maintain
copies by hand — each tool gets a generated **shim** that points back to the
canonical file. A shim is a thin `SKILL.md` whose body says: *read and follow
the canonical instructions at `skills/<name>/SKILL.md`*, carrying no logic of its
own.

Shim targets (one per supported tool):

| Tool        | Shim location                          |
|-------------|----------------------------------------|
| Claude Code | `.claude/skills/<name>/SKILL.md`       |
| Cursor      | `.cursor/skills/<name>/SKILL.md`       |
| OpenCode    | `.opencode/skills/<name>/SKILL.md`     |
| Codex       | `.codex/skills/<name>/SKILL.md`        |

Frontmatter strategy:

- **Canonical** `skills/<name>/SKILL.md` → general fields only.
- **Shim** → general fields **plus** the keys that specific tool understands
  (e.g. Claude's `allowed-tools`). The general fields come from the canonical
  file; the tool-specific keys are added by the generator.

The shim directories are **generated artifacts** — edit the canonical skill, not
the shims.

## Generating shims

Shims are produced by the `shimify` command of the OS CLI, run through `uv`:

```bash
uv run memos shimify          # regenerate all shims for all tools
```

Run it after adding or changing a skill. See [scripts.md](scripts.md) for the
`memos` CLI.

A tool scans its skill directory at startup, not on the fly, so after running
`shimify` **reload skills in your IDE/agent** for new or renamed skills to appear
(in Claude Code: `/reload-skills`, or restart the session).

## Conventions

- Skills are written in English like every other record.
- One folder per skill; folder name == `name` == `{category}.{entity}.{action}`.
- Add a skill when a multi-step job recurs; bump `version` (SemVer) on change.
