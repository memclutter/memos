# 003 — Fix Migrations-table creation on MySQL (empty ENUM)

## Goal

Make `EnsureMigrationsTable` succeed on every NocoDB backend, including external
MySQL sources, while keeping `Direction` and `Status` as SingleSelect. This fixes
the reproduced [issue #1](https://github.com/memclutter/nocodb-migrator/issues/1):
`./nocodb-migrate info` fails with `ER_PARSE_ERROR` on a MySQL-backed instance.

## Background (reproduced root cause)

On a MySQL-backed NocoDB, creating the `Migrations` table fails because the v3
**bulk** `POST /tables` call (table + fields in one request) emits the MySQL DDL
for the SingleSelect columns *before* applying their choices, producing an empty
`` `Direction` enum `` → invalid SQL. SQLite tolerates it (ENUM ≈ TEXT), which is
why it was never caught. Verified fix: create the table first, then add the
SingleSelect fields via separate `POST /tables/{id}/fields` calls — NocoDB then
generates `enum('up','down')` / `enum('success','failed')` correctly.

## Scope

- Change `EnsureMigrationsTable` to create the table without the select fields,
  then add `Direction` and `Status` via separate field-create calls.
- Add a backend-parameterized integration regression test across **SQLite,
  MySQL, and Postgres** (the external SQL backends run NocoDB with `NC_DB`
  pointing at a DB container on a shared testcontainers network) that creates the
  Migrations table and asserts success — it fails before the fix (MySQL/Postgres)
  and passes after.

## Acceptance criteria

- `EnsureMigrationsTable` succeeds against a MySQL-backed NocoDB; `Direction` /
  `Status` are real `enum('up','down')` / `enum('success','failed')` columns.
- `Direction` and `Status` remain SingleSelect with their choices (no downgrade
  to text).
- The full unit suite stays green.
- The new backend-parameterized regression test (SQLite / MySQL / Postgres)
  guards the fix in CI.

## Out of scope

- The broader Meta API v3 audit (issue #2) — this is one concrete finding from it.
- Reporting the underlying behaviour upstream to NocoDB (worth doing separately).

## Status

Backlog. Next phase: `sys.task.plan`.
