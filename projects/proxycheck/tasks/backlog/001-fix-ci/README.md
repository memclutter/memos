# 001 — Fix CI test runs in GitHub Actions

## Goal

Make both GitHub Actions workflows (`go`, `golangci-lint`) green again on every
push and pull request to `main`.

## Why

Both workflows currently fail on every run, so CI gives no signal:

- **`go`** — the matrix pins Go `1.17`/`1.18`, which the macOS runners can no
  longer download (`Failed to download version 1.17: 403`), and the whole matrix
  is cancelled when macOS fails. It also uses deprecated `actions/checkout@v2`
  and `actions/setup-go@v2`, and uploads coverage via the retired
  `bash <(curl -s https://codecov.io/bash)` script.
- **`golangci-lint`** — `actions/setup-go` reads `go-version: ${{ matrix.go }}`
  but the matrix key is `go_version`, so Go is never installed and setup-go
  fails immediately. It also pins golangci-lint `v1.42.1` and runs the lint over
  a full 3-OS × 2-Go matrix.

## Scope

- Rewrite `.github/workflows/go.yml` and `.github/workflows/golangci-lint.yml`.
- Go matrix: the two latest stable Go versions.
- OS: Ubuntu only (the proxy/nginx service containers already only run there).
- Coverage upload via `actions/codecov-action`.
- No changes to product code or to the Go test files beyond what's needed to
  keep them passing.

## Acceptance criteria

- A push to `main` and a pull request both produce green `go` and
  `golangci-lint` checks.
- Tests still run with `-race` and produce a coverage profile; coverage is
  uploaded to Codecov via `codecov-action`.
- The service-backed tests (`PROXY_URL`/`TARGET_URL`) still run on Ubuntu; the
  unreachable-proxy test still runs everywhere.
- No deprecated action versions and no failed-download errors in the run logs.
