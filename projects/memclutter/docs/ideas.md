# New project ideas — AI-native portfolio

## Why this list exists

The `memclutter` GitHub profile ([profile.md](../spec/profile.md)) currently
showcases backend/DevOps tooling (Go CLIs, infra utilities) but almost nothing
that signals **AI engineer** depth — ai-native products, agent workflows,
LLM tooling. The goal of this document is to generate, vet, and tier candidate
projects that close that gap **without abandoning the existing moat**: 8+
years of backend/SRE/DevOps (Go, Python, Kubernetes, Terraform, Postgres,
Redis) is the differentiator versus the flood of thin prompt-wrapper repos. The
strongest ideas sit at the intersection of *infra/platform engineering* and
*AI-native workflows* — not at "yet another chatbot UI."

This file is a backlog of raw ideas, not specs. A promising idea graduates into
a real task via `sys.task.specify` (or a brand-new project via
`sys.project.specify`) only after it survives the filter in step 4 below.

## 1. Idea-generation algorithm

1. **Map strengths → AI-infra needs.** For each core skill (Go, Python,
   Kubernetes, Terraform, Postgres, Redis, Vue), list the adjacent pain point
   in the current AI tooling stack: agent runtimes, LLM observability, eval
   pipelines, RAG infra, MCP tooling, FinOps for LLM spend, sandboxing for
   agent-executed code. Backend/DevOps skill + AI-native problem = candidate
   idea.
2. **Sweep sources for signal.** On a recurring cadence (see §3), scan the
   sources below for: recurring complaints ("there's no good X for Y"), a
   newly-published spec/protocol worth tooling around (e.g. MCP), a
   trending-but-immature GitHub repo with an obvious gap, or a job-posting
   pattern repeating a skill not yet represented in the profile.
3. **Draft the one-liner.** For each signal, write a single sentence: problem,
   who hits it, why *this* author (backend/DevOps background) is credible to
   build it. Discard anything that is a pure prompt wrapper with no infra
   component — it doesn't differentiate the profile.
4. **Score and filter.** Rate every surviving one-liner 1–3 on:
   - **Signal** — does it visibly demonstrate ai-native/agent/LLM-workflow
     skill, not just "calls an API"?
   - **Moat** — does it lean on Go/Python/K8s/Terraform/Postgres/Redis in a
     way a non-infra person couldn't replicate quickly?
   - **Scope** — buildable and shippable solo within a bounded timeframe?
   - **Testability** — can correctness be demonstrated with automated tests
     (unit/integration/eval), not just a demo gif?
   Keep anything scoring ≥ 2 on all four; drop the rest from this file.
5. **Tier by implementation + testing weight** (see §3 below) so the backlog
   always has a quick win available alongside a flagship bet.
6. **Promote, don't accumulate.** Re-review this list monthly: prune ideas a
   third party has already shipped well, or that no longer reflect current
   tooling (e.g. a protocol superseded); promote at most one Tier 1–2 idea
   per cycle into an actual task/project so the backlog stays a backlog, not a
   museum.

## 2. Information sources

Used to feed step 2 above — re-scanned each review cycle, not read linearly.

