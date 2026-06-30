# memclutter — GitHub Profile

Personal GitHub profile README ([github.com/memclutter](https://github.com/memclutter)).
The special `memclutter/memclutter` repository whose `README.md` is rendered
on the GitHub profile page.

## What this project is

A single Markdown document that presents the owner to anyone visiting the GitHub
profile: a short bio, the tech stack, GitHub statistics widgets, featured
projects, and social links.

## How it fits the OS

Source changes happen inside `vcs/memclutter/`. This OS repo only pins the
submodule commit. No build or deployment steps — GitHub renders the README
automatically.

## Living spec

`spec/` holds the current truth about what the profile contains and why each
section exists. Use `sys.task.specify` to start a task and `sys.task.finish` to
fold it back into the spec.
