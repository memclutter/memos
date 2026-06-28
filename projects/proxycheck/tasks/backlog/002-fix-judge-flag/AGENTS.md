---
id: 002-fix-judge-flag
status: backlog
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

- [ ] 1. Extract `NewApp() *cli.App` (judge + threads flags, `Action`) shared by
  `cmd/main.go` and tests; collapse `main` to `NewApp().Run(os.Args)`. No
  behaviour change yet — keeps the hardcoded judge for now.
- [ ] 2. 🔴 Add regression test `cli_test.go`: `NewApp().Run(["proxycheck",
  "--judge", "foo", "not-an-addr"])` must return an error mentioning
  `unknown judge: foo`. Run it and confirm it **fails** on current code (proves
  the bug). [spec: unknown name → non-zero, nothing probed]
- [ ] 3. 🔴 Add unit test in `judges_test.go` for `ResolveJudge`: `azenv.php` and
  `proxyjudge.us` resolve to the right judge (no error); `foo` errors with a
  message listing both valid names. Confirm it **fails to compile/pass** (proves
  the gap). [spec: registry lookup + default]
- [ ] 4. Implement `ResolveJudge(name) (Judge, error)` and `judgeNames()` (sorted
  keys, comma-joined) in `judges.go`.
- [ ] 5. Wire `Action` (`cli.go`): resolve judge from `c.String("judge")` before
  the pool, `return err` on failure, pass the resolved `Judge` to every worker;
  remove the hardcoded `&AZEnvPhpJudge{}`. [spec: flag selects judge; default
  `proxyjudge.us` now in effect]
- [ ] 6. 🟢 Run the tests from steps 2–3 and confirm they pass (regression gone).
- [ ] 7. Green-gate: `go build ./...`, `go test ./... -race`, `gofmt`/`goimports`,
  `golangci-lint run` all clean. [spec: CI stays green]
- [ ] 8. Update `projects/proxycheck/spec/cli.md` per spec.md Target state (real
  `--judge` behaviour + new success criterion) — done at Finish via
  `sys.task.finish`, listed here for traceability.
