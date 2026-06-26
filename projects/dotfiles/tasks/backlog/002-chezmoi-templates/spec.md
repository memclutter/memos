# Spec — 002-chezmoi-templates

## Problem

Personal values are committed as plain literals: `dot_gitconfig` hardcodes the
owner's name and email. Today that is merely not portable — anyone forking the
repo inherits the owner's identity — but the same pattern would leak genuine
secrets (tokens, machine-specific paths) into version control the moment they
appear. The project's boundaries already say host-specific and secret values
should go through chezmoi templates; that mechanism does not exist yet, and there
is no documented way to add one.

## Goal

Adopt chezmoi templating: source personal and host-specific values from chezmoi
data instead of literals, starting with the Git identity, and document the
convention so every future config follows it safely.

## User journeys

- **Apply on a new machine:** the owner runs `chezmoi init` + `chezmoi apply`;
  chezmoi prompts for / reads the identity data and renders `~/.gitconfig` with
  the right name and email — no literal identity stored in the repo.
- **Add a host-specific value:** the owner follows the documented steps — declare
  the variable in chezmoi data, reference it in a `.tmpl` source file, run
  `chezmoi apply` — and the value is filled per machine without editing the repo.
- **Avoid leaking a secret:** when a config would need a token, the docs point the
  owner to the templating/secret path instead of committing it in plain text.

## Success criteria

- `dot_gitconfig` is replaced by `dot_gitconfig.tmpl`; the `[user]` name and email
  come from chezmoi template data, and `chezmoi apply` reproduces the same
  `~/.gitconfig` as before.
- The repo contains no committed personal identity literal for the Git user.
- A documented, repeatable procedure exists for adding a new templated /
  host-specific value, including where the variables are defined.
- Secrets are never committed in plain text; the docs state how to handle them.

## Affected spec sections

- spec/templates.md — NEW: the chezmoi templating capability — the `.tmpl`
  convention, where template variables/data live, the add/fill/apply workflow,
  and the secrets-vs-literals rule.
- spec/configs.md — modify: Git config is now `dot_gitconfig.tmpl`; the `[user]`
  identity is described as template-sourced rather than literal; Deployment list
  updated.
- spec/overview.md — modify: add the templates capability to the Capabilities
  index; tighten the boundary so "host-specific or secret values" points at the
  now-existing templating mechanism.

## Target state

After this task ships, `spec/templates.md` documents templating as a first-class
capability: source files ending in `.tmpl` are rendered by chezmoi, template
variables come from chezmoi's config/data, and there is a step-by-step way to add
a new templated value plus an explicit rule that secrets go through templates/
secret storage and never into committed literals. `spec/configs.md` shows the Git
config as `dot_gitconfig.tmpl` with a template-sourced `[user]` identity, while
the aliases and other static settings remain as-is. `spec/overview.md` lists the
templates capability and its boundary references the implemented mechanism.

## Out of scope

- Templating the Vim config or any config without personal/host-specific values
  (no benefit yet).
- Integrating an external secret manager — the rule and a simple chezmoi-native
  approach are enough for now; a full secrets backend is a later task if needed.
- The zsh config (task 001), though it must adopt this convention if/when it
  carries host-specific values.

## Boundaries

- ✅ Always: source personal/host-specific values from chezmoi data; keep the
  templating convention documented and consistent.
- ⚠️ Ask first: introducing an external secret-manager dependency; templating
  beyond the values that actually need it.
- 🚫 Never: commit secrets or personal identity literals in plain text; change the
  effective applied output of `~/.gitconfig` for the owner. Reference the global
  rules ([git.md](../../../../rules/git.md), [data.md](../../../../rules/data.md)).
