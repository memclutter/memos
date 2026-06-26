# Plan — 003-vcs-submodule-layout

## Approach

Two moving parts: (1) a **text/rule change** — replace every description of the
fixed `repo/` submodule with the `vcs/<repo-name>/` layout, and (2) a **physical
migration** — move the one existing submodule (`dotfiles`) into the new path with
its history and pinned commit intact. Do the text edits first, then the
migration, then regenerate skill shims and run `memos doctor` so the rules, the
spec, and the on-disk tree all agree in the same commit.

Per the owner's directive, the project `AGENTS.md` frontmatter gains a `vcs:`
**list**, written as an array even when a project has a single repository.

## Stack

No app stack — this is OS-maintenance work: Markdown rules/spec, YAML frontmatter,
git submodules, and the Python `memos` CLI ([python.md](../../../rules/python.md))
for the optional doctor check. No base-stack deviation.

## Architecture

### Naming rule

A submodule lives at `projects/<name>/vcs/<repo-name>/`, where `<repo-name>` is
the GitHub repository name = the basename of the clone URL without `.git`
(`git@github.com:memclutter/dotfiles.git` → `dotfiles`). A project may have
several entries under `vcs/`; `self: true` projects have **no** `vcs/` folder on
disk.

### Frontmatter shape (`vcs:` list)

Replace the single `repo:` scalar with a `vcs:` list of clone URLs; the folder
name is derived from each URL, so no separate `name` key is needed:

```yaml
# single-repo project (dotfiles) — still an array
vcs:
  - git@github.com:memclutter/dotfiles.git

# multi-repo project — one entry per repo
vcs:
  - git@github.com:memclutter/foo-api.git
  - git@github.com:memclutter/foo-web.git
```

For `self: true` (memos), keep a `vcs:` entry with the canonical repo URL as
informational (as `repo:` is today), and state in the body that there is no
physical `vcs/` folder because the source is the OS root.

### Text edits (the rule surface)

- `rules/projects.md` — rewrite the anatomy diagram and prose: `vcs/<repo-name>/`
  container, one-or-many repos, the `vcs:` frontmatter list, the `self: true`
  exception (no `vcs/`), and the "Add a project" snippet
  (`git submodule add <url> projects/<name>/vcs/<repo-name>`). Clone instructions
  (`--recurse-submodules`) are unchanged.
- `rules/repo-structure.md` — the top-level tree/notes mentioning projects "as
  submodules" stay correct; no `repo/` literal there, but verify.
- `AGENTS.md` (root index) — the **Projects** paragraph mentions `repo/`; reword
  to `vcs/<repo-name>/`.
- `skills/sys.project.specify/SKILL.md` — step 2 submodule path → `vcs/<repo-name>`
  and the frontmatter template `repo:` → `vcs:` list; bump `version`, then
  `uv run memos shimify` (never hand-edit shims, [skills.md](../../../rules/skills.md)).
- `projects/dotfiles/AGENTS.md` + `README.md`, `projects/memos/AGENTS.md` —
  frontmatter `repo:` → `vcs:` and any `repo/` path references.

### Physical migration (dotfiles)

```bash
mkdir -p projects/dotfiles/vcs
git mv projects/dotfiles/repo projects/dotfiles/vcs/dotfiles
# verify: .gitmodules path + section name updated, same pinned commit
git submodule status projects/dotfiles/vcs/dotfiles
```

`git mv` rewrites the submodule `path` in `.gitmodules` and `.git/config` and
preserves the gitlink (pinned commit). Verify the `[submodule "…"]` section name
is also updated to `projects/dotfiles/vcs/dotfiles`; fix it by hand in
`.gitmodules` if git left the old name.

### Optional doctor check (recommended)

`memos doctor` does **not** validate project layout today, so it passes trivially
after migration. Recommend adding a small read-only check (`check_project_layout`
in [doctor.py](../../../scripts/memos/src/memos/doctor.py)) that, for every
non-`self` project, asserts: no `repo/` folder remains, and every `.gitmodules`
path for that project sits under `projects/<name>/vcs/`. This gives the new
invariant teeth.

> **Scope flag for the owner:** adding this check also touches `spec/cli.md`, so
> it extends the spec.md *Affected spec sections* (currently `workflow.md` +
> `overview.md`) with `spec/cli.md` at Finish. If we skip the check, no doctor
> code changes and the merge contract is unchanged. Recommendation: include it.

## Trade-offs & alternatives

- **`vcs:` as URL list vs. list of `{name, url}` objects** — chose plain URLs and
  derive the folder name; the name is redundant with the URL. Rejected the object
  form as verbose. (If a repo ever needs a folder name different from its GitHub
  name, revisit — not a case today.)
- **Uniform `vcs/<repo-name>/` even for single-repo projects** vs. a short
  `vcs/` or keeping `repo/` for the common case — chose uniform; the whole point
  is unambiguous, self-identifying folders.
- **`git mv` vs. deinit + re-add submodule** — `git mv` preserves history, the
  gitlink, and the pinned commit in one step; remove-and-readd risks losing the
  pin and is noisier. Chose `git mv`.

## Constraints & risks

- **History/pin integrity** — the migration must not change the pinned commit
  (`2b334c0`) or lose submodule history; verify with `git submodule status`
  before committing.
- **Stale references** — a missed `repo/` mention leaves rules and spec
  disagreeing; mitigate with a repo-wide grep (below).
- **Shim drift** — after editing the skill, shims must be regenerated or
  `memos doctor` fails the shims check.
- **`self: true` ambiguity** — be explicit that memos has a `vcs:` URL but no
  `vcs/` folder, so no one looks for a missing submodule.

## Testing strategy

Proves the spec.md success criteria:

- `git submodule status` → `dotfiles` resolves at the same commit under
  `projects/dotfiles/vcs/dotfiles`; no `projects/dotfiles/repo` exists.
- `grep -rn "/repo\b\|repo/" rules/ AGENTS.md skills/ projects/*/AGENTS.md` (and
  similar) returns no stale submodule references.
- Fresh `git clone --recurse-submodules` (or `git submodule update --init`)
  populates `vcs/dotfiles`.
- `uv run memos doctor` passes; if the layout check is added, extend
  `tests/test_doctor.py` to cover the pass case and a `repo/`-present failure.
- `sys.project.specify` (re-read after edit) scaffolds new submodules under
  `vcs/<repo-name>/` and writes a `vcs:` array.
