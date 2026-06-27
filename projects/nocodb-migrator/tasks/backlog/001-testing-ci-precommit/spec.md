# Spec — 001-testing-ci-precommit

## Problem

The tool has almost no automated verification: a single
`internal/migration/parser_test.go` exists, and nothing exercises the actual
NocoDB integration — the API client, the in-base `Migrations` table, or the
operation executor. Nothing runs in CI, and there are no local hooks. This is
exactly how the implementation drifted away from the live Meta API v3
(memclutter/nocodb-migrator issues #1 and #2): a malformed `Migrations`-table
call now fails with a raw SQL parse error, and there is no test that would have
caught it. Without tests, a fix to the API surface can silently break another
path.

## Goal

Make the tool's behaviour against NocoDB verifiable and keep it from drifting
again: a unit suite over the API/storage/executor layers, an opt-in integration
suite that runs the real commands against a dockerized NocoDB, a GitHub Actions
pipeline running them, and a pre-commit configuration that runs the fast checks
on every commit.

## User journeys

- A contributor runs `go test ./...` and gets fast, deterministic unit coverage
  of the API client, storage, and executor without any network or NocoDB
  instance.
- A contributor opts into the integration suite (build tag / env var); it spins
  up NocoDB in Docker, runs `up` then `down` against it, and asserts the
  resulting schema and data — catching any divergence from Meta API v3.
- A contributor opens a PR; CI runs lint + unit on every push, and the
  integration job (separate, slower) verifies the end-to-end flow before merge.
- A contributor commits; pre-commit runs `gofmt`/`goimports`, `golangci-lint`,
  and the fast unit tests, blocking the commit on failure.

## Success criteria

- `go test ./...` passes and meaningfully covers `internal/api`,
  `internal/storage`, and `internal/migration` execution via an in-process
  `httptest` mock NocoDB server.
- An opt-in integration suite applies and rolls back a migration against a
  dockerized NocoDB and asserts the schema/data outcome; it is skipped by
  default so the unit run needs no Docker.
- A GitHub Actions workflow runs lint + unit on every push/PR and runs the
  integration suite in a separate job that brings up NocoDB.
- A `.pre-commit-config.yaml` (pre-commit framework) runs formatting, lint, and
  fast unit tests; `pre-commit run --all-files` passes.
- No real `NOCODB_API_TOKEN`, base id, or URL is committed; integration
  configuration is read from the environment / ephemeral docker instance.

## Affected spec sections

- spec/quality.md — NEW capability: the testing strategy (unit + integration
  layers and what each covers), the CI pipeline, and the pre-commit setup.
- spec/overview.md — add `quality.md` to the Capabilities list and add a
  product-wide success criterion that the integration boundary is covered by an
  automated suite running in CI.

## Target state

### spec/overview.md (after)

The Capabilities list gains an entry:

> - [quality.md](quality.md) — the automated test strategy (unit tests over the
>   API client, storage, and executor; opt-in integration tests against a
>   dockerized NocoDB), the GitHub Actions CI pipeline, and the local pre-commit
>   checks.

Product-wide success criteria gain:

> - The NocoDB integration boundary is covered by an automated test suite: unit
>   tests run on every CI push/PR alongside lint, and an opt-in integration
>   suite exercises `up`/`down`/`info` against a real dockerized NocoDB.

### spec/quality.md (NEW)

Describes the end state of project quality tooling:

- **Unit tests** — standard `testing` + table-driven, `testify` for assertions.
  An in-process `httptest` server stands in for NocoDB; tests assert the request
  method/path/headers (`xc-token`, base id) and the response decoding for the
  client, the `Migrations`-table create/list/insert logic in storage, and the
  operation→endpoint dispatch in the executor. No network, runs by default.
- **Integration tests** — gated behind a build tag (e.g. `//go:build
  integration`) and/or an env flag, started against a NocoDB brought up in
  Docker (testcontainers-go is the expected mechanism). They apply a migration
  with `up`, inspect the resulting tables/fields/records, then `down`, asserting
  the base returns to its prior state. Skipped when Docker/the flag is absent.
- **CI** — a GitHub Actions workflow: one job runs `gofmt`/`goimports` check +
  `golangci-lint` + `go test ./...` (unit) on every push and PR; a separate job
  runs the integration suite with NocoDB available. Lint config lives in
  `.golangci.yml`.
- **pre-commit** — a `.pre-commit-config.yaml` (pre-commit framework) running
  formatting, `golangci-lint`, and the fast unit tests on commit;
  `CONTRIBUTING.md` documents installing and running the hooks and both suites.

## Out of scope

- Fixing the actual API drift / issue #1 and #2 bugs — this task builds the
  safety net that proves and guards such fixes; the fixes themselves are
  separate tasks (the audit, etc.).
- Adding new operation or column types, or changing the migration file format.
- Release automation / publishing the binary.

## Boundaries

- ✅ Always — keep unit tests network-free via `httptest`; gate integration
  tests so the default `go test ./...` needs no Docker; read all integration
  configuration from the environment / an ephemeral instance.
- ⚠️ Ask first — pulling in an integration framework beyond Docker +
  testcontainers-go; adding a CI provider other than GitHub Actions; changing
  the base stack (rules/stack.md) to satisfy tooling.
- 🚫 Never — commit a real `NOCODB_API_TOKEN`, base id, or instance URL; encode
  endpoints outside Meta API v3 in tests; let tests mutate a shared/real NocoDB
  base instead of an ephemeral one.
