# 003 — keep repo metadata out of $HOME

## Goal

Stop chezmoi from deploying the repository's own metadata files (`README.md`,
`LICENSE`) into the home directory. They must stay in the git repo (for GitHub)
but never land in `$HOME`.

## Scope

- Make `chezmoi apply` ignore `README.md` and `LICENSE` so they are not
  materialised in `$HOME`.
- Remove the stray copies that earlier applies already left in `$HOME`.
- Record in the living spec that repo metadata is not deployed.

## Acceptance criteria

- After applying, `~/README.md` and `~/LICENSE` do not exist.
- `README.md` and `LICENSE` are still present in the repo.
- A fresh `chezmoi apply` on a clean machine produces only the intended dotfiles
  in `$HOME`, not repo metadata.
