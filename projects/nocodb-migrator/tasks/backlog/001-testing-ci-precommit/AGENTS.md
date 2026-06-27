---
id: 001-testing-ci-precommit
status: backlog
created: 2026-06-27
updated: 2026-06-27
---

## Goal

Add an automated test suite (unit + integration against a real NocoDB), a
GitHub Actions CI pipeline, and a pre-commit configuration to nocodb-migrator,
so the tool's behaviour against the Meta API v3 is verifiable and protected from
silent drift.

## Scope

- Unit tests for `internal/api`, `internal/storage`, and `internal/migration`
  execution, driven by an in-process `httptest` mock NocoDB server.
- Integration tests, build-tag / env gated, that run `up`/`down`/`info` against
  a NocoDB instance started in Docker.
- GitHub Actions: a fast job (lint + unit) on every push/PR and a separate,
  gated integration job that brings up NocoDB.
- A `.pre-commit-config.yaml` using the pre-commit framework: `gofmt`/
  `goimports`, `golangci-lint`, and the fast unit tests.
- A `.golangci.yml` (lint runs in CI per rules/go.md) and a short
  `CONTRIBUTING.md` section on running the suites and hooks.

## Acceptance criteria

- `go test ./...` passes; unit tests cover the API client request/response
  shaping, the storage `Migrations` table logic, and executor operation
  dispatch.
- Opt-in integration suite applies and rolls back a migration against a
  dockerized NocoDB and asserts the schema/data result.
- CI green on PR: lint + unit always; integration in its own job.
- `pre-commit run --all-files` passes locally.

## Constraints

- Follow [go.md](../../../../../rules/go.md): standard `testing` + table-driven
  tests, `testify` allowed; `gofmt`/`goimports` + `golangci-lint` in CI.
- Follow [docker.md](../../../../../rules/docker.md) and
  [git.md](../../../../../rules/git.md) (Conventional Commits, green CI per PR).
- Never commit a real `NOCODB_API_TOKEN`, base id, or instance URL; integration
  config comes from the environment / ephemeral docker instance only.
- Target Meta API v3 only — tests must encode the v3 contract, not invent new
  endpoints.
- ⚠️ Ask before pulling in a heavyweight integration framework beyond the base
  stack (Docker + testcontainers-go is the expected approach; confirm if
  deviating).
