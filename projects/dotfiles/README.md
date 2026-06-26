# dotfiles

Personal dotfiles — the configuration files that keep a consistent development
environment across machines. Managed with [chezmoi](https://chezmoi.io): files
are stored here with chezmoi's source-state naming (e.g. `dot_gitconfig` →
`~/.gitconfig`) and applied to the home directory with `chezmoi apply`.

Today it ships Git and Vim configuration; the repository is meant to grow to
cover more of the shell/dev environment over time.

## Apply locally

```bash
# one-time: point chezmoi at this repo
chezmoi init memclutter/dotfiles
# preview, then apply to $HOME
chezmoi diff
chezmoi apply
```

## How it fits the OS

This is a project under the [memos](../..) operating system. The living product
spec lives in [spec/](spec/); work happens as SDD tasks under
[tasks/](tasks/) and lands in the upstream repo via the [repo/](repo/) submodule
(`git@github.com:memclutter/dotfiles.git`).
