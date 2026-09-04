# Phase 5 — Submit and walkthrough

## Validate

1. Fetch the live PR and compare `head_sha` with `tasks.md`.
2. Validate every approved comment path and diff anchor against the current `gh pr diff`.
3. Deduplicate comments by fingerprint and defect, and skip fingerprints already submitted.
4. Revalidate that each comment remains `high` confidence, has a concrete consequence (logic, behavior, security, test gap, or maintainability regression), is `blocker` or `recommended` unless broader feedback was requested, and still matches the current code.
5. Mark stale anchors `stale_anchor`. Show nearby current diff and ask whether to re-anchor, convert to a top-level note, or drop.
6. If any changed lines remain `not_reviewed`, identify them and either review them or explicitly explain the residual gap before requesting submission approval.
7. Only actionable, code-anchored, user-approved comments may be submitted as inline comments. The review-body summary always posts.

## Review event

The GitHub review must use one of: `APPROVE`, `REQUEST_CHANGES`, or `COMMENT`. Recommend one, then wait for the user to pick:

- `REQUEST_CHANGES` when any submitted inline comment is a `blocker`
- `APPROVE` when there are no blockers and the user is ready to sign off
- `COMMENT` when feedback is non-blocking, questions remain, or they do not want to approve or block

Do not default the event. Do not submit until the user names the event and replies **APPROVED** after seeing the exact payload.

## Review body

Always post a top-level review summary **in addition to** any user-approved inline comments. Draft it from `COVERAGE.md` and `BUSINESS_CLAIMS.md`. Show the exact body in the approval gate.

```markdown
## Review summary

**Verdict:** <approve | request changes | comment>

### Human vs agent review
- Changed lines: N
- Human-reviewed (shown in chat): N (N%)
- Agent-reviewed only: N (N%) — <brief reason mix, e.g. tests summarized, peripheral>
- Not reviewed: N (N%) — <none, or why left uncovered>

### Business content reviewed
<2–4 sentences: confirmed claims walked, any skipped claims, unresolved prompts.>

### Test coverage of new code
<prose from TESTS.md: which new/changed product behaviors are covered by which tests; uncovered claims/branches; residual test risk. No test source.>

### CI workflow scope
<whether the GitHub workflows that run on this PR execute the tests that impact this project; name jobs/selectors and any path-filter or package-selector gaps.>

Inline comments below are separate, user-requested findings.
```

Keep this short. Do not paste code. Do not omit the human/agent split, new-code coverage, or CI workflow scope.

## Final approval gate

Show:

- the exact review body above
- the chosen review event
- every inline comment as a numbered item with path/range, severity, confidence, and the exact body that will be posted (or “none”). Re-paste every inline GitHub body in this message. A pointer to an earlier turn does not count.
- unresolved business prompts
- total changed lines, human-presented %, agent-only % by reason, not-reviewed %, and excluded count

Invite edits to any comment before submission. Apply requested wording changes, re-show the affected exact bodies, and ask the user to confirm the event and reply **APPROVED** before any GitHub write. The walkthrough comment decision determines eligibility, but it is not submission approval.

## Submit

Create **one** GitHub review: the summary body, the chosen event, and every valid inline comment.

If an inline anchor fails, do not dump all comments into the body. Re-anchor or post only that issue as a top-level note referencing its file/range after approval. The human/agent summary stays in the review body.

Always submit this review, including when there are no inline comments.

## Walkthrough

Write `SUBMISSION.md`:

- PR/head SHA and review URL/id
- review event and exact review body
- submitted comment ids and fingerprints
- skipped duplicates and stale anchors
- security, logic/quality, test-coverage of new code, and CI workflow scope summaries
- business claims walked and unresolved prompts
- final coverage totals and agent-only reason breakdown (human vs agent)

Set `phase: complete` and all task checkboxes complete. Do not delete artifacts without separate approval.
