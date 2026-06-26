# Tasks

Tasks belong to a project. They live under `projects/<project-name>/tasks/`,
split into status folders. **There is no global `tasks/` folder.**

```
projects/<project-name>/tasks/
├── backlog/    # someday / maybe
├── active/     # in progress
└── done/       # finished
    └── 001-add-search/
        ├── README.md   # task description for humans
        ├── AGENTS.md   # task spec for the agent (frontmatter metadata)
        └── log/
            ├── 001-initial-attempt/
            │   └── README.md   # summary + execution artifacts
            └── 002-fix-edge-cases/
                └── README.md
```

## A task is a folder

Named `{NNN}-{task-name-in-kebab-case}`, where `NNN` is a zero-padded sequential
number per project (`001`, `002`, …). Inside:

- `README.md` — the task for humans: goal, scope, acceptance criteria.
- `AGENTS.md` — the task for the agent, with metadata in YAML frontmatter.
- `log/` — execution history. **Each iteration of working the task creates a new
  log folder** `{NNN}-{description-in-kebab-case}` (numbered per task). Artifacts
  of that iteration go inside it, with a `README.md` summary of what was done.

## Task `AGENTS.md` frontmatter

```markdown
---
id: 001-add-search
status: active        # backlog | active | done
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
---

Agent-facing spec: precise goal, scope, acceptance criteria, and constraints.
```

## Lifecycle

1. **Define (постановка).** Create the task folder in `backlog/` with `README.md`
   and `AGENTS.md` (`status: backlog`).
2. **Start.** Move the folder to `active/`; set `status: active`.
3. **Work.** Do the work in the project's `repo/`. Each run/iteration adds a new
   `log/{NNN}-...` folder with its artifacts and a summary `README.md`.
4. **Finish.** Set `status: done`, move the folder to `done/`, and commit. The
   commit is the record — there is no separate log file (see
   [history.md](history.md)).

## Conventions

- Task ID = folder name: `{NNN}-{slug}`. Numbering is per project.
- All task files are in English.
- One task = one logical outcome with checkable acceptance criteria.
