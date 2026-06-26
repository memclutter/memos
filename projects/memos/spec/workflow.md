# Workflow: projects, tasks, and SDD

## Purpose

The OS runs every piece of work the same way: each project is a folder that
mirrors a GitHub repo, work is sliced into tasks, and tasks move through
Spec-Driven Development. This is the operating loop the rest of the OS exists to
support.

## Behaviour

### Projects

- Each project lives under `projects/<name>/` with `README.md` (human),
  `AGENTS.md` (agent + frontmatter), `spec/` (living product spec), `repo/` (git
  submodule), `tasks/`, and `docs/` ([projects.md](../../../rules/projects.md)).
- Source changes are made in `repo/`; this OS repo pins the submodule commit.
- The OS manages itself as the `memos` project with `self: true` — no `repo/`,
  because a repo can't contain itself; its source is the OS repo root and edits
  commit directly.

### Tasks

- Tasks belong to a project under `tasks/{backlog,active,done}/`, each a folder
  `{NNN}-{slug}` with `README.md`, `AGENTS.md`, `spec.md`, optional `plan.md`, and
  a `log/` of execution iterations ([tasks.md](../../../rules/tasks.md)).
- A task is one logical outcome with checkable acceptance criteria.

### Spec-Driven Development

- SDD runs at two altitudes ([sdd.md](../../../rules/sdd.md)): a project is one
  **living spec** (`spec/`), and each task is a **delta** against it.
- Three layers: constitution (`AGENTS.md`) / living product spec (`spec/`) / task
  delta (`tasks/.../spec.md`).
- The task loop is four gated phases — Specify → Plan → Tasks → Implement — driven
  by `sys.task.specify`, `sys.task.plan`, `sys.task.breakdown`.
- A closing **Finish** gate (`sys.task.finish`) folds the task's `Target state`
  into `spec/` (**merge-on-done**), so `spec/` holds only shipped reality.
- Bootstrapping or refreshing a project's living spec is `sys.project.specify`.

## Success criteria

- Every project folder has the full anatomy (`spec/`, `tasks/`, `docs/`, and
  `repo/` unless `self: true`).
- A finished task's delta is reflected in `spec/`, and its folder sits in
  `tasks/done/` with `status: done`.
- The commit history — not a manual journal — is the record of when work happened
  ([history.md](../../../rules/history.md)).
