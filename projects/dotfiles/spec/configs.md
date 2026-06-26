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

There is no install script; chezmoi is the only mechanism.

### Git config (`dot_gitconfig`)

- `[user]` — owner identity: `name = Memory Clutter`, `email = memclutter@gmail.com`.
- `[push] default = simple` — push only the current branch to its upstream.
- `[core] autocrlf = input` — normalise CRLF to LF on commit, leave checkout as-is.
- `[alias]` — short aliases for everyday commands, e.g. `st` (status), `co`
  (checkout), `cb` (checkout -b), `cm` (commit -m), `df` (diff --color=auto),
  `ph` (push), `pl` (pull), `pr` (pull --rebase), `aa` (add .), `bd` (branch -D).

### Vim config (`dot_vimrc`)

- `tabstop=4`, `shiftwidth=4`, `expandtab` — 4-space soft tabs for indentation.

## Success criteria

- `chezmoi apply` materialises `~/.gitconfig` and `~/.vimrc` with exactly the
  settings above.
- The Git aliases resolve (e.g. `git st` runs `git status`).
- Vim indents with 4 spaces and inserts spaces instead of tab characters.
