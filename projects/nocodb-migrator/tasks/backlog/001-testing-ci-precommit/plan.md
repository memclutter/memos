# Plan — 001-testing-ci-precommit

## Approach

Test at the HTTP boundary, not behind a hand-rolled interface. `api.NewClient`
already takes the base URL as a constructor argument, so every layer
(`internal/api`, `internal/storage`, `internal/migration`) can be driven against
an in-process `net/http/httptest` server with zero production-code refactor. This
is deliberate: the bugs we care about (issues #1/#2) are *request/response
shaping* against Meta API v3 — exactly what a mock at the HTTP layer asserts and
what a mock at a Go-interface layer would hide.

This task delivers the **unit** layer plus its plumbing; the end-to-end
integration layer against a real dockerized NocoDB is task
002-integration-tests-nocodb.

Two deliverables:

1. Unit suite (default `go test`) over api/storage/executor via `httptest`.
2. Plumbing: `.golangci.yml`, GitHub Actions workflow (lint + unit),
   `.pre-commit-config.yaml`, `CONTRIBUTING.md` docs.

## Stack

Base stack (Go), no deviation in production code. Test/tooling additions:

- `net/http/httptest` (stdlib) — mock NocoDB server for unit tests.
- `github.com/stretchr/testify` — assertions (allowed by [go.md](../../../../../rules/go.md)).
- `golangci-lint` (already mandated by go.md) with a committed `.golangci.yml`.
- GitHub Actions for CI; `pre-commit` framework for local hooks.

testify is the only new `go.mod` require this task introduces (testcontainers-go
belongs to task 002).

## Architecture

### Unit tests (no network, run by default)

A small test helper spins an `httptest.Server` whose handler routes on
method+path and returns canned JSON, recording the last request for assertions.
`NewClient(server.URL, token, baseID)` points the real resty client at it.

- `internal/api/nocodb_test.go` — table-driven over each client method. Assert:
  - method + path (`/api/v3/meta/bases/{baseID}/tables...`, `/api/v3/data/...`),
  - `xc-token` header and base id present on every request,
  - request body shaping (e.g. `InsertRecord` wraps values under `fields`;
    `DeleteRecord`/`DeleteRecords` send `[{"id": ...}]`),
  - response decoding incl. the `{"records":[...]}` → `RecordList` mapping and
    the `id`/`Id` duplication,
  - error decoding: a NocoDB error body surfaces `message`; a non-decodable body
    falls back to the status code.
- `internal/storage/migrations_test.go` — drive `MigrationsStorage` against the
  mock: `EnsureMigrationsTable` creates the table with the expected field set
  when `GetTableByName` 404s and is a no-op when it exists; `RecordMigration`,
  `GetAppliedMigrations`, `GetCurrentVersion`, `IsMigrationApplied`,
  `DeleteMigrationRecord` round-trip correctly. The mock captures the
  `CreateTable` body so a regression in the `Migrations`-table payload (issue #1)
  is caught here.
- `internal/migration/operations_test.go` + `executor_test.go` — assert
  `ExecuteOperation` dispatches each of the eight op types to the right endpoint
  sequence and that an unknown type errors; `ExecuteMigration` stops and wraps on
  the first failing operation.
- Keep existing `parser_test.go`; extend if gaps surface.

A shared `internal/testutil` (or per-package helper) builds the mock server and
the client to avoid duplication.

### Tooling

- `.golangci.yml` — a reasonable default linter set (govet, staticcheck,
  errcheck, gofmt/goimports, ineffassign, unused).
- `.github/workflows/ci.yml` — a `lint-unit` job on every push/PR: setup-go,
  `gofmt`/`goimports` diff check, `golangci-lint run`, `go test ./...`. (Task 002
  adds a separate `integration` job.)
- `.pre-commit-config.yaml` (pre-commit framework): hooks for `go fmt`/goimports,
  `golangci-lint`, and fast `go test ./...` (unit only).
- `CONTRIBUTING.md` — document `pre-commit install` and running the unit suite.

## Trade-offs & alternatives

- **httptest at the HTTP boundary vs. a mockable client interface.** An interface
  would let storage/executor tests bypass HTTP, but it would also stop asserting
  the exact v3 wire contract — the thing that broke. Chosen: httptest, no
  interface, no production refactor.
- **Splitting integration out.** Integration (testcontainers-go + a NocoDB
  container) is slower, needs Docker, and has its own bootstrap risk; keeping it
  out of this task lets the unit safety net land fast and keeps the pre-commit /
  fast-CI path free of Docker. It becomes task 002.

## Constraints & risks

- Follow [go.md](../../../../../rules/go.md) (table-driven, testify ok) and
  [git.md](../../../../../rules/git.md) (Conventional Commits, green CI per PR).
- 🚫 No real `NOCODB_API_TOKEN`/base id/URL committed; unit tests use only the
  in-process mock.
- Tests must encode Meta API **v3** only — do not invent endpoints to make a test
  pass; a mismatch with real NocoDB is a finding for the issue-#2 audit, surfaced
  properly by task 002's integration suite, not something to paper over here.
- **Risk: the mock can drift from real NocoDB** (a unit test passing against a
  mock that encodes a wrong contract). Mitigation: task 002's integration suite
  is the cross-check; keep mock responses faithful to the documented v3 shapes.

## Testing strategy

The deliverable *is* the unit suite, so "proving the spec" means the suite exists
and is wired in:

- `go test ./...` green locally and in CI with the unit coverage enumerated above
  (api request/response shaping, storage `Migrations` logic, executor dispatch).
- CI: PR shows a green `lint-unit` job on every push.
- `pre-commit run --all-files` passes; documented in `CONTRIBUTING.md`.
