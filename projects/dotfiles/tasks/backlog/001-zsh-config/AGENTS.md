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

## Tasks breakdown

All source changes happen inside `vcs/dotfiles/`; this OS repo only pins the
bumped submodule commit.

- [ ] 1. Add `.chezmoiexternal.toml` at the repo root declaring Oh My Zsh as a
  `type = "git-repo"` external (`url = ohmyzsh.git`, no `refreshPeriod` — clone
  only; OMZ self-updates). → fresh-machine journey.
- [ ] 2. Add `dot_zshrc` portable core: base PATH (`$HOME/bin`,
  `$HOME/.local/bin`, `/usr/local/bin`), Oh My Zsh scaffold (`ZSH`,
  `ZSH_THEME="robbyrussell"`, `plugins=(git)`, `source $ZSH/oh-my-zsh.sh`, OMZ
  auto-update left enabled), and the Docker Compose aliases verbatim. Drop the
  default OMZ comment boilerplate. → clean-load + aliases criteria.
- [ ] 3. Append the guarded tool PATH blocks to `dot_zshrc` (Go, NVM, PostgreSQL,
  Android SDK, Yandex Cloud, opencode, LM Studio): wrap each in an existence
  guard and use `$HOME` — **preserving the actual install paths** from the
  current `~/.zshrc` (e.g. `$HOME/go1.24`, `$HOME/Projects/vendors/nvm`), no
  tidying to defaults. → portability criterion + migration safety.
- [ ] 4. Verify: `chezmoi diff` then `chezmoi apply`; confirm `~/.oh-my-zsh`
  present and `~/.zshrc` rendered; `zsh -i -c exit` loads with no errors/warnings;
  `alias dc` → `docker compose`; `grep -R memclutter dot_zshrc
  .chezmoiexternal.toml` is empty; guarded paths skip cleanly when a tool dir is
  absent.  ⚠️ run the real `chezmoi apply` on the owner's machine — confirm first.
- [ ] 5. Commit & push inside `vcs/dotfiles/`, then bump the submodule pin in
  this OS repo (`chore(submodule): bump dotfiles`).

The `spec/configs.md` + `spec/overview.md` updates are folded by the Finish gate
(`sys.task.finish`), not a separate implementation step.
