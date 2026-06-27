---
id: 003-fix-migrations-mysql-enum
status: backlog
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
