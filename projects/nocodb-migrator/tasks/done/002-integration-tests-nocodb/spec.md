# Spec — 002-integration-tests-nocodb

## Problem

Task 001 gives the tool a unit safety net, but unit tests drive an in-process
mock NocoDB: they assert the contract *we believe* is correct. That is exactly
the blind spot behind issues #1 and #2 — the implementation drifted from the live
Meta API v3, and a mock encoding the same wrong assumption would pass. Nothing
runs the real `up`/`down`/`info` flow against an actual NocoDB, so real-world
breakage (e.g. the `Migrations`-table SQL parse error) goes uncaught.

## Goal

Add an opt-in integration suite that brings up a real NocoDB in Docker and runs
the tool end to end against it, asserting schema and data, plus a separate CI job
that runs it. This is the cross-check that validates the v3 contract for real.

## User journeys

- A contributor runs `go test -tags=integration ./...`; the suite spins up NocoDB
  in Docker, applies a migration with `up`, asserts the resulting tables/fields/
  records, runs `down`, and asserts the base returns to its prior state.
- A contributor on a machine without Docker runs the tagged suite and it skips
  cleanly with a clear message instead of failing.
- A contributor opens a PR; a separate `integration` CI job verifies the
  end-to-end flow before merge, while the fast `lint-unit` job (task 001) keeps
  giving a quick signal.

## Success criteria

- `go test -tags=integration ./...` applies and rolls back a migration against a
  dockerized NocoDB and asserts the schema/data outcome; default `go test ./...`
  still skips it and needs no Docker.
- A tagged run without Docker skips with a clear message rather than failing.
- A separate `integration` GitHub Actions job runs the suite and is green on PRs.
- No real `NOCODB_API_TOKEN`, base id, or URL is committed; configuration comes
  only from the ephemeral container.

## Affected spec sections

- spec/quality.md — extend the capability (created by task 001) with the
  integration-test layer: the build-tag gate, the testcontainers-go + NocoDB
  setup, the end-to-end `up`/`down` assertion, and the separate CI job.

## Target state

### spec/quality.md (after, integration paragraph added)

The quality capability gains an **Integration tests** section:

> - **Integration tests** — gated behind a build tag (`//go:build integration`)
>   and a Docker-availability check, started against a NocoDB brought up in Docker
>   via testcontainers-go. They apply a migration with `up`, inspect the resulting
>   tables/fields/records, then `down`, asserting the base returns to its prior
>   state. Skipped when Docker or the tag is absent, so the default unit run needs
>   no Docker.

The **CI** section gains a second job:

> A separate `integration` job runs `go test -tags=integration ./...` with Docker
> available; it is kept off the fast lint+unit critical path.

## Out of scope

- The unit suite, base CI workflow, `.golangci.yml`, and pre-commit config — those
  ship in task 001.
- Fixing any drift the integration suite uncovers (issues #1/#2) — those are
  separate tasks; this task builds the test that finds them.

## Boundaries

- ✅ Always — gate integration tests behind the build tag and a Docker check so
  the default `go test ./...` and the pre-commit hook stay Docker-free; use an
  ephemeral container, never a shared/real base.
- ⚠️ Ask first — an integration mechanism beyond Docker + testcontainers-go; a CI
  provider other than GitHub Actions.
- 🚫 Never — commit a real `NOCODB_API_TOKEN`, base id, or instance URL; encode
  endpoints outside Meta API v3; paper over a real-NocoDB failure by weakening the
  assertion instead of filing it as an issue-#1/#2 finding.
