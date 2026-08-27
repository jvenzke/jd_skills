---
name: meta-review
description: >-
  Review how skills performed in the current chat against their own
  instructions and a shared workflow bar (numbered tasks, blocking
  clarify, named gates, durable resume artifacts, terse output). Propose
  compact skill edits and log approved recurring problems. Use at the
  end of a session where one or more skills were used.
disable-model-invocation: true
---

# Meta Review

Review only the current chat context. Do not use parent transcripts unless
the user starts a separate review process. Stay in chat; do not write
`.working_items/` for the review itself.

## Shared bar

Grade the **spirit**, not a copy of antigravity file trees. Other skills may
use different paths, phase names, and gates — judge them against *their*
`SKILL.md`. Use this bar only where it fits the skill’s job (multi-step
work, irreversible actions, handoff to a later chat). Do not force
`.working_items/`, `agent_notes.md`, phases, or deep-module writeups onto
skills that do not have those jobs.

When the skill’s workflow is in play, check:

- **Numbered workflow + resume**: Followed the skill’s task order. A later
  chat could continue from disk, not chat memory.
- **Blocking clarify only**: Asked only decisions the codebase cannot
  answer. Independent questions in one numbered pass with recommended
  options; paused for a reply before planning or acting.
- **Named gate**: Irreversible work waited for the skill’s explicit
  sign-off (**APPROVED** or equivalent). Did not treat “continue” as
  blanket approval unless the skill allows it.
- **Durable next-step artifacts**: Wrote whatever that skill already names
  so a fresh chat can resume (plan, tasks, walkthrough, claims file, etc.).
  Do not invent a layout the skill does not specify.
- **Terse + owner split**: Plans and chat stayed compact. Main agent owned
  verification, artifacts, and user-facing summary. Subagents were optional,
  read-constrained, and did not approve or ship.
- **Simple surface (implementation work only)**: Prefer a small
  caller/researcher entrypoint and hidden plumbing when the skill was
  changing code. Do not apply this to purely conversational skills.

Do **not** recommend splitting one workflow across slash commands or
merging independent skills. Tightly coupled steps belong in one skill.

## Workflow

1. Identify every skill clearly used in the chat, plus any user-named subset.
2. Show the proposed review list and ask the user to approve or change it
   before evaluating.
3. Read `meta-review/problems.md` once, then each approved skill's `SKILL.md`.
4. Use a read-only subagent only for long, messy, or multi-skill sessions;
   verify its recommendations yourself.
5. For each skill, compare observed behavior against its `SKILL.md`, the
   **Shared bar** (where it applies), and approved user expectations.
6. Treat a problem as recurring when the same skill has the same failure
   pattern twice or the issue matches an active log entry.
7. Keep findings and fixes terse; include only critical evidence.
8. Group findings by skill and ask for a decision on each issue: apply the
   suggested edit, log the problem, or disregard it.
9. Do not edit a skill, update the log, commit, or push without explicit
    user approval for that action.

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
4. After the commit succeeds, move the matching active entries into a
   single compact resolved entry with the short commit hash and subject.
5. If the user declines the commit, leave the entries active and report
   that resolution logging is blocked.

Resolved entry format:

```markdown
- YYYY-MM-DD | skill: <name> | fixed: <summary> | commit: <hash> <subject> | compressed: <N> entries
```

## Final Report

End with a concise chat report: skills reviewed, issues
applied/logged/disregarded, missing or confirmed next-step artifacts,
unresolved recurring problems, and any commit or push status.
