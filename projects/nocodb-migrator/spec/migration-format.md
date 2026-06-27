# migration-format

## Purpose

The JSON format a migration file uses: the operations it can contain, the NocoDB
column types those operations may reference, and the validation the tool applies
before executing anything. This is the contract a migration author writes
against.

## Behaviour

### File shape

A migration file is a JSON object with a single `operations` array. Operations
execute top to bottom; the same shape is used for both `*.up.json` and
`*.down.json` files (the direction is conveyed by the file name, not the
content).

```json
{
  "operations": [
    { "type": "create_table", "table": "Users", "columns": [ /* ... */ ] }
  ]
}
```

### Operation types

Eight operation types are supported. Each carries the fields relevant to it:

- `create_table` — `table` (name) and `columns` (≥1 column definitions).
- `alter_table` — `table`; `data` may set `title` and/or `description`.
- `drop_table` — `table`.
- `create_field` — `table` and a single `column` definition. For a
  `LinkToAnotherRecord` column, `options.relatedTable` (a table name) is resolved
  to the related table's id and a `relation_type` is required (defaults to `hm`).
- `alter_field` — `table` plus either `field_id` or a `column` whose `name`
  identifies the field; provided column attributes are updated.
- `drop_field` — `table` plus either `field_id` or `column.name`.
- `insert_row` — `table` and a `data` object (≥1 field) of column → value.
- `delete_row` — `table` plus either `record_id` or a `where` object matching
  records to delete.

A column definition has `name` and `type` (both required) and optional
`required`, `unique`, `default_value`, `description`, and `options`.

### Supported column types

`SingleLineText`, `LongText`, `Number`, `Decimal`, `Currency`, `Percent`,
`DateTime`, `Date`, `Email`, `PhoneNumber`, `URL`, `SingleSelect`,
`MultiSelect`, `Checkbox`, `Rating`, `Attachment`, `JSON`,
`LinkToAnotherRecord`, `User`, `CreatedTime`, `CreatedBy`, `LastModifiedTime`,
`LastModifiedBy`, `ID`. A column whose `type` is outside this set is rejected.

### Validation

Migrations are validated after parsing and before any operation runs:

- The migration must contain at least one operation.
- Every operation's `type` must be one of the eight known types.
- Per-type required fields must be present (e.g. `create_table` needs `table`
  and at least one column; `delete_row` needs `record_id` or `where`;
  `alter_field`/`drop_field` need `field_id` or `column.name`).
- Each column referenced by `create_table`/`create_field`/`alter_field` is
  checked for a non-empty `name` and a `type` from the supported set.

A validation failure aborts the migration with a wrapped error that names the
offending operation index, so nothing is partially applied from that file.

## Success criteria

- A migration with an empty or missing `operations` array is rejected before any
  API call.
- An unknown operation `type` or an unsupported column `type` is rejected with an
  error naming the offending value/index.
- A `create_table` operation with no columns, or a `delete_row` with neither
  `record_id` nor `where`, fails validation.
- A valid `*.up.json` and `*.down.json` pair round-trips: applying up then down
  leaves the base as it was before (for the operations the pair covers).
