---
name: doc.prose.review
description: Review Markdown prose against The Elements of Agent Style (21 rules)
  to strip LLM writing tells. Audits a file, prints a per-rule scorecard, and on
  the owner's confirm writes a polished copy beside it as FILE.reviewed.md (never
  in place). Use to clean up docs, READMEs, proposals, or research prose an agent
  wrote.
category: doc
entity: prose
action: review
version: 0.1.0
x-shim:
  claude:
    allowed-tools: Bash, Read, Write, AskUserQuestion
---

# doc.prose.review

Post-hoc review for prose an agent has already written. Audit a Markdown file
against the 21 rules of *The Elements of Agent Style* (vendored as
[references/RULES.md](references/RULES.md)), report which rules it breaks, and —
only if the owner asks — produce a polished copy beside the original.

Talk to the owner in Russian; write every file in English (see
[language.md](../../rules/language.md)).

The ruleset is third-party content under CC BY 4.0. Keep the attribution intact
and do not strip the SPDX headers from `references/RULES.md` /
`references/SOURCES.md`. See [references/ATTRIBUTION.md](references/ATTRIBUTION.md).

## Invocation

| Shape | Behavior |
| --- | --- |
| `doc.prose.review FILE` | Audit FILE against all 21 rules, print the scorecard, then ask whether to write `FILE.reviewed.md`. |
| `doc.prose.review A.md B.md` | Audit both drafts, print a per-rule delta table comparing them. No polish, no write. |

Mode is inferred from the argument count. If no file is given, ask the owner
which file to review before doing anything. There are no flags.

## Workflow (single file)

1. **Load the rules.** Read [references/RULES.md](references/RULES.md) in full — it carries the
   directive, severity, scope, and BAD → GOOD examples for every rule. These
   examples are the judging standard; do not review from memory.
2. **Read the target.** Read FILE. Treat fenced code blocks, frontmatter,
   tables, link syntax, and inline code spans as off-limits to the prose rules —
   they are structure, not prose.
3. **Audit.** Walk the prose against each rule. Some rules are mechanical and
   should be checked literally with line numbers (RULE-05, 06, 12, B, C, D, G,
   I, and the bullet/structure rules A, E). The rest are judgment calls
   (RULE-01, 03, 04, 07, 08, 11, F, H) — apply the rule's directive and its
   examples. Honor the escape hatch in `RULES.md`: a rule that fights the
   sentence is dropped, not forced.
4. **Report.** Print a scorecard: one line per rule with a violation, its
   severity, a count, and the first few offending excerpts with line numbers.
   Order by severity (critical → low). If nothing fires, say so and stop.
5. **Ask.** Use AskUserQuestion: "Написать вычитанную копию в `FILE.reviewed.md`?"
   Wait for the answer.
6. **Polish (only on yes).** Rewrite the flagged spans into a new file at
   `FILE.reviewed.md`. Obey the invariants below. Never edit FILE in place.
7. **Diff.** Print `git diff --no-index FILE FILE.reviewed.md` so the owner can
   accept or discard the result themselves.

## Workflow (A/B compare)

1. Read [references/RULES.md](references/RULES.md), then audit `A.md` and `B.md` independently.
2. Print one table: rows are rules that fired in either draft, columns are A and
   B with the violation counts, plus a delta column.
3. Stop. No questions, no polish, no file writes. This is the regression-check
   shape.

## Polish invariants (hard)

- **No new facts.** Add no metric, number, citation, link, or claim that is not
  already in the source. If a claim is flagged as unsupported (RULE-H), leave it
  flagged — never invent evidence.
- **Preserve structure.** Code fences, tables, frontmatter, heading levels, list
  nesting, link syntax, and inline code spans stay byte-identical unless the
  violation *is* the structure (e.g. RULE-A prose-as-bullets, RULE-G heading
  case).
- **Preserve meaning.** Touch only the spans the audit flagged. Do not rewrite
  paragraphs that passed.
- **Write beside, never in place.** Output goes to `FILE.reviewed.md`. FILE is
  read-only.

## Self-verification

When asked "is doc.prose.review active?", reply on one line:

`doc.prose.review active: audits 21 rules from skills/doc.prose.review/references/RULES.md (CC BY 4.0); workflow at skills/doc.prose.review/SKILL.md.`
