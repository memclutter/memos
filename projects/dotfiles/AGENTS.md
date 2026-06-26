---
name: dotfiles
vcs:
  - git@github.com:memclutter/dotfiles.git
self: false
status: active
stack: [chezmoi]
created: 2026-06-26
---

Personal dotfiles managed with [chezmoi](https://chezmoi.io). This project is a
**deliberate deviation** from the base stack ([rules/stack.md](../../rules/stack.md)):
it ships no application code — only configuration files for the development
environment, plus the chezmoi source-state convention that maps them to `$HOME`.

## Architecture

- Source files live at the repo root using chezmoi's source-state naming:
  `dot_<name>` materialises as `~/.<name>` on `chezmoi apply`
  (`dot_gitconfig` → `~/.gitconfig`, `dot_vimrc` → `~/.vimrc`).
- There is no install script or build step; chezmoi is the single deployment
  mechanism. Adding a tool's config means adding the matching `dot_*` source file.

## Conventions

- Keep configs minimal and portable across machines; avoid host-specific values
  unless gated by chezmoi templates.
- The `[user]` identity in `dot_gitconfig` is the owner's
  (`memclutter@gmail.com`, `Memory Clutter`).
- Source changes are committed and pushed inside `vcs/dotfiles/`, then this OS
  pins the new submodule commit (`chore(submodule): bump dotfiles`).
