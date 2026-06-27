# Git standards

## Commits

- Use [Conventional Commits](https://www.conventionalcommits.org/):
  `type(scope): summary`, e.g. `feat(api): add user search endpoint`.
- Types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `ci`, `build`,
  `perf`, `style`.
- Imperative mood, lowercase summary, no trailing period.
- **Sign every commit to a github.com repository** so it shows as Verified.
  Signing is wired up globally in the owner's git config (managed via the
  dotfiles project): `~/.gitconfig` includes `~/.gitconfig_github` (which sets
  `user.signingkey`, `commit.gpgsign`, and `tag.gpgSign`) only for repos whose
  remote is on github.com, via `includeIf "hasconfig:remote.*.url:…"`. So any
  repo with a github remote — the OS repo and every `vcs/<repo-name>/` submodule
  — signs automatically; non-github repos sign nothing unless they opt in
  locally. Never push an unsigned commit to a github repo (and `git push
  --force-with-lease` to re-sign if an unsigned one slipped through). For the SSH
  remote form, the include pattern must be `git@github.com:*/**` — a bare `**`
  does not span the `/` after the colon.

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
