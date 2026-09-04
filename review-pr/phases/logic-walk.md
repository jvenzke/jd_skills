# Phase 4 — Intent-complete logic walkthrough

Walk all confirmed claims in one turn by default, ordered by risk/dependency:

1. contracts, schemas, migrations, interfaces
2. domain/service logic
3. APIs, controllers, jobs, events
4. persistence and integrations
5. UI/state flows
6. tests proving the behavior (prose summary only; do not paste test source)

Do not ask the user to select slices first. They may skip a claim. Never split merely because there are two or three claims.

Split into another turn only when the user asks or the claim paths plus commented ranges would be unreadable in one response (normally more than four core files or an unusually large paste). Explain the split before pausing.

Primary human-review units are the **claim**, important design/boundary decision, unresolved ambiguity, and surviving finding—not the raw hunk. Do not paste large implementation spans merely to raise `human_presented`.

## Walkthrough

1. Repeat every claim id and exact claim text in chat. Never require the user to open `BUSINESS_CLAIMS.md`.
2. For each confirmed claim, use this structure:
   - claim text
   - implementation path the agent traced (files/symbols/flow; cite ranges in prose)
   - tests/evidence supporting it (prose only for tests)
   - architecture/boundary changes that materially matter
   - residual uncertainty
   - surviving findings, if any
3. Show exact changed **product** code as fenced blocks using Cursor's code citation format (`startLine:endLine:path`) when it is useful for human judgment, especially when:
   - a proposed finding needs human evaluation
   - an important public/module boundary changed
   - product intent is ambiguous
   - the user asks to expand the path
   - direct inspection is necessary to confirm a design decision
   Include at most five surrounding context lines. A path/line reference alone is not `human_presented`.
4. Print every changed product range that anchors a proposed comment, even if the path was already summarized.
5. For changed tests, do not print source. Summarize in chat: file, scenario/setup, assertions, and which claim or branch it covers.
6. Print a **Test coverage of new code** block: which new/changed product behaviors are covered by which tests (prose), and which new ranges, branches, or claims are uncovered. Print a **CI workflow scope** block: which GitHub workflows/jobs run on this PR and whether they execute the tests that impact this project (path filters, package selectors, skipped jobs).
7. Compare the traced path, callers, summarized tests, specialist evidence (including QUALITY.md correctness and maintainability), and local patterns against the claim.
8. If `review_risk` is `high` (or a medium PR still reshaped a public/module boundary), include a **Boundary decisions** block: what changed at the boundary, why it matters, residual risk. The user confirms this in the same walkthrough turn—no extra gate.
9. Inspect remaining core hunks and summarize role and disposition. Do not paste every changed hunk to make coverage hunk-complete.
10. Present surviving findings as a single numbered comment list. For each, include file/range, severity, confidence, concise rationale, and the exact proposed GitHub body.
11. By default, include only `high` confidence `blocker` or `recommended` findings with a concrete consequence: broken logic, unintended behavior, security risk, a material test gap (including CI that never runs this project's tests), or a maintainability regression with a concrete fix direction. Exclude nits unless the user requested them.
12. Present unresolved product intent as chat questions and record them in `HUMAN_REVIEW_PROMPTS.md`; do not turn ambiguity into an inline comment.
13. Ask once whether the shown implementation matches all claims (and boundary decisions when presented) and which comments to approve, reject, or edit. Wait for the user's response.
14. Record the user's answer verbatim when it changes or clarifies a business claim. Update `COMMENTS.md`, `HUMAN_REVIEW_PROMPTS.md`, `LOGIC_WALKTHROUGH.md`, `COVERAGE.md` (including Human oversight), and `tasks.md`.

## Coverage presentation

Read `../coverage-protocol.md`. A **product** hunk becomes `human_presented` only when its exact changed lines were printed in the current turn. That is exposure, not proof of review. Test hunks are summarized in this turn and marked `agent_reviewed_not_shown` / `test_summarized_in_chat`. Other inspected core hunks may be summarized and marked `agent_reviewed_not_shown` / `covered_by_static_review`. Incidental changes use the most specific agent-only reason.

End the walkthrough turn with presentation totals **and** oversight (do not treat shown hunks as the human-review score):

```markdown
| this turn | hunks | % of PR |
| --- | ---: | ---: |
| shown in chat (`human_presented`) | N | N% |
| agent-only — <reason> | N | N% |
| still not reviewed | N | N% |

### Human oversight
- claims confirmed:
- architecture/boundary decisions reviewed:
- findings approved/rejected/edited:
- unresolved business questions answered:
```

Recompute cumulative totals in `COVERAGE.md`; do not estimate. Displayed hunks are not the primary measure of meaningful human review.

## Output lanes

- Actionable, code-anchored issue → proposed comment in `COMMENTS.md`.
- Technically valid but unclear business behavior → `HUMAN_REVIEW_PROMPTS.md`.
- Clean code → mark coverage and continue; do not manufacture feedback.
