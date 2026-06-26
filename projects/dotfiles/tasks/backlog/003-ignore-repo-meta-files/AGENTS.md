---
id: 003-ignore-repo-meta-files
status: backlog
created: 2026-06-26
updated: 2026-06-26
---

Stop chezmoi from deploying the repo's own metadata (`README.md`, `LICENSE`) into
`$HOME` while keeping those files in the git repo. Also remove the stray copies
prior applies already placed in `$HOME`. Acceptance: after `chezmoi apply`,
`~/README.md` and `~/LICENSE` are absent, the files still exist in the repo, and a
fresh apply yields only intended dotfiles in `$HOME`. The mechanism (e.g.
`.chezmoiignore`) is a `sys.task.plan` decision.

## Tasks breakdown

All source changes happen inside `vcs/dotfiles/`; this OS repo only pins the
bumped submodule commit.

- [ ] 1. Add `.chezmoiignore` at the repo root with `README.md` and `LICENSE`
  (bare names, matched against target paths). → exclusion criterion.
- [ ] 2. Verify exclusion (non-destructive): `chezmoi -S <vcs/dotfiles> managed`
  no longer lists `README.md` / `LICENSE`; `chezmoi -S <vcs/dotfiles> diff` shows
  no changes for them; the real dotfiles (`.gitconfig`, `.vimrc`, `.zshrc`) stay
  managed. → real-dotfiles-unaffected criterion.
- [ ] 3. One-off cleanup: `rm -f ~/README.md ~/LICENSE`, then confirm a `chezmoi
  apply` does not recreate them.  ⚠️ deletes files in `$HOME` — confirm with the
  owner first; touch only these two paths.
- [ ] 4. Commit & push (GPG-signed) inside `vcs/dotfiles/`, then bump the
  submodule pin in this OS repo.

The `spec/configs.md` + `spec/overview.md` updates are folded by the Finish gate
(`sys.task.finish`), not a separate implementation step.
