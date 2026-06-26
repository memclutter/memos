# Plan — 001-zsh-config

## Approach

Bring the owner's existing `~/.zshrc` under chezmoi as `dot_zshrc`, cleaned up to
be machine-portable, and make the Oh My Zsh framework reproducible by declaring
it as a chezmoi external. A single `chezmoi apply` on a fresh machine then both
clones Oh My Zsh into `~/.oh-my-zsh` and writes `~/.zshrc`, so a new interactive
shell loads without errors.

The current `~/.zshrc` is split into three kinds of content:

1. **Portable core — keep verbatim (trimmed):** the Oh My Zsh scaffold
   (`ZSH`, `ZSH_THEME="robbyrussell"`, `plugins=(git)`, `source
   $ZSH/oh-my-zsh.sh`), the base PATH (`$HOME/bin:$HOME/.local/bin:/usr/local/bin`),
   and the Docker Compose aliases (`dc`, `dcps`, `dcl`, `dclf`, `dce`, `dcd`,
   `dcu`, `dcud`, `dcdvro`, `dcrun`). The large block of default Oh My Zsh
   comment boilerplate is dropped to keep the file readable.
2. **Tool PATH blocks — keep but guard:** Go, NVM, PostgreSQL, Android SDK,
   Yandex Cloud, opencode, LM Studio. Each is wrapped in an existence check and
   all `/home/memclutter/...` absolutes become `$HOME/...`, so a machine without
   that tool sources the config cleanly (success criterion: no errors/warnings).
3. **Oh My Zsh framework itself — chezmoi external:** declared in
   `.chezmoiexternal.toml`, cloned/refreshed by chezmoi rather than installed by
   hand.

This satisfies the spec's portability criterion (no host-specific or personal
literals committed) while keeping the owner's actual working setup intact.

## Stack

[chezmoi](https://chezmoi.io) only — consistent with the project's documented
deviation from the base stack ([stack.md](../../../../rules/stack.md)). New
chezmoi mechanism introduced by this task: **externals**
(`.chezmoiexternal.toml`, `git-repo` type) to vendor Oh My Zsh. No install
script, no build step — chezmoi remains the single deployment mechanism, as the
project `AGENTS.md` requires.

## Architecture

### Source files (added under `vcs/dotfiles/`)

- `dot_zshrc` → `~/.zshrc` (chezmoi source-state naming, like `dot_gitconfig` /
  `dot_vimrc`).
- `.chezmoiexternal.toml` → declares the Oh My Zsh external. Not materialised
  into `$HOME`; it is chezmoi configuration the repo root.

### `.chezmoiexternal.toml`

```toml
[".oh-my-zsh"]
    type = "git-repo"
    url = "https://github.com/ohmyzsh/ohmyzsh.git"
    refreshPeriod = "168h"
```

- `type = "git-repo"` clones the repo to `~/.oh-my-zsh` on first apply and
  pulls on later applies.
- `refreshPeriod = "168h"` (7 days) bounds how often chezmoi refetches, so apply
  stays fast.
- Because chezmoi owns Oh My Zsh updates, `dot_zshrc` **disables Oh My Zsh's own
  auto-update** with `zstyle ':omz:update' mode disabled` to avoid two updaters
  fighting.

### `dot_zshrc` shape

Ordered sections:

1. Base PATH (`$HOME/bin`, `$HOME/.local/bin`, `/usr/local/bin`).
2. Oh My Zsh scaffold: `export ZSH="$HOME/.oh-my-zsh"`,
   `ZSH_THEME="robbyrussell"`, `zstyle ':omz:update' mode disabled`,
   `plugins=(git)`, `source $ZSH/oh-my-zsh.sh`.
3. Docker Compose aliases (verbatim — already portable).
4. Guarded tool PATH blocks, each of the form:

   ```sh
   if [ -d "$HOME/.opencode/bin" ]; then
     export PATH="$HOME/.opencode/bin:$PATH"
   fi
   ```

   NVM keeps its `[ -s "$NVM_DIR/nvm.sh" ] && . ...` guard pattern but with a
   portable `NVM_DIR`. Go/PostgreSQL/Android/Yandex Cloud/opencode/LM Studio each
   get a directory/file guard and `$HOME`-relative paths.

### Data flow

`chezmoi apply` → (a) reads `.chezmoiexternal.toml`, clones/refreshes
`~/.oh-my-zsh`; (b) renders `dot_zshrc` to `~/.zshrc`. A new login/interactive
zsh sources `~/.zshrc`, which sources `$ZSH/oh-my-zsh.sh` (now present), then
applies aliases and guarded PATH additions.

### Spec updates (folded at Finish, per [sdd.md](../../../../rules/sdd.md))

- `spec/configs.md`: add `dot_zshrc → ~/.zshrc` to Deployment, a "Zsh config
  (`dot_zshrc`)" Behaviour subsection (Oh My Zsh via external, theme, git plugin,
  Docker aliases, guarded tool PATHs), and zsh success criteria. Document
  `.chezmoiexternal.toml` as the mechanism for the Oh My Zsh external.
