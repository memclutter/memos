# middleware

## Purpose

The extension contract that lets cross-cutting behaviour be added to a request
without touching the core engine. It is the only coupling between the core and
the companion modules: middleware modules implement these interfaces, and the
core invokes them during `Exec()`.

## Behaviour

Two interfaces, declared in the core `gorequests` module, are the extension
points:

- `ClientOverrideMiddleware` — `ClientOverride(c *http.Client) (*http.Client,
  error)`. Called for each attached middleware after the client is created and
  before the request is built. Used to swap or reconfigure the client/transport
  (proxying, retries). Returning an error aborts `Exec()`.
- `RequestOverrideMiddleware` — `RequestOverride(r *http.Request)
  (*http.Request, error)`. Called for each attached middleware after the request
  is built and just before `Do`. Used to mutate the outgoing request. Returning
  an error aborts `Exec()`.

`Use(middlewares ...interface{})` accepts any value and type-asserts it against
both interfaces independently:

- A value implementing `ClientOverrideMiddleware` is appended to the
  client-override list.
- A value implementing `RequestOverrideMiddleware` is appended to the
  request-override list.
- One value may implement both and will be registered in both lists.
- A value implementing neither is silently ignored.

Middlewares run in the order they were attached, client-overrides first (during
client setup) then request-overrides (just before sending).

## Success criteria

- A type implementing only `ClientOverride` is invoked with the client and never
  the request; a type implementing only `RequestOverride` is invoked with the
  request and never the client.
- An error returned from any middleware propagates out of `Exec()` and stops the
  request.
- Multiple middlewares attached via separate `Use()` calls all run, in
  attachment order.

## Cross-references

- [proxy-middleware.md](proxy-middleware.md) and
  [retry-middleware.md](retry-middleware.md) are the two shipped
  implementations, both `ClientOverride`.
