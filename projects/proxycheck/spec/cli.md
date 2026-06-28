# cli

## Purpose

The `proxycheck` command-line program: take a list of proxies, check them
concurrently, and print the working ones. It is the thin user-facing wrapper
around the [checking](checking.md) engine.

## Behaviour

Invocation (binary built from `./cmd`):

```bash
proxycheck [--judge <name>] [--threads <n>] [ip:port ...]
```

**Input feed.** Proxies come from one of two sources:

- If one or more positional arguments are given, they are the proxy list
  (`proxycheck 1.2.3.4:8080 5.6.7.8:3128`).
- If no arguments are given, the proxy list is read from **stdin**, one
  `ip:port` per line; blank lines are skipped
  (`cat proxies.txt | proxycheck`).

**Flags.**

- `--threads <n>` — size of the worker pool that checks proxies concurrently.
  Default `10`.
- `--judge <name>` — names the proxy judge to check through. Resolved against the
  `Judges` registry (`azenv.php`, `proxyjudge.us`). Default `proxyjudge.us`. An
  unknown name is rejected: the command prints `unknown judge: <name>` with the
  list of valid names and exits non-zero without checking any proxy.

**Concurrency.** A pool of `--threads` workers pulls proxies from the feed and
runs a [check](checking.md) on each. One slow or unreachable proxy only occupies
its own worker and never blocks the others; the program exits after every proxy
has been processed.

**Output.** For each proxy that is online (reachable through at least one
protocol), one line is written to **stdout**, tab-separated:

```
<addr>\t<protocols>\t<speed>
```

where `<protocols>` is a comma-separated subset of `http,https,socks4,socks5`
and `<speed>` is a Go duration string (e.g. `412ms`). Proxies that fail every
protocol are reported on **stderr** as `invalid proxy <addr>: <errors>` and are
absent from stdout. This stdout/stderr split makes it easy to pipe the clean
list onward while still seeing failures.

## Success criteria

- Proxies supplied as arguments and proxies piped on stdin are both checked;
  blank stdin lines are ignored.
- Online proxies appear on stdout in the `addr<TAB>protocols<TAB>speed` format;
  failing proxies appear only on stderr.
- `--threads` bounds the number of concurrent checks; the command terminates
  once the feed is exhausted and all workers finish.
- `--judge` selects the judge used for checking; an unknown judge name is
  rejected with a non-zero exit and no proxies are checked.
