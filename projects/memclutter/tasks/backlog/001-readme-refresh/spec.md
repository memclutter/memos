# Spec — 001-readme-refresh

## Problem

The current profile README was written as a generic showcase template. It has
three concrete issues:

1. **Stale project links** — the Featured Projects section lists ten repos
   (e.g. `go-microservices-template`, `kubernetes-ops-toolkit`) that either do
   not exist publicly or are not tracked in this OS. A visitor who clicks them
   hits a 404, which damages credibility.
2. **Visual noise** — three GitHub statistics widgets, a badge grid spanning
   five categories, and an empty "Coming soon" articles block fill the page
   without telling a startup partner anything actionable.
3. **Wrong audience framing** — the current vision targets "recruiters,
   open-source collaborators, or curious developers." A startup partner needs a
   different signal: technical depth, real shipped code, and a clear way to
   start a conversation.

## Goal

A lean profile README that a startup partner can read in under 60 seconds and
walk away knowing: this person builds backend/DevOps tooling in Go, is a
co-founder of vAIbe Studio, here are their real projects, here is how to reach
them.

## User journeys

**Journey 1 — Startup founder evaluating a potential CTO/technical co-founder**

1. Lands on `github.com/memclutter`.
2. Reads the header and About section — understands role, experience, and
   current focus within 15 seconds.
3. Scrolls to Featured Projects — sees 3–4 real, linked repos with one-line
   descriptions; clicks one or two to verify depth.
4. Finds a direct contact link (Telegram or email) and reaches out.

**Journey 2 — Technical co-founder / early engineer checking fit**

1. Lands on profile, scans tech stack — wants to know Go / Python / DevOps,
   not a full badge grid.
2. Reads project descriptions — validates that the work is real and
   production-oriented.
3. Exits to explore a specific repo or clicks a contact badge.

## Success criteria

- [ ] Every repo linked in Featured Projects exists as a public GitHub repo
      under `memclutter`.
- [ ] Featured Projects lists only repos present in `projects/` of the memos
      OS: **confparse**, **gorequests**, **nocodb-migrator**, **proxycheck**.
- [ ] About section mentions co-founder role at vAIbe Studio with a link to
      [vaibe.studio](https://vaibe.studio).
- [ ] vAIbe-OS (`github.com/vaibe-studio/vaibe-os`) is listed in Open-source
      projects alongside the memos OS repos.
- [ ] GitHub Stats / Streak widgets: at most one widget, or removed entirely.
- [ ] "Latest Articles" section removed.
- [ ] Tech Stack collapsed: one compact section (badges or plain text) covering
      only the core: Go, Python, PostgreSQL, Redis, Docker, Kubernetes, Vue.js.
- [ ] Total top-level sections ≤ 5.
- [ ] README renders without errors on GitHub (light + dark theme).
- [ ] A visitor sees the owner's role + primary contact without scrolling on a
      1080 p screen.

## Affected spec sections

- `spec/profile.md` — **modify**: rewrite Behaviour to reflect the new
  simplified section structure, updated Featured Projects list, removed
  Articles section, collapsed Tech Stack, reduced Stats widgets.
- `spec/overview.md` — **modify**: update Vision paragraph (audience now
  primarily startup partners / technical co-founders).

## Target state

### spec/overview.md — Vision paragraph (after)

```markdown
A single Markdown file rendered by GitHub as the public face of the
`memclutter` account. Its primary audience is startup founders and technical
co-founders evaluating a potential backend/DevOps partner. The page answers
three questions quickly — who is this person, what have they actually shipped,
and how to start a conversation.
```

### spec/profile.md — Behaviour (after)

The README is organised into the following sections in order:

**Header**
- H1 greeting: `# Hi, I'm memclutter`
- One-line subtitle (plain text or italic): role + years of experience.

**About**
Short paragraph or 3-bullet list covering: current role, co-founder of
[vAIbe Studio](https://vaibe.studio), primary skills (Go, Python, DevOps/SRE),
and what kind of collaboration they are open to.
No animated SVGs in the header — optional single typing SVG is acceptable.

**Tech Stack**
One compact group of `for-the-badge` badges covering core skills only:
Go, Python, PostgreSQL, Redis, Docker, Kubernetes, Vue.js.
No sub-categories, no Monitoring/Logging category, no Ansible, no MongoDB,
no RabbitMQ, no Bash, no JavaScript as separate entries.

**Open-source projects**
A flat bulleted list (no sub-sections). Includes repos tracked in the memos OS
plus vAIbe-OS:

| Repo | Org | Description |
|------|-----|-------------|
| vaibe-os | vaibe-studio | Personal OS for running open-source projects — rules, skills, and agent workflows. |
| confparse | memclutter | Declarative CLI flag & config parser for Go — struct tags to flags with env fallbacks. Zero deps. |
| gorequests | memclutter | Fluent HTTP client wrapper for Go: build, send, decode in one chain. |
| nocodb-migrator | memclutter | CLI for versioned schema & data migrations in NocoDB via Meta API v3. |
| proxycheck | memclutter | Fast concurrent proxy checker for HTTP, HTTPS, SOCKS4/5 — CLI + library. |

**Connect**
Five flat-square badges: vAIbe Studio (vaibe.studio), Website (memclutter.me),
Telegram, LinkedIn, GitHub.
Twitter badge removed (low signal for startup partners).

**Removed sections (compared to current)**
- GitHub Statistics (3 widgets → 0 or 1)
- GitHub Streak widget
- Featured Projects sub-categories (Golang / IaC / Python DevOps / Other)
- Latest Articles placeholder block
- Footer profile-view counter (optional: keep or remove)

## Out of scope

- Adding new repos to the OS or to GitHub (that is a separate task per repo).
- Writing actual blog articles.
- Updating `memclutter.me` or `vaibe.studio` websites.
- Changing the GitHub username or account settings.
- Specifying or importing `vaibe-os` as a project in the memos OS (separate
  task if needed).

## Boundaries

✅ Always
- Edit only `vcs/memclutter/README.md` in the submodule.
- Commit inside the submodule with Conventional Commits, then bump the
  submodule pointer in the OS repo.
- Keep the Connect section (ask before any removal of social links).

⚠️ Ask first
- Adding a GitHub Stats widget back (even a single one).
- Changing the primary contact channel order.
- Including any repo not yet tracked in the memos OS.

🚫 Never
- Link to repos that are private or do not exist.
- Add CI, workflows, or scripts to `memclutter/memclutter`.
