# 001 — readme-refresh

## Goal

Rewrite the GitHub profile README to be a lean, focused introduction for a
potential startup partner or technical co-founder. Replace placeholder and
non-existent project links with the real repos tracked in this OS; strip
visual clutter that adds noise without value.

## Scope

- Rewrite `vcs/memclutter/README.md`.
- Update the living spec (`spec/profile.md`, `spec/overview.md`) to reflect
  the new target audience and simplified structure.

## Acceptance criteria

1. Every repo linked in Featured Projects exists and is public under
   `github.com/memclutter`.
2. The About Me section accurately reflects current role, skills, and contact.
3. GitHub Stats / Streak widgets are reduced to at most one or removed entirely.
4. The "Latest Articles" placeholder section is removed.
5. A visitor can read the whole page in under 60 seconds.
6. The README renders without errors in GitHub's Markdown engine.
