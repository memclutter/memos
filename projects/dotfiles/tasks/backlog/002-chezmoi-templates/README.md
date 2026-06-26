# 002 — chezmoi templates

**Goal:** move personal and host-specific values out of literal config files into
chezmoi templates, and document how templating works so future configs follow
the same convention.

**Scope:**
- Convert `dot_gitconfig` to a template (`dot_gitconfig.tmpl`) so the `[user]`
  identity (name, email) comes from chezmoi data, not hardcoded literals.
- Establish where template variables live (chezmoi data / config) and the
  convention for adding a new templated value.
- Document the workflow — how to add, fill, and apply a templated value, and the
  rule for secrets vs. plain literals.

**Acceptance:**
- `chezmoi apply` still produces a correct `~/.gitconfig` with the owner's
  identity, now sourced from template data.
- A documented, repeatable way exists to add a new templated/host-specific value.
- Secrets are never committed in plain text.
- A `spec/templates.md` capability describes the convention; `spec/configs.md`
  reflects that the Git config is templated.
