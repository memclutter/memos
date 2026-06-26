---
name: sys.task.specify
description: Start a task in a project — scaffold
  projects/<name>/tasks/backlog/<NNN>-<slug>/ (README.md, AGENTS.md, log/) and
  expand the owner's vision into spec.md (SDD Specify phase). Use when the owner
  wants to begin a new task.
category: sys
entity: task
action: specify
version: 0.1.0
x-shim:
  claude:
    allowed-tools: Bash, Read, Write, AskUserQuestion
---

# sys.task.specify

The **Specify** phase of [Spec-Driven Development](../../rules/sdd.md): create the
task folder and turn the owner's vision into a written `spec.md`. Follows
[tasks.md](../../rules/tasks.md). Talk to the owner in Russian; write every file
in English.

## 1. Resolve the project

- If a project was given as an argument, use it.
- Otherwise **scan `projects/`** for existing project folders and ask the owner
  to pick one via the user-question tool. Never guess.
- If there are no projects yet, stop and offer to run `sys.project.create`
  first.

```bash
ls -1 projects/ 2>/dev/null   # the choices to offer
```

## 2. Gather the vision

- **slug** — short kebab-case task name. If not given, ask.
- **vision** — what the owner wants and why. Ask for the problem, the desired
  outcome, and who it is for. Keep digging until you can write user journeys and
  checkable success criteria. Specify captures **what & why**, not *how* — leave
  stack and architecture for `sys.task.plan`.

## 3. Allocate the next number

`NNN` is zero-padded and sequential **per project**, across all status folders.

```bash
ls -d projects/<project>/tasks/{backlog,active,done}/[0-9]*-* 2>/dev/null \
  | sed -E 's#.*/([0-9]+)-.*#\1#' | sort -n | tail -1
# next = that + 1, zero-padded to 3 digits (001, 002, ...)
```

## 4. Scaffold the task folder

New tasks start in `backlog/`.

```bash
mkdir -p projects/<project>/tasks/backlog/<NNN>-<slug>/log
touch projects/<project>/tasks/backlog/<NNN>-<slug>/log/.gitkeep
```

Write the files:

- `README.md` — human-facing: title, goal, scope, acceptance criteria.
- `AGENTS.md` — agent-facing, with frontmatter exactly as in
  [tasks.md](../../rules/tasks.md):

  ```markdown
  ---
  id: <NNN>-<slug>
  status: backlog
  created: <YYYY-MM-DD>
  updated: <YYYY-MM-DD>
  ---

  Precise goal, scope, acceptance criteria, and constraints for the agent.
  ```

- `spec.md` — the Specify artifact:

  ```markdown
  # Spec — <NNN>-<slug>

  ## Problem
  What hurts today and why it matters.

  ## Goal
  The outcome we want, in one or two sentences.

  ## User journeys
  Concrete flows from the user's point of view.

  ## Success criteria
  Checkable conditions that say the task is done.

  ## Out of scope
  What this task deliberately does not cover.

  ## Boundaries
  - ✅ Always: …
  - ⚠️ Ask first: …
  - 🚫 Never: …
  Reference the global rules; record only the project/task delta.
  ```

## 5. Commit

```bash
git add -A
git commit -m "feat(task): specify <project>/<NNN>-<slug>"
```

Then tell the owner (in Russian) the task ID, where it lives, and suggest the
next phase: `sys.task.plan`.
