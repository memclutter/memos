---
name: sys.task.breakdown
description: Slice a task's spec and plan into a reviewable checklist of small
  steps inside its AGENTS.md — the SDD Tasks phase. Use after sys.task.plan,
  before implementation begins.
category: sys
entity: task
action: breakdown
version: 0.1.0
x-shim:
  claude:
    allowed-tools: Bash, Read, Write, Edit, AskUserQuestion
---

# sys.task.breakdown

The **Tasks** phase of [Spec-Driven Development](../../rules/sdd.md): slice an
existing task's `spec.md` and `plan.md` into a checklist of small, reviewable
steps, written into the task's `AGENTS.md`. Talk to the owner in Russian; write
every file in English.

## 1. Locate the task

- Resolve the project (scan `projects/` and ask if not given — never guess).
- Find the task folder under `tasks/{backlog,active}/<NNN>-<slug>/`.
- **Read `spec.md` and `plan.md` first.** If `spec.md` is missing, stop and point
  to `sys.task.specify`; if `plan.md` is missing on a non-trivial task, suggest
  `sys.task.plan`.

## 2. Slice into steps

- Each step is **small and independently reviewable** — one logical change.
- Don't mix unrelated concerns in one step (e.g. auth and schema changes).
- Order by dependency; note where a step is a ⚠️ gate that needs owner approval
  (per the spec's boundaries).
- Each step should trace back to a success criterion in `spec.md`.

## 3. Write the checklist into AGENTS.md

Append a section to the task's `AGENTS.md` (keep the existing frontmatter):

```markdown
## Tasks breakdown

- [ ] 1. <small, reviewable step>
- [ ] 2. <next step>
- [ ] 3. <next step>  ⚠️ ask owner before applying
```

The agent ticks boxes as it implements; each box maps to one or more `log/`
iterations.

## 4. Commit

```bash
git add -A
git commit -m "feat(task): break down <project>/<NNN>-<slug>"
```

Then tell the owner (in Russian) the breakdown is ready. To start implementing,
move the folder to `active/` and set `status: active` (see
[tasks.md](../../rules/tasks.md)).
