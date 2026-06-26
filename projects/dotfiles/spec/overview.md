# dotfiles — Product spec

## Vision

A personal, version-controlled set of dotfiles that gives the owner a consistent
development environment on any machine with a single `chezmoi apply`. Today it
covers Git, Vim, and the zsh shell (with Oh My Zsh); the intent is to grow into
the broader dev environment (e.g. a multiplexer like tmux and a bootstrap/install
flow) so a fresh machine can be brought up to the owner's setup quickly. New
configs are added one tool at a time, each as a deliberate, reviewed addition.

## Capabilities

- [configs.md](configs.md) — the configuration files chezmoi manages and what
  each one sets up.

## Product-wide success criteria

- The repository can be applied with `chezmoi apply` to produce the expected
  files in `$HOME` without manual copying.
- Every managed file uses chezmoi's source-state naming (`dot_<name>`).
- Configs are portable: applying them on a fresh machine yields a working,
  host-independent setup.

## Boundaries

Beyond the global rules ([git.md](../../../rules/git.md)), the project deltas are:

- ✅ Always — manage every dotfile through chezmoi source-state naming; keep
  configs minimal and machine-portable.
- ⚠️ Ask first — adding host-specific or secret values (prefer chezmoi templates
  / secrets over committing literals); introducing an install/bootstrap script.
- 🚫 Never — commit secrets or credentials in plain text; add application code
  (this repo is configuration only, a documented deviation from
  [stack.md](../../../rules/stack.md)).
