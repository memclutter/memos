# nocodb-migrator

A command-line migration tool for [NocoDB](https://nocodb.com). It brings the
familiar `create` / `up` / `down` / `info` migration workflow to a NocoDB base:
schema and data changes are described as timestamped JSON files and applied
against a NocoDB instance through its Meta API v3. Applied migrations are tracked
in a `Migrations` table that the tool creates inside the base itself, so no
external state store is needed.

Written in Go, distributed as a single binary (`nocodb-migrate`).

## Run locally

```bash
# build the binary
cd vcs/nocodb-migrator
go build -o nocodb-migrate

# configure (.env in the working directory, or environment variables)
cat > .env <<'EOF'
NOCODB_URL=http://localhost:8080
NOCODB_API_TOKEN=your_api_token_here
NOCODB_BASE_ID=your_base_id_here
NOCODB_MIGRATIONS_DIR=./migrations
EOF

# author a migration, then apply / inspect / roll back
./nocodb-migrate create add_users_table
./nocodb-migrate up
./nocodb-migrate info
./nocodb-migrate down 1
```

A reachable NocoDB instance with a valid API token and base id is required; the
tool talks only to that instance's Meta API v3.

## How it fits the OS

This is a project under the [memos](../..) operating system. The living product
spec lives in [spec/](spec/); work happens as SDD tasks under
[tasks/](tasks/) and lands in the upstream repo via the
[vcs/nocodb-migrator/](vcs/nocodb-migrator/) submodule
(`git@github.com:memclutter/nocodb-migrator.git`).
