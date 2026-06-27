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

### Integration tests

An opt-in integration suite runs the real `up`/`down` command path against a
NocoDB started in Docker (testcontainers-go), the cross-check the unit mocks
cannot give. It is gated behind the `integration` build tag, so the default
`go test ./...` and the pre-commit hook never compile testcontainers or need
Docker; it runs via `go test -tags=integration ./...`.

A container helper in `internal/testutil` starts `nocodb/nocodb` (a pinned tag
exposing Meta API v3), waits for readiness, and bootstraps a usable API token and
base (signup → API token → workspace → base). The end-to-end test applies a
migration with `runUp`, asserts the resulting tables/fields/records and the
recorded `Migrations` row via the client, then `runDown` and asserts the base
returns to its prior state. When Docker is not available the suite skips cleanly
rather than failing. A failure against real NocoDB means the implementation has
diverged from the live Meta API v3 — a bug to fix, not a test to weaken.

The helper is **backend-parameterized** (`StartNocoDBOn`): besides the default
bundled store (SQLite), it can run NocoDB against an external **MySQL** or
**PostgreSQL** source — a second DB container on a shared network, wired via
`NC_DB`. A backend matrix test creates the `Migrations` table on each of SQLite,
MySQL, and Postgres and asserts the select columns and their choices; it is the
regression guard for the issue #1 empty-`enum` bug (which surfaces only on the
external SQL backends).

### Continuous integration

A GitHub Actions workflow (`.github/workflows/ci.yml`) runs on every pull request
and on pushes to `main` in two independent jobs:

- `lint-unit` — a `gofmt` check, `golangci-lint run` (configured by
  `.golangci.yml`, golangci-lint v2 via `golangci-lint-action@v7`), and
  `go test ./...`.
- `integration` — `go test -tags=integration ./...` on a Docker-enabled runner,
  kept off the fast lint+unit critical path.

CI must be green before a change is merged.

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
  merges; a separate `integration` job runs the build-tag-gated suite against a
  dockerized NocoDB.
- `go test -tags=integration ./...` applies and rolls back a migration against a
  real NocoDB container and asserts the schema/data outcome; without Docker it
  skips cleanly.
- `pre-commit run --all-files` passes.
- No real `NOCODB_API_TOKEN`, base id, or instance URL appears in tests or CI;
  unit tests rely on the in-process mock and integration tests on an ephemeral
  container only.
