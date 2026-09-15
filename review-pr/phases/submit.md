# Phase 5 — Submit

## Validate

1. Fetch the live PR and compare `head_sha` with `tasks.md`. If changed, summarize and refresh without waiting. Apply [`follow-up.md`](follow-up.md) when incremental.
2. Apply [`../comment-model.md`](../comment-model.md): validate approved anchors against the current diff, deduplicate fingerprints/defects, skip submitted fingerprints, and revalidate evidence, confidence, severity, scope, and public wording.
3. For stale anchors, show nearby current diff and stop with `**Next:** re-anchor, convert to a top-level note, or drop.`
4. If migrations or ordered deploy steps exist, require the PR body or linked release notes to state migration order, merge-vs-deploy timing, and rollback. Treat scripts as likely run only in dev. Missing instructions remain or become a blocker. Otherwise record “no ordered migration/deploy steps.”
5. Resolve or explicitly explain every remaining `not_reviewed` section before asking for a review type.
6. Only eligible, user-approved comments post inline. The summary body always posts.

## Review event

Recommend:

- `REQUEST_CHANGES` when any submitted inline comment is a `blocker`
- `APPROVE` when no blocker remains and the user is ready to sign off
- `COMMENT` when feedback is non-blocking, questions remain, or the user does not want to approve/block

`future_work` never drives `REQUEST_CHANGES`. The recommendation does not authorize a write.

## Review body

Always post a concise top-level summary in addition to inline comments:

```markdown
## Review summary

**Verdict:** <approve | request changes | comment>
**Review risk:** <low | medium | high> — <reasons>

### What was reviewed
<behaviors checked and residual uncertainty in product terms>

### Presentation
- Changed sections: N (added lines: N, deleted lines: N)
- Shown in chat (`human_presented`): N (N%) — code exposure only
- Agent-reviewed only: N (N%) — <reason mix>
- Not reviewed: N (N%) — <none or explanation>

### Test coverage of new code
<covered new/changed behavior, gaps, and residual test risk>

### CI workflow scope
<whether PR workflows/jobs execute this project's impacting tests and any selector/filter gaps>

### Deploy / migration order
<documented order/timing/rollback, or “no ordered migration/deploy steps”>

Inline comments below are separate findings.
```

Do not paste code or use claim ids/local artifact names. Presentation is exposure, not Human review. For incremental review, add **Follow-up** with prior event/SHA and addressed/still-open/stale/reintroduced counts in product language; presentation values cover the update diff.

## Review type gate

Show:

- exact review body
- every inline comment, numbered, with path/range, comment-model chat snippet, severity, confidence, and exact public body; say “none” when empty
- unresolved business prompts
- section totals, status percentages, excluded count, and Human oversight from `COVERAGE.md`
- clearly labeled recommended event

Re-paste bodies; do not point to an earlier turn. Ask only:

```markdown
Submit as which review type?
1. Approve PR (`APPROVE`)
2. Request changes (`REQUEST_CHANGES`)
3. Comment (`COMMENT`)
```

Invite comment edits in the same turn. Apply `comment-model.md`, re-show affected bodies, and ask again. Naming one type authorizes the write; walkthrough approval does not.

## Submit

Create one GitHub review containing the summary, chosen event, and eligible inline comments. Always submit the review, even with no inline comments.

If an inline anchor fails after authorization, do not move all comments into the body. Re-anchor it or post only that finding as a separate top-level note after resolving the stale-anchor stop; the note still follows `comment-model.md`.

Write `SUBMISSION.md` with:

- PR/head SHA and review URL/id
- risk/reasons, chosen event, and exact body
- submitted comment ids/fingerprints, duplicates, and stale anchors
- security, logic/quality, test coverage, CI scope, and deploy/migration summaries
- claims walked and unresolved prompts
- presentation totals/reasons and Human oversight
- incremental prior-review identity and comment outcomes when applicable

Set `phase: complete`, complete all tasks, and do not delete artifacts without separate approval.
