# configs

## Purpose

The configuration files the repository manages, and how they reach `$HOME`. This
is the whole product today: a small, curated set of dev-environment configs
applied via chezmoi.

## Behaviour

### Deployment

Files are stored at the repo root with chezmoi source-state names and applied to
the home directory with `chezmoi apply`:

- `dot_gitconfig` → `~/.gitconfig`
- `dot_vimrc` → `~/.vimrc`
- `dot_zshrc` → `~/.zshrc`

There is no install script; chezmoi is the only mechanism. The one external
dependency, Oh My Zsh, is declared in `.chezmoiexternal.toml` and cloned by
chezmoi to `~/.oh-my-zsh` on first apply (no refresh period — the framework
self-updates).

### Git config (`dot_gitconfig`)

- `[user]` — owner identity: `name = Memory Clutter`, `email = memclutter@gmail.com`,
  and `signingkey` (the public GPG key id used to sign commits — not a secret).
- `[init] defaultBranch = main` — new repositories start on `main`.
- `[push] default = simple` — push only the current branch to its upstream.
- `[core] autocrlf = input` — normalise CRLF to LF on commit, leave checkout as-is.
- `[alias]` — short aliases for everyday commands, e.g. `st` (status), `co`
  (checkout), `cb` (checkout -b), `cm` (commit -m), `df` (diff --color=auto),
  `ph` (push), `pl` (pull), `pr` (pull --rebase), `aa` (add .), `bd` (branch -D).

### Vim config (`dot_vimrc`)

- `tabstop=4`, `shiftwidth=4`, `expandtab` — 4-space soft tabs for indentation.

### Zsh config (`dot_zshrc`)

- Oh My Zsh framework (cloned via the `.chezmoiexternal.toml` external above),
  theme `robbyrussell`, plugin set `(git)`, auto-update left enabled.
- Docker Compose aliases — `dc`, `dcps`, `dcl`, `dclf`, `dce`, `dcd`, `dcu`,
  `dcud`, `dcdvro`, `dcrun`.
- Tool PATH/env blocks for Go, NVM, PostgreSQL, Android SDK, Yandex Cloud,
  opencode, and LM Studio. Each is `$HOME`-relative and guarded by an existence
  check, so a machine missing a tool still loads the shell cleanly. The blocks
  keep the owner's actual install paths (e.g. `$HOME/go1.24`,
  `$HOME/Projects/vendors/nvm`), so the config is portable across the owner's
  machines without losing tools from `PATH`.

## Success criteria

- `chezmoi apply` materialises `~/.gitconfig`, `~/.vimrc`, and `~/.zshrc` with
  exactly the settings above, and clones Oh My Zsh to `~/.oh-my-zsh`.
- The Git aliases resolve (e.g. `git st` runs `git status`).
- Vim indents with 4 spaces and inserts spaces instead of tab characters.
- A fresh interactive zsh session sources `~/.zshrc` without errors or warnings,
  and `dc` resolves to `docker compose`.
