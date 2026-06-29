# 002 — Fix Exec() panic on short error bodies

## Goal

Make a status-code mismatch in `gorequests.Exec()` return a clean error instead
of panicking when the response body is shorter than 50 bytes.

## Scope

- The error path in `Exec()` (core `gorequests` repo) where a failing/non-OK
  status builds an error from `res.Status + string(body[:50])`.

## Acceptance criteria

- A request whose response trips `ResponseCodeFail` / `ResponseCodeOk` with a
  body shorter than 50 bytes returns an error rather than panicking with a slice
  out-of-range.
- The returned error still carries the status and the response body for
  diagnosis.
- A regression test covers a short error body (and an empty one).
- The `body[:50]` "known gap" is removed from `spec/http-client.md`.
