---
name: confparse
vcs:
  - git@github.com:memclutter/confparse.git
self: false
status: active
stack: [go]
created: 2026-06-28
---

# confparse

A declarative command-line argument parser for Go. The public surface is a
single exported function, `confparse.Parse(container interface{})`, which reads
struct tags off a pointer-to-struct and declares the matching `flag` flags.

## Architecture

- Single Go package `confparse`, one source file `parse.go`, module
  `github.com/memclutter/confparse`. No runtime dependencies beyond the standard
  library (`flag`, `os`, `reflect`, `strconv`, `time`). `testify` is a test-only
  dependency.
- `Parse` reflects over the container's fields, extracts the `name`, `value`,
  `usage`, and `envVar` tags, registers each field with the standard `flag`
  package via `flag.XxxVar` against the field's address, then calls
  `flag.Parse()`.
- Type dispatch is a `switch` on the field's pointer type; the set of supported
  types is whatever that switch handles today (see [spec/parsing.md](spec/parsing.md)).

## Conventions

- Follows the global [Go rules](../../rules/go.md): `gofmt`/`goimports`,
  table-driven tests, wrapped errors.
- Tests are table-driven in `parse_test.go` and run on every push via the
  `go.yml` GitHub Actions workflow; coverage is reported to Codecov.
- This is a public, imported library: treat the exported API and struct-tag
  names (`name`, `value`, `usage`, `envVar`) as a stability contract — changing
  them is a breaking change and needs a new major version.

## Working here

Source changes happen inside [vcs/confparse/](vcs/confparse/), committed and
pushed there; this OS repo then pins the new submodule commit with a
`chore(submodule): bump confparse` commit. See the root
[AGENTS.md](../../AGENTS.md) and [rules/projects.md](../../rules/projects.md).
</content>
