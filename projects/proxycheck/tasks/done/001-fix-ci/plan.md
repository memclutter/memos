# Plan — 001-fix-ci

## Approach

Rewrite both workflow files in `vcs/proxycheck/.github/workflows/` rather than
patch them in place — each has multiple independent problems (dead toolchains,
deprecated actions, a config typo, a wasteful matrix), and a clean rewrite is
easier to review than a chain of edits.

Two principles drive the rewrite:

1. **Pin Go versions explicitly.** The matrix runs the two latest stable Go
   releases, pinned by number: `go: [ '1.25', '1.26' ]`. Pinning keeps CI
   reproducible — a given commit always tests against the same toolchains, so a
   red build means our code changed, not the runner's default Go. (The 403s were
   caused not by pinning per se but by pinning *unmaintained* versions (1.17/1.18)
   that the runners can no longer fetch; pinning current versions avoids that.)
   Bumping these numbers becomes a deliberate, reviewable change on a new Go
   release.
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
        go: [ '1.25', '1.26' ]
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
        if: ${{ matrix.go == '1.26' }}
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
- Coverage uploads once, only on the `1.26` leg, to avoid double counting.

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
          go-version: '1.26'
      - uses: golangci/golangci-lint-action@v6
        with:
          version: v2.12.2
```

Notes:
- The core bug fix: `go-version` now reads a real value (`'1.26'`, the latest
  pinned Go) instead of the empty `${{ matrix.go }}`.
- Lint runs once on Ubuntu — no OS/Go matrix. Linting is platform-independent.
- `version: v2.12.2` replaces the pinned `v1.42.1` — a *pinned* current linter,
  not `latest`. Same reproducibility argument as the Go versions: a fixed linter
  means a red lint reflects our code, not a new rule shipped upstream. The repo
  has no `.golangci.yml`, so golangci-lint v2 default rules apply and need no
  config migration. (Implementer: confirm `v2.12.2` is a real release compatible
  with Go 1.26 at execution time; if not, pin the nearest current v2 patch.)
- The non-existent `master` branch trigger is dropped; `tags: v*` is kept so
  release tags still get linted.

## Trade-offs & alternatives

- **Pinned numbers vs `oldstable`/`stable` aliases.** Aliases would track Go
  automatically and never need touching, but they make test outcomes depend on
  whenever the runner's default Go moves — a green→red flip with no code change.
  The owner chose pinning for reproducibility: a commit always tests the same
  toolchains. Cost: Go bumps are now a manual, deliberate edit (the right place
  for that decision). The staleness that broke CI came from pinning *unmaintained*
  versions, which pinning *current* ones (1.25/1.26) avoids.
- **Dropping Windows/macOS.** Loses cross-platform build coverage. Acceptable:
  the product is a networking CLI/library with no OS-specific code paths, and the
  service-backed tests never ran off Ubuntu anyway. Revisit if a platform bug
  appears (noted in spec Out of scope).
- **Pinned `golangci-lint` vs `latest`.** Same call as the Go versions: `latest`
  can introduce new findings on an unrelated run, so the linter is pinned
  (`v2.12.2`). Bumping it is a deliberate follow-up when we choose to.
- **Keeping Codecov vs dropping it.** Owner chose to keep it and will add the
  `CODECOV_TOKEN` secret. `fail_ci_if_error: false` ensures an upload hiccup
  never reds the build — coverage reporting is informational, not a gate.

## Constraints & risks

- **`CODECOV_TOKEN` secret.** The owner adds it in repo Settings → Secrets. Until
  then uploads are skipped/soft-failed (never block CI thanks to
  `fail_ci_if_error: false`).
- **`go.mod` declares `go 1.18`.** The pinned `1.25`/`1.26` are far newer; that
  is fine — the module's declared minimum is a floor, not a CI target. Not
  changing `go.mod` in this task (would be a separate, deliberate decision per
  spec Boundaries).
- **Pinned versions must be real, current releases.** Verify at execution time
  that Go `1.25` and `1.26` and golangci-lint `v2.12.2` exist and are mutually
  compatible; adjust the exact pins to the nearest current release if any has
  moved. This is the deliberate-bump cost of pinning.
- **New linter may surface findings** the old `v1.42.1` missed. If lint fails on
  real issues, fix them minimally without changing behaviour; if a finding is a
  false positive for this codebase, address it in the breakdown.
- **Service container image tags** (`proxy.py:v2.4.4`, `nginx:1.23.2`) are
  retained as-is since the Ubuntu job was already passing with them.

## Testing strategy

Prove the spec's success criteria by observing CI itself:

1. Push the branch / open a PR and confirm both `go` and `golangci-lint` checks
   go green.
2. Inspect the `go` run logs: both the `1.25` and `1.26` legs run, tests run
   with `-race`, `request_test.go` tests actually execute (not "Skipped because
   PROXY_URL not set"), proving the service env reached them.
3. Confirm the coverage step uploads on the `1.26` leg (or soft-fails cleanly
   if the token is not yet set) and never reds the build.
4. Confirm no `Failed to download version … 403` and no deprecated-action
   failures appear in either workflow.

Local sanity before pushing: `go test ./... -race` (service-backed tests will
self-skip locally without `PROXY_URL`/`TARGET_URL`, which is expected) and
`golangci-lint run` if available.
