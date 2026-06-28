# parsing

## Purpose

Turn a tagged Go struct into command-line flags. This is the entire product: one
exported function that reflects over a configuration struct, registers each field
with the standard `flag` package, and parses `os.Args` into it — with optional
defaults and environment-variable fallbacks.

## Behaviour

### Entry point

```go
func Parse(container interface{}) error
```

`container` must be a pointer to a struct. `Parse` iterates the struct's fields,
reads each field's tags, declares a `flag` bound to the field's address, then
calls `flag.Parse()` to populate the struct from `os.Args`. It returns an error
only when a field's default `value` cannot be parsed into the field's type
(see [Errors](#errors)).

### Struct tags

Each field is configured by tags on the struct field:

| Tag      | Meaning                                                              |
|----------|---------------------------------------------------------------------|
| `name`   | Flag name, e.g. `name:"addr"` registers `-addr`.                     |
| `value`  | Default value as a string; parsed into the field's type.            |
| `usage`  | Help text shown by the `flag` package's usage output.               |
| `envVar` | Environment variable to source the default from (see below).        |

```go
type Config struct {
	Addr    string        `name:"addr" value:":8000" usage:"Listen and serve address"`
	Timeout time.Duration `name:"timeout" value:"200ms" usage:"Timeout value"`
	ApiKey  string        `name:"apiKey" envVar:"API_KEY" usage:"API key"`
	Debug   bool          `name:"debug" envVar:"DEBUG"`
}
```

A field with no recognised tags / unsupported type is simply skipped (no flag is
registered for it). `usage` and `value` are both optional.

### Supported field types

The type switch handles exactly these field types; any other type is silently
ignored:

- `string`
- `int`
- `int64`
- `uint`
- `uint64`
- `bool`
- `time.Duration`

`value` strings are converted per type: `strconv.Atoi` / `ParseInt` / `ParseUint`
/ `ParseBool`, and `time.ParseDuration` for durations. An empty `value` yields
the type's zero value (e.g. `false`, `0`, `0s`).

### Defaults and precedence

For each field, the effective default is computed before the flag is registered:

1. Start with the `value` tag (or the type's zero value if absent).
2. If `envVar` is set **and** that environment variable is non-empty, its value
   replaces the default.
3. The CLI flag (`-name ...`) then overrides whatever default was chosen, via the
   standard `flag` parsing.

So precedence is **CLI flag > environment variable > `value` default > zero
value**. The environment value, when used, must be parseable into the field's
type just like a `value` default.

### Environment extension

`envVar` exists so an application can read configuration from the environment
without extra code: set `envVar:"API_KEY"` and confparse seeds that field's
default from `$API_KEY`. An unset or empty environment variable is ignored and
the `value` default (or zero value) stands.

### Errors

`Parse` returns the underlying conversion error when a default (`value`, or the
sourced environment value) is not parseable into the field's type — for example
`value:"abc"` on an `int` field returns `strconv.Atoi: parsing "abc": invalid
syntax`, and `value:"bad"` on a `time.Duration` returns `time: invalid duration
"bad"`. Flag-parsing failures (bad CLI input) are handled by the standard `flag`
package according to the active `flag.CommandLine` error-handling mode.

## Success criteria

- A pointer-to-struct with `name` tags is populated from matching CLI flags.
- Each supported type (`string`, `int`, `int64`, `uint`, `uint64`, `bool`,
  `time.Duration`) parses both its `value` default and a CLI-supplied value.
- A non-empty `envVar` environment variable supplies the default; a CLI flag
  still overrides it.
- An unparseable default `value` makes `Parse` return the conversion error.
- Behaviour is covered by the table-driven tests in
  [vcs/confparse/parse_test.go](../vcs/confparse/parse_test.go) and `go test ./...`
  passes.
</content>
