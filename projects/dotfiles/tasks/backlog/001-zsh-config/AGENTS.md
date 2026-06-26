---
id: 001-zsh-config
status: backlog
created: 2026-06-26
updated: 2026-06-26
---

Add a chezmoi-managed zsh configuration to the dotfiles repo, delivered like the
existing configs (source-state `dot_zshrc` → `~/.zshrc`, applied with `chezmoi
apply`). Keep the baseline minimal and machine-portable; defer framework/plugin
and prompt decisions to `sys.task.plan`. Acceptance: `chezmoi apply` produces a
working `~/.zshrc` that loads without errors in a fresh interactive session, and
`spec/configs.md` records zsh as a managed config.
