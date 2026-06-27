# 001 — Testing, CI, and pre-commit for nocodb-migrator

## Goal

Make the tool's behaviour against NocoDB verifiable and keep it from drifting
away from the live Meta API v3 again. Add an automated test suite (unit +
integration against a real NocoDB), wire it into GitHub Actions CI, and run the
fast checks locally on every commit via pre-commit.

## Scope

- **Unit tests** for the NocoDB API client, storage, and executor using an
  in-process `httptest` mock server — no network, fast, table-driven.
- **Integration tests** that bring up a real NocoDB instance in Docker and run
  `up` / `down` / `info` end to end against it, behind a build tag / env gate so
  they don't run by default.
- **CI** (GitHub Actions): lint (`gofmt`/`golangci-lint`) + unit tests on every
  push and PR; integration tests in a separate, slower job that spins up NocoDB.
- **pre-commit** (pre-commit framework, `.pre-commit-config.yaml`): formatting,
  lint, and the fast unit tests on every commit.

## Acceptance criteria

- `go test ./...` passes with meaningful unit coverage of `internal/api`,
  `internal/storage`, and `internal/migration` execution.
- An opt-in integration suite applies and rolls back a migration against a
  dockerized NocoDB and asserts the resulting schema/data.
- CI is green on PRs: lint + unit always; integration in its own job.
- `pre-commit run --all-files` passes locally and is documented in
  `CONTRIBUTING.md`.

## Status

Backlog. Next phase: `sys.task.plan`.
