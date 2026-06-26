---
name: sys.project.specify
description: Bootstrap or refresh a project's living product spec — scaffold
  projects/<name>/spec/ (overview.md + one file per capability) describing what
  the product does now. The project-level SDD Specify phase. Use to start the
  living spec for a new project or reverse-engineer it for an existing one.
category: sys
entity: project
action: specify
version: 0.1.0
x-shim:
  claude:
    allowed-tools: Bash, Read, Write, Edit, AskUserQuestion
---

# sys.project.specify

The **project-level Specify** phase of [Spec-Driven Development](../../rules/sdd.md):
create the project's **living product spec** under `projects/<name>/spec/` — the
single source of truth for *what the product does now*. Tasks later amend it with
deltas (merge-on-done). Follows [projects.md](../../rules/projects.md). Talk to the
owner in Russian; write every file in English.

> The living spec holds **only shipped reality**. Do not write planned or
> aspirational behaviour here — that belongs in a task's delta `spec.md` until it
> ships. See [sdd.md](../../rules/sdd.md).

## 1. Resolve the project

- If a project was given as an argument, use it.
- Otherwise **scan `projects/`** and ask the owner to pick one via the
  user-question tool. Never guess.

```bash
ls -1 projects/ 2>/dev/null              # the choices to offer
ls -1 projects/<project>/spec/ 2>/dev/null   # does a living spec already exist?
```

If `spec/` already has content, this is a **refresh**: read what's there and
amend it rather than overwriting. If it's empty/absent, this is a **bootstrap**.

## 2. Establish the current truth

The living spec must match reality, so gather it from real sources, not guesses:

- Read the project's `AGENTS.md` (purpose, architecture, conventions) and
  `README.md`.
- For an existing product, inspect `repo/` — entry points, routes/commands,
  models, and any existing docs — to reverse-engineer what it actually does.
- For a brand-new project with no code yet, capture the agreed initial scope
  from the owner; keep it to what the first release will genuinely ship.

Confirm scope and the capability split with the owner before writing.

## 3. Decide the capability split

`spec/` is conceptually one document, physically one file per capability/domain
so it scales. Pick a small set of capability files (e.g. `auth.md`, `search.md`,
`billing.md`) plus the always-present `overview.md`. Prefer few, cohesive files;
split further only when one grows unwieldy.

## 4. Write the living spec

```bash
mkdir -p projects/<project>/spec
```

- `spec/overview.md` — the product as a whole:

  ```markdown
  # <project> — Product spec

  ## Vision
  What the product is and who it's for, in a few sentences.

  ## Capabilities
  Index of the capability files in this spec, one line each.

  ## Product-wide success criteria
  Checkable conditions that hold across the whole product.

  ## Boundaries
  Product-wide ✅ Always / ⚠️ Ask first / 🚫 Never. Reference the global rules
  ([git.md](../../../rules/git.md), [data.md](../../../rules/data.md)); record only
  the project delta.
  ```

- `spec/<capability>.md` — one per capability:

  ```markdown
  # <capability>

  ## Purpose
  What this capability does and why it exists.

  ## Behaviour
  Concrete, current behaviour — user journeys, rules, edge cases. Describe what
  ships today, with examples over prose.

  ## Success criteria
  Checkable conditions specific to this capability.
  ```

Reference the global rules instead of repeating them; write only the
project-specific content.

## 5. Commit

```bash
git add -A
git commit -m "feat(project): specify <project> living spec"
```

For a `self: true` project (the OS itself), the spec lives at
`projects/memos/spec/` and changes commit directly — there is no submodule to
bump.

Then tell the owner (in Russian) where the living spec lives and that tasks will
now be written as deltas against it (`sys.task.specify`), folded back in at Finish
(`sys.task.finish`).
