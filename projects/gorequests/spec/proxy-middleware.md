# proxy-middleware

## Purpose

`gorequests-proxy` routes a request through a proxy without the caller touching
transports. It is a `ClientOverride` middleware (package `gorequests_proxy`,
module `github.com/memclutter/gorequests-proxy`) attached via `Use()`.

## Behaviour

The middleware is the `Proxy` struct:

```go
type Proxy struct {
	Proxies    []string
	AllowEmpty bool
}
```

On `ClientOverride`:

1. Each entry in `Proxies` is trimmed of whitespace and empty entries are
   dropped.
2. If no proxies remain: return the client unchanged when `AllowEmpty` is true,
   otherwise return an error (`nil proxies`).
3. One proxy URL is chosen at random from the remaining list and parsed; a parse
   failure is an error.
4. If the URL scheme contains `socks`, the transport dials through
   `h12.io/socks`; otherwise the transport's `Proxy` is set to
   `http.ProxyURL(proxyUrl)` (HTTP/HTTPS proxies).
5. The override is applied to the existing transport:
   - a plain `*http.Transport` is patched in place;
   - a `retryablehttp.RoundTripper` (left by the retry middleware) has its inner
     `*http.Transport` patched, so proxy composes with retry;
   - any other transport type is an error (`unsupported http transport type`).

Proxy URLs carry credentials inline, e.g.
`http://user:pass@host:3128`, `socks5://host:1080`.

## Success criteria

- With a non-empty `Proxies` list, the request egresses through one of the
  listed proxies; HTTP(S) and SOCKS schemes are both honoured.
- An empty list errors by default and is tolerated when `AllowEmpty` is true.
- Attaching `Proxy` after `Retry` in the chain proxies the retrying client (the
  `retryablehttp.RoundTripper` branch).
- `go test ./...` passes in `vcs/gorequests-proxy` on Go 1.18.
