---
name: gorequests
vcs:
  - git@github.com:memclutter/gorequests.git
  - git@github.com:memclutter/gorequests-proxy.git
  - git@github.com:memclutter/gorequests-retry.git
self: false
status: active
stack: [go]
created: 2026-06-29
---

A small Go HTTP client family: one fluent wrapper around `net/http`
(`gorequests`) plus pluggable middleware shipped as separate modules
(`gorequests-proxy`, `gorequests-retry`). The goal is to collapse the
boilerplate of building a request, checking status codes, and decoding the body
into a single readable chain, while keeping cross-cutting concerns (proxying,
retries) as opt-in middleware. Follows the base stack
([rules/go.md](../../rules/go.md)): Go modules, wrapped errors, table-driven
tests. Licensed LGPL-2.1.

## Architecture

The project is three independent Go modules under `vcs/`, linked only by the
middleware contract — each middleware module imports nothing from the core; the
core imports nothing from the middlewares. They compose at the call site through
`Use()`.

- **`vcs/gorequests`** — the core wrapper, module
  `github.com/memclutter/gorequests`. `requests.go` holds the unexported
  `requestsInstance` builder and the `Exec()` engine; `requests_typing.go`
  declares the public `RequestsInstance` interface and the two middleware
  interfaces; `requests_mock.go` provides testify mocks for both. Verb helpers
  (`Get`, `Post`, …) construct a builder via `Requests()`.
- **`vcs/gorequests-proxy`** — module
  `github.com/memclutter/gorequests-proxy`, package `gorequests_proxy`. A single
  `Proxy` type implementing `ClientOverride`: picks a random proxy from a list
  and rewires the client transport (HTTP(S) via `http.ProxyURL`, SOCKS via
  `h12.io/socks`). Knows how to patch both a plain `*http.Transport` and a
  `retryablehttp.RoundTripper`, so it composes with the retry middleware.
- **`vcs/gorequests-retry`** — module
  `github.com/memclutter/gorequests-retry`, package `gorequests_retry`. A single
  `Retry` type implementing `ClientOverride` by wrapping the client in
  `hashicorp/go-retryablehttp`.

## Conventions

- The two extension points are the interfaces `ClientOverrideMiddleware`
  (`ClientOverride(*http.Client) (*http.Client, error)`) and
  `RequestOverrideMiddleware` (`RequestOverride(*http.Request) (*http.Request,
  error)`). `Use(...interface{})` type-asserts each argument against both, so one
  value can implement either or both. Client overrides run before the request is
  built; request overrides run after, just before `Do`.
- Minimum Go is **1.18** for the core and proxy modules, **1.17** for retry
  (`go.mod`); CI runs `1.18`/`1.19` (retry also `1.17`) on Ubuntu, Windows, and
  macOS.
- The core depends on `github.com/memclutter/gocore` for slice helpers
  (`coreslices`). Code is from 2023 and predates this OS's current Go baseline —
  modernising it (Go version bump, dropping `ioutil`, golangci-lint v2) is task
  work, not assumed truth.
- Source changes are committed and pushed inside the relevant
  `vcs/<repo-name>/`, then this OS pins the new submodule commit
  (`chore(submodule): bump <repo-name>`).
- Heads-up: the core `README.md` shows an aspirational API (`Request()`, a
  `ResponseJson(&v, ".ip")` selector) that the shipped code does **not**
  implement. The living spec describes the real, shipped API.
