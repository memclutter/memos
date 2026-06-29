# retry-middleware

## Purpose

`gorequests-retry` retries failed requests — network errors and retryable status
codes — without the caller writing a retry loop. It is a `ClientOverride`
middleware (package `gorequests_retry`, module
`github.com/memclutter/gorequests-retry`) attached via `Use()`, backed by
`hashicorp/go-retryablehttp`.

## Behaviour

The middleware is the `Retry` struct:

```go
type Retry struct {
	RetryMax     int
	RetryWaitMin time.Duration
	RetryWaitMax time.Duration
}
```

On `ClientOverride`:

1. A new `retryablehttp.Client` is created with the incoming `*http.Client` as
   its underlying `HTTPClient`.
2. `RetryMax`, `RetryWaitMin`, and `RetryWaitMax` are copied onto it; the logger
   is disabled (`Logger = nil`).
3. It returns `rc.StandardClient()` — a standard `*http.Client` whose transport
   is a `retryablehttp.RoundTripper`. Retry policy and exponential backoff
   between `RetryWaitMin` and `RetryWaitMax` come from `go-retryablehttp`
   defaults (retries on connection errors and 5xx/429-style responses).

Because the result's transport is a `retryablehttp.RoundTripper`, the proxy
middleware recognises and patches it — so `Retry` and `Proxy` compose
regardless of order, as long as `Retry` is applied first.

## Success criteria

- A transient network failure or a retryable status code is retried up to
  `RetryMax` times with backoff bounded by `RetryWaitMin`/`RetryWaitMax`.
- No retry logging is emitted.
- The returned client composes with `gorequests-proxy` (see
  [proxy-middleware.md](proxy-middleware.md)).
- `go test ./...` passes in `vcs/gorequests-retry` on Go 1.17.
