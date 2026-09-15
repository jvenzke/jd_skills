# Comment model

The main agent writes every GitHub-facing finding. Specialists return structured evidence only.

## Local record

Each `COMMENTS.md` entry contains:

- stable fingerprint from PR, `head_sha`, path, diff position, and normalized body
- path/range and exact quoted code
- source phase and claim id when applicable
- severity and confidence from `phases/skeptic.md`
- concrete trigger, execution path, consequence, and fix direction
- verbatim GitHub body
- anchor, approval, prior-comment, and submission status

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

When proposing, editing, or re-showing a comment in chat, put the GitHub-anchored `@@` hunk in that numbered block (with path/range, severity, confidence, and public body). Use a fenced `diff` from `git diff <coverage_base>...<head_sha>`: removed lines, ≤5 context; shrink a huge hunk to the failing statements plus that context. Add at most one extra hunk when the consequence is off the anchor. Do not paste test source; for CI/workflow findings show the selector/job hunk.

For `future_work`, **Issue** describes today's limitation; **Proposed fix** describes the later work and why it is outside this PR. `future_work` never drives `REQUEST_CHANGES` and must not disguise an in-scope defect.

## Eligibility

Only user-approved, currently valid and anchored comments may be submitted. By default propose:

- `high` confidence `blocker` or `recommended` findings that survive `phases/skeptic.md` and have a concrete correctness, behavior, security, test-coverage, CI-scope, or maintainability consequence
- concrete `future_work` beyond this PR's slice

Exclude nits unless requested. Route unresolved product intent to `HUMAN_REVIEW_PROMPTS.md`, not an inline comment.

Rewrite user-added or edited wording into the template and re-show it before submission. At submit, deduplicate by fingerprint and defect, skip already-submitted fingerprints, and revalidate anchors and eligibility.
