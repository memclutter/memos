---
id: 002-fix-judge-flag
status: active
created: 2026-06-28
updated: 2026-06-28
---

Fix the `--judge` flag so it selects the proxy judge instead of being ignored.

**Goal.** In `cli.go` the worker calls `Check(proxyAddr, &AZEnvPhpJudge{})` —
hardcoded. `c.String("judge")` is never read, so both the flag value and the
`proxyjudge.us` default are dead. Read the flag, look the name up in the `Judges`
registry, and pass the resolved judge to `Check`.

**Behaviour decisions (from the owner).**
- Unknown `--judge <name>` → fail fast: return an error so the CLI exits
  non-zero, message `unknown judge: <name>` plus the list of valid names; do not
  check any proxy.
- Default stays `proxyjudge.us` (the existing flag default) and must now actually
  be used.

**Scope.** `Action` in `vcs/proxycheck/cli.go`; the `Judges` map in
`vcs/proxycheck/judges.go` is the source of valid names. Resolve the judge once,
before the worker pool starts, and share it across workers.

**Acceptance.**
- `--judge azenv.php` / `--judge proxyjudge.us` / no flag each route through the
  named (or default) judge.
- `--judge foo` exits non-zero with `unknown judge: foo` and lists valid names;
  nothing is probed.
- Add/extend a test covering judge resolution (valid name resolves, unknown name
  errors).

**Constraints.** Inherit global Go rules ([go.md](../../../../../rules/go.md)) and
the project boundary that adding a *new* judge needs the owner's sign-off — this
task wires up the existing two, it does not add judges. Source changes happen in
`vcs/proxycheck/`; this OS repo only re-pins the submodule.

## Tasks breakdown

TDD order: write tests, confirm red, implement, confirm green.

- [x] 1. Extract `NewApp() *cli.App` (judge + threads flags, `Action`) shared by
  `cmd/main.go` and tests; collapse `main` to `NewApp().Run(os.Args)`. No
  behaviour change yet — keeps the hardcoded judge for now.
- [x] 2. 🔴 Add regression test `cli_test.go`: `NewApp().Run(["proxycheck",
  "--judge", "foo", "not-an-addr"])` must return an error mentioning
  `unknown judge: foo`. Confirmed RED on current code — it did not abort, printed
  `invalid proxy not-an-addr` and then hung at `wg.Wait()` (60s timeout),
  surfacing the channel-close deadlock too. [spec: unknown name → non-zero]
- [x] 3. 🔴 Add unit test in `judges_test.go` for `ResolveJudge`: `azenv.php` and
  `proxyjudge.us` resolve to the right judge (no error); `foo` errors with a
  message listing both valid names. Red (function absent). [spec: registry lookup]
- [x] 4. Implement `ResolveJudge(name) (Judge, error)` and `judgeNames()` (sorted
  keys, comma-joined) in `judges.go`.
- [x] 5. Wire `Action` (`cli.go`): resolve judge from `c.String("judge")` before
  the pool, `return err` on failure, pass the resolved `Judge` to every worker;
  remove the hardcoded `&AZEnvPhpJudge{}`. [spec: flag selects judge; default
  `proxyjudge.us` now in effect]
- [x] 5b. Fix the discovered deadlock: `close(proxyAddrs)` after the feed loop so
  workers' range loops end and `wg.Wait()` returns (owner-approved, in scope).
  [spec/cli.md: program exits once the feed is exhausted]
- [x] 6. 🟢 Tests from steps 2–3 pass in 0.004s (regression gone).
- [x] 7. Green-gate: `go vet`, `go test ./... -race` (1.0s), `gofmt -l` (clean),
  `golangci-lint run` all exit 0. [spec: CI stays green]
- [ ] 8. Update `projects/proxycheck/spec/cli.md` per spec.md Target state (real
  `--judge` behaviour + new success criterion) — done at Finish via
  `sys.task.finish`, listed here for traceability.
