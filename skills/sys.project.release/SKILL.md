---
name: sys.project.release
description: Cut a SemVer release for a repo — pick the next version, build
  release notes from Conventional Commits since the last tag, create and push an
  annotated tag, and publish a GitHub release with gh. Works for the OS repo or a
  project's repo under vcs/<repo-name>/. Use when the owner wants to ship a new version.
category: sys
entity: project
action: release
version: 0.1.1
x-shim:
  claude:
    allowed-tools: Bash, Read, Write, Edit, AskUserQuestion
---

# sys.project.release

Cut a release following [git.md](../../rules/git.md): SemVer tag
`vMAJOR.MINOR.PATCH`, notes built from Conventional Commits. Talk to the owner in
Russian; write every artifact (tag message, notes, changelog) in English.

## 1. Resolve the target repo

- **Default:** the OS repo itself (the current working directory root).
- **A project:** if the owner names one, work inside its repo under
  `projects/<name>/vcs/<repo-name>/` (its own git repo + GitHub remote). Scan
  `projects/` and ask which repo if ambiguous; never guess.

Run the rest of the steps in that repo's root.

## 2. Pre-flight checks

```bash
git rev-parse --abbrev-ref HEAD          # must be the releasable main
git status --porcelain                   # must be empty (clean tree)
git fetch --tags origin
git log --oneline origin/main..HEAD      # must be empty (pushed, up to date)
```

Stop and tell the owner if the tree is dirty, the branch isn't `main`, or local
commits aren't pushed. Don't release a moving target.

## 3. Pick the version

```bash
git tag --sort=-v:refname | head -1      # the previous tag (PREV)
```

- Take the version from the owner's request, or propose the next SemVer bump from
  the commits since `PREV` (breaking → MAJOR, `feat` → MINOR, else PATCH) and
  confirm.
- Validate the `vMAJOR.MINOR.PATCH` shape and refuse a tag that already exists.

## 4. Build release notes

Group Conventional Commits since the previous tag by type into Markdown sections
(Features, Fixes, Docs, Chore, …). Lead with a one-line summary of the release.

```bash
git log --pretty='- %s' PREV..HEAD       # source lines to group and clean up
```

Write the notes to a scratch file for the tag message and the GitHub release. If
the repo keeps a `CHANGELOG.md` (Keep a Changelog format), prepend a new section
for this version; if it has none, the GitHub release body is the record.

## 5. Tag and push

```bash
git tag -a <version> -m "<version> — <short title>"   # annotated; -m and -F can't mix
git push origin <version>
```

The full notes go to the GitHub release below; the tag carries the short title.

## 6. Publish the GitHub release

```bash
gh release create <version> --title "<version> — <short title>" \
  --notes-file <notes-file> --latest
```

For a project repo, add `--repo memclutter/<name>` if `gh` doesn't infer it.

## 7. Report

Tell the owner (in Russian) the version, the tag, and the release URL
(`gh release view <version> --json url -q .url`).
