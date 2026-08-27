# Phase 6 — Submit and walkthrough

## Validate

1. Fetch the live PR and compare `head_sha` with `tasks.md`.
2. Validate every approved comment path and diff anchor against the current `gh pr diff`.
3. Skip duplicate fingerprints already submitted.
4. Mark stale anchors `stale_anchor`. Show nearby current diff and ask whether to re-anchor, convert to a top-level note, or drop.
5. Only actionable, code-anchored, user-approved comments may be submitted.

## Final approval gate

Show:

- all comments exactly as they will appear
- review event (`COMMENT` by default; `REQUEST_CHANGES` only when explicitly requested)
- unresolved business prompts
- total changed lines, human-presented %, agent-only % by reason, not-reviewed %, and excluded count

Ask the user to reply **APPROVED** before any GitHub write. An earlier claim/comment approval is not submission approval.

## Submit

Create one GitHub review containing all valid inline comments. Use a minimal body (`Reviewed with inline comments.`) unless blockers or cross-cutting context require more.

If an inline anchor fails, do not dump all comments into the body. Re-anchor or post only that issue as a top-level note referencing its file/range after approval.

If there are no approved comments, skip GitHub submission unless the user explicitly asks for a no-findings review.

## Walkthrough

Write `SUBMISSION.md`:

- PR/head SHA and review URL/id
- submitted comment ids and fingerprints
- skipped duplicates and stale anchors
- security and test-coverage summaries
- business claims walked and unresolved prompts
- final coverage totals and agent-only reason breakdown
- final review event

Set `phase: complete` and all task checkboxes complete. Do not delete artifacts without separate approval.
