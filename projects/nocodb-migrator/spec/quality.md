# quality

## Purpose

How the project keeps the tool correct and prevents it from drifting away from
the live NocoDB Meta API v3: the automated test strategy, the continuous
integration pipeline, and the local pre-commit checks. The integration boundary
(`internal/api`) is the part most prone to silent breakage, so it is the focus of
the test coverage.

## Behaviour

### Unit tests

Unit tests use the standard `testing` package with table-driven cases and
`testify` for assertions. An in-process `httptest`-based **mock NocoDB** lives in
`internal/testutil`: a stateful fake of the Meta API v3 table, field, and record
endpoints that records every request, so tests run with no network and no live
instance via `go test ./...`.

The suite covers the three layers that touch NocoDB:

- `internal/api` — the client's wire contract: the `xc-token` header and base id
  on every request, the request paths, request-body shaping (insert wraps values
  under `fields`; deletion sends `[{"id": …}]`), response decoding (the
  `{"records":[…]}` envelope into `RecordList`, id exposed under both `id` and
  `Id`), and error decoding (a NocoDB error body surfaces its `message`, a
  non-decodable body falls back to the status code).
- `internal/storage` — the `Migrations` table logic: `EnsureMigrationsTable`
  creates the table with the expected field set and is idempotent, and migration
  records round-trip through `RecordMigration` / `GetAppliedMigrations` /
  `GetCurrentVersion` / `IsMigrationApplied` / `DeleteMigrationRecord`. The
  captured create-table payload is asserted so a malformed `Migrations`-table
  request cannot regress unnoticed.
- `internal/migration` — the executor: `ExecuteOperation` dispatches each of the
  eight operation types to the right endpoint, an unknown type errors, and
  `ExecuteMigration` stops and wraps on the first failing operation.

### Continuous integration

A GitHub Actions workflow (`.github/workflows/ci.yml`) runs a `lint-unit` job on
every pull request and on pushes to `main`: a `gofmt` check, `golangci-lint run`
(configured by `.golangci.yml`, golangci-lint v2 via `golangci-lint-action@v7`),
and `go test ./...`. CI must be green before a change is merged.

### pre-commit

A `.pre-commit-config.yaml` (the pre-commit framework) runs `gofmt`,
`golangci-lint`, and the unit tests on every commit via `language: system` local
hooks, so the Go toolchain on the developer's `PATH` is reused. `CONTRIBUTING.md`
documents `pre-commit install` and running the hooks and the suite.

## Success criteria

- `go test ./...` passes with no network or NocoDB instance and covers the API
  client, the `Migrations` storage, and the executor against the in-process mock.
- `golangci-lint run ./...` reports no issues; `gofmt` reports no unformatted
  files.
- The CI `lint-unit` job runs lint and unit tests on every push/PR and gates
  merges.
- `pre-commit run --all-files` passes.
- No real `NOCODB_API_TOKEN`, base id, or instance URL appears in tests or CI;
  tests rely only on the in-process mock.

## Not yet covered

End-to-end integration tests against a real dockerized NocoDB are not part of the
suite yet; they are tracked separately and, when added, will be build-tag gated
so the default `go test ./...` stays network-free.
