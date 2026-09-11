# Follow-up review (prior submitted review)

Use this file when the **current GitHub user** already submitted a review on this PR with event `APPROVE`, `REQUEST_CHANGES`, or `COMMENT`. Detect from GitHub (source of truth), not only local `SUBMISSION.md`. Pending/unsubmitted reviews do not count.

This is not a sixth task. It changes how tasks 1–5 run: every phase reviews the **update since that submission**, and reports whether **prior comments were addressed**.

## Detect

During intake (and on `head_sha` refresh), fetch:

- `gh api user --jq .login`
- this user's submitted PR reviews (newest first): id, event, `submitted_at`, `commit_id`
- review threads/comments (inline + body), including resolved/outdated flags

If none exist, `review_scope: full` and skip the rest of this file.

If one or more exist, set on `tasks.md`:

```yaml
review_scope: incremental
prior_review_id: <id>
prior_review_event: APPROVE | REQUEST_CHANGES | COMMENT
prior_review_head_sha: <commit_id of that review>
```

Use the latest submitted review by this user. Also persist `PRIOR_REVIEW.md` (below).

## Update diff

The review surface is `prior_review_head_sha...head_sha` (GitHub three-dot compare / `git diff A...B` after fetch).

- Initialize `COVERAGE.md` from that update diff, not the full PR diff.
- Core vs incidental, specialists, skeptic, walkthrough, and proposed **new** comments are limited to update sections, plus any file still carrying an unresolved or stale prior comment.
- Fetch full PR metadata as usual so claims and prior-comment context stay accurate; do not re-present the already-reviewed base in chat.

If the update diff is empty (no new commits), do not re-walk the old implementation. Report “no new changes,” re-check prior comments against current code, and continue to submit only if the user still wants a new review event (common after fixes that GitHub already included in the last `commit_id`).

## Prior comments

For each inline or review-body issue this user already submitted, classify:

| status | meaning |
| --- | --- |
| `addressed` | thread resolved **or** current code no longer has the defect (quote/anchor stale and the failure path is gone) |
| `still_open` | unresolved and the defect still applies; re-anchor if the section moved |
| `stale` | outdated/unanchorable and not yet verified fixed — inspect current code this pass and upgrade to `addressed` or `still_open` |
| `reintroduced` | previously addressed (or not present at last review) and the update brings the defect back |

Do not reset `COMMENTS.md`. Mark prior submitted rows with the new status. Propose a new inline comment only for `still_open` / `reintroduced` that still meet the default bar, or for **new** defects on the update diff. Do not re-submit fingerprints already posted unless re-anchoring a `still_open` issue after approval. New GitHub wording follows SKILL.md rule 7 (self-contained; no claim ids or local artifact names).

Print a short **Prior comments** block in intake, after specialists, and in the walkthrough (full table in the walkthrough; counts elsewhere).

## Claims

Reuse confirmed claims when product intent is unchanged. Print them only as a one-line reminder, not a full re-confirmation gate.

Ask for confirmation only when the update adds, drops, or materially changes observable behavior — and only for those added/edited claims. Unchanged confirmed claims stay confirmed.

Walk only claims whose implementing sections appear in the update diff, plus any claim tied to a `still_open` / `reintroduced` comment. Note skipped unchanged claims as already reviewed at `prior_review_head_sha`.

## Phase constraints

- **Intake:** chat output is the update (commits, files, risk delta, claim delta, prior-comment counts), not a full-PR recap. Recompute `review_risk` from the **update** (raise if new higher-risk surfaces appear; do not lower a stored high rating just because this push is small).
- **Specialists:** inspect update sections and lingering prior-comment locations only. Write the usual artifacts; open with an `Update since <sha>` section. Do not re-derive findings on unchanged, already-reviewed code.
- **Skeptic:** run on new candidates and on `still_open` / `stale` / `reintroduced` prior items. Addressed items are out of scope unless the update reintroduces them.
- **Walkthrough:** show new/changed product code needed for judgment on the update; summarize tests added/changed in the update; include **Prior comments** with addressed vs still open. Next actions cover intent only for changed claims, plus new/still-open comments.
- **Submit:** review body must state this is a follow-up, the prior event/SHA, and prior-comment outcomes. New inline comments are only the newly approved ones.

## PRIOR_REVIEW.md

```markdown
---
review_scope: incremental
prior_review_id: <id>
prior_review_event: APPROVE | REQUEST_CHANGES | COMMENT
prior_review_head_sha: <sha>
current_head_sha: <sha>
---

# Prior review

## Update since last review
<commits, files, one-paragraph summary>

## Prior comments

| id | path | summary | status | note |
| --- | --- | --- | --- | --- |
```
