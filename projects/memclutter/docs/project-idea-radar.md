# Project idea radar — 50 ideas by relevance tier

## Why this exists

[`ideas.md`](ideas.md) organizes the backlog by **direction** (AI-workflow, Games,
DevOps tools, ...) with an effort tier inside each. This document slices the
same kind of brainstorm along a different, complementary axis: **how close an
idea sits to the existing skillset**, cross-referenced against live 2026
community trend signals. Use it as a wide radar sweep; promote anything that
survives contact with `ideas.md`'s own filter (§1.4) into a real task via
`sys.task.specify`.

## Method and sources

Each idea was scored against the current GitHub profile — repos `confparse`,
`gorequests` / `gorequests-proxy` / `gorequests-retry`, `nocodb-migrator`,
`proxycheck`, `dotfiles`, and the core stack (Go, Python, PostgreSQL, Redis,
Docker, Kubernetes, Vue.js) — and against a trend-signal scan across:

- GitHub trending scans for self-hosted Go DevOps tools (Gantry, Mortise,
  usulnet, Pipewright).
- The [Vela Partners "19 Open-Source AI Infrastructure Trends 2026"](https://vela.partners/blog/emerging-open-source-ai-infrastructure-trends-2026)
  report (star counts and 90-day growth cited below come from there).
- The MCP project's own 2026 roadmap (enterprise-readiness gaps, gateway/proxy
  patterns).
- Live, still-open GitHub issues/discussions on `n8n-io/n8n` and
  `immich-app/immich`.

## Tiers

- **Tier 1 — relevant to existing experience, riding a live trend.** Directly
  extends a shipped repo or the Go/DevOps/SRE/Postgres/Kubernetes core
  skillset, and rides a currently-trending community topic (MCP servers,
  self-hosted single-binary DevOps tools, AI gateways, proxy/anti-censorship
  tooling).
- **Tier 2 — half known, half new, riding a live trend.** Roughly half the
  work sits on known ground (Go backend, Postgres, Vue, Kubernetes, DevOps
  packaging); the other half deliberately picks up a new skill (Rust, WASM,
  vector search, speech models, smart-contract basics) inside a trending
  space.
- **Tier 3 — pure experiment, no relevance filter.** Robotics, hardware,
  creative coding, RF/DSP, PL theory, and on-chain toys — chosen for breadth
  and fun, explicitly exempt from the pain-validation and stack-relevance
  filters used for the other two tiers.

## Tier 1 — familiar + trending (18)

