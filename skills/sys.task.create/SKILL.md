---
name: sys.task.create
description: Create a new task inside a project — pick the project (ask the owner
  if not given), allocate the next NNN, and scaffold
  projects/<name>/tasks/backlog/<NNN>-<slug>/ with README.md, AGENTS.md, and a
  log/ folder. Use when the owner wants to add a task to a project.
category: sys
entity: task
action: create
version: 0.1.0
x-shim:
  claude:
    allowed-tools: Bash, Read, Write, AskUserQuestion
---

# sys.task.create

Create a new task inside a project, following [tasks.md](../../rules/tasks.md).
Talk to the owner in Russian; write every file in English.

## 1. Resolve the project

- If a project was given as an argument, use it.
- Otherwise **scan `projects/`** for existing project folders and ask the owner
  to pick one via the user-question tool. Never guess.
- If there are no projects yet, stop and offer to run `sys.project.create`
  first.

```bash
ls -1 projects/ 2>/dev/null   # the choices to offer
```

## 2. Resolve task inputs

- **slug** — short kebab-case task name. If not given, ask.
- **goal / scope / acceptance criteria** — gather from the owner; keep criteria
  checkable.

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

Write the two files:

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

## 5. Commit

```bash
git add -A
git commit -m "chore(task): add <project>/<NNN>-<slug>"
```

Then tell the owner (in Russian) the task ID and where it lives. Starting work
later means moving the folder to `active/` and setting `status: active`.
