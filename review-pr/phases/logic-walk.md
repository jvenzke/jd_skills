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

## Walkthrough

1. Repeat every claim id and exact claim text in chat. Never require the user to open `BUSINESS_CLAIMS.md`.
2. For each claim, print the changed **product** ranges needed to prove or disprove it as fenced code blocks using Cursor's code citation format (`startLine:endLine:path`). Include at most five surrounding context lines.
3. Print every changed product range that anchors a proposed comment, even if the range was already summarized elsewhere.
4. For changed tests, do not print source. Summarize in chat: file, scenario/setup, assertions, and which claim or branch it covers.
5. Explain how the shown path implements the claim and compare product code, callers, summarized tests, specialist evidence, and local patterns against it.
6. Inspect the rest of the core change and summarize its role and disposition. Do not paste every changed line merely to make coverage line-complete.
7. Present surviving findings as a single numbered comment list. For each, include file/range, severity, confidence, concise rationale, and the exact proposed GitHub body.
8. By default, include only `high` confidence `blocker` or `recommended` findings with a concrete consequence: broken logic, unintended behavior, security risk, or a material test gap. Exclude nits unless the user requested them.
9. Present unresolved product intent as chat questions and record them in `HUMAN_REVIEW_PROMPTS.md`; do not turn ambiguity into an inline comment.
10. Ask once whether the shown implementation matches all claims and which comments to approve, reject, or edit. Wait for the user's response.
11. Record the user's answer verbatim when it changes or clarifies a business claim. Update `COMMENTS.md`, `HUMAN_REVIEW_PROMPTS.md`, `LOGIC_WALKTHROUGH.md`, `COVERAGE.md`, and `tasks.md`.

## Coverage presentation

Read `../coverage-protocol.md`. A **product** range becomes `human_presented` only when its exact changed lines were printed in the current turn. A path/range mention does not count. Test ranges are summarized in this turn and marked `agent_reviewed_not_shown` / `test_summarized_in_chat`. Other inspected core ranges may be summarized and marked `agent_reviewed_not_shown` / `covered_by_static_review`. Incidental changes use the most specific agent-only reason.

End the walkthrough turn with:

```markdown
| this turn | lines | % of PR |
| --- | ---: | ---: |
| shown in chat | N | N% |
| agent-only — <reason> | N | N% |
| still not reviewed | N | N% |
```

Recompute cumulative totals in `COVERAGE.md`; do not estimate.

## Output lanes

- Actionable, code-anchored issue → proposed comment in `COMMENTS.md`.
- Technically valid but unclear business behavior → `HUMAN_REVIEW_PROMPTS.md`.
- Clean code → mark coverage and continue; do not manufacture feedback.
