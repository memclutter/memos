# profile

## Purpose

Define the sections of the GitHub profile README, what each contains, and the
visual conventions that keep it consistent.

## Behaviour

The README (`vcs/memclutter/README.md`) is organised into the following sections
in order:

### Header

- An animated typing SVG from `readme-typing-svg.herokuapp.com` centred on the
  page; cycles through: "Backend / DevOps / SRE Engineer", "8+ Years of
  Experience", "Golang • Python • Bash", "Kubernetes • Terraform • AWS".
- Font: Fira Code, colour `#2E9EF7`.

### About Me

A short bulleted list with five entries:

| Bullet | Content |
|--------|---------|
| Currently working at | **Fabrique Studio** (Moscow) |
| Learning | **Rust**, **Service Mesh (Istio)**, **eBPF** |
| Ask me about | **Golang**, **Python**, **Kubernetes**, **Terraform**, **CI/CD** |
| How to reach me | [memclutter.me](https://memclutter.me) |
| Fun fact | "I love solving complex scalability challenges" |

### Tech Stack

Badge grid grouped by category (`style=for-the-badge`, white logo colour where
applicable):

| Category | Badges |
|----------|--------|
| Languages | Go, Python, Bash, JavaScript |
| DevOps & Cloud | Kubernetes, Docker, Terraform, Ansible |
| Databases & Message Queues | PostgreSQL, MongoDB, Redis, RabbitMQ |
| Monitoring & Logging | Prometheus, Grafana |
| Frontend | Vue.js |

### GitHub Statistics

Three widgets from `github-readme-stats` / `github-readme-streak-stats`,
centred, theme `tokyonight`, `hide_border=true`:
- GitHub Stats (shows icons)
- Top Languages (compact layout)
- GitHub Streak

### Featured Projects

Four sub-sections (Golang, Infrastructure as Code, Python DevOps, Other
Projects), each a bulleted list of linked repo names with one-line descriptions.
Current entries:

| Repo | Description |
|------|-------------|
| go-microservices-template | Production-ready microservice architecture template |
| kubernetes-ops-toolkit | CLI tools for K8s cluster management |
| gocore | Collection of useful patterns and snippets |
| terraform-aws-modules | Terraform modules for AWS |
| ansible-infrastructure | Ansible playbooks for server configuration |
| kubernetes-manifests | Helm charts for production stacks |
| devops-automation-python | Cloud platform automation scripts |
| ci-cd-helpers | Utilities for CI/CD pipelines |
| vue-admin-monitoring | Monitoring admin dashboard |
| algorithms-golang | Algorithm problem solutions |

### Latest Articles

Placeholder block wrapped in `<!-- BLOG-POST-LIST:START/END -->` comments; body
currently reads "Coming soon: articles about DevOps practices".

### Connect

Four flat-square badges linking to: Website (memclutter.me), LinkedIn, Twitter,
Telegram.

### Footer

Profile-view counter (`komarev.com/ghpvc`) and "⭐️ From memclutter" attribution,
both centred.

## Success criteria

- Every linked repo in Featured Projects exists and is public under
  `github.com/memclutter`.
- All external widget/badge URLs return HTTP 200.
- The README renders identically in GitHub's light and dark themes (badge text
  remains legible in both).
