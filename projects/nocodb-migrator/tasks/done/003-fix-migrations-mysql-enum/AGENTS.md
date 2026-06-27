---
id: 003-fix-migrations-mysql-enum
status: done
created: 2026-06-27
updated: 2026-06-27
---

## Goal

Fix the reproduced issue #1: `EnsureMigrationsTable` fails on a MySQL-backed
NocoDB because the bulk `POST /tables` create emits an empty `enum` for the
SingleSelect `Direction`/`Status` columns. Create the table first, then add those
two fields via separate `POST /tables/{id}/fields` calls so NocoDB materializes
the ENUM values — keeping the select semantics. Guard it with a MySQL-backed
integration regression test.

## Scope

- `internal/storage/migrations.go` — split `EnsureMigrationsTable`: create the
  `Migrations` table with only the non-select fields (`Timestamp`, `Name`,
  `AppliedAt`), then create `Direction` and `Status` (SingleSelect, with choices)
  via the client's `CreateField`.
- A backend-parameterized integration regression test (build-tag `integration`),
  table-driven over **SQLite, MySQL, Postgres**: for the SQL backends start the DB
  + NocoDB (`NC_DB=mysql2://…` / `pg://…`) on a shared testcontainers network;
  bootstrap; assert `EnsureMigrationsTable` succeeds and `Direction`/`Status`
  carry their choices. Extend `internal/testutil` with a `Backend`-parameterized
  `StartNocoDBOn`, keeping `StartNocoDB` as the SQLite wrapper.

## Acceptance criteria

- `EnsureMigrationsTable` succeeds on SQLite, MySQL, and Postgres; on MySQL the
  columns are real `enum('up','down')` / `enum('success','failed')` (equivalent on
  Postgres); no `ER_PARSE_ERROR`.
- `Direction`/`Status` stay SingleSelect with choices (per the cli.md design
  intent — no `SingleLineText` downgrade).
- Unit suite stays green; the new backend-parameterized test fails before the fix
  (MySQL/Postgres subtests) and passes after; SQLite green throughout.

## Constraints

- Follow [go.md](../../../../../rules/go.md), [docker.md](../../../../../rules/docker.md),
  [git.md](../../../../../rules/git.md).
- 🚫 Do NOT replace SingleSelect with SingleLineText — the select semantics are
  intentional ([spec/cli.md](../../../spec/cli.md)).
- Keep the change to the table-creation path; do not alter the migration file
  format or the recorded-row schema.
- Target Meta API v3 only.

## Tasks breakdown

- [x] 1. Fix `EnsureMigrationsTable` (`internal/storage/migrations.go`): create the
  table with only `Timestamp`/`Name`/`AppliedAt`, then add `Direction` and
  `Status` (SingleSelect + choices) via `client.CreateField`. Make the
  "table exists" branch idempotent — add any missing select field — so a partial
  create heals on re-run. (success: table creates on all backends; selects kept)
- [x] 2. Update `internal/storage/migrations_test.go` for the new call sequence:
  assert `EnsureMigrationsTable` issues `CreateTable` (non-select fields) then two
  `CreateField` calls carrying the right choices; cover the heal-on-existing path.
  Keep `go test ./...` green.
- [x] 3. Backend-parameterize `internal/testutil` (`//go:build integration`):
  add a `Backend` enum (`SQLite`/`MySQL`/`Postgres`) and `StartNocoDBOn(t, backend)`
  reusing `bootstrap()`; keep `StartNocoDB` as a thin `SQLite` wrapper so the
  existing e2e test is untouched. Add the shared-network plumbing (`network.New`).
- [x] 4. Add the **MySQL** backend to the helper: `mysql:8` (prefer the
  testcontainers mysql module) with alias, started/awaited before NocoDB; NocoDB
  `Env: NC_DB=mysql2://mysql:3306?u=root&p=<pw>&d=nocodb`. Sanity-run.
- [x] 5. Add the **Postgres** backend: `postgres:16` (prefer the postgres module)
  with alias; NocoDB `Env: NC_DB=pg://postgres:5432?u=postgres&p=<pw>&d=nocodb`.
  Confirm the `NC_DB` shape; sanity-run.
- [x] 6. Write the table-driven regression test
  (`internal/storage/migrations_integration_test.go`, `//go:build integration`)
  over SQLite/MySQL/Postgres: per backend, `EnsureMigrationsTable()` →
  `require.NoError`, then assert `Direction`/`Status` are SingleSelect with their
  choices. Verify it is **red before the fix** (stash step 1, MySQL/Postgres fail)
  and **green after**.
- [x] 7. Final matrix: `go test -tags=integration ./...` green on all backends;
  default `go test ./...` + `golangci-lint` (both tag sets) clean; confirm the CI
  `integration` job picks up the new test (pulls `mysql:8`/`postgres:16`).
