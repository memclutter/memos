# Base stack

The default toolbox. New tools are added deliberately, project by project, as a
way to learn. When a project introduces something outside this list, record the
choice and the reason in that project's README; if it becomes a recurring habit,
add or extend a rule file here.

| Layer         | Default        |
|---------------|----------------|
| Backend       | Go, Python     |
| Database      | PostgreSQL     |
| Cache / queue | Redis          |
| Frontend      | Vue.js         |
| Packaging     | Docker         |

Per-language and per-tool conventions live in their own rule files:
[go.md](go.md), [python.md](python.md), [vue.md](vue.md),
[docker.md](docker.md), [data.md](data.md).
