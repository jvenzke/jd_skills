# Phase 5 — Submit and walkthrough

## Validate

1. Fetch the live PR and compare `head_sha` with `tasks.md`. If it differs, summarize the update, then refresh context and rebuild coverage without waiting (`incremental`: update diff only). Do not reset `COMMENTS.md`; re-anchor or drop stale comments in the steps below. If this user already has a submitted review and `review_scope` was `full`, switch to `incremental` per `follow-up.md` before drafting the payload.
2. Validate every approved comment path and diff anchor against the current `gh pr diff`.
3. Deduplicate comments by fingerprint and defect, and skip fingerprints already submitted.
4. Revalidate that each comment remains `high` confidence (trigger, traced path, consequence, attempted cheap falsification), has a concrete consequence (logic, behavior, security, test gap, or maintainability regression), is `blocker` or `recommended` unless broader feedback was requested, and still matches the current code.
5. Mark stale anchors `stale_anchor`. Show nearby current diff and ask whether to re-anchor, convert to a top-level note, or drop.
6. If any changed hunks remain `not_reviewed`, identify them and either review them or explicitly explain the residual gap before asking for the review type.
7. Only actionable, code-anchored, user-approved comments may be submitted as inline comments. The review-body summary always posts.

## Review event

The GitHub review must use one of: `APPROVE`, `REQUEST_CHANGES`, or `COMMENT`. Recommend one using:

- `REQUEST_CHANGES` when any submitted inline comment is a `blocker`
- `APPROVE` when there are no blockers and the user is ready to sign off
- `COMMENT` when feedback is non-blocking, questions remain, or they do not want to approve or block

Do not default the event. Do not wait here. Show the exact payload in **Review type gate**, then ask which type to submit. Naming **Approve PR**, **Request changes**, or **Comment** (or `APPROVE` / `REQUEST_CHANGES` / `COMMENT`) is the GitHub write. Do not also require **APPROVED**. If they edit comments instead of naming a type, apply the edits, re-show the payload, and ask for the type again.

## Review body

Always post a top-level review summary **in addition to** any user-approved inline comments. Draft it from `COVERAGE.md` and `BUSINESS_CLAIMS.md`. Show the exact body in the review type gate.

```markdown
## Review summary

**Verdict:** <approve | request changes | comment>
**Review risk:** <low | medium | high> — <reasons>

### Presentation
- Changed hunks: N (added lines: N, deleted lines: N)
- Shown in chat (`human_presented`): N (N%) — code exposure only
- Agent-reviewed only: N (N%) — <brief reason mix, e.g. tests summarized, peripheral>
- Not reviewed: N (N%) — <none, or why left uncovered>

### Human oversight
- Claims confirmed: <ids / none>
- Architecture/boundary decisions reviewed: <none, or what the user confirmed>
- Findings approved/rejected/edited: <counts>
- Unresolved business questions answered: <yes/no/partial; remaining>

### Business content reviewed
<2–4 sentences: confirmed claims walked, any skipped claims, unresolved prompts.>

### Test coverage of new code
<prose from TESTS.md: which new/changed product behaviors are covered by which tests; uncovered claims/branches; residual test risk. No test source.>

### CI workflow scope
<whether the GitHub workflows that run on this PR execute the tests that impact this project; name jobs/selectors and any path-filter or package-selector gaps.>

Inline comments below are separate, user-requested findings.
```

Keep this short. Do not paste code. Do not omit presentation vs oversight, new-code coverage, or CI workflow scope. Never label `human_presented` as Human-reviewed.

On `incremental`, add a **Follow-up** subsection: prior review event and SHA, and prior-comment outcomes (`addressed` / `still_open` / `stale` / `reintroduced` counts). Presentation numbers are for the update diff.

## Review type gate

Show:

- the exact review body above
- every inline comment as a numbered item with path/range, severity, confidence, and the exact body that will be posted (or “none”). Re-paste every inline GitHub body in this message. A pointer to an earlier turn does not count.
- unresolved business prompts
- hunk coverage (`changed_hunks`, `added_lines`, `deleted_lines`, `human_presented` %, agent-only % by reason, not-reviewed %, excluded count) and the human-oversight bullets
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

If an inline anchor fails, do not dump all comments into the body. Re-anchor or post only that issue as a top-level note referencing its file/range after the user names the review type. The presentation/oversight summary stays in the review body.

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
- presentation totals (hunks, added/deleted lines) and agent-only reason breakdown
- human-oversight summary (claims, boundary decisions, finding decisions, prompts)
- on `incremental`: prior review id/event/SHA and prior-comment statuses

Set `phase: complete` and all task checkboxes complete. Do not delete artifacts without separate approval.
