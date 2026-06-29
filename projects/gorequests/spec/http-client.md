# http-client

## Purpose

The core `gorequests` module: a fluent builder over `net/http` that lets a
caller construct a request, send it, assert the response status, and decode the
body in a single chain. It is the foundation every other module extends.

## Behaviour

A request is built through the `RequestsInstance` interface. Construction starts
either with `Requests()` (empty builder) or a verb helper that presets the
method and URL:

- `Trace`, `Connect`, `Head`, `Options`, `Get`, `Post`, `Put`, `Delete`,
  `Patch` — each is `Requests().Method(verb).Url(url, args...)`.
- `Url(format, args...)` runs the URL through `fmt.Sprintf`, so URLs can be
  templated inline, e.g. `Get("https://api/%s/%d", kind, id)`.

The builder methods are chainable and each returns the instance:

- `Method(string)` — set the HTTP verb.
- `Header(key, value)` — add a header (additive; multiple values accumulate).
- `Cookies(...*http.Cookie)` — attach cookies.
- `Data([]byte, contentType...)` — raw body with an optional content type.
- `Form(url.Values)` — form body; sets `Content-Type:
  application/x-www-form-urlencoded`.
- `Json(any)` — JSON body; marshals the value and sets `Content-Type:
  application/json`.
- `ResponseCodeOk(...int)` — whitelist of acceptable status codes.
- `ResponseCodeFail(...int)` — blacklist of failing status codes.
- `ResponseRaw(*[]byte)` — capture the raw response body.
- `ResponseJson(any)` — unmarshal the JSON response body into the target.
- `Use(...interface{})` — attach middleware (see [middleware.md](middleware.md)).
- `Exec() error` — build and send the request, then apply response handling.

`Exec()` runs this pipeline:

1. Choose the body: raw `Data` if set; otherwise `Form` (form-encoded) takes
   precedence over `Json`. The matching content type is applied.
2. Create an `*http.Client{}` and run every client-override middleware over it.
3. Build the `*http.Request`, set content type, add accumulated headers and
   cookies.
4. Run every request-override middleware over the request, then `client.Do`.
5. Read the full body. If `ResponseCodeFail` codes are set and the status
   matches one, return an error. If `ResponseCodeOk` codes are set and the
   status matches none, return an error.
6. If `ResponseRaw` was given, copy the body into it. If `ResponseJson` was
   given, unmarshal the body into it.

Mocks for both middleware interfaces (`mockClientOverrideMiddleware`,
`mockRequestOverrideMiddleware`) are shipped for testing consumers.

## Success criteria

- `gorequests.Get(url).ResponseCodeOk(200).ResponseJson(&v).Exec()` issues the
  request, fails on a non-200 status, and decodes the body into `v`.
- A `Form` body and a `Json` body each set their respective `Content-Type`
  automatically; `Form` wins when both are set.
- Headers added via repeated `Header` calls all reach the wire.
- `go test ./...` passes in `vcs/gorequests` on Go 1.18.

## Known gaps (shipped reality)

- The README advertises `Request()` and a JSON-path selector
  (`ResponseJson(&v, ".ip")`); the shipped API is `Requests()` and
  `ResponseJson(v)` with no selector.
- The status-mismatch error slices the body as `body[:50]`, which panics on
  bodies shorter than 50 bytes — a real bug, recorded here as current behaviour,
  not endorsed.
