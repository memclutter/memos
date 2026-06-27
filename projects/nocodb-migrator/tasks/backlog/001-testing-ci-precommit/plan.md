# Plan — 001-testing-ci-precommit

## Approach

Test at the HTTP boundary, not behind a hand-rolled interface. `api.NewClient`
already takes the base URL as a constructor argument, so every layer
(`internal/api`, `internal/storage`, `internal/migration`) can be driven against
an in-process `net/http/httptest` server with zero production-code refactor. This
is deliberate: the bugs we care about (issues #1/#2) are *request/response
shaping* against Meta API v3 — exactly what a mock at the HTTP layer asserts and
what a mock at a Go-interface layer would hide. Integration tests then run the
real `up`/`down`/`info` flow against a NocoDB container to confirm the v3
contract end to end.

Three deliverables, layered cheapest-first:

1. Unit suite (default `go test`) over api/storage/executor via `httptest`.
2. Integration suite (build-tag gated) via testcontainers-go + a NocoDB image.
3. Plumbing: `.golangci.yml`, GitHub Actions workflow, `.pre-commit-config.yaml`,
   `CONTRIBUTING.md` docs.

## Stack

Base stack (Go), no deviation in production code. Test/tooling additions:

- `net/http/httptest` (stdlib) — mock NocoDB server for unit tests.
- `github.com/stretchr/testify` — assertions (allowed by [go.md](../../../../../rules/go.md)).
- `github.com/testcontainers/testcontainers-go` — start NocoDB in Docker for the
  integration suite (the expected mechanism per the task AGENTS.md). NocoDB runs
  standalone on its bundled SQLite meta-store, so a single container suffices —
  no separate DB service.
- `golangci-lint` (already mandated by go.md) with a committed `.golangci.yml`.
- GitHub Actions for CI; `pre-commit` framework for local hooks.

All test-only deps go in `go.mod` as normal requires (build-tag isolation keeps
testcontainers out of the default unit build path at test time).

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

### Integration tests (build-tag `integration`, opt-in)

- Files tagged `//go:build integration`. Default `go test ./...` skips them; run
  via `go test -tags=integration ./...`. Also guard on a Docker-availability
  check so a tagged run without Docker skips with a clear message rather than
  failing.
- `testcontainers-go` starts `nocodb/nocodb` (pinned tag), waits for HTTP ready,
  provisions an API token / base (via NocoDB's bootstrap), and exposes
  `NOCODB_URL`/`NOCODB_API_TOKEN`/`NOCODB_BASE_ID` to the test.
- One end-to-end test: apply a migration with the real `up` path → assert the
  table/fields/records exist via the client → run `down` → assert the base
  returns to its prior state. This is the test that would have caught the
  `Migrations`-table SQL error and any v3 endpoint drift.

### Tooling

- `.golangci.yml` — a reasonable default linter set (govet, staticcheck,
  errcheck, gofmt/goimports, ineffassign, unused).
- `.github/workflows/ci.yml` — two jobs:
  - `lint-unit` (every push/PR): setup-go, `gofmt`/`goimports` diff check,
    `golangci-lint run`, `go test ./...`.
  - `integration` (separate job): Docker available on `ubuntu-latest` runners;
    `go test -tags=integration ./...`. Slower; kept off the critical fast path.
- `.pre-commit-config.yaml` (pre-commit framework): hooks for `go fmt`/goimports,
  `golangci-lint`, and fast `go test ./...` (unit only). Integration tests are
  *not* in the hook (too slow / needs Docker).
- `CONTRIBUTING.md` — document `pre-commit install`, running unit vs integration
  suites, and the Docker requirement for integration.

## Trade-offs & alternatives

- **httptest at the HTTP boundary vs. a mockable client interface.** An interface
  would let storage/executor tests bypass HTTP, but it would also stop asserting
  the exact v3 wire contract — the thing that broke. Chosen: httptest, no
  interface, no production refactor.
- **testcontainers-go vs. docker-compose vs. a shared remote NocoDB.** Compose
  needs external orchestration in CI; a shared instance violates the "ephemeral,
  never a real base" boundary. testcontainers gives per-test isolated lifecycle
  in Go. Chosen: testcontainers.
- **Integration gate: build tag vs. env var only.** Build tag keeps the default
  `go test ./...` (and the pre-commit hook) from even compiling the Docker deps
  path; pair it with a runtime Docker check for a clean skip. Chosen: both.

## Constraints & risks

- Follow [go.md](../../../../../rules/go.md) (table-driven, testify ok),
  [docker.md](../../../../../rules/docker.md), and [git.md](../../../../../rules/git.md)
  (Conventional Commits, green CI per PR).
- 🚫 No real `NOCODB_API_TOKEN`/base id/URL committed; integration config comes
  only from the ephemeral container.
- **Risk: NocoDB bootstrap in a container** (creating the first token/base
  programmatically) is the fiddliest part and may need a signup/auth call before
  the API token works. Mitigation: encapsulate setup in one helper; pin the image
  tag so behaviour is stable.
- **Risk: integration job flakiness/time** on CI. Mitigation: separate job, not
  blocking the fast lint+unit signal; generous wait-for-ready strategy.
- Tests must encode Meta API **v3** only — do not invent endpoints to make a test
  pass; a failing test against real NocoDB is a finding for the issue-#2 audit,
  not something to paper over.

## Testing strategy

The deliverable *is* the test suite, so "proving the spec" means the suite exists
and is wired in:

- `go test ./...` green locally and in CI with the unit coverage enumerated above
  (api request/response shaping, storage `Migrations` logic, executor dispatch).
- `go test -tags=integration ./...` applies+rolls back a migration against a
  dockerized NocoDB and asserts schema/data — passing proves the v3 contract;
  failing pinpoints drift for follow-up issue-#1/#2 tasks.
- CI: PR shows a green `lint-unit` job on every push and a separate `integration`
  job.
- `pre-commit run --all-files` passes; documented in `CONTRIBUTING.md`.
