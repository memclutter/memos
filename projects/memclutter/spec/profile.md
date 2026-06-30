# profile

## Purpose

Define the sections of the GitHub profile README, what each contains, and the
visual conventions that keep it consistent. The target audience is startup
founders and technical co-founders.

## Behaviour

The README (`vcs/memclutter/README.md`) is organised into the following sections
in order:

### Header

- H1 greeting: `# Hi, I'm memclutter`
- Animated typing SVG from `readme-typing-svg.herokuapp.com`, centred; cycles
  through: "Backend / DevOps / SRE Engineer", "Co-founder @ vAIbe Studio",
  "8+ Years Building Production Systems".
- Font: Fira Code, colour `#2E9EF7`.

### About

A bulleted list with five entries:

| Bullet | Content |
|--------|---------|
| Role | Backend / DevOps / SRE engineer with 8+ years in high-load systems |
| Company | Co-founder @ [vAIbe Studio](https://vaibe.studio) — AI-native products & tooling |
| Open to | technical co-founder & early-stage startup partnerships |
| Core skills | Go · Python · Kubernetes · Terraform · PostgreSQL |
| Reach me | [Telegram](https://t.me/memclutter) · [memclutter.me](https://memclutter.me) |

### Tech Stack

One flat group of `for-the-badge` badges, no sub-categories:
Go, Python, PostgreSQL, Redis, Docker, Kubernetes, Vue.js.

### Open-source projects

A flat bulleted list (no sub-sections):

| Repo | Org | Description |
|------|-----|-------------|
| [vaibe-os](https://github.com/vaibe-studio/vaibe-os) | vaibe-studio | Personal OS for running open-source projects — rules, skills, and agent workflows. |
| [confparse](https://github.com/memclutter/confparse) | memclutter | Declarative CLI flag & config parser for Go. Struct tags to flags with env fallbacks. Zero deps. |
| [gorequests](https://github.com/memclutter/gorequests) | memclutter | Fluent HTTP client for Go: build, send, and decode requests in one chain. |
| [nocodb-migrator](https://github.com/memclutter/nocodb-migrator) | memclutter | Versioned schema & data migrations for NocoDB via Meta API v3. |
| [proxycheck](https://github.com/memclutter/proxycheck) | memclutter | Concurrent proxy checker for HTTP/HTTPS/SOCKS4/5 — CLI + library. |

### Connect

Five `flat-square` badges in order: vAIbe Studio (vaibe.studio), Website
(memclutter.me), Telegram, LinkedIn, GitHub.

### Removed sections (vs. previous version)

- GitHub Statistics (3 widgets)
- GitHub Streak widget
- Top Languages widget
- Featured Projects sub-categories (Golang / IaC / Python DevOps / Other)
- Latest Articles placeholder block
- Footer profile-view counter

## Success criteria

- Every linked repo in Open-source projects exists and is public under its org.
- All external badge/widget URLs return HTTP 200.
- The README renders identically in GitHub's light and dark themes.
- A visitor sees the owner's role, co-founder status, and primary contact
  without scrolling at 1080 p viewport.
- Total `##` sections = 4 (About, Tech Stack, Open-source projects, Connect).
