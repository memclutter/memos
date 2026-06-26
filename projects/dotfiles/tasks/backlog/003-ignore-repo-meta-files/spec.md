# Spec — 003-ignore-repo-meta-files

## Problem

The dotfiles repo keeps `README.md` and `LICENSE` at its root for GitHub. chezmoi
applies every source-root file that has no special meaning, and since these two
carry no `dot_` prefix and nothing tells chezmoi to skip them, they are deployed
verbatim — leaving `~/README.md` and `~/LICENSE` sitting in the home directory.
These are repository metadata, not dotfiles; they clutter `$HOME` and are not
something the owner wants materialised on any machine.

## Goal

Repository metadata (`README.md`, `LICENSE`) stays in the git repo but is never
deployed to `$HOME` by `chezmoi apply`, and the stray copies already present are
removed.

## User journeys

- **Fresh machine:** the owner runs `chezmoi apply`; `$HOME` receives only the
  intended dotfiles (`~/.gitconfig`, `~/.vimrc`, `~/.zshrc`, `~/.oh-my-zsh`), with
  no `~/README.md` or `~/LICENSE`.
- **Existing machine:** the owner pulls this change and re-applies; the stray
  `~/README.md` and `~/LICENSE` from earlier applies are gone, and they are not
  recreated on subsequent applies.
- **Maintaining the repo:** `README.md` and `LICENSE` remain at the repo root so
  the GitHub project page and license are intact.

## Success criteria

- `chezmoi apply` does not create `~/README.md` or `~/LICENSE`; the dry-run /
  managed list no longer shows them as targets.
- `README.md` and `LICENSE` still exist at the repo root and are committed.
- The stray `~/README.md` and `~/LICENSE` left by previous applies no longer
  exist on the owner's machine.
- A fresh `chezmoi apply` on a clean machine yields a home with only the intended
  dotfiles, not repo metadata.

## Affected spec sections

- spec/configs.md — modify: note in Deployment that repository metadata
  (`README.md`, `LICENSE`) is kept in the repo but excluded from `chezmoi apply`;
  add a success criterion that these files are never materialised in `$HOME`.
- spec/overview.md — modify (if needed): reinforce the product-wide criterion
  that only intended dotfiles land in `$HOME` (no repo metadata).

## Target state

After this task ships, `spec/configs.md` states that the repo root holds the
managed `dot_*` source files plus repository metadata (`README.md`, `LICENSE`),
and that the metadata is explicitly excluded from deployment so `chezmoi apply`
never places it in `$HOME`. The Deployment section names the exclusion mechanism,
and Success criteria assert that `~/README.md` / `~/LICENSE` are never created and
that only intended dotfiles reach `$HOME`. `spec/overview.md` reflects that
applying the repo yields a clean home containing just the owner's dotfiles.

## Out of scope

- Choosing the exclusion mechanism (e.g. `.chezmoiignore` vs. another approach) —
  that is a `sys.task.plan` decision.
- Restructuring the repo (e.g. moving sources into a subdirectory) — only the
  deployment behaviour of the existing layout changes.
- Any change to what the dotfiles themselves contain.

## Boundaries

- ✅ Always: keep `README.md` and `LICENSE` in the git repo; verify with a real
  `chezmoi apply` (or dry-run) that they are not deployed; clean up the stray
  copies in `$HOME`.
- ⚠️ Ask first: deleting anything in `$HOME` beyond the two stray metadata files;
  moving or renaming the repo's source files.
- 🚫 Never: remove `README.md` or `LICENSE` from the repository; break deployment
  of the real dotfiles. Reference the global rules
  ([git.md](../../../../rules/git.md)).
