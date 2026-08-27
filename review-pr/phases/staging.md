# Phase 5 — Staging review

Before final submission, consolidate locally staged comments.

1. Re-fetch PR head once. If `head_sha` drifted, show what changed and ask before refreshing/re-reviewing affected artifacts.
2. Deduplicate comments by fingerprint and defect.
3. Revalidate that every comment:
   - is user-approved
   - has `high` confidence
   - is `blocker` or `recommended` unless broader feedback was requested
   - cites a changed path/range and still matches current code
   - has a concise, actionable, verbatim body
4. Present every proposed comment as a numbered item with path/range, severity, confidence, and full body. Do not replace the body with a summary.
5. Show open human prompts and the cumulative coverage summary.
6. If any changed lines remain `not_reviewed`, identify the ranges and ask whether to review or explicitly leave them uncovered.
7. Let the user approve all, reject all, or select comment numbers. Update `COMMENTS.md`.

No GitHub write occurs in this phase.
