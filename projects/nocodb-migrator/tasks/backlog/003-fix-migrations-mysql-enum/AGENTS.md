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
- A MySQL-backed integration regression test (build-tag `integration`): start
  MySQL + NocoDB (`NC_DB=mysql2://…`) on a shared testcontainers network,
  bootstrap, and assert `EnsureMigrationsTable` / `runUp` succeed and the select
  fields carry their choices.

## Acceptance criteria

- Against MySQL-backed NocoDB, the Migrations table is created with real
  `enum('up','down')` / `enum('success','failed')` columns; no `ER_PARSE_ERROR`.
- `Direction`/`Status` stay SingleSelect with choices (per the cli.md design
  intent — no `SingleLineText` downgrade).
- Existing SQLite integration test + unit suite stay green; the new MySQL test
  fails before the fix and passes after.

## Constraints

- Follow [go.md](../../../../../rules/go.md), [docker.md](../../../../../rules/docker.md),
  [git.md](../../../../../rules/git.md).
- 🚫 Do NOT replace SingleSelect with SingleLineText — the select semantics are
  intentional ([spec/cli.md](../../../spec/cli.md)).
- Keep the change to the table-creation path; do not alter the migration file
  format or the recorded-row schema.
- Target Meta API v3 only.
