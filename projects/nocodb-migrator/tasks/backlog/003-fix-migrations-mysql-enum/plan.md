# Plan — 003-fix-migrations-mysql-enum

## Approach

Two-step table creation in the storage layer, plus a backend-parameterized
integration regression test across SQLite, MySQL, and Postgres. The investigation
already proved the fix on a live MySQL-backed NocoDB: creating the table without
the SingleSelect fields and then adding `Direction`/`Status` via separate
`POST /tables/{id}/fields` calls yields real `enum('up','down')` /
`enum('success','failed')` columns, whereas the bulk `POST /tables` emits a
value-less `enum`. The api client already exposes both `CreateTable` and
`CreateField`, so the change is confined to `internal/storage/migrations.go` — no
client or format changes.

## Stack

Base stack (Go), no new production deps. Tests reuse testcontainers-go (already
present) and add MySQL and Postgres containers on a shared network. The DB
readiness dance is the fiddly part: prefer the testcontainers **mysql** and
**postgres** modules (`testcontainers-go/modules/{mysql,postgres}`) for reliable
waits over generic containers with log-based waits
(`wait.ForLog("ready for connections").WithOccurrence(2)` for MySQL; the postgres
module handles the double-start wait for PG). Decide during implementation,
preferring the modules for stability. Postgres aligns with the project base stack
(rules/data.md), MySQL is the backend from the issue #1 report.

## Architecture

### Fix — `EnsureMigrationsTable`

Today the method builds one `TableCreate` with all five fields and calls
`CreateTable`. Change to:

1. `CreateTable` with only the non-select fields: `Timestamp` (Number), `Name`
   (SingleLineText), `AppliedAt` (DateTime). Capture `table.ID`.
2. `CreateField(table.ID, …)` for `Direction` (SingleSelect, choices up/down) and
   for `Status` (SingleSelect, choices success/failed) — the exact `FieldCreate`
   options the code uses today, just sent per-field.
3. Set `s.tableID = table.ID`.

Idempotency / partial-failure hardening: the existing early-return when the table
already exists would, after a mid-create failure, leave a table missing its
select fields. Make the "table exists" branch ensure `Direction`/`Status` are
present (look them up in the fetched schema; `CreateField` any that are missing)
so a re-run heals a partial create. Keep this minimal and table-scoped.

No change to `RecordMigration`, the recorded-row schema, or the migration format.

### Regression test — backend-parameterized topology

Extend `internal/testutil` (under `//go:build integration`) so NocoDB can be
started on a chosen backend. Introduce a `Backend` enum (`SQLite`, `MySQL`,
`Postgres`) and a `StartNocoDBOn(t, backend) *NocoDB`:

- **SQLite** — the current single-container path (no `NC_DB`).
- **MySQL** — a `network.New(ctx)` shared network; a MySQL container (`mysql:8`,
  `MYSQL_ROOT_PASSWORD`, `MYSQL_DATABASE=nocodb`), `NetworkAliases` → `mysql`,
  started and waited on first; then NocoDB with
  `Env: NC_DB=mysql2://mysql:3306?u=root&p=<pw>&d=nocodb`.
- **Postgres** — same shape with a `postgres:16` container (alias `postgres`,
  `POSTGRES_PASSWORD`/`POSTGRES_DB`) and
  `Env: NC_DB=pg://postgres:5432?u=postgres&p=<pw>&d=nocodb`.

All three return the same `*NocoDB` struct and reuse the existing `bootstrap()`
(signup → token → workspace → base) unchanged — it only needs `n.URL`.
`t.Cleanup` terminates the NocoDB container, and the DB container + network where
present. Keep the existing `StartNocoDB` as a thin wrapper over
`StartNocoDBOn(t, SQLite)` so the current integration test is untouched.

The regression test (e.g. `internal/storage/migrations_integration_test.go`,
build-tag `integration`) is **table-driven over the three backends**: for each,
start NocoDB on that backend, build a client, call
`storage.NewMigrationsStorage(client).EnsureMigrationsTable()` and
`require.NoError`, then `GetTableByName("Migrations")` and assert `Direction` /
`Status` are present, `type == SingleSelect`, and carry their choices. On the
pre-fix bulk path the MySQL and Postgres subtests fail (`EnsureMigrationsTable`
errors, e.g. `ER_PARSE_ERROR` on MySQL); all pass after the fix. SQLite is
included so the matrix documents that the two-step path is correct there too.

Whether the empty-enum bug also reproduces on Postgres with the *old* code is
confirmed during implementation; either way the parameterized test pins the
behaviour and guards the fix.

### CI

The existing `integration` job runs `go test -tags=integration ./...`, which
picks up the new test automatically (it also pulls the `mysql:8` and
`postgres:16` images). No new job needed; note the extra image-pull/startup time
for the two DB backends.

## Trade-offs & alternatives

- **Separate field-create vs. SingleLineText.** SingleLineText would also fix the
  crash but is explicitly rejected — the select semantics are by design
  (spec/cli.md). Separate field-create preserves them. Chosen.
- **Assert via the NocoDB API vs. connecting to MySQL to read `information_schema`.**
  Asserting the field type + choices through the client is enough for the
  regression (the bug manifests as a failed `EnsureMigrationsTable`); a raw MySQL
  DDL check is stronger but couples the test to the physical table name. Default
  to the API-level assertion; optionally add a DDL check if cheap.
- **DB modules vs. generic containers.** The mysql/postgres modules remove DB
  readiness flakiness at the cost of one more (largely transitive) dependency each.
  Lean modules.
- **Three backends vs. MySQL only.** The bug was found on MySQL, but Postgres is
  the project's base-stack SQL engine and a likely second victim of the same
  upstream behaviour; SQLite is the default store. Covering all three turns the
  test into a backend matrix that both reproduces issue #1 and prevents a silent
  regression on any supported backend. The cost is CI time for two extra DB
  containers — accepted, kept in the separate `integration` job.

## Constraints & risks

- Follow [go.md](../../../../../rules/go.md), [docker.md](../../../../../rules/docker.md),
  [git.md](../../../../../rules/git.md).
- 🚫 Keep `Direction`/`Status` as SingleSelect — no text downgrade.
- **Risk: DB container startup time/flakiness in CI** (now MySQL *and* Postgres).
  Mitigation: use the DB modules' readiness waits; start the DB before NocoDB;
  generous timeouts; the matrix runs in the separate `integration` job.
- **Risk: NocoDB needs the DB reachable at boot.** Start order + NocoDB's own
  connect-retry cover it; wait NocoDB on `/api/v1/version` after the DB is ready.
- **Risk: NC_DB connection-string shape differs per engine** (`mysql2://` vs
  `pg://`). Centralize the per-backend `NC_DB` in the helper and confirm each
  during implementation.
- **Scope creep:** user-authored `create_field`/`create_table` SingleSelect
  operations likely hit the same upstream limitation. Out of scope here; flag as
  a follow-up (and an issue-#2 audit point).

## Testing strategy

- Unit suite (mock NocoDB) updated to reflect the new call sequence:
  `EnsureMigrationsTable` now issues a `CreateTable` (non-select fields) followed
  by two `CreateField` calls — assert that sequence and the per-field choices in
  `internal/storage/migrations_test.go`.
- New backend-parameterized integration test (SQLite, MySQL, Postgres): the
  MySQL/Postgres subtests are red before the fix and green after; SQLite stays
  green throughout — the regression guard and backend matrix.
- The existing SQLite end-to-end integration test stays green.
- `go test ./...` (default) stays network-free and green; `golangci-lint` clean.
