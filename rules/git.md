# Git standards

## Commits

- Use [Conventional Commits](https://www.conventionalcommits.org/):
  `type(scope): summary`, e.g. `feat(api): add user search endpoint`.
- Types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `ci`, `build`,
  `perf`, `style`.
- Imperative mood, lowercase summary, no trailing period.
- **Sign every commit** (`git commit -S`, GPG/SSH) so it shows as Verified on
  GitHub. The signing key is configured in the owner's git config; enable
  `commit.gpgsign = true` so signing is automatic. This applies in every repo —
  the OS repo and each project repo under `vcs/<repo-name>/` (a per-repo
  `commit.gpgsign` must be set in each, since global config is not inherited by
  submodule git dirs). Never push an unsigned commit.

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
