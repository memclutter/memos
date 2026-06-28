# Spec — 002-fix-judge-flag

## Problem

The `proxycheck --judge <name>` flag is parsed but ignored. In `Action`
(`cli.go`) every worker calls `Check(proxyAddr, &AZEnvPhpJudge{})` with a
hardcoded judge, and `c.String("judge")` is never read. So:

- The flag's documented default (`proxyjudge.us`) never takes effect — the engine
  silently uses AZEnv instead.
- `--judge proxyjudge.us` and `--judge azenv.php` produce identical behaviour.
- A `Judges` registry already exists keyed by `azenv.php` / `proxyjudge.us` but is
  unused by the CLI.

A user choosing a judge gets no say, and the help text lies about the default.

## Goal

Make `--judge <name>` actually select the proxy judge, resolved through the
existing `Judges` registry, with the `proxyjudge.us` default genuinely in effect.

## User journeys

- A user runs `proxycheck --judge azenv.php 1.2.3.4:8080` and the proxy is
  checked against the AZEnv judge.
- A user runs `proxycheck --judge proxyjudge.us ...` (or omits the flag) and the
  proxy is checked against the proxyjudge.us judge.
- A user mistypes `proxycheck --judge azenv 1.2.3.4:8080`; the command prints
  `unknown judge: azenv` with the list of valid names and exits non-zero without
  probing anything.

## Success criteria

- The judge passed to `Check` is the one named by `--judge`, resolved via the
  `Judges` map; the default `proxyjudge.us` is used when the flag is omitted.
- An unknown `--judge` name makes `Action` return an error → non-zero exit, with
  a message naming the bad value and listing the valid names; no proxy is checked.
- A test covers judge resolution: a valid name resolves to the right judge, an
  unknown name yields an error.
- `go build`, `go test ./...`, `gofmt`/`goimports`, and `golangci-lint` stay
  green (CI per [git.md](../../../../../rules/git.md)).

## Affected spec sections

- spec/cli.md — modify: replace the `--judge` "not yet wired through" caveat with
  the real behaviour (registry lookup, default, unknown-name error).
- spec/checking.md — no change (the `Judges` registry and `Judge` interface are
  already specced correctly; this task only consumes them).
- spec/overview.md — no change.

## Target state

`spec/cli.md`, under **Flags**, the `--judge` bullet must read approximately:

> - `--judge <name>` — names the proxy judge to check through. Resolved against
>   the `Judges` registry (`azenv.php`, `proxyjudge.us`). Default `proxyjudge.us`.
>   An unknown name is rejected: the command prints `unknown judge: <name>` with
>   the list of valid names and exits non-zero without checking any proxy.

The standalone "*Current shipped behaviour:* the flag is accepted but the engine
always uses the AZEnv judge … the value is not yet wired through." sentence is
removed. `spec/cli.md` **Success criteria** gains:

> - `--judge` selects the judge used for checking; an unknown judge name is
>   rejected with a non-zero exit and no proxies are checked.

## Out of scope

- Adding new judges or new judge implementations (project boundary: ask first).
- Changing the `Judge` interface, timeouts, or the per-protocol probing logic.
- Changing the output format, threads flag, or feed behaviour.

## Boundaries

- ✅ Always — resolve the judge through the existing `Judges` registry; keep the
  CLI and package independently usable.
- ⚠️ Ask first — adding/altering judges or changing the default judge name.
- 🚫 Never — bundle proxy lists; introduce network behaviour without an explicit
  judge.
Inherits global Go ([go.md](../../../../../rules/go.md)) and Git
([git.md](../../../../../rules/git.md)) rules.
