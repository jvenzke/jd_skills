# Follow-up review

Apply when the current GitHub user already submitted `APPROVE`, `REQUEST_CHANGES`, or `COMMENT` on this PR. This modifies phases 1–5; it is not a sixth task.

## Detect

Fetch the current user, their submitted reviews newest-first, and review threads/comments with resolved/outdated status. Pending reviews do not count. GitHub is source of truth.

If found, use the latest submitted review and set:

```yaml
review_scope: incremental
prior_review_id: <id>
prior_review_event: APPROVE | REQUEST_CHANGES | COMMENT
prior_review_head_sha: <review commit_id>
```

Write `PRIOR_REVIEW.md`. With no submitted review by this user, use `review_scope: full` even if others reviewed. Explicit “full re-review” also uses `full`. Pending reviews, issue comments, and unsubmitted inlines do not set scope.

## Scope

Review `prior_review_head_sha...head_sha`:

- initialize coverage from this update diff
- classify core/incidental, risk, specialists, skeptic, walkthrough, and new findings from update sections
- additionally inspect unresolved/stale prior-comment locations
- fetch full metadata for context, but do not re-present the reviewed base

For an empty update, report no new changes and re-check prior comments. Do not re-walk old code. Continue to submission only if the user wants another review event.

## Prior comments

Classify each prior issue:

| status | meaning |
| --- | --- |
| `addressed` | resolved or current code removes the failure |
| `still_open` | defect remains; re-anchor if needed |
| `stale` | unanchorable and not yet verified |
| `reintroduced` | update restores a previously absent/addressed defect |

Never reset `COMMENTS.md`. Apply `../comment-model.md` to new, still-open, reintroduced, or re-anchored findings. Do not edit posted threads in place or re-submit a fingerprint unless approved re-anchoring is needed.

Show prior-comment counts in the walkthrough preamble and the full status list before new comments.

## Claims

Reuse unchanged confirmed claims with a one-line reminder. Walk only affected claims and claims tied to still-open/reintroduced findings. Added, removed, or materially changed update behavior is walked as new or changed claims.

## Phase application

- **Intake:** update commits/files, risk delta, claim delta, and prior-comment counts; never lower stored high risk. Re-match the update's changed paths against `../redzones.md`; a new match adds to `redzone_paths` and existing matches stay.
- **Specialists:** update sections plus lingering comment locations; artifacts begin `Update since <sha>`.
- **Skeptic:** new candidates and still-open/stale/reintroduced prior items.
- **Walkthrough:** affected claims, update diffs (tests summarized unless asked), and prior-comment statuses. Red-zone sections in the update are shown in full.
- **Submit:** summary identifies prior event/SHA and comment outcomes; only newly approved comments post.

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
<commits, files, summary>

## Prior comments

| id | path | summary | status | note |
| --- | --- | --- | --- | --- |
```
