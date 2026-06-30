---
id: 001-readme-refresh
status: backlog
created: 2026-06-30
updated: 2026-06-30
---

Rewrite `vcs/memclutter/README.md` to target startup partners and technical
co-founders. The new README must be short enough to read in one scroll, list
only real repos tracked in the memos OS, and communicate clearly who the owner
is and how to reach them.

## Precise goal

Replace the current bloated profile page with a lean document that answers
three questions for a startup partner:

1. Who is this person and what do they build?
2. What are their real, live open-source projects?
3. How do I contact them?

## Scope

- `vcs/memclutter/README.md` — the only file to change.
- `spec/profile.md` — update to reflect new structure.
- `spec/overview.md` — update Vision (target audience shift to startup partners).

## Acceptance criteria

- Every repo in Featured Projects exists as a public GitHub repo under
  `memclutter`.
- Featured Projects lists only repos present in `projects/` of the memos OS
  (currently: confparse, gorequests, nocodb-migrator, proxycheck).
- GitHub Stats and Streak widgets: at most one (or none).
- "Latest Articles" section removed.
- "Tech Stack" either removed or collapsed to a single compact line/group.
- Total visible sections ≤ 5.
- Renders correctly on GitHub (no broken images, no raw HTML errors).

## Constraints

- Do not add CI, workflows, or scripts to the `memclutter/memclutter` repo.
- Keep Conventional Commits inside the submodule.
- Ask the owner before removing the Connect / social links section.
