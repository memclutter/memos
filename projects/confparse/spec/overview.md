# confparse — Product spec

## Vision

confparse is a tiny, dependency-free Go library that lets an application declare
its command-line configuration as a tagged struct instead of hand-wiring the
standard `flag` package. The developer writes one struct and calls
`confparse.Parse(&cfg)`; confparse turns each field into a CLI flag, applies
per-field defaults, and optionally seeds defaults from environment variables. It
is for Go developers who want concise, declarative configuration for CLIs and
services without pulling in a heavy framework.

## Capabilities

- [parsing.md](parsing.md) — declarative struct-tag parsing: the `Parse` entry
  point, supported field types, the `name`/`value`/`usage`/`envVar` tags,
  defaults, environment-variable fallbacks, and error behaviour.

## Product-wide success criteria

- A pointer to a tagged struct passed to `confparse.Parse` populates its fields
  from `os.Args` (and environment, where `envVar` is set) with no other wiring.
- The library has no runtime dependencies beyond the Go standard library.
- `go test ./...` in `vcs/confparse/` passes; CI (`go.yml`) is green on `main`
  and coverage is reported to Codecov.
- The exported API is a single function, `Parse(container interface{}) error`.

## Boundaries

Global rules apply ([git.md](../../../rules/git.md), [go.md](../../../rules/go.md)).
Project-specific deltas:

- ✅ **Always** — keep the library standard-library-only at runtime; keep tests
  table-driven and CI green before pushing.
- ⚠️ **Ask first** — adding a new supported field type or a new struct tag
  (extends the public contract); adding any runtime dependency.
- 🚫 **Never** — make a backward-incompatible change to the exported `Parse`
  signature or to the existing tag names (`name`, `value`, `usage`, `envVar`)
  without a new major version.
</content>
