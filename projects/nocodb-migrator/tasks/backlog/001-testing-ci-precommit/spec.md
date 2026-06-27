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

Give the tool a fast, deterministic unit test suite over the API/storage/executor
layers — driven by an in-process mock NocoDB so it needs no network — and wire it
into GitHub Actions CI (lint + unit) and a local pre-commit configuration.
End-to-end coverage against a real dockerized NocoDB is split into a separate
task (002-integration-tests-nocodb).

## User journeys

- A contributor runs `go test ./...` and gets fast, deterministic unit coverage
  of the API client, storage, and executor without any network or NocoDB
  instance.
- A contributor opens a PR; CI runs lint + unit on every push and blocks merge on
  failure.
- A contributor commits; pre-commit runs `gofmt`/`goimports`, `golangci-lint`,
  and the fast unit tests, blocking the commit on failure.

## Success criteria

- `go test ./...` passes and meaningfully covers `internal/api`,
  `internal/storage`, and `internal/migration` execution via an in-process
  `httptest` mock NocoDB server.
- A GitHub Actions workflow runs lint (`gofmt`/`goimports` check +
  `golangci-lint`) and unit tests on every push/PR.
- A `.pre-commit-config.yaml` (pre-commit framework) runs formatting, lint, and
  fast unit tests; `pre-commit run --all-files` passes.
- No real `NOCODB_API_TOKEN`, base id, or URL is committed; tests use only the
  in-process mock.

## Affected spec sections

- spec/quality.md — NEW capability: the unit testing strategy (what the
  api/storage/executor unit tests cover and the httptest mock approach), the CI
  pipeline (lint + unit), and the pre-commit setup. The integration-test layer is
  described by its own task (002) and folded in when that ships.
- spec/overview.md — add `quality.md` to the Capabilities list and add a
  product-wide success criterion that the integration boundary is covered by unit
  tests running in CI.

## Target state

### spec/overview.md (after)

The Capabilities list gains an entry:

> - [quality.md](quality.md) — the automated test strategy (unit tests over the
>   API client, storage, and executor against an in-process mock NocoDB), the
>   GitHub Actions CI pipeline, and the local pre-commit checks.

Product-wide success criteria gain:

> - The NocoDB integration boundary is covered by unit tests that run on every CI
>   push/PR alongside lint, exercising the API client, storage, and executor
>   against an in-process mock.

### spec/quality.md (NEW)

Describes the end state of project quality tooling (unit layer):

- **Unit tests** — standard `testing` + table-driven, `testify` for assertions.
  An in-process `httptest` server stands in for NocoDB; tests assert the request
  method/path/headers (`xc-token`, base id) and the response decoding for the
  client, the `Migrations`-table create/list/insert logic in storage, and the
  operation→endpoint dispatch in the executor. No network, runs by default with
  `go test ./...`.
- **CI** — a GitHub Actions workflow whose job runs `gofmt`/`goimports` check +
  `golangci-lint` + `go test ./...` (unit) on every push and PR. Lint config
  lives in `.golangci.yml`.
- **pre-commit** — a `.pre-commit-config.yaml` (pre-commit framework) running
  formatting, `golangci-lint`, and the fast unit tests on commit;
  `CONTRIBUTING.md` documents installing and running the hooks and the suite.

> The integration-test layer (dockerized NocoDB, end-to-end `up`/`down`) is added
> by task 002-integration-tests-nocodb and extends this capability.

## Out of scope

- **Integration tests against a real dockerized NocoDB** — split into task
  002-integration-tests-nocodb (testcontainers-go, end-to-end `up`/`down`, a
  separate CI job).
- Fixing the actual API drift / issue #1 and #2 bugs — this task builds the unit
  safety net; the fixes themselves are separate tasks.
- Adding new operation or column types, or changing the migration file format.
- Release automation / publishing the binary.

## Boundaries

- ✅ Always — keep unit tests network-free via `httptest` so the default
  `go test ./...` needs no Docker or live instance.
- ⚠️ Ask first — adding a CI provider other than GitHub Actions; changing the
  base stack (rules/stack.md) to satisfy tooling.
- 🚫 Never — commit a real `NOCODB_API_TOKEN`, base id, or instance URL; encode
  endpoints outside Meta API v3 in tests.
