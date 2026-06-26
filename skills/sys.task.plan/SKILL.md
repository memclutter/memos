---
name: sys.task.plan
description: Write a task's plan.md from its spec — the SDD Plan phase. Turn the
  owner's stack, architecture, and constraints into a technical plan for an
  existing task. Use after sys.task.specify, before sys.task.breakdown.
category: sys
entity: task
action: plan
version: 0.1.0
x-shim:
  claude:
    allowed-tools: Bash, Read, Write, AskUserQuestion
---

# sys.task.plan

The **Plan** phase of [Spec-Driven Development](../../rules/sdd.md): turn an
existing task's `spec.md` into a technical `plan.md`. Talk to the owner in
Russian; write every file in English.

Trivial tasks may skip planning — say so and stop if a `plan.md` would add
nothing.

## 1. Locate the task

- Resolve the project (scan `projects/` and ask if not given — never guess).
- Find the task folder under `tasks/{backlog,active}/<NNN>-<slug>/`. If the slug
  is ambiguous, list candidates and ask.
- **Read `spec.md` first.** If it is missing, stop and point to
  `sys.task.specify`.

## 2. Gather technical inputs

From the owner and the project's `AGENTS.md` / global rules:

- **Stack** — default to the [base stack](../../rules/stack.md); confirm
  deviations.
- **Architecture** — components, data flow, key interfaces.
- **Constraints** — performance, compatibility, deadlines, things to avoid.

The plan answers **how**; it must satisfy the spec's **what & why**. Reference
the global rules ([go.md](../../rules/go.md), [python.md](../../rules/python.md),
[data.md](../../rules/data.md), …) instead of repeating them.

## 3. Write plan.md

```markdown
# Plan — <NNN>-<slug>

## Approach
The chosen strategy in a few sentences, and why.

## Stack
What we use and any deviation from the base stack (with reason).

## Architecture
Components, data flow, interfaces, schema/migrations.

## Trade-offs & alternatives
What we considered and rejected, and why.

## Constraints & risks
Performance, compatibility, security, deadlines; known risks.

## Testing strategy
How we will prove the success criteria from spec.md are met.
```

## 4. Commit

```bash
git add -A
git commit -m "feat(task): plan <project>/<NNN>-<slug>"
```

Then tell the owner (in Russian) the plan is ready and suggest the next phase:
`sys.task.breakdown`.
