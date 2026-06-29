---
id: 002-fix-exec-short-body-panic
status: backlog
created: 2026-06-29
updated: 2026-06-29
---

Fix the panic in `gorequests.Exec()` (core `gorequests` repo) where a status-code
mismatch builds its error as `res.Status + string(body[:50])`, which slices out
of range when the response body is shorter than 50 bytes.

Goal: a failing/non-OK status returns a clean error that includes the status and
the response body, for any body length (including empty), without panicking.

Scope: the two error branches in `Exec()` (`ResponseCodeFail` and
`ResponseCodeOk`) in `vcs/gorequests/requests.go`, plus a regression test. No
API change.

Constraints: changes are made and pushed inside `vcs/gorequests/`, then the OS
pins the bump. Use `fmt.Errorf` with a proper format string (the current code
passes a built string as the format argument — fix that too).
