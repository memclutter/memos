# Spec — 003-fix-migrations-mysql-enum

## Problem

On a NocoDB instance backed by an external **MySQL** source, the very first
command fails:

```
{"error":"ERR_DATABASE_OP_FAILED","message":"There was a syntax error in your SQL query.","code":"ER_PARSE_ERROR"}
Error: failed to ensure migrations table: failed to create Migrations table...
```

This is the reproduced root cause of memclutter/nocodb-migrator **issue #1**. The
tool creates the `Migrations` table with a single bulk `POST /api/v3/meta/bases/
{baseId}/tables` request that includes the SingleSelect `Direction` and `Status`
fields. On MySQL, NocoDB generates that column's DDL *before* applying the field
choices, emitting a value-less `` `Direction` enum `` — invalid MySQL syntax.
SQLite has no real ENUM (it maps to TEXT), so the empty enum is harmless there,
which is why the existing SQLite integration test and all unit tests pass while
real MySQL users hit `ER_PARSE_ERROR`.

It is **not** a payload-format bug: the `options.choices` shape the tool sends
matches the official v3 REST schema (`FieldOptions_Select`: `choices[]` of
`{title, color}`), confirmed against the live API and the published swagger. The
choices are even stored in NocoDB's metadata — they just don't reach the MySQL
ENUM DDL on the bulk path.

## Goal

Make `EnsureMigrationsTable` succeed on every NocoDB backend — the bundled SQLite
store and external **MySQL** and **PostgreSQL** sources — while keeping
`Direction`/`Status` as SingleSelect, by creating the table first and then adding
the two select fields via separate field-create calls. Guard the fix with a
backend-parameterized regression test across SQLite, MySQL, and Postgres.

## User journeys

- A user points the tool at a MySQL-backed NocoDB base and runs
  `nocodb-migrate info` / `up`: the `Migrations` table is created without error,
  with `Direction` and `Status` as proper `enum(...)` columns, and the command
  proceeds.
- A contributor runs the backend-parameterized integration test; for each of
  SQLite, MySQL, and Postgres it stands up NocoDB on that backend, creates the
  Migrations table, and asserts the select columns and their choices — failing on
  the old bulk-create code (at least on MySQL/Postgres) and passing on the fix.

## Success criteria

- `EnsureMigrationsTable` succeeds against NocoDB on SQLite, MySQL, and Postgres;
  on MySQL the `Direction`/`Status` columns are real `enum('up','down')` /
  `enum('success','failed')`, with no `ER_PARSE_ERROR`, and the equivalent holds
  on Postgres.
- `Direction` and `Status` remain SingleSelect carrying their choices — no
  downgrade to `SingleLineText`.
- The unit suite stays green.
- A backend-parameterized integration regression test covers SQLite, MySQL, and
  Postgres; it fails against the pre-fix bulk-create path (on the external SQL
  backends) and passes after the fix; it runs in CI.

## Affected spec sections

- spec/cli.md — modify: the `Migrations` tracking-table description states the
  table is created first and its SingleSelect fields (`Direction`, `Status`) are
  added as separate field-create calls so their choices materialize on every
  backend.
- spec/quality.md — modify: the integration-test section becomes
  backend-parameterized — the default bundled-SQLite run plus external MySQL and
  Postgres sources (NocoDB with `NC_DB` pointing at a DB container on a shared
  testcontainers network) — as the regression guard for issue #1.
- spec/overview.md — modify: add a product-wide success criterion that the
  `Migrations` table is created successfully on external SQL backends (MySQL and
  PostgreSQL), not only the bundled store.

## Target state

### spec/cli.md (after)

The "Migrations tracking table" section keeps the field list and the
SingleSelect-by-design note, and adds: the table is created in two steps — the
non-select fields (`Timestamp`, `Name`, `AppliedAt`) in the create-table request,
then `Direction` and `Status` added via separate field-create calls — because a
single bulk create does not materialize select choices into the column on
external SQL sources such as MySQL.

### spec/quality.md (after)

The Integration tests section becomes backend-parameterized: besides the default
single-container run on the bundled store (SQLite), MySQL- and Postgres-backed
scenarios start NocoDB with `NC_DB` pointing at a MySQL or Postgres container on a
shared network and assert that the `Migrations` table is created with valid
select columns (e.g. `enum(...)` on MySQL) — the regression guard for issue #1.

### spec/overview.md (after)

Product-wide success criteria gain: the in-base `Migrations` table is created
successfully regardless of the NocoDB backend, including external SQL sources
such as MySQL and PostgreSQL.

## Out of scope

- The broader Meta API v3 audit (issue #2); this task fixes one concrete finding.
- Filing the underlying behaviour upstream with NocoDB (do separately).
- Any change to the migration file format, operation types, or the recorded-row
  schema.
- Reworking how user migrations create their own SingleSelect fields (the same
  upstream limitation may apply to `create_table`/`create_field` operations — a
  candidate follow-up, but this task scopes only the internal `Migrations` table).

## Boundaries

- ✅ Always — keep `Direction`/`Status` as SingleSelect with their choices; keep
  unit tests network-free; gate the MySQL regression test behind the
  `integration` build tag and a Docker check.
- ⚠️ Ask first — extending the fix to user-authored `create_field`/`create_table`
  select handling; changing the client's `CreateField`/`CreateTable` signatures
  in a way that ripples beyond storage.
- 🚫 Never — replace SingleSelect with SingleLineText; commit a real token/base/
  URL; target a NocoDB API version other than Meta API v3.
