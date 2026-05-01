---
name: meta-review
description: Review how skills performed in the current chat, identify missed instructions or bloat, propose compact improvements, and log approved recurring problems. Use at the end of a chat session where one or more skills were used.
disable-model-invocation: true
---

# Meta Review

Review only the current chat context. Do not use parent transcripts unless the user starts a separate review process.

## Workflow

1. Identify every skill clearly used in the chat, plus any user-named subset.
2. Show the proposed review list and ask the user to approve or change it before evaluating.
3. Read `meta-review/problems.md` once, then each approved skill's `SKILL.md`.
4. Use a read-only subagent only for long, messy, or multi-skill sessions; verify its recommendations yourself.
5. For each skill, compare observed behavior against its instructions and approved user expectations.
6. Check whether the skill forgot steps, struggled, caused confusion, duplicated another skill, or exceeded 40 actionable directives in `SKILL.md`.
7. Count only actionable bullets or numbered steps; ignore frontmatter, headings, examples, and reference links.
8. Treat a problem as recurring when the same skill has the same failure pattern twice or the issue matches an active log entry.
9. Suggest a split when a skill has independent triggers/workflows or cannot fit the instruction budget after compression.
10. Suggest a merge when skills are usually invoked together, duplicate decision logic, and have no meaningful independent use.
11. Keep findings and fixes terse; include only critical evidence.
12. Group findings by skill and ask for a decision on each issue: apply the suggested edit, log the problem, or disregard it.
13. Do not edit a skill, update the log, commit, or push without explicit user approval for that action.

## Logging

Use `problems.md` as the only persistent log.

For approved log-only issues, append one compact active entry:

```markdown
- YYYY-MM-DD | skill: <name> | symptom: <critical symptom> | cause: <likely cause> | fix: <short proposed fix> | decision: logged | evidence: <short note>
```

When an approved skill fix resolves active recurring entries:

1. Apply the approved edit.
2. Ask before committing; commit only relevant skill and log files.
3. Do not push unless the user separately approves the push.
4. After the commit succeeds, move the matching active entries into a single compact resolved entry with the short commit hash and subject.
5. If the user declines the commit, leave the entries active and report that resolution logging is blocked.

Resolved entry format:

```markdown
- YYYY-MM-DD | skill: <name> | fixed: <summary> | commit: <hash> <subject> | compressed: <N> entries
```

## Final Report

End with a concise chat report: skills reviewed, issues applied/logged/disregarded, unresolved recurring problems, merge/split guidance, and any commit or push status.
