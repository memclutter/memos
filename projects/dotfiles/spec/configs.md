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
- `dot_gitconfig_github` → `~/.gitconfig_github`
- `dot_vimrc` → `~/.vimrc`
- `dot_zshrc` → `~/.zshrc`

There is no install script; chezmoi is the only mechanism. The one external
dependency, Oh My Zsh, is declared in `.chezmoiexternal.toml` and cloned by
chezmoi to `~/.oh-my-zsh` on first apply (no refresh period — the framework
self-updates).

The repo root also holds repository metadata (`README.md`, `LICENSE`) for
GitHub. These are excluded from deployment via `.chezmoiignore`, so `chezmoi
apply` keeps them in the repo but never places them in `$HOME`.

### Git config (`dot_gitconfig`)

- `[user]` — owner identity: `name = Memory Clutter`, `email = memclutter@gmail.com`.
  The signing key lives in `dot_gitconfig_github` (below), not here.
- `[init] defaultBranch = main` — new repositories start on `main`.
- `[push] default = simple` — push only the current branch to its upstream.
- `[core] autocrlf = input` — normalise CRLF to LF on commit, leave checkout as-is.
- `[alias]` — short aliases for everyday commands, e.g. `st` (status), `co`
  (checkout), `cb` (checkout -b), `cm` (commit -m), `df` (diff --color=auto),
  `ph` (push), `pl` (pull), `pr` (pull --rebase), `aa` (add .), `bd` (branch -D).
- `[includeIf "hasconfig:remote.*.url:…"]` — three conditional includes that pull
  in `~/.gitconfig_github` only when a repo's remote is on github.com (SSH
  `git@github.com:*/**`, HTTPS `https://github.com/**`, and `ssh://` forms). The
  SSH pattern uses `:*/**` because git's wildmatch `**` does not span the `/`
  after the colon.

### GitHub signing config (`dot_gitconfig_github`)

Included by `dot_gitconfig` only for github.com remotes, so commit signing is
scoped to GitHub and other repos can stay unsigned or use a different key:

- `[user] signingkey` — the public GPG key id used to sign (not a secret).
- `[commit] gpgsign = true` and `[tag] gpgSign = true` — sign commits and tags
  automatically in any repo with a github.com remote.

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

- `chezmoi apply` materialises `~/.gitconfig`, `~/.gitconfig_github`, `~/.vimrc`,
  and `~/.zshrc` with exactly the settings above, and clones Oh My Zsh to
  `~/.oh-my-zsh`.
- The Git aliases resolve (e.g. `git st` runs `git status`).
- In a repo with a github.com remote, `git config commit.gpgsign` is `true` and
  `user.signingkey` is set; in a repo with a non-github remote, both are unset.
- Vim indents with 4 spaces and inserts spaces instead of tab characters.
- A fresh interactive zsh session sources `~/.zshrc` without errors or warnings,
  and `dc` resolves to `docker compose`.
- `chezmoi apply` never materialises `~/README.md` or `~/LICENSE`; repository
  metadata stays in the repo only (`chezmoi managed` does not list them).
