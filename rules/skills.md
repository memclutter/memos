# Skills

`skills/` holds **agent skills** that are available to the agent working in this
OS. A skill packages reusable instructions (and optional scripts) for a recurring
job, so the agent can invoke it instead of re-deriving the steps each time.

```
skills/
└── <skill-name>/
    └── SKILL.md     # the skill definition (frontmatter + instructions)
```

- One folder per skill, named in kebab-case.
- `SKILL.md` carries YAML frontmatter with at least a `name` and a `description`
  (the description is what the agent matches against to decide relevance), then
  the instructions in the body. Supporting files (scripts, templates) live
  alongside it in the skill folder.
- Skills are written in English like every other record.
- Add a skill when a multi-step job recurs across projects (e.g. scaffolding a
  new project, bootstrapping CI, cutting a release).
