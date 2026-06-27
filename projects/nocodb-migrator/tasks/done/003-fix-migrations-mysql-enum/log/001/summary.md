# Iteration 001 — fix Migrations-table creation on MySQL/Postgres

## What shipped (in vcs/nocodb-migrator)

- **Fix** `internal/storage/migrations.go`: `EnsureMigrationsTable` now creates the
  table with only the non-select fields (`Timestamp`/`Name`/`AppliedAt`), then
  adds `Direction`/`Status` (SingleSelect + choices) via separate
  `client.CreateField` calls (`migrationsSelectFields` + `ensureSelectFields`).
  The "table exists" branch heals a partial create by adding any missing select
  field. SingleSelect semantics preserved (no SingleLineText downgrade).
- **Unit tests** `internal/storage/migrations_test.go`: assert the new sequence
  (bulk create carries only the non-select fields; Direction/Status added as two
  separate SingleSelect field-creates with choices) and the heal-on-existing path.
- **Backend-parameterized helper** `internal/testutil/nocodb_container.go`
  (`integration` tag): a `Backend` enum (`SQLite`/`MySQL`/`Postgres`) and
  `StartNocoDBOn`; `StartNocoDB` is now a thin SQLite wrapper. External backends
  start a DB container (`mysql:8` / `postgres:16`) on a shared `network.New`
  network and point NocoDB at it via `NC_DB` (`mysql2://…` / `pg://…`).
- **Regression test** `internal/storage/migrations_integration_test.go`
  (`integration` tag): table-driven over SQLite/MySQL/Postgres — asserts
  `EnsureMigrationsTable` succeeds and Direction/Status are SingleSelect with
  choices.

## Verification

- Multi-backend integration test green: sqlite 10s, mysql 62s, postgres 42s.
- Regression is genuine: stashing the fix, the MySQL subtest fails with the exact
  `ER_PARSE_ERROR` / "failed to create Migrations table" from issue #1; restoring
  the fix makes it pass.
- `go test ./...` (default, no Docker) green; `golangci-lint` clean on both the
  default and `integration` tag sets; `gofmt` clean; `go mod tidy` stable.
- CI: the existing `integration` job runs `go test -tags=integration ./...`, so it
  picks up the new test automatically (now also pulls `mysql:8` / `postgres:16`).

## Notes / follow-ups

- Postgres also reproduced the need for the two-step path (the regression test
  exercises it); the fix is backend-agnostic.
- User-authored `create_field`/`create_table` SingleSelect operations likely hit
  the same upstream NocoDB limitation on external SQL backends — out of scope
  here, flagged for the issue #2 audit and a possible upstream report.
