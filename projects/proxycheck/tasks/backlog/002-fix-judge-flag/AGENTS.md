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
