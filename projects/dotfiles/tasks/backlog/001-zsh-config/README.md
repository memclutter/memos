# 001 — zsh config

**Goal:** bring the zsh shell under dotfiles, so a fresh machine gets the owner's
zsh setup with a single `chezmoi apply`.

**Scope:** add a chezmoi-managed `~/.zshrc` (and any supporting files it needs)
that provides a working, machine-portable interactive shell baseline. Keep it
minimal — just enough to be the owner's daily shell. Framework/plugin choices
are left to the Plan phase.

**Acceptance:**
- `chezmoi apply` materialises `~/.zshrc`.
- A new login/interactive zsh session loads it with no errors.
- The config is portable (no host-specific literals committed).
- `spec/configs.md` lists zsh among the managed configs.
