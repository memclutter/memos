---
id: 001-readme-refresh
status: done
created: 2026-06-30
updated: 2026-06-30
---

Rewrite `vcs/memclutter/README.md` to target startup partners and technical
co-founders. The new README must be short enough to read in one scroll, list
only real repos tracked in the memos OS, and communicate clearly who the owner
is and how to reach them.

## Precise goal

Replace the current bloated profile page with a lean document that answers
three questions for a startup partner:

1. Who is this person and what do they build? (include: co-founder of
   [vAIbe Studio](https://vaibe.studio))
2. What are their real, live open-source projects? (include vaibe-os)
3. How do I contact them?

## Scope

- `vcs/memclutter/README.md` — the only file to change.
- `spec/profile.md` — update to reflect new structure.
- `spec/overview.md` — update Vision (target audience shift to startup partners).

## Acceptance criteria

- Every repo in Featured Projects exists as a public GitHub repo under
  `memclutter`.
- Featured Projects lists repos tracked in the memos OS (confparse, gorequests,
  nocodb-migrator, proxycheck) plus vaibe-studio/vaibe-os.
- GitHub Stats and Streak widgets: at most one (or none).
- "Latest Articles" section removed.
- "Tech Stack" either removed or collapsed to a single compact line/group.
- Total visible sections ≤ 5.
- Renders correctly on GitHub (no broken images, no raw HTML errors).

## Constraints

- Do not add CI, workflows, or scripts to the `memclutter/memclutter` repo.
- Keep Conventional Commits inside the submodule.
- Ask the owner before removing the Connect / social links section.

## Tasks breakdown

- [x] 1. Verify `vaibe-studio/vaibe-os` is public: `gh repo view vaibe-studio/vaibe-os --json visibility`  ⚠️ stop and ask owner if private
- [x] 2. Verify all four `memclutter/*` repos are public: confparse, gorequests, nocodb-migrator, proxycheck
- [x] 3. Write new `vcs/memclutter/README.md` matching the Target State in `spec.md` (5 sections: Header → About → Tech Stack → Open-source projects → Connect)
- [x] 4. Sanity-check the file: count `## ` headings (expect 4), grep confirms 0 hits for `github-readme-stats`, `streak-stats`, `BLOG-POST-LIST`
- [x] 5. Commit inside the submodule: `git commit -m "feat: refresh profile README"`
- [x] 6. Push submodule to GitHub: `git push origin main`
- [x] 7. Visual check: open `github.com/memclutter` in browser — render correct, role + contact visible above fold at 1080 p
- [x] 8. Bump submodule pointer in OS repo: `git add projects/memclutter/vcs/memclutter && git commit -m "chore(submodule): bump memclutter"`
- [x] 9. Update `projects/memclutter/spec/profile.md` to Target State from `spec.md`
- [x] 10. Update `projects/memclutter/spec/overview.md` Vision paragraph to Target State from `spec.md`
