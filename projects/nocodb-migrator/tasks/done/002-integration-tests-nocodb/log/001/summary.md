# Iteration 001 — integration suite, container helper, CI job

## What shipped (in vcs/nocodb-migrator, all under the `integration` build tag)

- `internal/testutil/nocodb_container.go` — `StartNocoDB(t)`: brings up
  `nocodb/nocodb:2026.06.1` via testcontainers-go, waits for `/api/v1/version`,
  and `bootstrap`s a usable `xc-token` + base. A `requireDocker` guard `t.Skip`s
  when Docker is absent (checks `DOCKER_HOST` / the docker socket — no docker
  client dependency, since moby v28 added required options args to the client
  methods).
- `cmd/integration_test.go` — `TestUpDownAgainstRealNocoDB`: writes a temp
  migrations dir, sets the four env vars, calls the real `runUp(0)`, asserts the
  Widgets table/fields/row and the `Migrations` record via the client, then
  `runDown(0)` and asserts the table is gone.
- `.github/workflows/ci.yml` — a separate `integration` job running
  `go test -tags=integration ./...` on `ubuntu-latest`, independent of `lint-unit`.
- `CONTRIBUTING.md` / `CHANGELOG.md` — document the tagged suite and its Docker
  requirement; added `testcontainers-go` to `go.mod`.

## Bootstrap spike result (locked sequence for NocoDB 2026.06.1)

1. `POST /api/v1/auth/user/signup` `{email,password}` → JWT (first user = super
   admin).
2. `POST /api/v1/tokens` (`xc-auth: JWT`) `{description}` → API token.
3. `GET /api/v3/meta/workspaces` (`xc-token`) → default workspace id.
4. `POST /api/v3/meta/workspaces/{wsId}/bases` (`xc-token`) `{title}` → base id.

The `xc-token` works on all v3 endpoints the tool uses.

## Notable finding (for issue #1 / #2)

Running the **real binary** end to end against NocoDB 2026.06.1 (SQLite-backed)
**worked cleanly** — `up` created the table + row, `down` dropped it, and the
`Migrations` table was created without error. The `ER_PARSE_ERROR` from issue #1
is a MySQL error and did **not** reproduce here, so that bug is specific to a
MySQL-backed / older NocoDB environment, not the current v3 path on the default
store. Recorded as input for the issue-#1/#2 follow-up.

## Verification

- `go build ./...` / `go test ./...` (default) — clean; no testcontainers in the
  unit build.
- `golangci-lint run ./...` and `--build-tags=integration` — 0 issues; `gofmt`
  clean.
- `go test -tags=integration ./...` — `TestUpDownAgainstRealNocoDB` passes
  (~10–16s, fresh container each run).

## Out of scope / follow-ups

- The `where` query shape in `GetRecords`/`DeleteRecords` was not exercised by
  this migration (no conditional delete); worth a dedicated case in a future
  iteration and a likely issue-#2 audit point.
