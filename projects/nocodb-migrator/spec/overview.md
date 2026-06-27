# nocodb-migrator — Product spec

## Vision

A command-line migration tool for [NocoDB](https://nocodb.com), giving teams the
same disciplined, version-controlled schema-and-data workflow they expect from
SQL migration tools, but expressed against NocoDB's Meta API v3. Changes are
authored as timestamped JSON files, applied in order with `up`, rolled back with
`down`, and inspected with `info`. The set of applied migrations is tracked in a
`Migrations` table the tool maintains inside the target base, so the migration
history travels with the data and needs no external store. The product is a
single Go binary (`nocodb-migrate`) configured entirely from the environment.

## Capabilities

- [cli.md](cli.md) — the `nocodb-migrate` commands (`create`, `up`, `down`,
  `info`), environment configuration, migration file discovery and ordering, and
  the in-base `Migrations` tracking table.
- [migration-format.md](migration-format.md) — the JSON migration file format:
  the eight operation types, the supported NocoDB column types, and validation
  rules applied before a migration runs.
- [nocodb-api.md](nocodb-api.md) — the NocoDB Meta API v3 client: token
  authentication, the table/field/record endpoints used, and how operations map
  onto them.
- [quality.md](quality.md) — the automated test strategy (unit tests over the API
  client, storage, and executor against an in-process mock NocoDB, plus an opt-in
  integration suite running the real commands against a dockerized NocoDB), the
  GitHub Actions CI pipeline, and the local pre-commit checks.

## Product-wide success criteria

- `go build` produces a `nocodb-migrate` binary that exposes `create`, `up`,
  `down`, and `info` subcommands.
- With valid `NOCODB_URL`, `NOCODB_API_TOKEN`, and `NOCODB_BASE_ID`, the tool
  applies pending migrations against a live NocoDB base and records each in the
  `Migrations` table.
- Migrations apply in ascending timestamp order on `up` and roll back in
  descending order on `down`; an already-applied migration is not re-applied.
- A missing required environment variable, an unreachable instance, or an
  invalid migration JSON fails the command with a non-zero exit and a wrapped
  error message rather than partial silent success.
- The NocoDB integration boundary is covered by unit tests that run on every CI
  push/PR alongside lint (API client, storage, executor against an in-process
  mock) and by an opt-in integration suite that runs the real `up`/`down` against
  a dockerized NocoDB in a separate CI job.
- The in-base `Migrations` table is created successfully regardless of the NocoDB
  backend, including external SQL sources such as MySQL and PostgreSQL, not only
  the bundled store.

## Boundaries

Beyond the global rules ([git.md](../../../rules/git.md),
[go.md](../../../rules/go.md)), the project deltas are:

- ✅ Always — keep migrations expressed as the timestamped JSON file pair
  (`*.up.json` / `*.down.json`); read all configuration from the environment;
  resolve NocoDB tables and fields by title in migration JSON.
- ⚠️ Ask first — adding a new operation type or column type to the format;
  changing the migration file naming or ordering scheme; introducing local state
  outside the in-base `Migrations` table.
- 🚫 Never — commit a real `NOCODB_API_TOKEN`, base id, or instance URL (use
  `.env` / environment, with `.env.example` as the only committed template);
  target a NocoDB API version other than Meta API v3 without a deliberate task.
