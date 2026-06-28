# Plan — 001-fix-ci

## Approach

Rewrite both workflow files in `vcs/proxycheck/.github/workflows/` rather than
patch them in place — each has multiple independent problems (dead toolchains,
deprecated actions, a config typo, a wasteful matrix), and a clean rewrite is
easier to review than a chain of edits.

Two principles drive the rewrite:

1. **Let `setup-go` resolve versions.** Instead of hardcoding Go numbers that go
   stale (the root cause of the 403s), use the built-in aliases `oldstable` and
   `stable`. The matrix becomes `go: [oldstable, stable]`, which is exactly "the
   two latest stable Go versions" and never needs touching again.
2. **Ubuntu-only.** The service containers (`proxy.py`, `nginx`) already only run
   on Ubuntu, and the owner chose to drop Windows/macOS. Removing the OS matrix
   removes the fail-fast cross-cancellation and the macOS download failures at
   once.

## Stack

Base Go stack ([go.md](../../../../rules/go.md)). No application dependencies
change. Only GitHub Actions YAML changes; action versions bumped to current
majors:

- `actions/checkout@v4`
- `actions/setup-go@v5`
- `actions/codecov-action@v4`
- `golangci/golangci-lint-action@v6`

## Architecture

### `go.yml`

```yaml
name: go

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        go: [ oldstable, stable ]
    services:
      proxy:
        image: abhinavsingh/proxy.py:v2.4.4
        ports: [ "8899:8899" ]
      target:
        image: nginx:1.23.2
        ports: [ "80:80" ]
    env:
      PROXY_URL: 'http://localhost:8899'
      TARGET_URL: 'http://target:80'
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v5
        with:
          go-version: ${{ matrix.go }}
      - name: Test
        run: go test ./... -race -coverprofile=coverage.txt -covermode=atomic
      - name: Upload coverage
        if: ${{ matrix.go == 'stable' }}
        uses: codecov/codecov-action@v4
        with:
          token: ${{ secrets.CODECOV_TOKEN }}
          files: ./coverage.txt
          fail_ci_if_error: false
```

Notes:
- `services`/`env` move out of the `include` block and become unconditional —
  they are always valid now that only Ubuntu runs. This drops the brittle
  per-OS `include` matrix the old file used to null them out.
- `TARGET_URL` keeps using the `target` service hostname (`http://target:80`),
  matching the old working Ubuntu job; `PROXY_URL` stays `localhost:8899`.
- Coverage uploads once, only on the `stable` leg, to avoid double counting.

### `golangci-lint.yml`

```yaml
name: golangci-lint

on:
  push:
    branches: [ main ]
    tags: [ 'v*' ]
  pull_request:
    branches: [ main ]

permissions:
  contents: read

jobs:
  golangci:
    name: lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v5
        with:
          go-version: stable
      - uses: golangci/golangci-lint-action@v6
        with:
          version: latest
```

Notes:
- The core bug fix: `go-version` now reads a real value (`stable`) instead of the
  empty `${{ matrix.go }}`.
- Lint runs once on Ubuntu — no OS/Go matrix. Linting is platform-independent.
- `version: latest` replaces the pinned `v1.42.1`; per [go.md](../../../../rules/go.md)
  CI tracks the current linter. The repo has no `.golangci.yml`, so default
  rules apply and the newer linter needs no config migration.
- The non-existent `master` branch trigger is dropped; `tags: v*` is kept so
  release tags still get linted.

## Trade-offs & alternatives

- **`oldstable`/`stable` aliases vs pinned numbers.** Pinning (e.g. `1.25`,
  `1.26`) is reproducible but reintroduces the exact staleness that broke CI.
  Aliases are the right call for a small library that wants to track current Go;
  a regression on a future Go version is a signal we *want* to see.
- **Dropping Windows/macOS.** Loses cross-platform build coverage. Acceptable:
  the product is a networking CLI/library with no OS-specific code paths, and the
  service-backed tests never ran off Ubuntu anyway. Revisit if a platform bug
  appears (noted in spec Out of scope).
- **`golangci-lint version: latest` vs pinned.** `latest` can introduce new
  findings unexpectedly on a fresh run. Mitigated by there being no custom rule
  set; if it proves noisy, pin to a known-good version in a follow-up.
- **Keeping Codecov vs dropping it.** Owner chose to keep it and will add the
  `CODECOV_TOKEN` secret. `fail_ci_if_error: false` ensures an upload hiccup
  never reds the build — coverage reporting is informational, not a gate.

## Constraints & risks

- **`CODECOV_TOKEN` secret.** The owner adds it in repo Settings → Secrets. Until
  then uploads are skipped/soft-failed (never block CI thanks to
  `fail_ci_if_error: false`).
- **`go.mod` declares `go 1.18`.** `oldstable` will be far newer than 1.18; that
  is fine — the module's declared minimum is a floor, not a CI target. Not
  changing `go.mod` in this task (would be a separate, deliberate decision per
  spec Boundaries).
- **New linter may surface findings** the old `v1.42.1` missed. If lint fails on
  real issues, fix them minimally without changing behaviour; if a finding is a
  false positive for this codebase, address it in the breakdown.
- **Service container image tags** (`proxy.py:v2.4.4`, `nginx:1.23.2`) are
  retained as-is since the Ubuntu job was already passing with them.

## Testing strategy

Prove the spec's success criteria by observing CI itself:

1. Push the branch / open a PR and confirm both `go` and `golangci-lint` checks
   go green.
2. Inspect the `go` run logs: both `oldstable` and `stable` legs run, tests run
   with `-race`, `request_test.go` tests actually execute (not "Skipped because
   PROXY_URL not set"), proving the service env reached them.
3. Confirm the coverage step uploads on the `stable` leg (or soft-fails cleanly
   if the token is not yet set) and never reds the build.
4. Confirm no `Failed to download version … 403` and no deprecated-action
   failures appear in either workflow.

Local sanity before pushing: `go test ./... -race` (service-backed tests will
self-skip locally without `PROXY_URL`/`TARGET_URL`, which is expected) and
`golangci-lint run` if available.
