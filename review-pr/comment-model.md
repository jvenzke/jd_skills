# Comment model

The main agent writes every GitHub-facing finding. Specialists return structured evidence only.

## Local record

Each `COMMENTS.md` entry contains:

- stable fingerprint from PR, `head_sha`, path, optional diff position, and normalized body
- path/range and exact quoted code
- source phase and claim id when applicable
- severity and confidence from `phases/skeptic.md`
- concrete trigger, execution path, consequence, and fix direction
- verbatim GitHub body
- placement (`inline` or `summary`), anchor when inline, approval, prior-comment, and submission status

Never delete `COMMENTS.md` on resume or SHA change. Re-anchor or invalidate entries; preserve user-approved wording until the user drops it.

## Public wording

GitHub review bodies, inline comments, and fallback top-level finding notes are public and self-contained. Never expose claim ids, `.working_items/` paths, local artifact names, skill paths, or pointers to chat walkthroughs, coverage, or Human oversight. Restate expected product behavior in prose.

Every inline finding and fallback finding note uses exactly:

```markdown
## Issue

<expected behavior, trigger, and practical consequence in product language>

## Proposed fix

<one concise, actionable change; name files/functions only when useful>
```

Both headings must be present and non-empty. Do not add unlabeled sections, a code/snippet heading, or a menu of fixes. The top-level review summary does not use this template.

When proposing, editing, or re-showing an inline comment in chat, put the GitHub-anchored `@@` hunk in that numbered block (with path/range, severity, confidence, and public body). Use a fenced `diff` from `git diff <coverage_base>...<head_sha>`: removed lines, ≤5 context; shrink a huge hunk to the failing statements plus that context. Add at most one extra hunk when the consequence is off the anchor. Do not paste test source; for CI/workflow findings show the selector/job hunk. For unanchored `future_work`, show the affected path/range, severity, confidence, `summary` placement, and exact proposed summary text without inventing an `@@` hunk.

For `future_work`, **Issue** describes today's limitation and states either that the PR did not introduce or worsen the pre-existing defect or that the requested capability is beyond the confirmed slice. **Proposed fix** describes the later work and why it is outside this PR. Missing or contradicted confirmed behavior is an in-scope defect, never `future_work`.

`future_work` never drives `REQUEST_CHANGES`. Prominently label verified pre-existing security-boundary, corruption, tenant-isolation, or data-loss risks as urgent and recommend immediate separate remediation, while keeping the PR verdict based on effects caused or worsened by this PR.

## Eligibility

Only user-approved, currently valid findings may be submitted. Inline comments also require a current changed-line anchor. By default propose:

- `high` confidence `blocker` or `recommended` findings that survive `phases/skeptic.md` and have a concrete correctness, behavior, security, test-coverage, CI-scope, or maintainability consequence
- concrete `future_work` beyond this PR's slice, including verified actionable defects that pre-date the PR without being worsened or newly exposed by it

Exclude nits unless requested. Route unresolved product intent to `HUMAN_REVIEW_PROMPTS.md`, not an inline comment.

Put `future_work` inline when it has a natural changed-line anchor. Put valid unanchored `future_work` in the top-level review summary instead; do not force an unrelated anchor or drop it. Each summary item states the limitation, why it is outside this PR, and the concrete follow-up in self-contained product language. The same finding appears in only one place.

Rewrite user-added or edited inline/fallback wording into the template; rewrite summary `future_work` into the summary-item form above. Re-show it before submission. At submit, deduplicate by fingerprint and defect, skip already-submitted fingerprints, and revalidate anchors and eligibility.
