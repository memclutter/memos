# Plan — 003-ignore-repo-meta-files

## Approach

Add a `.chezmoiignore` file at the source root listing the repository metadata
that must not be deployed:

```
README.md
LICENSE
```

chezmoi reads `.chezmoiignore` and skips matching target paths during `apply`,
so `~/README.md` and `~/LICENSE` are no longer created — while the files stay in
the repo for GitHub. `.chezmoiignore` is itself a chezmoi special file (name
starts with `.chezmoi`), so it is never deployed to `$HOME`.

One important nuance drives the second half of the task: **chezmoi does not
remove files that become ignored.** Ignoring a path only makes chezmoi stop
managing it; the stray `~/README.md` and `~/LICENSE` from earlier applies are now
unmanaged and will simply be left in place. They must therefore be removed once,
by hand (`rm -f ~/README.md ~/LICENSE`), as a one-off cleanup step. After that,
`apply` will not recreate them.

## Stack

[chezmoi](https://chezmoi.io) only, consistent with the project. New mechanism:
`.chezmoiignore` (target-path exclusion). No install script, no source
restructuring.

## Architecture

- `vcs/dotfiles/.chezmoiignore` — new file, two entries (`README.md`, `LICENSE`).
  Patterns are bare names; chezmoi matches them against target paths relative to
  `$HOME`, i.e. `~/README.md` and `~/LICENSE`.
- No change to the existing `dot_*` sources or to `README.md` / `LICENSE`
  themselves; only deployment behaviour changes.
- Data flow: `chezmoi apply` → reads `.chezmoiignore` → excludes the two targets
  → applies only `dot_gitconfig`, `dot_vimrc`, `dot_zshrc`, and the Oh My Zsh
  external.

### Spec updates (folded at Finish)

- `spec/configs.md`: in Deployment, note that the repo root also holds metadata
  (`README.md`, `LICENSE`) excluded from deployment via `.chezmoiignore`; add a
  success criterion that they are never materialised in `$HOME`.
- `spec/overview.md`: reinforce that applying the repo yields a home containing
  only the owner's dotfiles, no repo metadata.

## Trade-offs & alternatives

- **Chosen: `.chezmoiignore`.** Declarative, chezmoi-native, zero restructuring;
  keeps the files exactly where GitHub expects them.
- *Rejected: move sources into a subdir* (e.g. `home/`) and point chezmoi's source
  there — heavier change, out of scope per the spec, and unnecessary.
- *Rejected: delete README/LICENSE from the repo* — they are needed for the
  GitHub project page and license; explicitly forbidden by the spec boundaries.

## Constraints & risks

- **No over-broad ignores:** the two entries must match only the metadata, not
  any real dotfile. Bare `README.md` / `LICENSE` are exact target names, so the
  risk is minimal; verify with `chezmoi managed`.
- **Manual cleanup is required and irreversible-ish:** removing `~/README.md` /
  `~/LICENSE` deletes files in `$HOME`. They are copies of repo files, so this is
  safe, but limit the deletion to exactly these two paths (per spec: ⚠️ ask before
  deleting anything else in `$HOME`).
- **Other machines:** the same one-off `rm` is needed wherever a prior apply left
  the strays; structure is identical across the owner's machines.

## Testing strategy

1. **Excluded from management:** `chezmoi -S <vcs/dotfiles> managed` no longer
   lists `README.md` / `LICENSE`; `chezmoi -S <vcs/dotfiles> diff` shows no
   changes for them.
2. **Not recreated:** after `rm -f ~/README.md ~/LICENSE` and a `chezmoi apply`,
   neither file reappears.
3. **Repo intact:** `README.md` and `LICENSE` still present and committed at the
   repo root.
4. **Real dotfiles unaffected:** `~/.gitconfig`, `~/.vimrc`, `~/.zshrc` still
   apply; `chezmoi managed` still lists them.
5. **OS repo green:** `uv run memos doctor` passes after the submodule bump.
