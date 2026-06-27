# Plan — 002-integration-tests-nocodb

> Draft carried over from task 001's split. Review and refine with `sys.task.plan`
> before implementation — especially the NocoDB bootstrap mechanism, which is the
> main unknown.

## Approach

Run the real `up`/`down`/`info` flow against a NocoDB container, gated so it never
touches the default test path. `api.NewClient` takes the base URL, so the test
just points the client at the container's URL with a bootstrapped token/base. The
suite is the cross-check the unit mocks (task 001) cannot provide.

## Stack

Base stack (Go) plus:

- `github.com/testcontainers/testcontainers-go` — start NocoDB in Docker for the
  integration suite. NocoDB runs standalone on its bundled SQLite meta-store, so a
  single container suffices — no separate DB service.
- Reuses task 001's `testify`, `.golangci.yml`, and CI workflow.

`testcontainers-go` is the only new `go.mod` require this task introduces.

## Architecture

- Files tagged `//go:build integration`. Default `go test ./...` skips them; run
  via `go test -tags=integration ./...`. Also guard on a Docker-availability check
  so a tagged run without Docker skips with a clear message rather than failing.
- A `testcontainers-go` helper starts `nocodb/nocodb` (pinned tag), waits for HTTP
  ready, provisions an API token / base (via NocoDB's bootstrap), and exposes
  `NOCODB_URL`/`NOCODB_API_TOKEN`/`NOCODB_BASE_ID` to the test.
- One end-to-end test: apply a migration with the real `up` path → assert the
  table/fields/records exist via the client → run `down` → assert the base returns
  to its prior state. This is the test that would have caught the
  `Migrations`-table SQL error and any v3 endpoint drift.
- CI: a separate `integration` job added to `.github/workflows/ci.yml` (Docker
  available on `ubuntu-latest`), running `go test -tags=integration ./...`. Slower;
  kept off the fast lint+unit critical path.

## Trade-offs & alternatives

- **testcontainers-go vs. docker-compose vs. a shared remote NocoDB.** Compose
  needs external orchestration in CI; a shared instance violates the "ephemeral,
  never a real base" boundary. testcontainers gives per-test isolated lifecycle in
  Go. Chosen: testcontainers.
- **Integration gate: build tag vs. env var only.** Build tag keeps the default
  `go test ./...` (and the pre-commit hook) from even compiling the Docker deps
  path; pair it with a runtime Docker check for a clean skip. Chosen: both.

## Constraints & risks

- Follow [go.md](../../../../../rules/go.md), [docker.md](../../../../../rules/docker.md),
  and [git.md](../../../../../rules/git.md).
- 🚫 No real `NOCODB_API_TOKEN`/base id/URL committed; config comes only from the
  ephemeral container.
- **Risk: NocoDB bootstrap in a container** (creating the first token/base
  programmatically) is the fiddliest part and may need a signup/auth call before
  the API token works. Mitigation: encapsulate setup in one helper; pin the image
  tag so behaviour is stable. This is the item to nail down in `sys.task.plan`.
- **Risk: integration job flakiness/time** on CI. Mitigation: separate job, not
  blocking the fast lint+unit signal; generous wait-for-ready strategy.
- Tests encode Meta API **v3** only — a failing test against real NocoDB is a
  finding for the issue-#2 audit, not something to paper over.

## Testing strategy

- `go test -tags=integration ./...` applies+rolls back a migration against a
  dockerized NocoDB and asserts schema/data — passing proves the v3 contract;
  failing pinpoints drift for follow-up issue-#1/#2 tasks.
- Default `go test ./...` still green and Docker-free.
- CI: a separate `integration` job green on PRs.
