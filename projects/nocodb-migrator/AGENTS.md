---
name: nocodb-migrator
vcs:
  - git@github.com:memclutter/nocodb-migrator.git
self: false
status: active
stack: [go]
created: 2026-06-27
---

A Go CLI that manages migrations for a [NocoDB](https://nocodb.com) base through
its Meta API v3. It follows the base stack ([rules/go.md](../../rules/go.md)):
Go modules, `cmd`/`internal` layout, wrapped errors, env-based config.

## Architecture

- `main.go` wires a [cobra](https://github.com/spf13/cobra) root command and
  loads a `.env` file (via `joho/godotenv`) before reading config from the
  environment.
- `cmd/` holds one file per subcommand (`create`, `up`, `down`, `info`) plus
  `common.go`, which builds the API client and resolves the migrations
  directory.
- `internal/api` is the NocoDB Meta API v3 client (built on `go-resty`):
  tables, fields, and records. `internal/migration` parses and validates
  migration JSON and executes each operation against the client.
  `internal/storage` manages the in-base `Migrations` tracking table.
- All state lives in NocoDB: applied migrations are rows in a `Migrations` table
  the tool creates on demand. There is no local lock or state file beyond the
  migration JSON files on disk.

## Conventions

- Migration files are named `{unix-timestamp}-{name}.{up|down}.json`; the
  timestamp is the ordering key. The `create` command scaffolds both files.
- Config is read only from the environment (`NOCODB_URL`, `NOCODB_API_TOKEN`,
  `NOCODB_BASE_ID`, optional `NOCODB_MIGRATIONS_DIR`); the first three are
  required and the command fails fast if any is missing.
- NocoDB entities are resolved by human-readable title (e.g. table/field names),
  not by id, in the migration JSON; the client maps names to ids at execution
  time.
- Source changes are committed and pushed inside `vcs/nocodb-migrator/`, then
  this OS pins the new submodule commit
  (`chore(submodule): bump nocodb-migrator`).
