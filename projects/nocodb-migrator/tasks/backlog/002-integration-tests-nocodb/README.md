# 002 — Integration tests against a dockerized NocoDB

## Goal

Prove the tool's behaviour against the *real* NocoDB Meta API v3 end to end: an
opt-in integration suite that brings up NocoDB in Docker and runs `up` / `down` /
`info` against it, asserting the resulting schema and data. This is the
cross-check that the unit mocks (task 001) cannot give and the test that would
have caught the issue #1 / #2 drift.

## Scope

- An integration test suite gated behind a build tag (`//go:build integration`)
  so the default `go test ./...` (and the pre-commit hook from task 001) never
  needs Docker.
- A `testcontainers-go` helper that starts `nocodb/nocodb` (pinned), waits for
  ready, bootstraps an API token / base, and exposes
  `NOCODB_URL`/`NOCODB_API_TOKEN`/`NOCODB_BASE_ID` to the test.
- One end-to-end test: apply a migration with `up`, assert tables/fields/records,
  run `down`, assert the base returns to its prior state.
- A separate `integration` CI job (extends the workflow from task 001) running
  `go test -tags=integration ./...`.

## Dependencies

- Builds on task 001 (unit suite, CI workflow, `CONTRIBUTING.md`) — extends the
  same `spec/quality.md` capability and the same CI workflow.

## Acceptance criteria

- `go test -tags=integration ./...` applies and rolls back a migration against a
  dockerized NocoDB and asserts the schema/data result; a tagged run without
  Docker skips cleanly rather than failing.
- A separate `integration` CI job is green on PRs.
- No real `NOCODB_API_TOKEN`, base id, or URL is committed; config comes only
  from the ephemeral container.

## Status

Backlog. Next phase: `sys.task.plan` (the plan below is a draft carried over from
task 001's split — review before implementation).
