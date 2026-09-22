---
name: open-pr
description: >-
  Drafts and posts GitHub pull request titles and bodies with Summary,
  Testing and Validation, and Prod migration. Use when opening a PR, running
  gh pr create or gh pr edit, updating a PR description, or pushing commits
  to a branch that already has an open pull request.
---

# Open PR

Public PR description for operators. Auto-attach whenever this chat would create a PR, edit the PR body, or push to a branch that already has an open PR. Do not wait for `/open-pr`.

Do not add approval gates or other blocking ceremonies. When the user asks to open a PR, draft from the available evidence and open it immediately. Afterward, show the posted title and body with the PR URL. Treat the body as editable: if the user requests changes after the PR is open, update it directly and show the revised body. The original request to open or update the PR authorizes that write; do not ask for a second confirmation.

`/d-antigravity` (and similar) still write `walkthrough.md`. Do not skip it. Do not link `.working_items/` on GitHub.

## When to run

1. `gh pr create`, or the user asks to open a PR.
2. `gh pr edit` of the description, or the user asks to update it.
3. About to `git push` to a branch that already has an open PR (`gh pr view --json url,title,body` for the current branch). Refresh the three sections for the new diff. If new work is not covered by recorded testing, state that plainly without blocking the push or update.

## Draft

Infer Summary from the branch diff vs the PR base (or default base). Prefer an existing walkthrough for behavior bullets; do not dump files or commits.

Title: short, from Summary. Use conventional commits only if this repo already does.

Record only testing and validation supported by the session or repository evidence. If nothing was run, say so plainly and open the PR without stopping to ask. Never invent commands, DBs, CI, or results.

DB name = the env actually queried this session (e.g. Snowflake database/schema). If it is unknown, say `Not specified`. No warehouse/SQL work: `N/A — no database changes`.

Prod migration: ordered **prod** risk only (SQL/schema/dbt applied out-of-band, expand/contract, dual-write, flags, merge-vs-deploy timing). Checked-in scripts are likely proven only in **dev**. Keep the checklist short and easy to follow. Rollback only as a gotcha when it is not trivial. No generic “deploy as usual” runbook. No extra top-level headings.

## Body template

Use these headings, this order, verbatim. No other top-level sections unless the user asks in this chat.

```markdown
## Summary
- {what the PR does — 1–5 behavior/outcome bullets}

## Testing and Validation
- DB: {env queried, or N/A — no database changes}
- What was tested/validated: {commands/checks/manual steps actually run}
- Results: {what happened}

## Prod migration
{No prod migration.  |  numbered checklist:}
1. {run these files/scripts in this order}
2. {when to merge/release code relative to those runs}
3. {how to validate prod is running properly}
4. {gotchas / notes — include rollback only if not trivial}
```

## Open, then refine

Use `git push -u` if needed, then `gh pr create` without a separate draft-approval round. Return the PR URL and the exact title and body that were posted.

For later feedback, revise the title or body with `gh pr edit` as requested. Do not reopen the approval cycle or require magic words such as **APPROVED**. Return the PR URL and the revised content.
