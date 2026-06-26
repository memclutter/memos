# memos

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Release](https://img.shields.io/github/v/release/memclutter/memos?sort=semver)](https://github.com/memclutter/memos/releases)
[![Last commit](https://img.shields.io/github/last-commit/memclutter/memos)](https://github.com/memclutter/memos/commits/main)

[![Go](https://img.shields.io/badge/Go-00ADD8?logo=go&logoColor=white)](rules/go.md)
[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)](rules/python.md)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white)](rules/data.md)
[![Redis](https://img.shields.io/badge/Redis-FF4438?logo=redis&logoColor=white)](rules/data.md)
[![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)](rules/docker.md)
[![Vue.js](https://img.shields.io/badge/Vue.js-4FC08D?logo=vuedotjs&logoColor=white)](rules/vue.md)

A **personal operating system** for running open-source projects — a single
repository that holds the rules, structure, tasks, and agent skills used to
build and maintain everything under
[github.com/memclutter](https://github.com/memclutter).

It contains **no application code of its own.** Each actual project lives in its
own GitHub repo and is mounted here as a git submodule. This repo is the layer
*around* those projects: how they are structured, how work is defined and
tracked, and the conventions an AI agent (or a human) follows when working on
them.

## Why

I run my open-source projects with the help of an AI agent. For that to be
consistent across many projects, the agent needs one place that answers: what
are the rules, what is the folder layout, what is the current task, and how is
work recorded. This repo is that place. New tools are adopted deliberately,
project by project — it doubles as a way to learn.

## Structure

```
.
├── AGENTS.md          # index of the rules — start here
├── CLAUDE.md          # pointer to AGENTS.md
├── rules/             # the rules, one file per topic (source of truth)
├── skills/            # agent skills available to the agent
└── projects/          # one folder per project
    └── <project>/
        ├── README.md  # project description (humans)
        ├── AGENTS.md  # project description (agent, with metadata)
        ├── repo/      # the project's git repository (submodule)
        ├── tasks/     # tasks: backlog / active / done
        └── docs/      # project documentation
```

- **[AGENTS.md](AGENTS.md)** is the entry point — a one-paragraph index over the
  rules in [`rules/`](rules/), each linking to the full text.
- There is **no global `tasks/` folder**; tasks belong to their project.
- The git log is the history of work — there is no manual activity journal.

## Getting started

Clone with all project submodules:

```bash
git clone --recurse-submodules git@github.com:memclutter/memos.git
# or, after a plain clone:
git submodule update --init --recursive
```

Then read [AGENTS.md](AGENTS.md) and the files under [`rules/`](rules/).

## Conventions

- All written records (code, docs, commits, tasks) are in **English**.
- Default stack: Go, Python, PostgreSQL, Redis, Docker, Vue.js — see
  [rules/stack.md](rules/stack.md).
- Commits follow [Conventional Commits](https://www.conventionalcommits.org/).

## License

See [LICENSE](LICENSE).
