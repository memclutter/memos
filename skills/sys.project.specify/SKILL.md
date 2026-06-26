---
name: sys.project.specify
description: Create a project and write its living product spec in one step —
  scaffold projects/<name>/ (README.md, AGENTS.md, repo/ submodule, tasks/, docs/)
  and projects/<name>/spec/ (overview.md + one file per capability) describing
  what the product does now. The project-level SDD Specify phase. Use to start a
  new project or to refresh an existing project's living spec.
category: sys
entity: project
action: specify
version: 0.2.1
x-shim:
  claude:
    allowed-tools: Bash, Read, Write, Edit, AskUserQuestion
---

# sys.project.specify

The **project-level Specify** phase of [Spec-Driven Development](../../rules/sdd.md):
bring a project into being and give it a **living product spec** under
`projects/<name>/spec/` — the single source of truth for *what the product does
now*. Tasks later amend it with deltas (merge-on-done). One skill creates the
project and specs it; there is no separate create step. Follows
[projects.md](../../rules/projects.md). Talk to the owner in Russian; write every
file in English.

> The living spec holds **only shipped reality**. Do not write planned or
> aspirational behaviour here — that belongs in a task's delta `spec.md` until it
> ships. See [sdd.md](../../rules/sdd.md).

## 1. Which starting state?

```bash
ls -1 projects/ 2>/dev/null   # existing project folders under this OS
```

Three cases, distinguished by whether the project folder and the GitHub repo
already exist:

- **Refresh** — the project already lives under `projects/<name>/`. Skip step 2;
  go to step 3 to amend its living spec. (Scan and ask via the user-question
  tool; never guess which project.)
- **Import** — no `projects/<name>/` folder yet, but the GitHub repo already
  exists (the owner is bringing an existing repo under this OS). Do step 2 — its
  `gh repo view … || gh repo create` guard skips creation, and `git submodule
  add` pulls in the existing repo — then reverse-engineer the spec from `repo/`
  in step 3.
- **New** — neither the folder nor the repo exists. Do step 2 to create the repo
  and scaffold, then step 3.

```bash
ls -1 projects/<project>/spec/ 2>/dev/null   # does a living spec already exist?
```

If `spec/` already has content, step 3 is a **refresh**: read it and amend rather
than overwrite. If it's empty/absent (New or Import), it's a **bootstrap**.

## 2. Create or import the project (New and Import)

Resolve inputs, refusing a `name` that already exists under `projects/`. For an
**Import**, the repo already holds reality — `description`/`stack` should reflect
what's actually there:

- **name** — kebab-case project name (also the GitHub repo name). If not given, ask.
- **description** — one sentence for README/About. If not given, ask.
- **stack** — the [base stack](../../rules/stack.md) subset the project needs;
  confirm if unclear.

Ensure the GitHub repo exists (ask the owner before creating a public repo):

```bash
gh repo view memclutter/<name> >/dev/null 2>&1 \
  || gh repo create memclutter/<name> --public \
       --description "<description>" --add-readme
```

Scaffold the folder and submodule:

```bash
mkdir -p projects/<name>/{spec,tasks/{backlog,active,done},docs}
git submodule add git@github.com:memclutter/<name>.git projects/<name>/repo
touch projects/<name>/tasks/{backlog,active,done}/.gitkeep
```

Write the project files (see [projects.md](../../rules/projects.md)):

- `projects/<name>/README.md` — human-facing: what the project is, how to run it
  locally (Docker), how it fits the OS.
- `projects/<name>/AGENTS.md` — agent-facing, with frontmatter exactly as in
  [projects.md](../../rules/projects.md):

  ```markdown
  ---
  name: <name>
  repo: git@github.com:memclutter/<name>.git
  status: active
  stack: [<stack>]
  created: <YYYY-MM-DD>
  ---

  Purpose, architecture notes, and project-specific conventions.
  ```

## 3. Establish the current truth

The living spec must match reality, so gather it from real sources, not guesses:

- Read the project's `AGENTS.md` (purpose, architecture, conventions) and
  `README.md`.
- For an existing product, inspect `repo/` — entry points, routes/commands,
  models, and any existing docs — to reverse-engineer what it actually does.
- For a brand-new project with no code yet, capture the agreed initial scope
  from the owner; keep it to what the first release will genuinely ship.

Confirm scope and the capability split with the owner before writing.

## 4. Decide the capability split

`spec/` is conceptually one document, physically one file per capability/domain
so it scales. Pick a small set of capability files (e.g. `auth.md`, `search.md`,
`billing.md`) plus the always-present `overview.md`. Prefer few, cohesive files;
split further only when one grows unwieldy.

## 5. Write the living spec

`projects/<project>/spec/` already exists from step 2 (or from an earlier run).

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

## 6. Commit

```bash
git add -A
git commit -m "feat(project): specify <project>"     # new project + its living spec
# or, refreshing an existing project's spec:
git commit -m "feat(project): refresh <project> living spec"
```

For a `self: true` project (the OS itself), the spec lives at
`projects/memos/spec/` and changes commit directly — there is no `repo/` submodule
to add.

Then tell the owner (in Russian) where the living spec lives and that tasks will
now be written as deltas against it (`sys.task.specify`), folded back in at Finish
(`sys.task.finish`).
