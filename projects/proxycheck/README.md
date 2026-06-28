# proxycheck

A proxy list checker. Given a list of `ip:port` proxies, it tests each one and
reports which are alive and which protocols (`http`, `https`, `socks4`,
`socks5`) they support, along with a rough response speed. Checks run through an
external "proxy judge" endpoint: the tool fetches the judge URL through each
proxy and treats an `HTTP 200` as proof that the proxy works for that protocol.

Written in Go, distributed as a single binary (`proxycheck`) and also usable as
an importable package (`github.com/memclutter/proxycheck`).

## Run locally

```bash
# build the binary
cd vcs/proxycheck
go build -o proxycheck ./cmd

# check proxies passed as arguments
./proxycheck 108.20.30.1:8080 89.33.123.100:3128

# or pipe a proxy list (one ip:port per line) on stdin
cat proxies.txt | ./proxycheck --threads 50
```

Online proxies are printed to stdout as `addr<TAB>protocols<TAB>speed`; failures
go to stderr. Outbound network access is required — each check makes a real
request to the proxy judge through the candidate proxy.

## How it fits the OS

This is a project under the [memos](../..) operating system. The living product
spec lives in [spec/](spec/); work happens as SDD tasks under [tasks/](tasks/)
and lands in the upstream repo via the [vcs/proxycheck/](vcs/proxycheck/)
submodule (`git@github.com:memclutter/proxycheck.git`).
