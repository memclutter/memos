---
id: 002-integration-tests-nocodb
status: backlog
created: 2026-06-27
updated: 2026-06-27
---

## Goal

Add an opt-in integration test suite that runs nocodb-migrator's `up`/`down`/
`info` against a real NocoDB started in Docker, plus a separate CI job for it, so
the tool's conformance to the live Meta API v3 is verified end to end. Builds on
task 001 (unit suite + CI workflow).

## Scope

- Integration tests tagged `//go:build integration`; default `go test ./...`
  skips them. Also guard on a Docker-availability check so a tagged run without
  Docker skips with a clear message instead of failing.
- A `testcontainers-go` helper: start `nocodb/nocodb` (pinned tag), wait for HTTP
  ready, bootstrap an API token / base, expose `NOCODB_URL`/`NOCODB_API_TOKEN`/
  `NOCODB_BASE_ID`.
- End-to-end test: `up` a migration → assert tables/fields/records via the client
  → `down` → assert prior state restored.
- A separate `integration` job added to `.github/workflows/ci.yml` running
  `go test -tags=integration ./...`.

## Acceptance criteria

- `go test -tags=integration ./...` applies and rolls back a migration against a
  dockerized NocoDB and asserts schema/data; without Docker it skips cleanly.
- A separate `integration` CI job is green on PRs.
- `spec/quality.md` gains the integration-test layer (folded at Finish).

## Constraints

- Follow [go.md](../../../../../rules/go.md), [docker.md](../../../../../rules/docker.md),
  and [git.md](../../../../../rules/git.md) (Conventional Commits, green CI per PR).
- 🚫 Never commit a real `NOCODB_API_TOKEN`, base id, or URL; config comes only
  from the ephemeral container.
- Target Meta API v3 only — a failing test against real NocoDB is a finding for
  the issue-#2 audit, not something to paper over.
- ⚠️ Ask before pulling in an integration framework beyond Docker +
  testcontainers-go.

## Tasks breakdown

- [ ] 1. **Bootstrap spike.** Pin a `nocodb/nocodb` tag that exposes
  `/api/v3/meta`; from a throwaway `//go:build integration` test, start the
  container and obtain a working `xc-token` + base id. Lock the exact
  signup → create-base → create-token calls. ⚠️ Gate: confirm the pinned tag and
  bootstrap sequence with the owner before building on them. (de-risks the rest)
- [ ] 2. Add `testcontainers-go` (under the `integration` tag only) and a
  `internal/testutil/nocodb_container.go` helper (`//go:build integration`):
  start NocoDB, wait for ready, `Bootstrap() (url, token, baseID)` using the
  calls from step 1. Verify it does not enter the default unit build
  (`go build ./...` / `go test ./...` still clean, no testcontainers pulled).
- [ ] 3. Add the Docker-availability runtime guard so a tagged run without Docker
  `t.Skip`s with a clear message instead of failing.
- [ ] 4. Write `cmd/integration_test.go` (`//go:build integration`, `package cmd`):
  `t.Setenv` the four env vars, write a temp migrations dir (create_table +
  create_field + insert_row up / reversing down), call `runUp(0)`, assert
  table/field/row + `Migrations` record via the client, call `runDown(0)`, assert
  prior state restored. Record any real-NocoDB divergence as an issue-#2 finding.
- [ ] 5. Extend `.github/workflows/ci.yml` with a separate `integration` job
  (`go test -tags=integration ./...` on `ubuntu-latest`), independent of
  `lint-unit`; confirm green on the PR.
- [ ] 6. Document the tagged suite and its Docker requirement in `CONTRIBUTING.md`
  (replace the "tracked separately" note from task 001 with how to run it).
