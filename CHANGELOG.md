# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-06-27

Onboarded the first application project, `nocodb-migrator`, and drove it end to
end through the SDD task loop.

### Added

- The `nocodb-migrator` project: specified, then delivered through the SDD task
  loop — 001 (unit tests, CI, pre-commit), 002 (integration tests against a
  dockerized NocoDB via testcontainers-go), and 003 (fix for `Migrations`-table
  creation on external MySQL/PostgreSQL backends, reproduced and root-caused).
  Submodule pinned at nocodb-migrator `v0.0.2`.
- Playwright MCP server config (`.mcp.json`, `.cursor/mcp.json`).

### Changed

- Commit signing: require signed commits, scoped to GitHub via a conditional
  include; recorded the intent in the dotfiles spec.

## [0.1.0] - 2026-06-26

Project submodule layout, the first onboarded project, and broader tooling.

### Added

- `vcs/<repo-name>/` submodule layout for projects: documented in the rules,
  scaffolded by `sys.project.specify`, and enforced by a new `memos doctor`
  project-layout check.
- The `dotfiles` project: living spec plus its zsh-configuration and
  repository-metadata-exclusion work, delivered end to end through the SDD task
  loop (submodule pinned at dotfiles `v0.0.3`).

### Changed

- Migrated the dotfiles submodule from `repo/` to `vcs/dotfiles/` and purged the
  stale `repo/` references across the rules and skills.

### Docs

- Added third-party references and attributions to the README; made
  import-existing-repo guidance explicit in `sys.project.specify`.

### Tooling

- pre-commit now mirrors CI (`ruff check`, `ruff format --check`, `mypy`,
  `memos doctor`).
- Moved the uv workspace root to `scripts/`, consolidating `.venv` and tool
  caches under `scripts/` instead of scattering them at the repo root.

## [0.0.3] - 2026-06-26

### Added

- `memos doctor` command, wired into pre-commit and CI.
- Project-level Spec-Driven Development: a living product spec bootstrapped by
  `sys.project.specify`, with the memos living spec specified.

### Changed

- Migrated the `memos` CLI into a uv-workspace package.
- Folded project creation into `sys.project.specify`.

### Fixed

- Corrected the `git tag` invocation in `sys.project.release`.

## [0.0.2] - 2026-06-26

### Added

- `memos` CLI with `shimify`, plus the `sys.project.create` and `sys.task.create`
  skills.
- The Spec-Driven Development workflow, the `doc.prose.review` skill, and the
  `sys.project.release` skill.
- Rules defining skill naming, shims, and scripts.

## [0.0.1] - 2026-06-26

Initial release.

### Added

- Repository foundation: `AGENTS.md` rule index, `CLAUDE.md` pointer, `LICENSE`,
  and `README.md`.
- Initial rules (data, Docker, Git, languages, project structure, tasks,
  workflow) and the `skills/` and `projects/` scaffolding.

[0.2.0]: https://github.com/memclutter/memos/releases/tag/v0.2.0
[0.1.0]: https://github.com/memclutter/memos/releases/tag/v0.1.0
[0.0.3]: https://github.com/memclutter/memos/releases/tag/v0.0.3
[0.0.2]: https://github.com/memclutter/memos/releases/tag/v0.0.2
[0.0.1]: https://github.com/memclutter/memos/releases/tag/v0.0.1
