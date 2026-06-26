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
├── skills/            # agent skills (canonical) available to the agent here
├── scripts/           # helper scripts that keep the OS running (memos CLI)
├── projects/          # open-source projects, one folder per project
└── .claude/ .cursor/ .opencode/ .codex/   # generated skill shims (do not edit)
```

- `rules/` is the single source of truth for how we work. `AGENTS.md` is its
  index; keep them in sync — when a rule file is added, removed, or renamed,
  update `AGENTS.md`.
- `skills/` holds the canonical agent skills; per-tool `.claude/`, `.cursor/`,
  `.opencode/`, `.codex/` directories hold **generated shims** — see
  [skills.md](skills.md).
- `scripts/` holds the `memos` CLI and other OS maintenance scripts — see
  [scripts.md](scripts.md).
- `projects/` holds one folder per project; each project owns its tasks and
  docs. There is **no global `tasks/` folder.** See [projects.md](projects.md)
  and [tasks.md](tasks.md).
