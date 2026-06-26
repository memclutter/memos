# Projects

Each open-source project is a separate GitHub repo under `memclutter`. Inside
this OS it lives as one folder under `projects/`, named in kebab-case after the
project.

## Anatomy of a project

```
projects/<project-name>/
├── README.md      # project description for humans
├── AGENTS.md      # project description for the agent (frontmatter metadata)
├── repo/          # the project's git repository, as a git submodule
├── tasks/         # tasks for this project (see tasks.md)
└── docs/          # project documentation
```

- `repo/` is the only git submodule; it points at
  `git@github.com:memclutter/<project-name>.git`. Everything else
  (`README.md`, `AGENTS.md`, `tasks/`, `docs/`) lives in this OS repo and
  describes/drives the project.
- Source changes are made, committed, and pushed **inside `repo/`**; this OS
  repo then pins the new submodule commit with a
  `chore(submodule): bump <project-name>` commit.
- The project's `AGENTS.md` governs project-specific details; the root rules
  govern cross-project conventions.

## Project `AGENTS.md` frontmatter

Metadata lives in YAML frontmatter:

```markdown
---
name: <project-name>
repo: git@github.com:memclutter/<project-name>.git
status: active        # idea | active | paused | archived
stack: [go, postgres, redis, docker]
created: <YYYY-MM-DD>
---

Agent-facing description of the project: purpose, architecture notes,
conventions specific to this project, and anything an agent must know before
working in `repo/`.
```

## Add a project

```bash
mkdir -p projects/<project-name>/{tasks/{backlog,active,done},docs}
git submodule add git@github.com:memclutter/<project-name>.git \
  projects/<project-name>/repo
# then create projects/<project-name>/README.md and AGENTS.md
```

Clone this OS with all submodules:

```bash
git clone --recurse-submodules git@github.com:memclutter/<this-repo>.git
# or, after a plain clone:
git submodule update --init --recursive
```