| Idea | One-liner | Trend signal | Relevance anchor |
|------|-----------|---------------|-------------------|
| `n8n-promote` | CLI that safely promotes n8n workflows and credentials dev→staging→prod, stripping the webhook/publish-history refs that break n8n's own import. | `n8n-io/n8n` issues #24367 / #21210 / #26814 still open in 2026 — recurring foreign-key import failures. | Same versioned-migration shape as `nocodb-migrator`. |
| `immich-vault` | Consistent, incremental, off-site (S3/B2) backup and restore CLI for Immich — DB and asset filesystem kept in sync. | Immich maintainers explicitly declined to build this (discussion #27504) — an open invitation. | CLI pattern from `nocodb-migrator`; Postgres backup expertise. |
| `mcp-proxycheck` | MCP server exposing `proxycheck`'s health/protocol checks as agent tools, so any AI agent can vet or rotate its own outbound proxies. | MCP servers (307K★, +19.7K/90d) crossed with cross-platform proxy tooling (411K★, +24.7K/90d). | Direct wrapper around the existing `proxycheck` repo. |
| `aigateway-lite` | Single Go binary LLM API gateway: load-balances, retries, and logs calls across OpenAI, Anthropic, and local providers. | "Centralized AI gateway" is the #1 recommended enterprise AI-security control in 2026 analyst reports. | Built directly on `gorequests` + `gorequests-retry`. |
| `oncall-copilot` | Slack slash-command that pulls Kubernetes logs, events, and metrics for a namespace and window, returns a ranked root-cause summary. | SRE/on-call copilots are the most-cited "real" AI-workflow use case in 2026 DevOps write-ups. | Direct reuse of the SRE/Kubernetes background. |
| `kube-confparse` | Extends `confparse`'s struct-tag config model to also emit matching Kubernetes ConfigMap and Secret manifests. | GitOps-native config management is a headline feature in every trending 2026 self-hosted IDP (Gantry, Mortise). | Direct extension of the `confparse` repo. |
| `proxy-judge-mesh` | A small distributed network of self-hosted proxy judges reporting into Postgres, corroborating `proxycheck` results from multiple vantage points. | Cross-platform proxy & anti-censorship is a top-4 2026 open-source infra trend (Vela Partners, +24.7K★/90d). | Extends `proxycheck`'s judge-based checking model. |
| `mcp-compose-bundles` | Curated, ready-to-deploy Docker Compose and Helm bundles for the most useful self-hostable MCP servers. | The official MCP registry explicitly defers packaging and curation to "downstream" projects. | Pure Docker/Helm packaging skill, no new protocol depth needed. |
| `ai-changelog-radar` | One feed aggregating breaking-change and deprecation announcements across OpenAI, Anthropic, and Google APIs. | Silent provider API breakage remains a recurring, unaddressed developer complaint into 2026. | Simple Go scraper/aggregator, same shape as existing CLI tools. |
| `egress-dlp-proxy` | Self-hosted forward proxy that inspects outbound LLM-API traffic for secrets and PII, blocking or logging before it leaves the network. | 43% of employees have pasted confidential data into an AI tool (Cyberhaven 2026); only 18% of orgs have a policy (Salesforce). | Pairs with `aigateway-lite`; Go proxy/middleware skill. |
| `k8s-cost-lens` | Self-hosted dashboard attributing Kubernetes cost and LLM API spend per namespace or team from existing metrics. | LLM cost/token observability is exploding — `honeybeepf-llm` and similar tools shipped through 2026. | Direct Kubernetes + Postgres background. |
| `agent-syscall-watch` | Lightweight Go tool (proc/ptrace-based) logging which files, commands, and network calls a terminal AI coding agent actually touches. | Terminal-based AI coding agents is the #2 2026 trend (561K★, +74.6K/90d); AgentSight proves the observability angle. | Go systems-tooling skill, a simpler entry point than full eBPF. |
| `postgres-mcp-migrator` | MCP server exposing safe, reviewable schema-migration and introspection tools for Postgres to AI agents. | MCP adoption is deepest in developer tooling, per MCP's own 2026 roadmap. | Migration-tool expertise from `nocodb-migrator` + Postgres background. |
| `redis-queue-board` | Self-hosted web dashboard for inspecting and retrying jobs across Redis-backed queues (Asynq, BullMQ, Sidekiq). | Single-binary self-hosted ops dashboards (Gantry, Mortise, usulnet) are the dominant 2026 Go-DevOps pattern. | Redis background + Vue.js frontend skill. |
| `gitops-drift-detector` | Go CLI/controller that continuously diffs live cluster state against Git-declared manifests and alerts on drift. | GitOps-native config is a named feature in every trending 2026 self-hosted platform (Gantry, Mortise). | Kubernetes background, same operator pattern space. |
| `vaibe-agent-evals` | CLI/service that scores AI-workflow agent outputs against golden datasets, for regression-testing prompts and pipelines. | n8n is absorbing Evaluations as a first-class 2026 feature — a sign the eval-tooling gap is real and current. | Directly serves vAIbe Studio's own AI products. |
| `inbox-triage-bot` | Self-hosted app that classifies a shared inbox or ticket queue and drafts (not auto-sends) replies for human approval. | Support/ops triage automation is a recurring 2026 AI-workflow ask, contested by Intercom Fin and Zendesk AI. | Backend/API integration skill; privacy-first self-hosted niche. |
| `proxy-leak-audit` | Deep anonymity scorer for proxies and VPNs: header leaks, DNS leaks, WebRTC leaks — beyond `proxycheck`'s protocol checks. | Anti-censorship/anonymity tooling keeps climbing (Vela Partners 2026 trend #4). | Direct extension of `proxycheck`'s anonymity-checking domain. |

## Tier 2 — stretch + trending (18)

| Idea | One-liner | Trend signal | Relevance anchor |
|------|-----------|---------------|-------------------|
| `llm-agent-arena` | Real-time spectator game where LLM-driven agents compete in a social-deduction format, with a public leaderboard. | Multi-agent orchestration & swarms is a top-5 2026 trend (359K★, +29.5K/90d); Pokémon-style benchmarks are saturated. | Go real-time backend is known; multi-agent harness design is new. |
| `rag-homelab` | Self-hosted semantic search / RAG over personal docs, logs, and homelab config using pgvector or Qdrant. | Local & on-device LLM inference is a top-3 2026 trend (502K★, +25.1K/90d). | Postgres/Go backend is known; embeddings and vector retrieval are new. |
| `mcp-router` | A smart reverse-proxy for MCP servers: auth, rate-limiting, and tool-namespacing across multiple upstream servers. | MCP's own 2026 roadmap flags gateway/proxy patterns as its top enterprise-readiness gap. | Go proxy skill is known; MCP protocol internals are new. |
| `tauri-nocodb-desktop` | Desktop GUI (Rust + Tauri backend, Vue frontend) wrapping `nocodb-migrator` for non-CLI users. | Lightweight native-feeling desktop apps (Tauri) are the default alternative to Electron bloat in 2026 tool releases. | Vue.js is known; Rust/Tauri packaging is new. |
| `voice-oncall-bot` | Adds hands-free voice interaction (STT/TTS) to `oncall-copilot` for hands-busy incident response. | AI voice cloning & speech is a top-6 2026 trend (328K★, +22.1K/90d). | SRE workflow is known; speech-model integration is new. |
| `wasm-plugin-runtime` | Lets users write `proxycheck`/`gorequests` protocol plugins in any language, compiled to WASM and loaded via wazero. | WASM sandboxing is the standard 2026 plugin-isolation pattern for edge AI runtimes and dev tools alike. | Go host runtime is known; WASM plugin ABI design is new. |
| `browser-agent-recorder` | Records a human's browser workflow and replays it as a reusable agent "skill" for browser-automation agents. | Browser automation (278K★) and agentic skills frameworks (305K★, +120K/90d) are both surging 2026 trends. | Backend orchestration is known; browser-agent tooling is new. |
| `terraform-provider-nocodb` | A proper Terraform/OpenTofu provider for NocoDB bases, schemas, and users — currently missing from the registry. | Registry-gap-hunting (per the Coolify-provider case study) surfaces NocoDB as still genuinely unfilled in 2026. | NocoDB domain expertise is known; Terraform provider SDK is new. |
| `agent-memory-store` | A persistent long-term memory API for AI agents: Postgres+Redis-backed, with embedding-ranked recall. | Persistent memory & context management is a top-11 2026 trend (220K★, +29.8K/90d). | Postgres/Redis is known; embedding-based memory ranking is new. |
| `doc2llm` | Self-hosted pipeline turning scanned PDFs and images into clean, LLM-ready markdown via OCR and layout models. | Document parsing & OCR for LLMs is a top-10 2026 trend (237K★, +11.4K/90d). | Python pipeline skill is known; vision/OCR models are new. |
| `agent-swarm-sim` | A visualizer and simulator for testing multi-agent coordination strategies before deploying them for real. | Multi-agent orchestration & swarms trend (#5, 359K★, +29.5K/90d). | Go backend/simulation is known; swarm-coordination theory is new. |
| `k8s-llm-scheduler` | A Kubernetes scheduler plugin that bin-packs local LLM inference (Ollama/vLLM) workloads onto GPU nodes more efficiently. | Local & on-device LLM inference (#3, 502K★) is pushing GPU-scheduling pain into ordinary clusters. | Kubernetes is known deeply; GPU-aware ML scheduling is new. |
| `edge-agent-kernel` | A small Rust AI-agent runtime for one concrete homelab device — e.g. a presence/automation agent on a Raspberry Pi. | Edge/IoT agent runtimes (oneclaw-style) are a fresh 2026 sub-trend inside local-LLM inference. | Homelab/systems design is known; Rust is a new language. |
| `x402-metered-api` | Adds machine-to-machine micropayment metering (x402 protocol) to an existing Go API so agents can pay per call. | x402 is the emerging 2026 standard for agent-to-agent payments, per ERC-8004/x402 infrastructure reports. | Go API design is known; the payment-rail protocol is new. |
| `notes-agent` | An AI-native note-taking app (Vue frontend) with agentic search, auto-tagging, and linking. | AI-native note-taking & knowledge bases is a top-12 2026 trend (200K★, +12.8K/90d). | Vue.js is known; deep agentic UX integration is new. |
| `anti-censorship-transport` | A pluggable-transport client (Snowflake/Tor-bridge style) for censorship circumvention, beyond simple proxy checking. | Cross-platform proxy & anti-censorship (#4, 411K★) is trending toward obfuscation, not just proxy lists. | Proxy-tooling domain is known; pluggable-transport protocols are new. |
| `speech-to-incident` | Real-time STT pipeline that transcribes on-call voice-bridge calls and feeds them into `oncall-copilot`. | AI voice/speech trend (#6, 328K★) meeting the on-call workflow. | SRE workflow is known; streaming speech models are new. |
| `gitea-mcp-actions` | An MCP server plus CI action exposing Gitea/Forgejo operations to AI agents, for self-hosted git users. | MCP adoption (307K★) is deepest in developer tooling; self-hosted git is underserved vs. GitHub's official server. | Git/CI/DevOps is known; MCP server authoring is new. |

## Tier 3 — pure experiment (14)

| Idea | One-liner | Trend signal | Relevance anchor |
|------|-----------|---------------|-------------------|
| `physical-mcp-trigger` | An ESP32 button/dial that acts as a tangible MCP client — pressing it fires a defined agent action. | Physical/embodied interfaces are an underexplored corner of the MCP ecosystem. | Zero backend overlap: embedded firmware + physical hardware. |
| `homelab-status-display` | An e-ink or LED desk display showing CI status, uptime, and LLM API spend. | Ambient physical dashboards are a popular 2026 Hackaday / r/esp32 project format. | Embedded hardware, not backend/DevOps. |
| `toy-os-kernel` | A from-scratch hobby OS kernel: bootloader, memory management, a minimal scheduler. | "Build your own OS" remains a classic mastery-signal moonshot (os.phil-opp.com, build-your-own-x). | Systems programming below any language/runtime shipped so far. |
| `robot-skill-ledger` | A toy network of $30 robots/Arduino rovers that publish and reuse learned "skills" via a shared ledger. | RoboNet-style robot-to-robot skill sharing is a fresh 2026 hackathon-born concept. | Robotics + light on-chain design — both entirely new. |
| `erc8004-agent-identity-demo` | A minimal demo of ERC-8004 verifiable agent identity plus x402 payments for a toy agent marketplace. | ERC-8004 + x402 is the emerging 2026 standard stack for autonomous agent economies. | Solidity and smart contracts — a fully new stack. |
| `onchain-dice-gamefi` | A tiny, provably-fair on-chain dice/card game — a deliberate crypto-stack stretch. | On-chain gaming discourse remains active in 2026 crypto-gaming communities. | Smart contracts + game rules, unrelated to backend/DevOps work. |
| `generative-art-plotter` | Algorithmic SVG art generation driven out to a physical pen plotter (Arduino/GRBL). | Creative-coding-to-physical-plotter is a steady favorite in generative-art and maker communities. | Creative coding + hardware control, no backend overlap. |
| `esolang-interpreter` | Design and implement a tiny esoteric programming language and its interpreter, for fun. | Esolang design is a long-running, low-stakes programming-language-theory tradition. | PL theory/interpreter design, unrelated to the day-to-day stack. |
| `sdr-signal-decoder` | Software-defined-radio decoder for weather-balloon and APRS signals using a cheap RTL-SDR dongle. | RTL-SDR hobby decoding is a perennial r/RTLSDR / Hackaday favorite. | RF/DSP — a completely new signal-processing domain. |
| `split-keyboard-firmware` | Custom QMK/ZMK firmware (and PCB) for a hand-wired split mechanical keyboard. | Custom keyboard firmware and builds are a durable maker / r/MechanicalKeyboards trend. | Embedded C + PCB design, unrelated to backend work. |
| `plant-care-bot` | Arduino + soil-moisture sensors + a tiny on-device vision model to detect plant health and auto-water. | Small on-device vision models on microcontrollers are a growing 2026 tinyML hobby trend. | Embedded hardware + tinyML, both new. |
| `selfplay-boardgame-rl` | A from-scratch reinforcement-learning agent (small neural net, self-play) for an underused board game — no LLM involved. | Self-play RL is enjoying renewed hobbyist interest as an LLM-agent counterpoint in 2026. | Classical ML/RL research, unrelated to backend/DevOps. |
| `drone-swarm-sim` | A simulated (or small real) multi-drone choreography controller exploring basic swarm control theory. | Embodied/physical AI operating systems (DimOS-style) are a hot 2026 GitHub trend. | Robotics/control theory, entirely new domain. |
| `synth-dsp-sequencer` | A hardware+software music synthesizer and step sequencer built from raw audio DSP. | DIY synth/Eurorack and audio-DSP hobby projects have a dedicated, active maker community. | Audio DSP + embedded hardware, unrelated to backend/DevOps. |

## Next step

This radar is a snapshot — trend signals and registry gaps age quickly (see
`ideas.md` §1.6's "promote, don't accumulate" rule). Before promoting any idea
here into a task, re-check its trend signal and, for Tier 1/2 ideas that touch
a specific external tool, re-confirm the gap is still open the way `ideas.md`
§1.2c requires.
