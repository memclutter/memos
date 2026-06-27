# Iteration 001 — implement unit suite, CI, pre-commit

## What shipped (in vcs/nocodb-migrator)

- `internal/testutil/fake.go` — stateful in-process fake NocoDB Meta API v3
  (tables/fields/records) that records every request; the shared harness for all
  unit tests.
- `internal/api/nocodb_test.go` — client wire-contract tests: auth header + base
  scoping, name resolution, `fields`-wrapped insert body, `[{"id":…}]` delete
  bodies, `{"records":[…]}`→`RecordList` decoding, error message vs status
  fallback.
- `internal/storage/migrations_test.go` — `EnsureMigrationsTable` payload guard
  (issue #1), idempotency, record round-trips, `DeleteMigrationRecord`.
- `internal/migration/operations_test.go` + `executor_test.go` — dispatch for all
  eight op types, unknown-type error, stop-and-wrap on first failure.
- `.golangci.yml` (v2), `.github/workflows/ci.yml` (`lint-unit` job),
  `.pre-commit-config.yaml`, `CONTRIBUTING.md` + `CHANGELOG.md` updates.
- Added `testify` to `go.mod`.

## Incidental fixes (to get a clean lint baseline)

Pre-existing lint failures fixed so the new CI gate is green: unchecked
`RecordMigration` errors in `cmd/up.go` (best-effort `_ =`), `gofmt`/`goimports`
in `cmd/down.go`/`cmd/info.go`/`parser_test.go`, two staticcheck S1009 nil-map
checks in `parser.go`, and unchecked closes in `parser_test.go`.

## Verification

- `go build ./...` — OK.
- `go test -count=1 ./...` — all packages pass.
- `golangci-lint run ./...` — 0 issues.
- `pre-commit run --all-files` — gofmt, golangci-lint, go test all pass.

## Out of scope / follow-ups

- Integration tests against a real dockerized NocoDB → task
  002-integration-tests-nocodb.
- A `where`-filtered list in the fake is intentionally permissive; the real
  `where` query shape is a finding for the issue-#2 audit, exercised by task 002.
