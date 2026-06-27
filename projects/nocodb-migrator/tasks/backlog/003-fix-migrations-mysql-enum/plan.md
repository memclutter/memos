# Plan — 003-fix-migrations-mysql-enum

## Approach

Two-step table creation in the storage layer, plus a MySQL-backed integration
regression test. The investigation already proved the fix on a live MySQL-backed
NocoDB: creating the table without the SingleSelect fields and then adding
`Direction`/`Status` via separate `POST /tables/{id}/fields` calls yields real
`enum('up','down')` / `enum('success','failed')` columns, whereas the bulk
`POST /tables` emits a value-less `enum`. The api client already exposes both
`CreateTable` and `CreateField`, so the change is confined to
`internal/storage/migrations.go` — no client or format changes.

## Stack

Base stack (Go), no new production deps. Tests reuse testcontainers-go (already
present) and add a MySQL container on a shared network. The MySQL readiness dance
is the one fiddly part: use the testcontainers **mysql module**
(`testcontainers-go/modules/mysql`) for a reliable wait, or a generic container
with a robust `wait.ForLog("ready for connections").WithOccurrence(2)` — decide
during implementation, preferring the module for stability.

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

### Regression test — MySQL-backed topology

Extend `internal/testutil` (under `//go:build integration`) with a helper that
brings up the two-container topology:

- A `network.New(ctx)` shared network.
- A MySQL container (`mysql:8`, `MYSQL_ROOT_PASSWORD`, `MYSQL_DATABASE=nocodb`),
  `NetworkAliases` → `mysql`, started first and waited on.
- A NocoDB container with `Env: NC_DB=mysql2://mysql:3306?u=root&p=<pw>&d=nocodb`
  on the same network, waited on `/api/v1/version`.
- Reuse the existing `bootstrap()` (signup → token → workspace → base) unchanged;
  it only needs `n.URL`.

Return the same `*NocoDB` struct so tests are backend-agnostic. `t.Cleanup`
terminates both containers and the network.

The test (e.g. `internal/storage/migrations_mysql_integration_test.go`, build-tag
`integration`): start the MySQL-backed NocoDB, build a client, call
`storage.NewMigrationsStorage(client).EnsureMigrationsTable()` and
`require.NoError`. Then `GetTableByName("Migrations")` and assert `Direction` /
`Status` are present, `type == SingleSelect`, and carry their choices. This fails
on the pre-fix bulk path (the `EnsureMigrationsTable` call errors with
`ER_PARSE_ERROR`) and passes after.

### CI

The existing `integration` job runs `go test -tags=integration ./...`, which will
pick up the new test automatically (it pulls the `mysql:8` image too). No new job
needed; note the extra image-pull time.

## Trade-offs & alternatives

- **Separate field-create vs. SingleLineText.** SingleLineText would also fix the
  crash but is explicitly rejected — the select semantics are by design
  (spec/cli.md). Separate field-create preserves them. Chosen.
- **Assert via the NocoDB API vs. connecting to MySQL to read `information_schema`.**
  Asserting the field type + choices through the client is enough for the
  regression (the bug manifests as a failed `EnsureMigrationsTable`); a raw MySQL
  DDL check is stronger but couples the test to the physical table name. Default
  to the API-level assertion; optionally add a DDL check if cheap.
- **mysql module vs. generic container.** The module removes MySQL readiness
  flakiness at the cost of one more (already-transitive) dependency. Lean module.

## Constraints & risks

- Follow [go.md](../../../../../rules/go.md), [docker.md](../../../../../rules/docker.md),
  [git.md](../../../../../rules/git.md).
- 🚫 Keep `Direction`/`Status` as SingleSelect — no text downgrade.
- **Risk: MySQL container startup time/flakiness in CI.** Mitigation: robust wait
  (module or `WithOccurrence(2)`); start MySQL before NocoDB; generous timeouts.
- **Risk: NocoDB needs MySQL reachable at boot.** Start order + NocoDB's own
  connect-retry cover it; wait NocoDB on `/api/v1/version` after MySQL is ready.
- **Scope creep:** user-authored `create_field`/`create_table` SingleSelect
  operations likely hit the same upstream limitation. Out of scope here; flag as
  a follow-up (and an issue-#2 audit point).

## Testing strategy

- Unit suite (mock NocoDB) updated to reflect the new call sequence:
  `EnsureMigrationsTable` now issues a `CreateTable` (non-select fields) followed
  by two `CreateField` calls — assert that sequence and the per-field choices in
  `internal/storage/migrations_test.go`.
- SQLite integration test stays green (the two-step path works there too).
- New MySQL-backed integration test: red before the fix, green after — the
  regression guard.
- `go test ./...` (default) stays network-free and green; `golangci-lint` clean.
