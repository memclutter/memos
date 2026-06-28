# proxycheck — Product spec

## Vision

proxycheck is a tool for validating proxy lists. Given a set of `ip:port`
proxies, it determines which are alive, which protocols (`http`, `https`,
`socks4`, `socks5`) each supports, and roughly how fast each responds. It is
aimed at anyone who collects raw proxy lists and needs to filter them down to the
working ones. It is delivered both as a standalone CLI (`proxycheck`) and as an
importable Go package whose `Check` function, `Feed`, and `Judge` interfaces can
be reused in other programs.

A check is performed by routing a request to an external **proxy judge** endpoint
through the candidate proxy: if the judge responds with `HTTP 200`, the proxy is
considered to work for that protocol.

## Capabilities

- [cli.md](cli.md) — the `proxycheck` command: input feeds (args / stdin),
  flags, concurrent checking, and the tab-separated output format.
- [checking.md](checking.md) — the check engine and reusable package API: feeds,
  judges, the per-protocol probing logic, and the `CheckResult` it returns.

## Product-wide success criteria

- A list of `ip:port` proxies passed as arguments or piped on stdin is checked,
  and only proxies that reach the judge through at least one protocol are
  reported as online.
- For each online proxy the report states which of `http`, `https`, `socks4`,
  `socks5` succeeded and a response-speed figure.
- Checking is concurrent and bounded by a configurable worker count; a single
  unreachable proxy never blocks the rest.
- The library package (`github.com/memclutter/proxycheck`) builds independently
  of the CLI and exposes `Check`, the `Feed`/`Judge` interfaces, and their
  shipped implementations.

## Boundaries

Inherits the global rules — Go conventions ([go.md](../../../rules/go.md)) and
Git/release flow ([git.md](../../../rules/git.md)). Project deltas:

- ✅ Always — keep the CLI and the package usable independently; treat `ip:port`
  (and bare `ip`, defaulting to port `80`) as the proxy address format.
- ⚠️ Ask first — adding new transport protocols or new judge implementations,
  changing the output format, or introducing network behaviour that runs without
  an explicit proxy/judge.
- 🚫 Never — bundle or ship proxy lists; the tool only checks lists the user
  supplies.
