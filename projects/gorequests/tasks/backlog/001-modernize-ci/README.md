# 001 — Modernize CI across the gorequests repos

## Goal

Bring the GitHub Actions CI of all three repositories (`gorequests`,
`gorequests-proxy`, `gorequests-retry`) up to the current `memclutter` baseline,
matching `proxycheck`.

## Scope

- Update the `go.yml` workflow: current `actions/checkout` and `actions/setup-go`,
  a current Go version matrix, and the official `codecov/codecov-action` instead
  of the piped `bash <(curl …)` uploader.
- Add a `golangci-lint.yml` workflow to each repo.
- Bump each module's minimum Go version (`go.mod`) to the new baseline and fix
  any lint findings the new pipeline surfaces.

## Acceptance criteria

- All three repos run an updated `go.yml` and a new `golangci-lint.yml`, both
  green on `main`.
- Coverage is uploaded via `codecov/codecov-action`.
- Each `go.mod` declares the agreed current minimum Go version; `go test ./...`
  passes on the CI matrix.
- The README "Go version" and CI badges remain accurate; a golangci-lint badge
  can now be added.
