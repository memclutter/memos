---
id: 001-fix-ci
status: backlog
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
- ⚠️ Codecov upload via `codecov-action` may need a `CODECOV_TOKEN` secret —
  confirm with the owner before assuming it is configured.
