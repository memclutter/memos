# History

**Git is the log.** Do not keep a manual, append-only journal of all work (a
global activity log, a running changelog of tasks). The commit history is the
single, authoritative record of *when* things happened.

- A finished task is recorded by committing the task folder moved to
  `projects/<name>/tasks/done/` — the commit, its message, and its timestamp are
  the log entry.
- A task's own `log/` folders are not a journal: they hold the *artifacts and
  summary* of each execution iteration (outputs, notes, results). That is task
  output, kept with the task — not a substitute for git history.
- To review history, use git: `git log`, `git log -- <path>`, `git blame`.
- Write good commit messages so the history is readable; see
  [git.md](git.md) (Conventional Commits).
- Exception: a user-facing `CHANGELOG.md` inside a *released* project is a
  product artifact, not a work log, and is fine — see [git.md](git.md).
