# Spec — 001-zsh-config

## Problem

The dotfiles repo manages Git and Vim, but not the shell. zsh is the owner's
interactive shell, yet its configuration is not version-controlled — a fresh
machine has no consistent zsh setup, and shell tweaks live only on whatever
machine they were made. The project's vision is to grow into the broader
shell/dev environment; the shell itself is the most natural next step.

## Goal

Bring zsh under dotfiles so `chezmoi apply` sets up the owner's interactive shell
on any machine, consistent with how Git and Vim are already managed.

## User journeys

- **Fresh machine:** the owner clones/initialises the dotfiles, runs `chezmoi
  apply`, opens a new terminal, and lands in a configured zsh — no manual editing
  of `~/.zshrc`.
- **Tweak the shell:** the owner edits the zsh source file in the repo, runs
  `chezmoi apply`, and the change takes effect; committing it propagates to every
  machine on the next apply.

## Success criteria

- `chezmoi apply` materialises `~/.zshrc` (plus any supporting source files the
  config needs).
- A new interactive/login zsh session sources the config without errors or
  warnings.
- The config is machine-portable: no host-specific or personal literals are
  committed (such values, if needed, follow the templating approach from task
  002).
- `spec/configs.md` lists zsh among the managed configs, with its target path.

## Affected spec sections

- spec/configs.md — modify: add a "Zsh config (`dot_zshrc`)" subsection under
  Behaviour and `dot_zshrc → ~/.zshrc` to the Deployment list; extend Success
  criteria to cover zsh.
- spec/overview.md — modify: zsh moves from a vision aspiration to a shipped
  capability (adjust the vision wording so it no longer lists zsh as "to grow
  into").

## Target state

After this task ships, `spec/configs.md` describes zsh as a managed config
alongside Git and Vim: `dot_zshrc` deploys to `~/.zshrc` via `chezmoi apply`, a
Behaviour subsection summarises what the config sets up (the concrete settings
are filled in from the implementation), and the Success criteria assert that a
fresh interactive zsh session loads cleanly. `spec/overview.md` vision reflects
that the shell is now covered, with remaining growth (tmux, bootstrap/install
flow) still listed as intent.

## Out of scope

- Choosing/installing a zsh framework or plugin manager (oh-my-zsh, zinit, …) —
  that is a Plan decision; this task only requires a working baseline.
- tmux, prompt theming engines, or an install/bootstrap script.
- Migrating personal values to templates — that is task 002.

## Boundaries

- ✅ Always: deliver zsh as a chezmoi source-state file; keep it minimal and
  portable; verify with a real `chezmoi apply` + fresh shell.
- ⚠️ Ask first: pulling in a heavyweight framework or many plugins; any
  host-specific value (route it through templating, task 002).
- 🚫 Never: commit secrets or personal literals in plain text; break a fresh
  shell's startup. Reference the global rules ([git.md](../../../../rules/git.md)).
