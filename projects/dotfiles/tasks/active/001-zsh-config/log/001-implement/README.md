# 001 — implement zsh config

Breakdown steps 1–3 implemented in `vcs/dotfiles/`; step 4 verified
non-destructively. Steps 5 (commit/push + submodule bump) and the spec fold
(Finish) follow.

## Done

- **Oh My Zsh external** — added `.chezmoiexternal.toml` declaring `~/.oh-my-zsh`
  as a `type = "git-repo"` external (`ohmyzsh.git`, no `refreshPeriod`: chezmoi
  clones once, the framework self-updates).
- **`dot_zshrc`** — new chezmoi source file → `~/.zshrc`. Portable core: base
  PATH, Oh My Zsh scaffold (`ZSH`, `ZSH_THEME="robbyrussell"`, `plugins=(git)`,
  `source $ZSH/oh-my-zsh.sh`, auto-update left enabled), Docker Compose aliases.
  Default OMZ comment boilerplate dropped.
- **Guarded tool PATHs** — Go, NVM, PostgreSQL, Android SDK, Yandex Cloud,
  opencode, LM Studio. Each wrapped in an existence guard and `$HOME`-relative,
  preserving the **actual install paths** from the old `~/.zshrc`
  (`$HOME/go1.24`, `$HOME/Projects/vendors/nvm`, …) — no tidying to defaults, so
  existing machines keep their tools on `PATH`.

## Verified

- `chezmoi -S <submodule> diff` → `~/.zshrc` replaced by the clean version, all
  tool blocks preserved with real paths.
- Isolated interactive load (`ZDOTDIR=/tmp/zt zsh -i`, real `~/.oh-my-zsh`, live
  `~/.zshrc` untouched) → no stderr output; `$ZSH`, `ZSH_THEME`, and
  `alias dc → docker compose` all correct.
- `grep memclutter dot_zshrc .chezmoiexternal.toml` → empty (no personal
  literals).

## Note

`chezmoi diff` also surfaced an unrelated discrepancy: the live `~/.gitconfig`
carries `signingkey` and `[init] defaultBranch = main` that are absent from the
repo's `dot_gitconfig`, so a full `chezmoi apply` would drop them. Out of scope
here; the zsh migration should be applied scoped (`chezmoi apply ~/.zshrc`). The
owner handles the backup before applying on each machine.
