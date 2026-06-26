# Data: PostgreSQL & Redis

## PostgreSQL

- The system of record. Schema changes go through versioned migrations
  (Go: `golang-migrate`/`goose`; Python: `alembic`).
- `snake_case` for tables and columns. Prefer explicit foreign keys and
  appropriate indexes.
- Never embed credentials; read them from the environment.

## Redis

- Use for caching, ephemeral state, queues, rate limiting — not as a system of
  record.
- Namespace keys: `<app>:<entity>:<id>`. Set TTLs on cache entries.
- Treat Redis as unreliable: the app must function (degraded) if it is down.
