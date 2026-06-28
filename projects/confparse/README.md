# confparse

Declarative command-line argument parser for Go projects. Describe your
configuration as a struct with tags and call `confparse.Parse` — fields become
CLI flags, with optional defaults and environment-variable fallbacks.

```go
type Config struct {
	Addr   string `name:"addr" value:":8000" usage:"Listen and serve address"`
	ApiKey string `name:"apiKey" envVar:"API_KEY" usage:"API key"`
}

cfg := &Config{}
if err := confparse.Parse(cfg); err != nil {
	log.Fatalf("parse configuration: %s", err)
}
```

## Install

```shell
go get github.com/memclutter/confparse
```

## Source

The library source lives in [vcs/confparse/](vcs/confparse/) (git submodule of
[github.com/memclutter/confparse](https://github.com/memclutter/confparse)). It
is a single-package Go module with no runtime dependencies beyond the standard
library; `testify` is used in tests only.

```shell
cd vcs/confparse
go test ./...
```

## How it fits the OS

This folder is the confparse project inside the personal OS (see the root
[AGENTS.md](../../AGENTS.md)). The living product spec is under
[spec/](spec/); tasks live under [tasks/](tasks/) and amend the spec as deltas,
folded back in at the Finish gate.
</content>
</invoke>
