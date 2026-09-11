# Phase 5 — Submit and walkthrough

## Validate

1. Fetch the live PR and compare `head_sha` with `tasks.md`. If it differs, summarize the update, then refresh context and rebuild coverage without waiting (`incremental`: update diff only). Do not reset `COMMENTS.md`; re-anchor or drop stale comments in the steps below. If this user already has a submitted review and `review_scope` was `full`, switch to `incremental` per `follow-up.md` before drafting the payload.
2. Validate every approved comment path and diff anchor against the current `gh pr diff`.
3. Deduplicate comments by fingerprint and defect, and skip fingerprints already submitted.
4. Revalidate that each comment remains `high` confidence (trigger, traced path, consequence, attempted cheap falsification), has a concrete consequence (logic, behavior, security, test gap, or maintainability regression), is `blocker` or `recommended` unless broader feedback was requested, and still matches the current code.
5. Scan the exact review body and every inline GitHub body. Rewrite before showing the payload if the text is not self-contained: claim ids (`C1`, `C2`, `claim c1`, and similar); `.working_items/`; distinctive review artifacts (`BUSINESS_CLAIMS.md`, `LOGIC_WALKTHROUGH.md`, `HUMAN_REVIEW_PROMPTS.md`, `PR_BRIEF.md`, `agent_notes.md`, `SUBMISSION.md`, `NEXT_CHAT_PROMPT.md`); skill paths (`coding-standards.md`); or pointers to chat walkthrough, coverage tables, or human-oversight bullets. Restate product intent in prose. Do not cite the local review workspace even if the filename is generic (`tasks.md`, `COMMENTS.md`).
6. Mark stale anchors `stale_anchor`. Show nearby current diff and ask whether to re-anchor, convert to a top-level note, or drop.
7. If any changed sections remain `not_reviewed`, identify them and either review them or explicitly explain the residual gap before asking for the review type.
8. Only actionable, code-anchored, user-approved comments may be submitted as inline comments. The review-body summary always posts.

## Review event

The GitHub review must use one of: `APPROVE`, `REQUEST_CHANGES`, or `COMMENT`. Recommend one using:

- `REQUEST_CHANGES` when any submitted inline comment is a `blocker`
- `APPROVE` when there are no blockers and the user is ready to sign off
- `COMMENT` when feedback is non-blocking, questions remain, or they do not want to approve or block

Do not default the event. Do not wait here. Show the exact payload in **Review type gate**, then ask which type to submit. Naming **Approve PR**, **Request changes**, or **Comment** (or `APPROVE` / `REQUEST_CHANGES` / `COMMENT`) is the GitHub write. Do not also require **APPROVED**. If they edit comments instead of naming a type, apply the edits, re-show the payload, and ask for the type again.

## Review body

Always post a top-level review summary **in addition to** any user-approved inline comments. Draft from confirmed intent and specialist evidence; do not name those files on GitHub. Show the exact body in the review type gate. Presentation metrics and human-oversight bullets stay in chat and `SUBMISSION.md` only.

```markdown
## Review summary

**Verdict:** <approve | request changes | comment>
**Review risk:** <low | medium | high> — <reasons>

### What was reviewed
<2–4 sentences in product terms: behaviors checked, residual uncertainty. No claim ids, no local artifact names.>

### Presentation
- Changed sections: N (added lines: N, deleted lines: N)
- Shown in chat (`human_presented`): N (N%) — code exposure only
- Agent-reviewed only: N (N%) — <brief reason mix, e.g. tests summarized, peripheral>
- Not reviewed: N (N%) — <none, or why left uncovered>

### Test coverage of new code
<which new/changed product behaviors are covered by which tests; uncovered behaviors/branches; residual test risk. No test source. No claim ids.>

### CI workflow scope
<whether the GitHub workflows that run on this PR execute the tests that impact this project; name jobs/selectors and any path-filter or package-selector gaps.>

Inline comments below are separate findings.
```

Keep this short. Do not paste code. Do not omit presentation vs oversight, new-code coverage, or CI workflow scope. Never label `human_presented` as Human-reviewed.

On `incremental`, add a **Follow-up** subsection: prior review event and SHA, and prior-comment outcomes (`addressed` / `still_open` / `stale` / `reintroduced` counts) in plain language. Chat-only presentation numbers are for the update diff.

## Review type gate

Show:

- the exact review body above (GitHub-facing; already scanned per Validate step 5)
- every inline comment as a numbered item with path/range, severity, confidence, and the exact body that will be posted (or “none”). Re-paste every inline GitHub body in this message. A pointer to an earlier turn does not count.
- unresolved business prompts
- section coverage (`changed_sections`, `added_lines`, `deleted_lines`, `human_presented` %, agent-only % by reason, not-reviewed %, excluded count) and the human-oversight bullets
- recommended type with the same rules as **Review event**, clearly labeled as a recommendation only

Ask only:

```markdown
Submit as which review type?
1. Approve PR (`APPROVE`)
2. Request changes (`REQUEST_CHANGES`)
3. Comment (`COMMENT`)
```

Invite edits to any comment in the same turn. Apply requested wording changes, re-show the affected exact bodies, and ask for the type again. Do not submit until the user names one of the three types. The walkthrough comment decision determines eligibility, but it is not submission.

## Submit

Create **one** GitHub review: the summary body, the chosen event, and every valid inline comment.

If an inline anchor fails, do not dump all comments into the body. Re-anchor or post only that issue as a top-level note referencing its file/range after the user names the review type.

Always submit this review, including when there are no inline comments.

## Walkthrough

Write `SUBMISSION.md`:

- PR/head SHA and review URL/id
- `review_risk` and reasons
- review event and exact review body
- submitted comment ids and fingerprints
- skipped duplicates and stale anchors
- security, logic/quality, test-coverage of new code, and CI workflow scope summaries
- business claims walked and unresolved prompts
- presentation totals (sections, added/deleted lines) and agent-only reason breakdown
- human-oversight summary (claims, boundary decisions, finding decisions, prompts)
- on `incremental`: prior review id/event/SHA and prior-comment statuses

Set `phase: complete` and all task checkboxes complete. Do not delete artifacts without separate approval.
