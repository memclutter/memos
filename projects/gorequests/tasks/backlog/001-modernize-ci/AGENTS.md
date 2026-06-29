---
id: 001-modernize-ci
status: backlog
created: 2026-06-29
updated: 2026-06-29
---

Modernize CI in all three repos under `projects/gorequests/vcs/` to the current
`memclutter` baseline, using `proxycheck` as the reference.

Goal: each of `gorequests`, `gorequests-proxy`, `gorequests-retry` runs an
updated `go.yml` (current `actions/checkout`/`setup-go`, current Go matrix,
`codecov/codecov-action`) plus a new `golangci-lint.yml`, both green on `main`,
with `go.mod` bumped to the agreed current minimum Go version.

Scope: the `.github/workflows/` of the three repos, their `go.mod` Go directive,
and any lint fixes the new pipeline requires. No behaviour changes to the
libraries.

Constraints: changes are made and pushed inside each `vcs/<repo-name>/`, then the
OS pins the bumps (`chore(submodule): bump …`). Pick the exact Go versions in
`sys.task.plan`.
