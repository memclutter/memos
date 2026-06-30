---
name: memclutter
vcs:
  - git@github.com:memclutter/memclutter.git
self: false
status: active
stack: [markdown]
created: 2026-06-30
---

Personal GitHub profile repository. This is a **deliberate deviation** from the
base stack ([rules/stack.md](../../rules/stack.md)): it ships no application
code — only a single `README.md` rendered by GitHub on the profile page.

## Architecture

- One file: `vcs/memclutter/README.md` — pure Markdown with embedded SVG badge
  widgets (shields.io, github-readme-stats, readme-typing-svg).
- No build step, no CI, no deployment. GitHub renders the file automatically
  whenever it is pushed to the `main` branch.

## Conventions

- Keep the README readable in plain text as well as rendered on GitHub.
- Badge URLs use `style=for-the-badge` for consistency across the Tech Stack
  section, and `style=flat-square` in the Connect section.
- Dynamic widgets (GitHub Stats, Streak, Top Languages) all share the
  `tokyonight` theme with `hide_border=true`.
- Source changes are committed and pushed inside `vcs/memclutter/`, then this OS
  pins the new submodule commit (`chore(submodule): bump memclutter`).