- `spec/overview.md`: zsh moves from vision aspiration to shipped capability.

## Trade-offs & alternatives

- **Oh My Zsh embedding — chosen: chezmoi external (`git-repo`).** Declarative
  and reproducible; one `chezmoi apply` brings up a fresh machine, matching the
  spec's fresh-machine journey.
  - *Rejected: `run_once_` installer script* — runs upstream `install.sh`, but
    imperative and less reproducible; closer to a bootstrap script, which the
    project lists under "Ask first".
  - *Rejected: don't manage Oh My Zsh (guard the source line)* — minimal but
    breaks the fresh-machine journey (no framework until manual install).
- **Tool PATH blocks — chosen: keep with guards + `$HOME`.** Preserves the
  owner's real environment now without committing personal absolutes or breaking
  shells that lack a tool.
  - *Rejected: drop them from baseline* — cleaner file but loses working setup.
  - *Deferred: move literals to templates* — only needed if a value cannot be
    made portable with a guard; that belongs to task 002 (templating), out of
    scope here.
- **Custom plugins/themes:** none today — `~/.oh-my-zsh/custom` holds only the
  stock `example.*`, and `robbyrussell` + `git` are built into Oh My Zsh, so no
  extra externals are required.

## Constraints & risks

- **Portability (spec criterion):** no `/home/memclutter/...` or other personal
  literals may be committed; every machine-specific path is `$HOME`-relative and
  guarded. This is the main correctness bar for the cleanup.
- **Clean startup (spec criterion):** a fresh shell must source without errors or
  warnings even when Go/NVM/Android/etc. are absent — guards enforce this.
- **External availability:** `chezmoi apply` needs network + GitHub access on
  first run to clone Oh My Zsh; offline first-apply will leave `~/.oh-my-zsh`
  missing and the `source` line will warn. Acceptable (documented assumption:
  fresh-machine setup is online); the source line can stay guarded if we want to
  be strict.
- **Two updaters:** mitigated by disabling Oh My Zsh auto-update so chezmoi's
  `refreshPeriod` is the single update path.
- **Secrets:** none in the current `~/.zshrc`; keep it that way
  ([git.md](../../../../rules/git.md)).
- **No host-specific values requiring templates** are introduced; if one appears,
  stop and route it through task 002 (per spec Boundaries).

## Testing strategy

Prove the spec's success criteria with a real apply, not just inspection:

1. **Applies cleanly:** `chezmoi apply` (or `chezmoi apply --dry-run --verbose`
   first) materialises `~/.zshrc` and clones `~/.oh-my-zsh`. Confirm `~/.oh-my-zsh`
   exists and `~/.zshrc` matches `dot_zshrc`.
2. **Fresh shell loads without errors/warnings:** start a new interactive shell,
   e.g. `zsh -i -c 'exit'`, and check there is no error/warning output; confirm
   the `robbyrussell` prompt and `$ZSH` are set.
3. **Portability under missing tools:** temporarily run with a tool dir absent
   (or inspect the guards) to confirm no block errors when its target is missing
   — the guarded PATH additions simply skip.
4. **Aliases resolve:** `alias dc` reports `docker compose`, etc.
5. **No personal literals committed:** `grep -R "memclutter" dot_zshrc
   .chezmoiexternal.toml` returns nothing (identity literals belong only in
   `dot_gitconfig`).
6. **Spec parity check:** `uv run memos doctor` / project-layout check stays
   green after the submodule bump.
