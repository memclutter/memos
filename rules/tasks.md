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
        ├── spec.md     # SDD Specify: what & why (user journeys, success criteria)
        ├── plan.md     # SDD Plan: how (stack, architecture, constraints)
        └── log/
            ├── 001-initial-attempt/
            │   └── README.md   # summary + execution artifacts
            └── 002-fix-edge-cases/
                └── README.md
```

Tasks follow [Spec-Driven Development](sdd.md): `spec.md`, `plan.md`, and the
breakdown checklist in `AGENTS.md` are the artifacts of the Specify, Plan, and
Tasks phases; the `log/` folders are the Implement phase.

## A task is a folder

Named `{NNN}-{task-name-in-kebab-case}`, where `NNN` is a zero-padded sequential
number per project (`001`, `002`, …). Inside:

- `README.md` — the task for humans: goal, scope, acceptance criteria.
- `AGENTS.md` — the task for the agent, with metadata in YAML frontmatter; holds
  the SDD **Tasks breakdown** checklist once the task is planned.
- `spec.md` — SDD Specify: what & why (user journeys, success criteria), written
  as a **delta against the project's living spec** (`projects/<name>/spec/`). It
  names the `spec/` sections it changes and their target state; it does not
  re-describe the whole product. See [sdd.md](sdd.md).
- `plan.md` — SDD Plan: how (stack, architecture, constraints). May be skipped
  for small, obvious tasks.
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

1. **Specify (постановка).** `sys.task.specify` creates the task folder in
   `backlog/` with `README.md` and `AGENTS.md` (`status: backlog`) and expands
   the owner's vision into `spec.md`.
2. **Plan.** `sys.task.plan` writes `plan.md` from the spec, stack, and
   constraints (skip for trivial tasks).
3. **Tasks (breakdown).** `sys.task.breakdown` slices spec + plan into a
   reviewable checklist inside `AGENTS.md`.
4. **Start.** Move the folder to `active/`; set `status: active`.
5. **Implement.** Do the work in the project's `repo/`, one chunk at a time. Each
   run/iteration adds a new `log/{NNN}-...` folder with its artifacts and a
   summary `README.md`.
6. **Finish.** `sys.task.finish` folds the task's delta into the project's living
   spec: apply the spec.md `Target state` to `projects/<name>/spec/`, verify
   `repo/` matches the updated spec, set `status: done`, move the folder to
   `done/`, and commit. The done task keeps its delta spec.md as history; the
   commit is the record — there is no separate log file (see
   [history.md](history.md)).

## Conventions

- Task ID = folder name: `{NNN}-{slug}`. Numbering is per project.
- All task files are in English.
- One task = one logical outcome with checkable acceptance criteria.
