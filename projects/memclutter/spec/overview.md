# memclutter — Product spec

## Vision

A single Markdown file rendered by GitHub as the public face of the
`memclutter` account. Its primary audience is startup founders and technical
co-founders evaluating a potential backend/DevOps partner. The page answers
three questions quickly — who is this person, what have they actually shipped,
and how to start a conversation.

## Capabilities

- [profile.md](profile.md) — sections, content, and structure of the README.

## Product-wide success criteria

- The README renders without errors in GitHub's Markdown engine.
- All badge and widget URLs are reachable and return valid images.
- A visitor can identify the owner's role, co-founder status, core skills, and
  primary contact channel within 30 seconds of landing on the page.

## Boundaries

✅ Always
- Edit only `vcs/memclutter/README.md`; no other files ship in this repo.
- Keep `main` branch releasable (every push is immediately live).
- Follow [rules/git.md](../../../rules/git.md) Conventional Commits inside the
  submodule.

⚠️ Ask first
- Adding a new top-level section to the README.
- Replacing a dynamic widget service with a different provider.

🚫 Never
- Embed secrets, tokens, or personal data beyond what is already public.
- Add a CI/CD pipeline or build artefacts to the repo.
