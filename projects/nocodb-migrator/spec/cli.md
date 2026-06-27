# cli

## Purpose

The `nocodb-migrate` command-line interface: how a user authors, applies, rolls
back, and inspects migrations, how the tool is configured, and how it discovers,
orders, and tracks migration files. This is the operator-facing surface of the
product.

## Behaviour

### Configuration

All configuration comes from the environment. On startup the tool loads a `.env`
file from the working directory if present (a missing file is not an error —
it logs and falls back to the ambient environment), then reads:

- `NOCODB_URL` (required) — base URL of the NocoDB instance.
- `NOCODB_API_TOKEN` (required) — API token sent as the `xc-token` header.
- `NOCODB_BASE_ID` (required) — id of the target base.
- `NOCODB_MIGRATIONS_DIR` (optional) — directory holding migration files;
  defaults to `./migrations`.

Any command that talks to NocoDB fails fast with a clear error if one of the
three required variables is empty. A relative migrations directory is resolved
against the current working directory.

### Commands

The root command `nocodb-migrate` exposes four subcommands and a `--version`
flag:

- `create <name>` — scaffolds a new migration. It ensures the migrations
  directory exists, takes a Unix timestamp, and writes two files:
  `{timestamp}-{name}.up.json` and `{timestamp}-{name}.down.json`, each
  pre-filled with an example (`create_table` for up, `drop_table` for down).
  It prints the two paths. This command does not contact NocoDB.
- `up [count]` — applies pending migrations in ascending timestamp order. With
  no argument it applies all pending; with `count` it applies at most that many.
- `down [count]` — rolls back applied migrations in descending timestamp order.
  `count` limits how many are rolled back (e.g. `down 1` rolls back the latest).
- `info` — prints the current version (`{timestamp}-{name}` of the latest
  successful `up`) and the list of recorded migrations with their direction and
  status.

### File discovery and ordering

For a given direction, the tool scans the migrations directory for files ending
in `.{up|down}.json`, parses the leading `{timestamp}-` prefix into the ordering
key and the remainder (before the suffix) into the migration name, and skips
files that don't match the pattern. `up` sorts ascending by timestamp; `down`
sorts descending.

### Applying (`up`)

1. Ensure the `Migrations` table exists (create it if absent).
2. Read the current version (highest timestamp among successful `up` records).
3. Select `*.up.json` migrations that are not yet successfully applied and whose
   timestamp is greater than the current version; optionally truncate to
   `count`.
4. For each, parse and validate the JSON, execute its operations in order, then
   record a row in `Migrations`. A parse or execution failure records a `failed`
   row and aborts the run with a wrapped error; remaining migrations are not
   attempted.

### Rolling back (`down`)

1. Ensure the `Migrations` table exists.
2. Select `*.down.json` migrations that are applied and at or below the current
   version, sorted newest-first; optionally truncate to `count`.
3. For each, parse and execute the down operations, then delete the
   corresponding `up` record from the `Migrations` table.

### The `Migrations` tracking table

State lives in the base, not on disk. On first use the tool creates a
`Migrations` table (if it does not already exist) with fields:

- `Timestamp` (Number) — timestamp parsed from the file name.
- `Name` (SingleLineText) — migration name.
- `AppliedAt` (DateTime) — when the row was recorded.
- `Direction` (SingleSelect: `up` / `down`).
- `Status` (SingleSelect: `success` / `failed`).

`Direction` and `Status` are **SingleSelect by design** — the fixed, colored
option set is the intended semantics (a constrained enumeration the user sees in
the NocoDB UI), not interchangeable with free `SingleLineText`. The table
creation must therefore materialize these select choices on every NocoDB backend,
including external SQL sources such as MySQL.

The current version is the highest `Timestamp` among rows with `Direction = up`
and `Status = success`. A migration counts as applied when such a row exists for
its timestamp and name. Rolling back deletes the matching `up` row.

## Success criteria

- `create foo` writes `{timestamp}-foo.up.json` and `{timestamp}-foo.down.json`
  into the migrations directory and prints both paths, without contacting
  NocoDB.
- Running `up` twice in a row applies each migration exactly once; the second
  run reports no pending migrations.
- `up 1` applies only the oldest pending migration; `down 1` rolls back only the
  newest applied one.
- With no `Migrations` table present, the first `up`/`down`/`info` creates it
  before doing its work.
- `info` on an empty history prints that no migrations are applied; after an
  `up`, it prints the current version and the recorded rows.
- Omitting any of `NOCODB_URL`, `NOCODB_API_TOKEN`, `NOCODB_BASE_ID` makes
  `up`/`down`/`info` exit non-zero naming the missing variable.