**Practitioner blogs / written deep-dives**
- [Simon Willison's blog](https://simonwillison.net/) — LLM tooling, agent
  experiments, MCP commentary.
- [Latent Space](https://www.latent.space/) (newsletter + podcast, swyx/Alessio)
  — AI engineering trends, tool ecosystem.
- [Hamel Husain](https://hamel.dev/) — LLM evals, fine-tuning, what actually
  matters in production AI systems.
- [Eugene Yan](https://eugeneyan.com/) — applied ML/LLM systems writing.
- [Chip Huyen](https://huyenchip.com/) — AI engineering / ML systems design.
- Provider engineering blogs: [Anthropic Engineering](https://www.anthropic.com/engineering),
  [OpenAI Cookbook](https://cookbook.openai.com/), [Google DeepMind blog](https://deepmind.google/discover/blog/).

**Protocols, frameworks, and their release notes**
- [Model Context Protocol](https://modelcontextprotocol.io/) spec + server
  registry — the main "what tooling does an agent need" signal right now.
- LangChain / LlamaIndex / CrewAI / AG2 (AutoGen) blogs and changelogs —
  agent-orchestration patterns and their gaps.
- Eval/observability vendors: [Langfuse](https://langfuse.com/),
  [Braintrust](https://www.braintrust.dev/), [Promptfoo](https://www.promptfoo.dev/),
  [Ragas](https://docs.ragas.io/), [Arize Phoenix](https://phoenix.arize.com/).
- Inference/serving infra: [vLLM](https://github.com/vllm-project/vllm),
  [Together AI blog](https://www.together.ai/blog), [Modal blog](https://modal.com/blog).

**Aggregators / community signal**
- [Hugging Face Daily Papers](https://huggingface.co/papers) and
  [Papers with Code trending](https://paperswithcode.com/) — research signal
  worth turning into infra.
- GitHub Trending (topics: `llm`, `agents`, `mcp`, `rag`) — what's getting
  adopted *this week*.
- `r/LocalLLaMA`, `r/MachineLearning`, Hacker News (`ai`, `llm` threads) —
  practitioner pain points, "why is there no good tool for X" threads.
- Curated lists: `awesome-llm-apps`, `awesome-mcp-servers`.

**Market signal**
- AI engineer / platform engineer job postings (titles, required-skills
  sections) — cross-check that backlog ideas track in-demand skills, not just
  personal curiosity.
- Dogfooding friction — anything annoying encountered while actually using
  Cursor/Claude Code/agents day to day is a first-party signal, weighted
  higher than any external source.

## 3. Ideas by tier

Tiers track **implementation effort + testing rigor**, not importance — a
Tier 1 project is still worth shipping for portfolio breadth.

### Tier 1 — Quick wins (days; unit/fixture-level tests; single Go/Python repo)

| Idea | One-liner | Why it fits |
|------|-----------|-------------|
| `mcp-postgres-toolkit` | Go MCP server exposing safe, read-only Postgres introspection/query tools for LLM agents | Direct reuse of Postgres depth; testable against a docker-compose Postgres fixture |
| `tokencost` | Go/Python CLI that counts tokens and estimates $ cost across OpenAI/Anthropic/Google given a prompt file | Pure-function core, deterministic test vectors, no live API needed for tests |
| `promptdiff` | CLI that diffs prompt/response pairs across model or prompt versions, like `git diff` for prompts | Useful for regression-testing prompt changes; tests are fixture-pair comparisons |
| `redis-llm-cache` | Redis-backed exact + semantic cache middleware for LLM provider calls (Go library) | Leans on Redis expertise; integration-testable with a Redis container |
| `mcp-k8s-readonly` | Read-only MCP server for Kubernetes introspection (pods/logs/events) for agent-assisted debugging | Leans on K8s/DevOps depth; read-only scope keeps it safe and easy to test (kind/k3d cluster in CI) |

### Tier 2 — Medium (1–3 weeks; integration tests, multi-component, docker-compose)

| Idea | One-liner | Why it fits |
|------|-----------|-------------|
| `agentops-lite` | Self-hosted, OpenTelemetry-compatible LLM/agent tracing service (Go API + Postgres + minimal Vue dashboard) | Mini self-hosted alternative to Langfuse/Helicone; full-stack but bounded scope |
| `evalkit` | CI-friendly eval harness: YAML test cases run against any OpenAI-compatible endpoint, rule-based + LLM-judge assertions, JUnit output | Marries CI/CD background with AI evals; deterministic test cases double as its own test suite |
| `ragctl` | "Terraform for RAG" — declarative CLI managing chunking config, embeddings, and pgvector/Qdrant indexes with plan/apply/destroy semantics | Directly ports IaC mental model to RAG infra; testable plan/apply against a local vector store |
| `mcp-gateway` | Go reverse proxy in front of multiple MCP servers: auth, rate limiting, audit logging, tool allow-listing | DevOps-flavored agent infra; ships with Docker Compose + Helm chart |
| `agent-sandbox-runner` | Dockerized service that safely executes untrusted LLM-agent-generated code (seccomp/gVisor-style isolation) behind an HTTP API | Leverages security/DevOps depth; testable via a battery of escape-attempt fixtures |

### Tier 3 — Flagship bets (months; e2e + load/security testing; sustained iteration)

| Idea | One-liner | Why it fits |
|------|-----------|-------------|
| `vaibe-agent-runtime` | Durable workflow engine purpose-built for long-running LLM agents (tool calls, retries, human-in-the-loop checkpoints), Postgres+Redis backed, MCP-exposed | "Temporal, but for agents" — the clearest case of backend depth + ai-native trend; needs durability/chaos testing |
| `llm-finops-platform` | Multi-tenant LLM spend tracking/forecasting platform (Go API, Vue dashboard, Postgres/Redis, Helm/Terraform deploy) with per-feature cost attribution and budget alerts | Productizes DevOps/FinOps instincts for AI-spending orgs; needs multi-tenant + load testing |
| `selfhosted-rag-stack` | One-click Terraform + Helm reference architecture: ingestion, pgvector/Qdrant, reranker, eval loop, observability, wired together | A complete "AI platform engineering" reference implementation; demands integration + perf testing across the whole stack |
| `mcp-server-registry` | Public registry + security scanner for community MCP servers (static analysis for prompt-injection/tool-abuse risk), with ratings | Community-facing, highest reach but also highest scope/security-testing bar |

## Next step

Pick one Tier 1 and (optionally) one Tier 2 idea per review cycle, run them
through `sys.project.specify` (new repo) or fold the smaller ones into an
existing repo via `sys.task.specify`, and update
[profile.md](../spec/profile.md)'s Open-source projects table once something
ships.
