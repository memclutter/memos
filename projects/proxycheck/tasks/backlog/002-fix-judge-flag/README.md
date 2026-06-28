# 002 — Fix the `--judge` flag

## Goal

Make the `proxycheck --judge <name>` flag actually select the proxy judge used
for checking. Today the flag is parsed but ignored: the engine always uses the
AZEnv judge regardless of what `--judge` says.

## Scope

- Wire the `--judge` flag value through to `Check` via the `Judges` registry.
- Resolve `--judge <name>` against the `Judges` map keys (`azenv.php`,
  `proxyjudge.us`).
- Reject an unknown judge name with a clear error and a non-zero exit, listing
  the available names.
- Keep the default judge as `proxyjudge.us` (the flag default) — and make that
  default genuinely take effect.

## Acceptance criteria

- `proxycheck --judge azenv.php ...` checks through AZEnv; `--judge proxyjudge.us`
  (and the no-flag default) checks through proxyjudge.us.
- `proxycheck --judge foo ...` exits non-zero with `unknown judge: foo` and lists
  the valid names; no proxies are checked.
- The CLI spec's "not yet wired through" caveat is removed once the flag works.
