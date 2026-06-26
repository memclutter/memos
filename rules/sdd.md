# Spec-Driven Development (SDD)

How we take a task from a rough idea to validated code: a **gated, four-phase**
process where the spec — not the chat history — is the ground truth. You stay
the final quality filter; the agent works against a written spec and verifies
itself against it.

> Don't wait until the end to see if the agent met the spec. Validate at every
> gate.

## Two levels: project spec and task spec

SDD runs at **two altitudes**. A project is itself one living spec; each task is
a *delta* against it. Three layers, from most stable to most volatile:

| Layer | Where | Describes | Changes |
|-------|-------|-----------|---------|
| **Constitution** | `projects/<name>/AGENTS.md` | principles, stack, boundaries, invariants | rarely |
| **Living product spec** | `projects/<name>/spec/` | *what the product does now* — the integral of all shipped tasks | on every finished task |
| **Task delta spec** | `tasks/.../spec.md` | *what one task changes* in the living spec | within a task |

- The **living product spec** (`spec/`) is the single source of truth for the
  product's current behaviour: `overview.md` (vision + product-wide success
  criteria) plus one file per capability/domain. Conceptually one document,
  physically split so it scales. See [projects.md](projects.md).
- A **task delta spec** never re-describes the whole product. It names the
  `spec/` sections it touches and the target state they must reach. See
  [tasks.md](tasks.md).
- **Merge-on-done.** `spec/` reflects **only shipped reality**. A task's delta is
  folded into `spec/` at the Finish gate, not before. While a task is `active`,
  `spec/` legitimately lags behind it — that is honest and keeps the product spec
  drift-free.

The four phases below are the **task-level** loop. Bootstrapping or amending the
living product spec is the `sys.project.specify` skill.

## The four phases

Each phase produces a written artifact and is a **checkpoint** — you don't move
on until the current one is validated. The phases map onto a task folder
(`projects/<name>/tasks/.../{NNN}-{slug}/`, see [tasks.md](tasks.md)):

| Phase         | What happens                                                        | Artifact                | Skill                |
|---------------|--------------------------------------------------------------------|-------------------------|----------------------|
| **Specify**   | Owner gives the vision; agent expands it into a detailed spec.      | `spec.md`               | `sys.task.specify`   |
| **Plan**      | Owner gives stack/architecture/constraints; agent writes the plan. | `plan.md`               | `sys.task.plan`      |
| **Tasks**     | Agent slices spec + plan into small, reviewable chunks.             | checklist in `AGENTS.md`| `sys.task.breakdown` |
| **Implement** | Agent works the chunks one at a time; you validate each.           | `log/{NNN}-.../`        | —                    |

- **Specify** describes *what* and *why*: user journeys and success criteria, as
  a **delta** against the living product spec (which `spec/` sections change and
  their target state). No implementation details.
- **Plan** describes *how*: technical decisions, stack, architecture, trade-offs,
  constraints.
- **Tasks** turns the plan into a checklist of small steps. Don't mix unrelated
  concerns in one step (e.g. auth and schema changes).
- **Implement** does the work in the project's `repo/`, one chunk at a time, each
  iteration recorded in a `log/` folder.
- **Finish** (the closing gate, after Implement) folds the task's delta into the
  living product spec: apply the `Target state` to `spec/`, verify `repo/` matches
  it, then close the task. Done by `sys.task.finish`.

## A good spec: six areas

A spec earns its keep by being concrete. Cover these areas — but **reference the
global rules instead of repeating them**; write only the project- or
task-specific delta:

- **Commands** — exact, runnable commands with flags (`pytest -v`, `go test ./...`).
- **Testing** — framework, where tests live, coverage expectations ([go.md](go.md), [python.md](python.md), [vue.md](vue.md)).
- **Project structure** — explicit paths.
- **Code style** — real examples over prose.
- **Git workflow** — branch, commit, PR conventions ([git.md](git.md)).
- **Boundaries** — what the agent must not touch (see below).

Prefer concrete examples to descriptions, and a short table of contents /
summary for long specs over dumping everything into one context.

## Boundaries: three tiers

State the limits explicitly in the spec or the project's `AGENTS.md`. Globals
already cover the common cases ([git.md](git.md), [data.md](data.md)) — record
only the project-specific delta:

- ✅ **Always** — safe, routine actions (e.g. run tests before committing).
- ⚠️ **Ask first** — high-impact changes (e.g. modifying a database schema).
- 🚫 **Never** — hard stops (e.g. commit secrets or API keys).

## Working with the agent

- **Spec is ground truth.** Lose the conversation, keep the spec. Keep it in
  version control; update it when requirements clarify.
- **Plan first.** Use a read-only / plan mode to refine the spec with the agent
  before it writes code.
- **One focused task at a time.** Feed chunks, not the whole world; use
  subagents for distinct domains (backend, frontend, testing) when it helps.
- **Self-verify.** After implementing, the agent compares the result against the
  spec and confirms every requirement is met; run tests at each milestone and
  feed failures back into the spec or the next chunk.
- **You remain the quality filter.** The agent drafts; you accept.

## When to use which phase

Small, obvious tasks can collapse phases — a one-line fix needs no `plan.md`. The
discipline scales with risk: the larger or more ambiguous the change, the more
each gate earns its place. This is engineering, not vibe coding.

---

Adapted from Addy Osmani, ["How to write a good spec for AI agents"](https://addyosmani.com/blog/good-spec/)
(addyosmani.com, 2026) — © 2026 Addy Osmani. The four-phase model
(Specify → Plan → Tasks → Implement) follows GitHub's open-source
[Spec Kit](https://github.com/github/spec-kit).
