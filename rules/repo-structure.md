# Repo structure

This repository is a **personal operating system** for running open-source
projects under [github.com/memclutter](https://github.com/memclutter). It holds
no application code of its own — only the rules, the projects (as submodules),
and the agent skills.

```
.
├── AGENTS.md          # index of the rules (one paragraph per rule file)
├── CLAUDE.md          # pointer to AGENTS.md
├── rules/             # the rules — one file per topic
├── skills/            # agent skills available to the agent here
└── projects/          # open-source projects, one folder per project
```

- `rules/` is the single source of truth for how we work. `AGENTS.md` is its
  index; keep them in sync — when a rule file is added, removed, or renamed,
  update `AGENTS.md`.
- `skills/` holds agent skills — see [skills.md](skills.md).
- `projects/` holds one folder per project; each project owns its tasks and
  docs. There is **no global `tasks/` folder.** See [projects.md](projects.md)
  and [tasks.md](tasks.md).
