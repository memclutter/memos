# 001 — Unit tests, CI, and pre-commit for nocodb-migrator

## Goal

Give the tool a fast unit safety net over its NocoDB integration and keep it from
drifting away from the live Meta API v3 again. Add unit tests (api / storage /
executor against an in-process mock), wire lint + unit into GitHub Actions CI,
and run the fast checks locally on every commit via pre-commit. End-to-end
integration against a real dockerized NocoDB is split into task
002-integration-tests-nocodb.

## Scope

- **Unit tests** for the NocoDB API client, storage, and executor using an
  in-process `httptest` mock server — no network, fast, table-driven.
- **CI** (GitHub Actions): lint (`gofmt`/`golangci-lint`) + unit tests on every
  push and PR.
- **pre-commit** (pre-commit framework, `.pre-commit-config.yaml`): formatting,
  lint, and the fast unit tests on every commit.

## Acceptance criteria

- `go test ./...` passes with meaningful unit coverage of `internal/api`,
  `internal/storage`, and `internal/migration` execution.
- CI is green on PRs: lint + unit on every push.
- `pre-commit run --all-files` passes locally and is documented in
  `CONTRIBUTING.md`.

## Out of scope

- Integration tests against a real dockerized NocoDB → task
  002-integration-tests-nocodb.

## Status

Backlog. Next phase: `sys.task.breakdown`.
