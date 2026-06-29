# gorequests — Product spec

## Vision

`gorequests` is a family of small Go libraries for making HTTP requests with
less ceremony. The core wrapper turns the standard `net/http`
build-do-check-decode dance into a single fluent chain; two companion middleware
modules add proxying and retries without bloating the core. It is for Go
developers who want `requests`-style ergonomics while staying on the standard
library and importing only what they use.

The three modules are independent — they share no code, only a tiny middleware
interface contract — so a consumer can take the core alone, or add either
middleware, and compose them at the call site with `Use()`.

## Capabilities

- [http-client.md](http-client.md) — the fluent request builder and execution
  engine in the core `gorequests` module: verbs, headers, cookies, bodies,
  status-code assertions, and response decoding.
- [middleware.md](middleware.md) — the extension contract: the two override
  interfaces and how `Use()` wires middleware into the request lifecycle.
- [proxy-middleware.md](proxy-middleware.md) — `gorequests-proxy`: route a
  request through a random HTTP(S) or SOCKS proxy from a list.
- [retry-middleware.md](retry-middleware.md) — `gorequests-retry`: retry on
  network errors and configured status codes via `go-retryablehttp`.

## Product-wide success criteria

- A GET-and-decode-JSON flow is expressible as one uninterrupted chain ending in
  `Exec()`.
- The core module has zero dependency on the middleware modules; each middleware
  module depends on the core only through the published interfaces.
- Adding proxy and/or retry behaviour requires only additional `Use()` calls —
  no change to the rest of the chain.
- Proxy and retry compose: a request can be both proxied and retried in the same
  chain.
- Each module builds and tests with `go test ./...` on its declared minimum Go
  version.

## Boundaries

Global rules apply ([git.md](../../../rules/git.md), [go.md](../../../rules/go.md));
only the project deltas are recorded here.

- ✅ Always — keep the core free of middleware imports; extend behaviour through
  the `ClientOverride` / `RequestOverride` interfaces, not by editing `Exec()`.
- ✅ Always — make source changes inside `vcs/<repo-name>/`, then pin the bump in
  this OS.
- ⚠️ Ask first — adding a new dependency to a module, or changing a module's
  minimum Go version / module path.
- ⚠️ Ask first — changing the public `RequestsInstance` interface or the
  middleware interfaces (these are the cross-module contract).
- 🚫 Never — introduce a dependency from the core module onto a middleware
  module.
- 🚫 Never — silently "fix" the libraries to match the aspirational README
  examples; reconcile docs and code as deliberate task work.
