# Docker & local dev

- Every project ships a `Dockerfile` (multi-stage, minimal final image) and a
  `docker-compose.yml` for local development.
- `docker compose up` must bring the full local stack up (app + Postgres +
  Redis as needed) with sensible defaults.
- Pin base image tags; do not rely on `latest`.
- Run as a non-root user in the final stage.
- Use `.dockerignore` to keep build context small.
- Configuration comes from environment variables; provide a committed
  `.env.example`.
