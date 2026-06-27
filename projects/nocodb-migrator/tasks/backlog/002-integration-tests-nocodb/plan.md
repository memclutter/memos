# Plan — 002-integration-tests-nocodb

## Approach

Drive the **real command path** end to end against a throwaway NocoDB container.
`cmd.runUp` / `cmd.runDown` are unexported and read all their configuration from
the environment (`initClient` → `NOCODB_URL`/`NOCODB_API_TOKEN`/`NOCODB_BASE_ID`,
`getMigrationsDir` → `NOCODB_MIGRATIONS_DIR`). So an integration test in
`package cmd`, compiled only under a build tag, can:

1. start NocoDB in Docker (testcontainers-go) and bootstrap a token + base,
2. set the env vars and point `NOCODB_MIGRATIONS_DIR` at a temp dir holding a
   `*.up.json` / `*.down.json` pair,
3. call `runUp(0)`, assert the resulting tables/fields/records via the api
   client, call `runDown(0)`, and assert the base is back to its prior state.

This exercises the same code a user runs (`up`/`down` → storage → executor →
client → live NocoDB), which is the only place the issue #1 / #2 drift actually
shows up. The unit suite (task 001) already covers shaping against a mock; this
task adds the real-server cross-check.

The single real unknown is **bootstrapping auth on a fresh container** (getting a
working `xc-token` and a base id). That is scheduled as the first step — a spike
against the pinned image — because the exact signup/token endpoints are
version-specific.

## Stack

Base stack (Go) plus one new test-only dependency:

- `github.com/testcontainers/testcontainers-go` — container lifecycle. NocoDB
  runs standalone on its bundled SQLite meta-store, so a single container
  suffices; no separate DB service.
- Reuses task 001's `testify`, `.golangci.yml`, and CI workflow.

`testcontainers-go` and its transitive deps land in `go.mod`, but only compile
under the `integration` build tag (see below), so the default unit build and the
pre-commit hook stay free of it.

## Architecture

### Build-tag + Docker gating

- All new integration files start with `//go:build integration`. Default
  `go test ./...` does not compile them; the suite runs via
  `go test -tags=integration ./...`.
- Runtime guard: before starting a container, check Docker is reachable
  (testcontainers' provider health check / `DOCKER_HOST`); if not, `t.Skip` with
  a clear message rather than failing. So a tagged run on a Docker-less machine
  skips cleanly.

### NocoDB container + bootstrap helper

`internal/testutil/nocodb_container.go` (also `//go:build integration`, so it
never enters the unit build):

- Starts `nocodb/nocodb` pinned to a specific tag that exposes `/api/v3/meta`
  (the exact tag is fixed in the spike — see Step 1), waits for HTTP readiness on
  the mapped port.
- `Bootstrap()` returns `(url, token, baseID)`:
  1. `POST /api/v1/auth/user/signup` `{email,password}` → super-admin JWT
     (`xc-auth`), since the first user on a fresh instance becomes admin.
  2. Create a base (title `migrator_it`) with the JWT → `baseID`. (v2 vs v3 meta
     path confirmed against the pinned image in the spike.)
  3. Create an API token with the JWT → `nc_pat_…` (`xc-token`). Endpoint
     confirmed in the spike.
- Exposes the three values to the test, which sets them as env vars (and restores
  them via `t.Setenv`, which auto-restores).

### The end-to-end test

`cmd/integration_test.go` (`//go:build integration`, `package cmd`):

- `t.Setenv` for the four env vars; write a temp migrations dir with a migration
  that creates a table, adds a field, inserts a row (covering create_table /
  create_field / insert_row) and a matching `*.down.json` that reverses it.
- `require.NoError(t, runUp(0))`; assert via `api.NewClient(...)` that the table,
  field, and row exist, and that the `Migrations` table recorded the apply.
- `require.NoError(t, runDown(0))`; assert the table is gone and the `Migrations`
  history reflects the rollback.

### CI

Extend `.github/workflows/ci.yml` with a second job `integration` (the `lint-unit`
job is untouched):

- `runs-on: ubuntu-latest` (Docker is available there), setup-go,
  `go test -tags=integration ./...`.
- Kept independent of `lint-unit` so the fast signal is never blocked by the
  slower container run.

## Trade-offs & alternatives

- **Drive `runUp`/`runDown` vs. exec the built binary vs. call executor+storage
  directly.** Calling the unexported `runUp`/`runDown` from an internal test runs
  the real command logic (env parsing, file discovery, ordering, recording)
  without a subprocess — truest e2e with the least machinery. Exec-ing the binary
  adds build/PATH plumbing for no extra coverage; calling executor+storage
  directly skips the command layer that `info`/ordering bugs live in. Chosen:
  internal `runUp`/`runDown`.
- **testcontainers-go vs. docker-compose vs. shared instance.** Compose needs
  external orchestration in CI; a shared instance breaks the "ephemeral, never a
  real base" boundary. Chosen: testcontainers.
- **Programmatic bootstrap vs. a pre-baked image/volume with a fixed token.**
  Programmatic is self-contained and survives image bumps; a pre-baked volume is
  a fallback if token creation proves too brittle on the pinned tag.

## Constraints & risks

- Follow [go.md](../../../../../rules/go.md), [docker.md](../../../../../rules/docker.md),
  and [git.md](../../../../../rules/git.md) (Conventional Commits, green CI per PR).
- 🚫 No real `NOCODB_API_TOKEN`/base id/URL committed; everything comes from the
  ephemeral container.
- **Primary risk — bootstrap brittleness.** The signup/base/token endpoints differ
  across NocoDB releases. Mitigation: Step 1 is a spike that pins the image tag
  and the exact three calls; the helper centralizes them so an image bump is a
  one-file change. Fallback: pre-baked volume with a known token.
- **Risk — CI time/flakiness.** A container cold start is slow. Mitigation:
  separate job off the fast path; generous wait-for-ready; pin the tag for
  reproducibility.
- A failing assertion against real NocoDB is a **finding for the issue #2 audit**
  (the implementation diverging from v3), not something to weaken the test for.
  Known suspects the e2e may surface: the `GetRecords`/`DeleteRecords` `where`
  query shape and the `Migrations`-table create payload.

## Testing strategy

The deliverable is the integration suite itself:

- `go test -tags=integration ./...` brings up NocoDB, applies a migration via the
  real `up`, asserts schema + data + `Migrations` record, rolls back via `down`,
  and asserts the prior state — green proves conformance to Meta API v3.
- Default `go test ./...` stays green and Docker-free (tag excludes the suite).
- A tagged run without Docker skips cleanly.
- CI shows a separate green `integration` job on PRs.

## Step order

1. **Spike: bootstrap.** Pin the `nocodb/nocodb` tag; from a one-off test, get a
   container up and obtain a working `xc-token` + base id; lock the exact
   signup/base/token calls. (De-risks everything else.)
2. Container + `Bootstrap()` helper in `internal/testutil` under the tag, with the
   Docker-availability skip.
3. The `cmd/integration_test.go` e2e (up → assert → down → assert) with a temp
   migrations dir.
4. The `integration` CI job; confirm green.
5. Docs: note the tagged suite and its Docker requirement in `CONTRIBUTING.md`.
