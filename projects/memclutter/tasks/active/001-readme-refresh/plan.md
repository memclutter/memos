# Plan — 001-readme-refresh

## Approach

Overwrite `vcs/memclutter/README.md` in-place with the new structure defined in
`spec.md` Target State. No tooling, no build step — GitHub renders the file on
every push to `main`. Commit inside the submodule, push it, then bump the
submodule pointer in the OS repo.

The new README has exactly five top-level sections:
**Header → About → Tech Stack → Open-source projects → Connect**.
Every section cut from the current file (Stats widgets, Articles, sub-category
project lists) is intentionally omitted, not moved elsewhere.

## Stack

Pure Markdown — deliberate deviation from the base stack, documented in
`projects/memclutter/AGENTS.md`. No dependencies, no build, no CI.

Badge rendering relies on two external services:
- `shields.io` — static badges (Tech Stack, Connect).
- `readme-typing-svg.herokuapp.com` — animated header tagline (optional; keep
  if it renders in under 3 s on a cold load, remove if it becomes a liability).

## Architecture

```
vcs/memclutter/
└── README.md          ← the only file changed in the submodule
```

Delivery sequence:

1. Edit `vcs/memclutter/README.md` to match the Target State (see below).
2. Inside `vcs/memclutter/`: `git commit -m "feat: refresh profile README"` +
   `git push origin main`.
3. In the OS repo root: `git add projects/memclutter/vcs/memclutter` +
   `git commit -m "chore(submodule): bump memclutter"`.

### New README structure

```markdown
# Hi, I'm memclutter

<typing-svg tagline>

## About

- Backend / DevOps / SRE engineer, 8+ years
- Co-founder @ [vAIbe Studio](https://vaibe.studio)
- Open to: technical co-founder & early-stage startup partnerships
- Skills: Go · Python · Kubernetes · Terraform · PostgreSQL
- Reach me: [Telegram](…) · [memclutter.me](https://memclutter.me)

## Tech Stack

<badges: Go, Python, PostgreSQL, Redis, Docker, Kubernetes, Vue.js>

## Open-source projects

- **[vaibe-os](https://github.com/vaibe-studio/vaibe-os)** —
  Personal OS for running open-source projects — rules, skills, agent workflows.
- **[confparse](https://github.com/memclutter/confparse)** —
  Declarative CLI flag & config parser for Go. Zero deps.
- **[gorequests](https://github.com/memclutter/gorequests)** —
  Fluent HTTP client for Go: build, send, decode in one chain.
- **[nocodb-migrator](https://github.com/memclutter/nocodb-migrator)** —
  Versioned schema & data migrations for NocoDB via Meta API v3.
- **[proxycheck](https://github.com/memclutter/proxycheck)** —
  Concurrent proxy checker for HTTP/HTTPS/SOCKS4/5 — CLI + library.

## Connect

<badges: vAIbe Studio · Website · Telegram · LinkedIn · GitHub>
```

### Badge conventions (unchanged from project AGENTS.md)

- Tech Stack: `style=for-the-badge`, `logoColor=white` where supported.
- Connect: `style=flat-square`.
- No `<div align="center">` wrappers on Tech Stack or projects — plain Markdown
  only; centre-align only the header typing SVG if kept.

## Trade-offs & alternatives

| Decision | Chosen | Rejected | Reason |
|----------|--------|----------|--------|
| Stats widgets | Remove all three | Keep one (GitHub Stats) | Adds 3 external requests on page load; conveys nothing a project link doesn't. Ask the owner if they want one back (spec boundary). |
| Typing SVG header | Keep (one line, optional) | Remove | Low cost, adds visual identity; can be cut with no spec change if it loads slowly. |
| Tech Stack format | Badge grid (one row, no sub-categories) | Plain-text list | Badges give fast visual scanning; one flat row avoids the "wall of badges" problem. |
| vaibe-os listing | Link to `vaibe-studio/vaibe-os` directly | Skip until imported into OS | Repo is public; linking it from the profile is independent of whether it's a submodule here. |
| Profile-view counter | Remove | Keep | Noise for startup partners; ego metric only. |

## Constraints & risks

- **Submodule push requires SSH access** — confirmed (`ssh -T git@github.com`
  succeeded). No HTTPS token needed.
- **External badge URLs** — all use shields.io; it has > 99 % uptime. If a badge
  fails to load GitHub shows a broken image, not an error. Acceptable risk.
- **vaibe-os repo visibility** — the plan assumes `vaibe-studio/vaibe-os` is
  public. Verify with `gh repo view vaibe-studio/vaibe-os` before linking.
- **No review step** — changes go live on `main` immediately after push.
  Preview in a local Markdown renderer before pushing.

## Testing strategy

Each success criterion from `spec.md` maps to a manual check after the push:

| Criterion | How to verify |
|-----------|---------------|
| All linked repos exist | `gh repo view <org>/<repo>` for each entry |
| vaibe-os is public | `gh repo view vaibe-studio/vaibe-os --json visibility` |
| ≤ 5 top-level sections | Count `## ` headings in the final file |
| No Stats/Streak widgets | `grep -c "github-readme-stats\|streak-stats" README.md` → 0 |
| No Articles section | `grep -c "BLOG-POST-LIST" README.md` → 0 |
| Renders on GitHub | Open `github.com/memclutter` in browser, check light + dark theme |
| Role + contact above fold | Screenshot at 1080 p viewport |
