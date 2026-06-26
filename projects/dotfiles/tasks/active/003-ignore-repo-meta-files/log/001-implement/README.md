# 001 — implement repo-metadata exclusion

All breakdown steps implemented and verified on the owner's machine.

## Done

- **`.chezmoiignore`** — added at the repo root with `README.md` and `LICENSE`,
  so chezmoi no longer deploys the repository metadata to `$HOME`. The file is a
  chezmoi special file and is itself never applied.
- **Stray cleanup** — removed `~/README.md` and `~/LICENSE` (copies left by
  earlier applies), with the owner's confirmation.

## Verified

- `chezmoi managed` lists only `.gitconfig`, `.oh-my-zsh`, `.vimrc`, `.zshrc` —
  `README.md` / `LICENSE` are gone from management.
- After `rm`, a full `chezmoi apply` (exit 0) does **not** recreate `~/README.md`
  or `~/LICENSE`.
- `README.md` and `LICENSE` still present at the repo root.

## Note

chezmoi does not remove files that become ignored — it only stops managing them —
so the one-off `rm` was necessary and is the documented cleanup for other
machines too (identical structure).
