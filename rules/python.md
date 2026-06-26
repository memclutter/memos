# Python standards

- Target a current supported CPython (3.12+).
- Dependency & env management with `uv` (preferred) or Poetry; pin versions.
- Format and lint with `ruff` (formatter + linter). Type-check with `mypy`.
- Full type hints on public functions; `from __future__ import annotations`
  where helpful.
- Project layout: `src/<package>/` with `pyproject.toml`.
- Tests with `pytest`.
- Config via environment variables; use `pydantic-settings` for typed config.
