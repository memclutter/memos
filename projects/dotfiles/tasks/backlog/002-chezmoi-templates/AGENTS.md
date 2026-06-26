---
id: 002-chezmoi-templates
status: backlog
created: 2026-06-26
updated: 2026-06-26
---

Introduce chezmoi templating to the dotfiles repo so personal and host-specific
values are no longer committed as literals. Convert `dot_gitconfig` to
`dot_gitconfig.tmpl`, sourcing the `[user]` identity from chezmoi data; define
where template variables live and the convention for adding new ones; document
the add/fill/apply workflow and the secrets rule. Adds a new `spec/templates.md`
capability and updates `spec/configs.md`. Acceptance: `chezmoi apply` reproduces
the correct `~/.gitconfig` from template data, with a repeatable, documented way
to add further templated values and no secrets in plain text.
