# Spec — 001-modernize-ci

## Problem

The three repos were imported with 2023-era CI: `actions/checkout@v2`,
`actions/setup-go@v2`, a stale Go matrix (`1.17`/`1.18`/`1.19` across a
Linux/Windows/macOS spread), and coverage uploaded with the deprecated
`bash <(curl -s https://codecov.io/bash)` script. There is no lint workflow at
all, even though the base stack ([rules/go.md](../../../../rules/go.md)) mandates
`golangci-lint` in CI. The pinned Go versions are years out of support, so the
spec's per-module success criteria ("builds on Go 1.18", "Go 1.17") describe an
obsolete baseline. `proxycheck` already modernized to current Go and current
actions; the gorequests family is the odd one out.

## Goal

Bring CI in all three repos up to the current `memclutter` baseline (matching
`proxycheck`): current actions, a current Go version matrix, the official Codecov
action, and a dedicated `golangci-lint` workflow — all green on `main`.

## User journeys

- A contributor opens a PR against any of the three repos: a `go.yml` workflow
  builds and tests on the current Go matrix, and a `golangci-lint.yml` workflow
  lints. Both must pass before merge.
- A maintainer reads a repo's README: the Go-version, CI, and a new
  golangci-lint badge reflect the real, current pipeline.

## Success criteria

- Each repo runs an updated `go.yml` using current `actions/checkout` and
  `actions/setup-go`, a current Go version matrix, and `codecov/codecov-action`
  for coverage upload (no piped `curl` uploader).
- Each repo runs a new `golangci-lint.yml` that is green.
- Each module's `go.mod` declares the agreed current minimum Go version, and
  `go test ./...` passes across the CI matrix.
- The libraries' runtime behaviour is unchanged (CI/tooling/version-bump only).

## Affected spec sections

- spec/http-client.md — update the success criterion that pins "Go 1.18" to the
  new baseline.
- spec/proxy-middleware.md — update the success criterion that pins "Go 1.18".
- spec/retry-middleware.md — update the success criterion that pins "Go 1.17".
- spec/overview.md — the "builds and tests on its declared minimum Go version"
  criterion stays; no version is hard-coded there.

## Target state

After this task, the per-module success criteria in `spec/http-client.md`,
`spec/proxy-middleware.md`, and `spec/retry-middleware.md` no longer pin an
out-of-support Go version. Each reads that `go test ./...` passes on the module's
current minimum Go version and across the CI matrix, and that CI runs both the
build/test workflow and a `golangci-lint` workflow. The exact version numbers are
fixed in `plan.md` and written into the spec at Finish.

## Out of scope

- Any change to library behaviour or public API.
- Dependency upgrades beyond what a Go-version bump or lint compliance forces.
- The `body[:50]` panic fix — that is task 002.

## Boundaries

- ✅ Always: keep all three repos on the same CI shape; use `proxycheck` as the
  template. Make changes inside `vcs/<repo-name>/`, then pin the bumps in the OS.
- ⚠️ Ask first: dropping or adding an OS to the test matrix; raising the minimum
  Go version beyond what `proxycheck` uses.
- 🚫 Never: change library behaviour or the public API in this task.
- Global rules apply ([go.md](../../../../rules/go.md),
  [git.md](../../../../rules/git.md)); only the task delta is recorded here.
