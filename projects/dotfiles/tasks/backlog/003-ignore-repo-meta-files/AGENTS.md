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
