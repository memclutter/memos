# Iteration 001 — rewrite workflows

## Summary

Rewrote both GitHub Actions workflows and fixed the lint findings they surfaced.
Opened [PR #1](https://github.com/memclutter/proxycheck/pull/1) on branch
`fix/ci-workflows`; all three checks (`lint`, `test (1.25)`, `test (1.26)`) are
green.

## What was done

- `go.yml`: Ubuntu-only, `fail-fast: false`, matrix `go: [ '1.25', '1.26' ]`,
  `checkout@v4` + `setup-go@v5`, service containers + `PROXY_URL`/`TARGET_URL`
  retained, `-race` + coverage profile. Coverage uploaded via
  `codecov-action@v4` on the `1.26` leg with `fail_ci_if_error: false`.
- `golangci-lint.yml`: single Ubuntu job, real `go-version: '1.26'` (fixed the
  empty `matrix.go` bug), `golangci-lint-action@v7` + golangci-lint `v2.12.2`,
  dropped the `master` trigger.
- Lint fixes (behaviour-preserving, no public API change): checked the deferred
  `Body.Close()` error; `//nolint:staticcheck` on the exported `FeedEnd`
  sentinel to keep its name; replaced deprecated `io/ioutil` with `io`.
- `go.mod`: bumped the `go` directive `1.18` → `1.25` (owner-approved, ⚠️ gate).

## Deviations from plan.md (discovered during CI)

1. **golangci-lint-action v6 → v7.** golangci-lint v2 is rejected by action v6
   (`v2 is not supported by golangci-lint-action v6, you must update to v7`).
   The plan said v6; corrected to v7.
2. **golangci-lint version v2.5.0 → v2.12.2.** v2.5.0 (planned) was stale; the
   current release at execution time is v2.12.2.
3. **go.mod `go 1.18` → `go 1.25`.** Not foreseen in the plan. govet failed
   under Go 1.26 stdlib (`cannot inline ioutil.ReadAll … into a file using
   go1.18`). Owner chose to bump the directive to 1.25 (lower CI leg). This is a
   real change to the library's minimum supported Go — noted for Finish/spec.

## Verification

- Local: `go build ./...`, `go test ./... -race` (pass), `golangci-lint run`
  (0 issues).
- CI: `lint` pass; `test (1.25)` and `test (1.26)` pass with 45.5% coverage.
  nginx/proxy.py service logs show real proxied requests
  (`GET target:80/not_found_page/ - 404`), proving the service-backed tests ran
  rather than self-skipping.
- No `Failed to download version … 403` and no deprecated-action failures.

## Open / pending

- **Step 6 — `CODECOV_TOKEN`.** Not yet configured: the codecov step logs
  `Token required because branch is protected` and soft-fails (does not red CI,
  as designed). Owner to add the secret in repo Settings → Secrets.
- **Step 8 — merge + submodule bump.** After the owner merges PR #1, bump the
  submodule pin in the OS repo and run `sys.task.finish`.
