---
name: sys.task.finish
description: Close a task — fold its delta spec.md Target state into the project's
  living spec (projects/<name>/spec/), verify repo/ matches, flip status to done,
  move the folder to done/, and commit. The SDD merge-on-done Finish gate. Use
  when a task's implementation is complete and validated.
category: sys
entity: task
action: finish
version: 0.1.0
x-shim:
  claude:
    allowed-tools: Bash, Read, Write, Edit, AskUserQuestion
---

# sys.task.finish

The **Finish** gate of [Spec-Driven Development](../../rules/sdd.md): merge a
completed task's delta into the project's **living product spec**, then close the
task. This is where `spec/` catches up to shipped reality (merge-on-done).
Follows [tasks.md](../../rules/tasks.md). Talk to the owner in Russian; write
every file in English.

> Only finish a task whose work is actually done and validated. If acceptance
> criteria aren't met, stop and say so — don't merge an unfinished delta.

## 1. Locate the task

- Resolve the project (scan `projects/` and ask if not given — never guess).
- Find the task under `tasks/active/<NNN>-<slug>/` (a task being finished should be
  `active`). If it's still in `backlog/`, point out it hasn't been started.
- **Read its `spec.md`**, especially `Affected spec sections` and `Target state`.

## 2. Verify the work matches the spec

- Confirm each `Success criterion` in `spec.md` is met. Where the project's
  rules define checks (tests, lint), run them in `repo/` and require green.
- Confirm the implementation in `repo/` actually delivers the `Target state`.
- If anything is unmet, stop and report it to the owner — do not proceed.

## 3. Merge the delta into the living spec

Apply the `Target state` to `projects/<project>/spec/`, section by section as
listed in `Affected spec sections`:

- **modify** — edit the named capability/overview file to the target state.
- **NEW** — create the new capability file; add it to the index in
  `spec/overview.md`.
- **remove** — delete behaviour no longer true; remove it from the index.

After merging, `spec/` must describe the product *as it now is* — only shipped
reality, no leftover planned wording. The task's own `spec.md` stays in the task
folder as the historical delta.

## 4. Close the task

```bash
# set status: done and the updated date in the task's AGENTS.md frontmatter,
# then move the folder
git mv projects/<project>/tasks/active/<NNN>-<slug> \
       projects/<project>/tasks/done/<NNN>-<slug>
```

Update the task `AGENTS.md` frontmatter: `status: done` and `updated: <today>`.

## 5. Commit

One commit captures both the spec merge and the task close:

```bash
git add -A
git commit -m "feat(task): finish <project>/<NNN>-<slug>"
```

For a non-`self` project, the implementation commits live in `repo/`; if `repo/`
advanced, also bump the submodule pointer with a
`chore(submodule): bump <project>` commit (see [projects.md](../../rules/projects.md)).
The commit is the record — there is no separate log file ([history.md](../../rules/history.md)).

Then tell the owner (in Russian) that the task is done and the living spec is
updated.
