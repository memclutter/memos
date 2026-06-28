# checking

## Purpose

The engine that decides whether a single proxy works, and the reusable Go
package API around it. This is the core of the product; the [CLI](cli.md) is one
caller of it.

## Behaviour

**Address parsing.** A proxy address is an `ip:port` string. A bare `ip` with no
port defaults to port `80`. A non-numeric port or an unparsable IP makes the
check fail immediately with a parse error.

**Per-protocol probing.** `Check(addr, judge)` tries the proxy against a fixed
protocol set in order: `http`, `https`, `socks4`, `socks5`. For each protocol it
builds a proxy URL (`<protocol>://<ip>:<port>`) and issues an HTTP `GET` to the
judge's target URL **through that proxy**:

- HTTP/HTTPS proxies use Go's `http.ProxyURL` transport.
- SOCKS4/SOCKS5 proxies dial through [h12.io/socks](https://h12.io/socks).
- The request uses the judge's recommended timeout, with keep-alives disabled.
- A response is a success only when the transport completes **and** the status
  code is `HTTP 200`; any transport error or non-200 status fails that protocol.

**Result.** `Check` returns a `CheckResult`:

- `Online` — `true` if at least one protocol succeeded.
- `Protocols` — the list of protocols that succeeded.
- `Speed` — a response-time figure derived from the successful probes (a
  `time.Duration`).
- `Err` — a map of the per-protocol errors for the protocols that failed (keyed
  by protocol name; the empty key holds an address-parse error).

**Judges.** A `Judge` supplies the target URL to fetch and the recommended
timeout. Two are shipped — `AZEnvPhpJudge` (`http://www.wfuchs.de/azenv.php`, 3s)
and `ProxyjudgeUsJudge` (`http://proxyjudge.us/`, 1s) — and are registered in the
`Judges` map keyed by `azenv.php` / `proxyjudge.us`.

**Feeds.** A `Feed` yields the next proxy address to check and returns the
`FeedEnd` sentinel error when exhausted. Two are shipped: `SliceFeed` (from a
`[]string`, e.g. CLI args) and `FileFeed` (one address per line from any
`io.Reader`, e.g. stdin, skipping blank lines).

**Package API.** Built as `github.com/memclutter/proxycheck`, the package exports
`Check`, `CheckResult`, the `Feed` and `Judge` interfaces, the `SliceFeed` /
`FileFeed` / `AZEnvPhpJudge` / `ProxyjudgeUsJudge` implementations, the `Judges`
registry, `ProxyRequest` (a single timed request through a proxy URL), and the
`FeedEnd` sentinel — so the engine is usable without the CLI.

## Success criteria

- A reachable proxy is reported `Online` with exactly the protocols that
  returned `HTTP 200` through the judge, and a non-zero `Speed`.
- An unreachable proxy is reported not online with a per-protocol error for each
  attempted protocol.
- An unparsable address fails fast with a parse error and is never probed.
- The `Feed` and `Judge` interfaces, their shipped implementations, and `Check`
  are importable and compile without the CLI command.
