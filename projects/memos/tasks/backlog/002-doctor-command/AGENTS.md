---
id: 002-doctor-command
status: backlog
created: 2026-06-26
updated: 2026-06-26
depends-on: 001-migrate-cli-to-package
---

Add a `doctor` subcommand to the `memos` CLI that runs consistency checks over
the OS and exits non-zero when any fails. Builds on the packaged CLI from task
001. Scope, success criteria, and the spec delta are in `spec.md`. Plan and
breakdown follow via `sys.task.plan` and `sys.task.breakdown`.
