# Plan — 002-fix-judge-flag

## Approach

The fix is small and localized to `vcs/proxycheck/cli.go`: read the `--judge`
flag, resolve it to a `Judge` through the existing `Judges` registry once before
the worker pool starts, and hand that resolved judge to every worker instead of
the hardcoded `&AZEnvPhpJudge{}`.

**Order of work is TDD** (owner's request): write the tests that confirm the bug
*first*, watch them go red against the current code, then implement, then watch
them go green as the regression check.

- The **behavioural regression test** is the one that genuinely reds on today's
  code: `--judge foo` is currently ignored, so the program proceeds and exits
  `0`; the test asserts an unknown judge produces an error / non-zero exit. To
  drive the real urfave/cli flag plumbing from a test (and avoid network),
  extract a `NewApp() *cli.App` constructor shared by `cmd/main.go` and the test,
  and feed a deliberately unparsable address so the pre-fix path fails fast on a
  parse error rather than dialling out.
- The **unit test** for `ResolveJudge` is TDD for the new logic: red because the
  function/behaviour does not exist yet, green once implemented.

To keep the resolution unit-testable without constructing a `*cli.Context`,
extract a tiny pure helper in `judges.go`:

```go
// ResolveJudge looks a judge up by its registry name.
func ResolveJudge(name string) (Judge, error) {
    judge, ok := Judges[name]
    if !ok {
        return nil, fmt.Errorf("unknown judge: %s (available: %s)", name, judgeNames())
    }
    return judge, nil
}
```

`judgeNames()` returns the sorted, comma-joined `Judges` keys (sort the keys so
the message is deterministic — Go map iteration order is random). `Action` then:

```go
judge, err := ResolveJudge(c.String("judge"))
if err != nil {
    return err   // urfave/cli prints it and exits non-zero; pool never starts
}
```

and the worker calls `Check(proxyAddr, judge)`. Returning the error from `Action`
before any feed read satisfies "no proxy is checked" for an unknown name.

## Stack

Base Go stack ([go.md](../../../../../rules/go.md)). No new dependencies —
`urfave/cli/v2` and `testify` are already in `go.mod`. The `Judges` map and the
`Judge` interface already exist; this task only consumes them.

## Architecture

- **`judges.go`** — add `ResolveJudge(name string) (Judge, error)` and an
  unexported `judgeNames() string` (sorted keys). `Judges` stays the single
  source of valid names.
- **`cli.go`** — in `Action`, resolve the judge from `c.String("judge")` before
  building the pool; on error return it; otherwise share the one `Judge` value
  across all workers (judges are stateless, safe to share). Replace the hardcoded
  `&AZEnvPhpJudge{}` at [cli.go:31](../../../vcs/proxycheck/cli.go#L31). Add a
  `NewApp() *cli.App` here (or in `cmd`) that builds the app with the `judge` /
  `threads` flags and `Action`, so both `cmd/main.go` and the regression test use
  the same wiring.
- **`cmd/main.go`** — collapse to `NewApp().Run(os.Args)`; keep `log.Fatalf` on
  error. The flag default `proxyjudge.us` lives in `NewApp` and now actually
  flows through `ResolveJudge`.

Data flow: `main.go` flag default → `c.String("judge")` → `ResolveJudge` →
`Judges[name]` → `Check(addr, judge)` → per-protocol probe.

## Trade-offs & alternatives

- **Helper in `judges.go` vs inline lookup in `Action`.** Inline is fewer lines
  but couples the only testable logic to `*cli.Context`, which is awkward to
  construct in a unit test. The exported `ResolveJudge` is trivially testable and
  is a natural part of the package API alongside `Judges`. Chosen.
- **Error vs silent fallback for unknown names.** Owner chose fail-fast (error +
  non-zero exit, no probing) over warning-and-default — clearer and avoids
  silently checking against the wrong judge.
- **Sharing one `Judge` value vs constructing per worker.** Judges are stateless
  (`AZEnvPhpJudge{}` / `ProxyjudgeUsJudge{}` hold no fields), so a single shared
  value is safe and simplest.

## Constraints & risks

- **Type note:** the old code passed `&AZEnvPhpJudge{}` (pointer); `Judges` holds
  values (`AZEnvPhpJudge{}`). Methods have value receivers, so a value satisfies
  `Judge` — passing the map value directly is correct.
- **Exit code:** rely on `urfave/cli` v2 turning a non-nil `Action` error into a
  non-zero exit and printing the message; confirm the message is the one from
  `ResolveJudge` (cli may prefix it — acceptable as long as `unknown judge: foo`
  and the available names are visible).
- **Lint/format:** keep `gofmt`/`goimports` and `golangci-lint` green per
  [git.md](../../../../../rules/git.md). Sorting keys needs `sort` import.
- No behaviour change to probing, timeouts, output format, or threads.

## Testing strategy

TDD: tests first, confirm red, fix, confirm green.

1. **Red — behavioural regression (`cli_test.go`):** build the app via `NewApp()`
   and call `app.Run([]string{"proxycheck", "--judge", "foo", "not-an-addr"})`;
   assert it returns a non-nil error mentioning `unknown judge: foo`. Run against
   the *current* code → must fail (today it returns nil / exits 0). The unparsable
   `not-an-addr` keeps the pre-fix path off the network (worker hits a parse
   error and returns nil).
2. **Red — unit (`judges_test.go`)**, table-driven with testify, matching the
   existing style:
   - `ResolveJudge("azenv.php")` → `AZEnvPhpJudge`, no error.
   - `ResolveJudge("proxyjudge.us")` → `ProxyjudgeUsJudge`, no error.
   - `ResolveJudge("foo")` → error, message contains `unknown judge: foo` and
     lists both valid names.
   - Assert judge identity via `TargetURL()` (avoids a type switch) or
     `assert.IsType`. Red because `ResolveJudge` does not exist yet.
3. **Implement** `ResolveJudge`/`judgeNames`/`NewApp` and wire `Action`.
4. **Green:** both tests above now pass — the regression test proves the flag is
   honoured and the bug is gone.
5. **Build/vet:** `go build ./...`, `go test ./... -race`, `golangci-lint run`
   stay green (service-backed `request_test.go` self-skips locally without
   `PROXY_URL`/`TARGET_URL`, as in task 001).
6. **Manual smoke (optional):** `proxycheck --judge foo 1.2.3.4:80` exits
   non-zero with the error and checks nothing; `--judge azenv.php` /
   `--judge proxyjudge.us` / no flag each run without error.
