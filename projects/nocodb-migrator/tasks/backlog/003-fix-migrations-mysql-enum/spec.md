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

Make `EnsureMigrationsTable` succeed on every NocoDB backend — including external
MySQL — while keeping `Direction`/`Status` as SingleSelect, by creating the table
first and then adding the two select fields via separate field-create calls. Add
a MySQL-backed regression test so the fix is guarded.

## User journeys

- A user points the tool at a MySQL-backed NocoDB base and runs
  `nocodb-migrate info` / `up`: the `Migrations` table is created without error,
  with `Direction` and `Status` as proper `enum(...)` columns, and the command
  proceeds.
- A contributor runs the MySQL-backed integration test; it stands up NocoDB on
  MySQL, creates the Migrations table, and asserts the select columns and their
  choices — failing on the old bulk-create code and passing on the fix.

## Success criteria

- Against a MySQL-backed NocoDB, `EnsureMigrationsTable` succeeds; the physical
  columns are `enum('up','down')` (Direction) and `enum('success','failed')`
  (Status). No `ER_PARSE_ERROR`.
- `Direction` and `Status` remain SingleSelect carrying their choices — no
  downgrade to `SingleLineText`.
- The existing SQLite integration suite and the unit suite stay green.
- A MySQL-backed integration regression test exists, fails against the pre-fix
  bulk-create path, and passes after the fix; it runs in CI.

## Affected spec sections

- spec/cli.md — modify: the `Migrations` tracking-table description states the
  table is created first and its SingleSelect fields (`Direction`, `Status`) are
  added as separate field-create calls so their choices materialize on every
  backend.
- spec/quality.md — modify: the integration-test section gains the MySQL-backed
  regression scenario (NocoDB on an external MySQL source via a shared
  testcontainers network).
- spec/overview.md — modify: add a product-wide success criterion that the
  `Migrations` table is created successfully on external SQL backends (e.g.
  MySQL), not only the bundled store.

## Target state

### spec/cli.md (after)

The "Migrations tracking table" section keeps the field list and the
SingleSelect-by-design note, and adds: the table is created in two steps — the
non-select fields (`Timestamp`, `Name`, `AppliedAt`) in the create-table request,
then `Direction` and `Status` added via separate field-create calls — because a
single bulk create does not materialize select choices into the column on
external SQL sources such as MySQL.

### spec/quality.md (after)

The Integration tests section notes a second topology: besides the default
single-container (bundled store) run, a MySQL-backed scenario starts NocoDB with
`NC_DB` pointing at a MySQL container on a shared network and asserts that the
`Migrations` table is created with valid `enum(...)` columns — the regression
guard for issue #1.

### spec/overview.md (after)

Product-wide success criteria gain: the in-base `Migrations` table is created
successfully regardless of the NocoDB backend, including external SQL sources
such as MySQL.

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
