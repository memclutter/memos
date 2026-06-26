---
name: sys.project.create
description: Create a new open-source project in the OS — scaffold its
  projects/<name>/ folder (README.md, AGENTS.md, tasks/, docs/), add its GitHub
  repo as the repo/ submodule, and commit. Use when the owner wants to start a
  new project under github.com/memclutter.
category: sys
entity: project
action: create
version: 0.1.0
x-shim:
  claude:
    allowed-tools: Bash, Read, Write, Edit, AskUserQuestion
---

# sys.project.create

Create a new project inside this OS, following [projects.md](../../rules/projects.md).
Talk to the owner in Russian; write every file in English.

## 1. Resolve inputs

- **name** — kebab-case project name (also the GitHub repo name). If not given,
  ask the owner.
- **description** — one sentence, for README/About. If not given, ask.
- **stack** — default to the base stack subset the project needs; confirm with
  the owner if unclear.

Refuse names that already exist under `projects/`.

## 2. Ensure the GitHub repo exists

The submodule needs `git@github.com:memclutter/<name>.git` to exist.

```bash
gh repo view memclutter/<name> >/dev/null 2>&1 \
  || gh repo create memclutter/<name> --public \
       --description "<description>" --add-readme
```

Ask the owner before creating a new public repo.

## 3. Scaffold the folder

```bash
mkdir -p projects/<name>/{tasks/{backlog,active,done},docs}
git submodule add git@github.com:memclutter/<name>.git projects/<name>/repo
touch projects/<name>/tasks/{backlog,active,done}/.gitkeep
```

## 4. Write the project files

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

## 5. Commit

```bash
git add -A
git commit -m "chore(project): add <name>"
```

Then tell the owner (in Russian) what was created and suggest the first task via
`sys.task.specify`.
