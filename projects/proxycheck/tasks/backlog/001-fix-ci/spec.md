# Spec — 001-fix-ci

## Problem

Both GitHub Actions workflows in `vcs/proxycheck/.github/workflows/` fail on
every run, so CI gives no real signal on a push or pull request:

- **`go.yml`** pins the Go matrix to `1.17` and `1.18`. The current macOS
  runners can no longer fetch those toolchains
  (`Failed to download version 1.17: Error: Unexpected HTTP response: 403`), and
  because the matrix uses fail-fast the macOS failure cancels the otherwise-green
  Ubuntu and Windows jobs. The workflow also uses deprecated
  `actions/checkout@v2` / `actions/setup-go@v2` (forced onto Node 24) and uploads
  coverage with the retired `bash <(curl -s https://codecov.io/bash)` uploader.
- **`golangci-lint.yml`** references `go-version: ${{ matrix.go }}` while the
  matrix defines `go_version`, so `setup-go` receives an empty version and the
  `Run actions/setup-go@v3` step fails before any linting happens. It also pins
  golangci-lint `v1.42.1`, runs the lint across a full 3-OS × 2-Go matrix, and
  triggers on a `master` branch that does not exist.

## Goal

Both `go` and `golangci-lint` checks run and pass on every push and pull request
to `main`, on current actions and a maintained Go matrix.

## User journeys

- A maintainer opens a pull request against `main`; the `go` and
  `golangci-lint` checks run and report green, giving a trustworthy merge signal.
- A maintainer pushes to `main`; tests run with `-race`, coverage is uploaded to
  Codecov, and the lint passes — no spurious red from toolchain-download or
  config errors.

## Success criteria

- A push to `main` and a pull request each produce passing `go` and
  `golangci-lint` checks.
- The `go` matrix runs the **two latest stable** Go versions on **Ubuntu only**;
  no `Failed to download version … 403` errors appear.
- Tests still run with `-race` and produce a coverage profile; coverage is
  uploaded via `actions/codecov-action` (not the retired bash uploader).
- The service-backed tests still get `PROXY_URL`/`TARGET_URL` from the proxy.py
  and nginx service containers on Ubuntu, and the unreachable-proxy test still
  runs.
- `golangci-lint` installs Go correctly (no empty `go-version`), runs once on
  Ubuntu with a current golangci-lint, and passes.
- No workflow references the non-existent `master` branch; all actions are on
  non-deprecated major versions.

## Affected spec sections

This task changes **CI/dev infrastructure only** (GitHub Actions workflows under
`vcs/proxycheck/.github/`); it does not change any product behaviour.

- None — the living product spec (`spec/overview.md`, `spec/cli.md`,
  `spec/checking.md`) describes what the product does, and that is unchanged.
  Nothing folds into `spec/` at Finish.

## Target state

No change to `projects/proxycheck/spec/`. The end state lives entirely in
`vcs/proxycheck/.github/workflows/`: `go.yml` and `golangci-lint.yml` rewritten
to satisfy the success criteria above. The exact action versions, Go versions,
and Codecov token handling are decided in `plan.md`.

## Out of scope

- Changing product code, the package API, or the CLI.
- Adding new test suites, new linters' rule sets, or new coverage targets.
- Restoring Windows/macOS build coverage (dropped deliberately; revisit later if
  cross-platform regressions appear).
- Adding release/publish automation (covered by `sys.project.release`, not CI).

## Boundaries

- ✅ Always: keep tests running with `-race`; keep the service-backed tests
  working on Ubuntu; use current, non-deprecated action versions.
- ⚠️ Ask first: relying on a `CODECOV_TOKEN` secret being configured; dropping
  Codecov entirely; changing which Go versions are the supported minimum
  (`go.mod` currently declares `go 1.18`).
- 🚫 Never: change product behaviour, the package API, or the CLI to make CI
  pass; commit secrets into the workflow files.
- Inherits the global Go and Git rules ([go.md](../../../../rules/go.md),
  [git.md](../../../../rules/git.md)).
