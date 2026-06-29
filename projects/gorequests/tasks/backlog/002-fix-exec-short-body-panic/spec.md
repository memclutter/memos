# Spec — 002-fix-exec-short-body-panic

## Problem

In the core `gorequests` module, `Exec()` reports a status-code mismatch like
this:

```go
return fmt.Errorf(res.Status + string(body[:50]))
```

Two defects:

1. `body[:50]` panics with a slice out-of-range whenever the response body is
   shorter than 50 bytes — which is common for error responses (`404`, empty
   bodies, short JSON like `{"error":"x"}`). Instead of a useful error, the
   caller's program crashes.
2. The built string is passed as the *format* argument to `fmt.Errorf`, so any
   `%` in the body is misinterpreted as a format verb.

This is recorded as a known gap in `spec/http-client.md` and should be removed
once fixed.

## Goal

A failing or non-OK status returns a clean error carrying the status and the
response body, for any body length including empty, without panicking.

## User journeys

- A caller sets `ResponseCodeOk(200)` and the server replies `404` with a short
  body: `Exec()` returns an error describing the status and body; the program
  keeps running.
- A caller sets `ResponseCodeFail(500)` and the server replies `500` with an
  empty body: `Exec()` returns an error and does not panic.

## Success criteria

- A status mismatch with a body shorter than 50 bytes (including an empty body)
  returns an error instead of panicking.
- The error message includes the response status and the body content.
- `%` characters in the body do not corrupt the message (a format string is used
  correctly).
- A regression test covers a short body and an empty body for both the
  `ResponseCodeOk` and `ResponseCodeFail` paths.

## Affected spec sections

- spec/http-client.md — remove the `body[:50]` bullet from "Known gaps (shipped
  reality)"; describe the error behaviour (status + body, no panic) in the
  Behaviour/Success-criteria sections.

## Target state

In `spec/http-client.md`, step 5 of the `Exec()` pipeline states that a status
mismatch returns an error containing the response status and body, for any body
length. The "Known gaps" section no longer lists the `body[:50]` panic (only the
README/aspirational-API gap remains, unless addressed elsewhere). A success
criterion states that a short or empty error body produces an error, not a
panic.

## Out of scope

- Changing which status codes are considered OK/fail, or the response-decoding
  behaviour.
- The README aspirational-API gap (separate concern).
- Any CI/tooling change — that is task 001.

## Boundaries

- ✅ Always: keep the public API unchanged; add a regression test with the fix.
- ⚠️ Ask first: changing the error message format beyond making it safe and
  informative.
- 🚫 Never: silence the mismatch (it must still return an error).
- Global rules apply ([go.md](../../../../rules/go.md)); only the task delta is
  recorded here.
