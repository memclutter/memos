---
name: proxycheck
vcs:
  - git@github.com:memclutter/proxycheck.git
self: false
status: active
stack: [go]
created: 2026-06-28
---

A Go tool that checks whether proxies in a list are alive and which protocols
they support. It ships both as a CLI binary (`proxycheck`) and as an importable
Go package (`github.com/memclutter/proxycheck`). It follows the base stack
([rules/go.md](../../rules/go.md)): Go modules, wrapped errors, table-driven
tests.

## Architecture

- The repo root is the library package `proxycheck`; `cmd/main.go` is the thin
  CLI entry point built on [urfave/cli v2](https://github.com/urfave/cli).
- `base.go` defines the two core interfaces: `Feed` (a source of the next proxy
  address to check) and `Judge` (a "proxy judge" endpoint plus its recommended
  timeout).
- `feed.go` implements `Feed`: `SliceFeed` (proxies from a string slice, e.g.
  CLI args) and `FileFeed` (one proxy per line from an `io.Reader`, e.g. stdin),
  both signalling exhaustion with the `FeedEnd` sentinel from `errors.go`.
- `judges.go` implements `Judge`: `AZEnvPhpJudge` and `ProxyjudgeUsJudge`, plus a
  `Judges` registry map keyed by name.
- `check.go` is the engine: `Check(addr, judge)` tries each protocol against the
  judge and returns a `CheckResult` (online flag, supported protocols, per-
  protocol errors, speed).
- `request.go` / `utils.go` do the network work: build a per-protocol
  `http.Transport` (HTTP/HTTPS via `http.ProxyURL`, SOCKS4/SOCKS5 via
  [h12.io/socks](https://h12.io/socks)) and run the timed request.
- `cli.go` wires it together: pick a feed, run a worker pool over `Check`, print
  online proxies to stdout and failures to stderr.

## Conventions

- Proxy addresses are `ip:port` strings; a bare `ip` defaults to port `80`.
- The protocol set tried per proxy is fixed: `http`, `https`, `socks4`,
  `socks5`. A proxy is "online" if at least one protocol reaches the judge.
- Source changes are committed and pushed inside `vcs/proxycheck/`, then this OS
  pins the new submodule commit (`chore(submodule): bump proxycheck`).
