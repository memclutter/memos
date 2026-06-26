# Projects

Each open-source project is a separate GitHub repo under `memclutter`. Inside
this OS it lives as one folder under `projects/`, named in kebab-case after the
project.

## Anatomy of a project

```
projects/<project-name>/
├── README.md      # project description for humans
├── AGENTS.md      # project description for the agent (frontmatter metadata)
├── spec/          # the living product spec — current truth (see sdd.md)
│   ├── overview.md     # vision + product-wide success criteria
│   └── <capability>.md # one file per capability/domain
├── repo/          # the project's git repository, as a git submodule
├── tasks/         # tasks for this project (see tasks.md)
└── docs/          # project documentation
```

- `spec/` is the **living product spec**: what the product does *now*, the
  integral of every shipped task. It holds only shipped reality — tasks fold
  their deltas in at the Finish gate ([sdd.md](sdd.md)). `overview.md` carries the
  vision and product-wide success criteria; each capability/domain gets its own
  file so the spec scales while staying conceptually one document. Bootstrap it
  with `sys.project.specify`.
- `repo/` is the only git submodule; it points at
  `git@github.com:memclutter/<project-name>.git`. Everything else
  (`README.md`, `AGENTS.md`, `tasks/`, `docs/`) lives in this OS repo and
  describes/drives the project.
- **Exception — the `memos` project (`self: true`):** the OS manages itself as a
  project too, under `projects/memos/`. A repository cannot contain itself as a
  submodule, so this project has **no `repo/`** — its source is the OS repo root.
  It carries `self: true` in its frontmatter and omits the `repo/` folder; edits
  to OS source are committed directly to this repo (no submodule pointer to bump).
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
self: false           # true only for the OS-self project (no repo/ submodule)
status: active        # idea | active | paused | archived
stack: [go, postgres, redis, docker]
created: <YYYY-MM-DD>
---

Agent-facing description of the project: purpose, architecture notes,
conventions specific to this project, and anything an agent must know before
working in `repo/`.
```

## Add a project

Use the `sys.project.specify` skill — it creates the project and writes its
living spec in one step. Under the hood it does:

```bash
mkdir -p projects/<project-name>/{spec,tasks/{backlog,active,done},docs}
git submodule add git@github.com:memclutter/<project-name>.git \
  projects/<project-name>/repo
# then write projects/<project-name>/README.md and AGENTS.md,
# and the living spec under spec/
```

Clone this OS with all submodules:

```bash
git clone --recurse-submodules git@github.com:memclutter/<this-repo>.git
# or, after a plain clone:
git submodule update --init --recursive
```
