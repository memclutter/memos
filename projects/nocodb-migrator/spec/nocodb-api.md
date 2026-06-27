# nocodb-api

## Purpose

How the tool talks to NocoDB: the Meta API v3 client, its authentication, the
endpoints it uses for tables, fields, and records, and how migration operations
map onto them. This is the integration boundary — the only external system the
product depends on.

## Behaviour

### Client and authentication

The client (built on `go-resty`) is constructed from `NOCODB_URL`,
`NOCODB_API_TOKEN`, and `NOCODB_BASE_ID`. Every request carries the token as the
`xc-token` header and `Content-Type: application/json`, with a 30-second
timeout. All endpoints are scoped to the configured base id.

### Resolving entities by name

Migration JSON references tables and fields by human-readable title. The client
lists the base's tables and matches by title to find a table id, then fetches the
full table schema (including its fields) to resolve a field title to a field id.
A name that matches nothing yields a "not found" error that aborts the operation.

### Endpoints used

Meta API v3, schema (`/api/v3/meta/bases/{baseId}/...`):

- `GET    /tables` — list tables (used to resolve a table by title).
- `POST   /tables` — create a table (with its fields).
- `GET    /tables/{tableId}` — fetch a table's full schema.
- `PATCH  /tables/{tableId}` — update a table (title/description).
- `DELETE /tables/{tableId}` — delete a table.
- `POST   /tables/{tableId}/fields` — create a field.
- `GET    /fields/{fieldId}` — fetch a field.
- `PATCH  /fields/{fieldId}` — update a field.
- `DELETE /fields/{fieldId}` — delete a field.

Meta API v3, data (`/api/v3/data/{baseId}/{tableId}/records`):

- `GET    /records` — list records (supports `limit`/`offset`, and a `where`
  query parameter used to find records for conditional deletion).
- `POST   /records` — insert a record; the body wraps the values under `fields`.
- `DELETE /records` — delete by a body array of `{ "id": ... }` objects (single
  or bulk).

### Operation → endpoint mapping

- `create_table` → POST tables; `alter_table` → resolve by name, PATCH table;
  `drop_table` → resolve by name, DELETE table.
- `create_field` → resolve table, POST field (resolving a
  `LinkToAnotherRecord`'s related table name to `related_table_id` and defaulting
  `relation_type` to `hm`); `alter_field` → resolve table/field, PATCH field;
  `drop_field` → resolve table/field, DELETE field.
- `insert_row` → resolve table, POST record; `delete_row` → resolve table, then
  DELETE by `record_id`, or look up records matching `where` and bulk-DELETE
  them.

### Error handling

Each call inspects the HTTP response: on an error status it attempts to decode
the NocoDB error body (`message` / `error`) and returns a wrapped Go error,
falling back to the status code (and response body for data calls) when the body
isn't a recognizable API error. Errors propagate up to fail the command rather
than being swallowed.

## Success criteria

- Every request sends the `xc-token` header and targets the configured base id;
  no endpoint outside Meta API v3 is called.
- Operations referencing a non-existent table or field fail with a "not found"
  error and do not issue a mutating call.
- A NocoDB error response surfaces its `message` in the returned error rather
  than a bare status code where the body is decodable.
- Conditional `delete_row` (`where`) first lists matching records, then deletes
  exactly those ids; a `where` matching nothing deletes nothing and succeeds.
