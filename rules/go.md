# Go standards

- Target the current stable Go release; manage deps with Go modules.
- Format with `gofmt`/`goimports`; lint with `golangci-lint`. Both run in CI.
- Layout: follow [golang-standards/project-layout](https://github.com/golang-standards/project-layout)
  pragmatically — `cmd/`, `internal/`, `pkg/`. Keep `internal/` for code not
  meant to be imported externally.
- Errors: wrap with `fmt.Errorf("...: %w", err)`; handle, don't ignore. No
  `panic` in library code.
- Config via environment variables (12-factor).
- Tests with the standard `testing` package + table-driven tests; `testify` is
  allowed for assertions.
- Every exported symbol has a doc comment.
