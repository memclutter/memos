---
id: 001-fix-ci
status: active
created: 2026-06-28
updated: 2026-06-28
---

Fix the two failing GitHub Actions workflows in `vcs/proxycheck/.github/workflows/`
(`go.yml`, `golangci-lint.yml`) so CI is green on push and PR to `main`.

Goal: green `go` and `golangci-lint` checks with up-to-date actions and a sane
matrix.

Scope:
- `go.yml`: drop Go 1.17/1.18, run the two latest stable Go versions; run on
  Ubuntu only; refresh `actions/checkout` and `actions/setup-go`; keep
  `-race` + coverage; upload coverage via `actions/codecov-action`.
- `golangci-lint.yml`: fix the `matrix.go` vs `matrix.go_version` mismatch that
  leaves Go uninstalled; run lint once on Ubuntu with a current Go; bump
  `golangci-lint-action` and the linter version; drop the non-existent `master`
  branch trigger.

Acceptance:
- Both workflows pass on a push to `main` and on a pull request.
- No deprecated-action warnings cause failures; no `Failed to download version
  … 403` errors.
- Tests keep running with `-race`; coverage is uploaded via codecov-action.

Constraints:
- This is CI/dev infrastructure only — do not change product behaviour, the
  package API, or the CLI. Do not touch product code; touch test files only if a
  test fails to run under the new Go versions.
- ⚠️ Codecov upload via `codecov-action` needs a `CODECOV_TOKEN` secret — the
  owner adds it; `fail_ci_if_error: false` keeps the upload from reding CI.

## Tasks breakdown

All work happens inside `vcs/proxycheck/` on a short-lived branch; the OS repo
pins the new submodule commit at Finish.

- [x] 1. Verify the pinned versions are real, current, mutually compatible
  releases: Go `1.25` and `1.26`, golangci-lint `v2.12.2`. If any has moved, pin
  the nearest current release and note it in the log. (Plan: Constraints & risks)
- [x] 2. Rewrite `.github/workflows/go.yml`: Ubuntu-only, `fail-fast: false`,
  matrix `go: [ '1.25', '1.26' ]`, `checkout@v4` + `setup-go@v5`; keep the
  `proxy`/`target` service containers and `PROXY_URL`/`TARGET_URL` env; keep
  `go test ./... -race -coverprofile=coverage.txt -covermode=atomic`.
  (Success criteria: green `go`, two pinned Go legs, `-race`, no 403s)
- [x] 3. Add the coverage upload step to `go.yml`: `codecov/codecov-action@v4`,
  `if: matrix.go == '1.26'`, `token: ${{ secrets.CODECOV_TOKEN }}`,
  `files: ./coverage.txt`, `fail_ci_if_error: false`. (Success criteria: coverage
  uploaded via codecov-action, never reds the build)
- [x] 4. Rewrite `.github/workflows/golangci-lint.yml`: single Ubuntu job,
  `checkout@v4` + `setup-go@v5` with `go-version: '1.26'` (fixes the empty
  `matrix.go` bug), `golangci-lint-action@v6` with `version: v2.12.2`; triggers
  `push` on `main` + `tags: v*` and `pull_request` on `main` (drop `master`).
  (Success criteria: green lint, Go installed, no `master` ref)
- [x] 5. Local sanity: run `go test ./... -race` (service-backed tests self-skip
  without `PROXY_URL`/`TARGET_URL` — expected) and `golangci-lint run` if
  available; fix any real lint findings minimally without changing behaviour.
  (Plan: Testing strategy)
- [ ] 6. Confirm the owner has added the `CODECOV_TOKEN` secret before relying on
  upload. ⚠️ ask owner. (Plan: Constraints & risks)
- [x] 7. Commit on a branch in `vcs/proxycheck/`, push, open a PR, and confirm
  both `go` and `golangci-lint` checks go green — inspect logs that both Go legs
  run, the service-backed tests execute (not skipped), and no 403/deprecation
  failures appear. (Success criteria: green on push and PR)
- [ ] 8. Merge, then bump the submodule pin in the OS repo
  (`chore(submodule): bump proxycheck`). Hand off to `sys.task.finish`.
