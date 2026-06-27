---
id: 001-testing-ci-precommit
status: active
created: 2026-06-27
updated: 2026-06-27
---

## Goal

Add a unit test suite (api / storage / executor against an in-process mock
NocoDB), a GitHub Actions CI pipeline (lint + unit), and a pre-commit
configuration to nocodb-migrator, so the tool's behaviour against the Meta API v3
is verifiable and protected from silent drift. Integration tests are split into
task 002-integration-tests-nocodb.

## Scope

- Unit tests for `internal/api`, `internal/storage`, and `internal/migration`
  execution, driven by an in-process `httptest` mock NocoDB server.
- GitHub Actions: a `lint-unit` job (lint + unit) on every push/PR.
- A `.pre-commit-config.yaml` using the pre-commit framework: `gofmt`/
  `goimports`, `golangci-lint`, and the fast unit tests.
- A `.golangci.yml` (lint runs in CI per rules/go.md) and a short
  `CONTRIBUTING.md` section on running the suite and hooks.

## Acceptance criteria

- `go test ./...` passes; unit tests cover the API client request/response
  shaping, the storage `Migrations` table logic, and executor operation
  dispatch.
- CI green on PR: lint + unit on every push.
- `pre-commit run --all-files` passes locally.

## Constraints

- Follow [go.md](../../../../../rules/go.md): standard `testing` + table-driven
  tests, `testify` allowed; `gofmt`/`goimports` + `golangci-lint` in CI.
- Follow [git.md](../../../../../rules/git.md) (Conventional Commits, green CI per PR).
- Never commit a real `NOCODB_API_TOKEN`, base id, or instance URL; unit tests
  use only the in-process mock.
- Target Meta API v3 only — tests must encode the v3 contract, not invent new
  endpoints.

## Tasks breakdown

- [ ] 1. Add a mock-NocoDB test helper: an `httptest.Server` that routes on
  method+path, returns canned JSON, and records the last request; plus a
  constructor wiring `api.NewClient(server.URL, ...)`. (success criterion: unit
  coverage via in-process mock)
- [ ] 2. Unit-test `internal/api` (`nocodb_test.go`), table-driven: method/path,
  `xc-token` + base id on every request, request-body shaping (`fields` wrap,
  `[{"id":…}]` delete bodies), response decoding (`{"records":[…]}`→`RecordList`,
  `id`/`Id`), and error decoding (message vs status fallback).
- [ ] 3. Unit-test `internal/storage` (`migrations_test.go`):
  `EnsureMigrationsTable` create-vs-noop and the captured `CreateTable` payload
  (issue #1 guard); `RecordMigration`, `GetAppliedMigrations`,
  `GetCurrentVersion`, `IsMigrationApplied`, `DeleteMigrationRecord` round-trips.
- [ ] 4. Unit-test `internal/migration` (`operations_test.go` + `executor_test.go`):
  `ExecuteOperation` dispatch for all eight op types + unknown-type error;
  `ExecuteMigration` stops and wraps on first failure. Keep/extend `parser_test.go`.
- [ ] 5. Add `.golangci.yml` (govet, staticcheck, errcheck, gofmt/goimports,
  ineffassign, unused) and make `go test ./...` + lint green locally.
- [ ] 6. Add `.github/workflows/ci.yml` with a `lint-unit` job (setup-go, fmt
  check, `golangci-lint run`, `go test ./...`) on push/PR.
- [ ] 7. Add `.pre-commit-config.yaml` (fmt/goimports, golangci-lint, fast
  `go test ./...`) and document `pre-commit install` + running the suite in
  `CONTRIBUTING.md`. Verify `pre-commit run --all-files` passes.
