---
name: sys.task.specify
description: Start a task in a project — scaffold
  projects/<name>/tasks/backlog/<NNN>-<slug>/ (README.md, AGENTS.md, log/) and
  expand the owner's vision into spec.md as a delta against the project's living
  spec (SDD Specify phase). Use when the owner wants to begin a new task.
category: sys
entity: task
action: specify
version: 0.2.0
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

## 1b. Read the living product spec

The task's `spec.md` is a **delta** against the project's living spec, so read it
first to know the current truth you're amending:

```bash
ls -1 projects/<project>/spec/ 2>/dev/null   # capabilities; empty = not bootstrapped
```

Read `spec/overview.md` and any relevant capability files. If `spec/` is missing
or empty, stop and offer to run `sys.project.specify` first — a task can't be a
delta against a spec that doesn't exist.

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

  ## Affected spec sections
  Which files in projects/<project>/spec/ this task changes. For each: path and a
  one-line note (modify / NEW / remove). This is the merge contract checked at
  Finish.
  - spec/<capability>.md — <what changes>
  - spec/overview.md — <e.g. add a success criterion> (if applicable)

  ## Target state
  How the affected spec/ sections must read AFTER this task ships. Write the
  intended end state, not a diff — sys.task.finish applies this to spec/.

  ## Out of scope
  What this task deliberately does not cover.

  ## Boundaries
  - ✅ Always: …
  - ⚠️ Ask first: …
  - 🚫 Never: …
  Reference the global rules; record only the project/task delta.
  ```

  Cross-check `Affected spec sections` against the current `spec/`: flag any
  conflict with another in-flight task and confirm the capability split with the
  owner if the task introduces a new capability file.

## 5. Commit

```bash
git add -A
git commit -m "feat(task): specify <project>/<NNN>-<slug>"
```

Then tell the owner (in Russian) the task ID, where it lives, and suggest the
next phase: `sys.task.plan`.
