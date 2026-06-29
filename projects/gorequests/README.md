# gorequests

A small family of Go HTTP-client libraries that make everyday requests read
like a sentence instead of a page of boilerplate. It is three packages:

- **[gorequests](https://github.com/memclutter/gorequests)** — the core fluent
  wrapper around `net/http`: build a request, set headers/body/cookies, assert
  the status code, and decode the response in one chain.
- **[gorequests-proxy](https://github.com/memclutter/gorequests-proxy)** —
  opt-in middleware that routes a request through an HTTP(S) or SOCKS proxy
  picked at random from a list.
- **[gorequests-retry](https://github.com/memclutter/gorequests-retry)** —
  opt-in middleware that retries on network errors and configured status codes,
  backed by `hashicorp/go-retryablehttp`.

The middlewares share nothing with the core except a small interface contract,
so you pull in only what you need and compose them with `Use()`.

## Example

```go
import (
	"net/http"
	"github.com/memclutter/gorequests"
	gorequests_proxy "github.com/memclutter/gorequests-proxy"
	gorequests_retry "github.com/memclutter/gorequests-retry"
)

var out map[string]string
err := gorequests.Get("https://api.ipify.org?format=json").
	Use(&gorequests_retry.Retry{RetryMax: 3}).
	Use(&gorequests_proxy.Proxy{Proxies: []string{"http://user:pass@host:3128"}}).
	ResponseCodeOk(http.StatusOK).
	ResponseJson(&out).
	Exec()
```

## Layout in this OS

This project is managed as part of the [memclutter OS](../../AGENTS.md). The
three repositories live as git submodules under `vcs/`; source changes are made
inside `vcs/<repo-name>/` and this OS pins the resulting commits. The living
product spec — what the libraries actually do today — is in [spec/](spec/), and
work is tracked under [tasks/](tasks/).

```bash
git submodule update --init --recursive   # fetch the three repos
cd vcs/gorequests && go test ./...         # run a module's tests
```
