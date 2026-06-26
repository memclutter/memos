# Git standards

## Commits

- Use [Conventional Commits](https://www.conventionalcommits.org/):
  `type(scope): summary`, e.g. `feat(api): add user search endpoint`.
- Types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `ci`, `build`,
  `perf`, `style`.
- Imperative mood, lowercase summary, no trailing period.

## Branches

- `main` is always releasable.
- Work on short-lived branches: `feat/<slug>`, `fix/<slug>`, `chore/<slug>`.

## Pull requests

- One logical change per PR. Description states what and why.
- CI must be green before merge. Squash-merge into `main`.

## Releases

- Tag with SemVer: `vMAJOR.MINOR.PATCH`.
- Keep a `CHANGELOG.md` in each project (Keep a Changelog format).

## Submodules (this OS repo)

- Make source changes inside `projects/<name>/`, push there, then bump the
  pinned commit here with its own `chore(submodule): bump <name>` commit.
