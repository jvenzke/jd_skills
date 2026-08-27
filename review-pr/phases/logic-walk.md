# Phase 4 — Claim-driven logic walkthrough

Walk confirmed claims one at a time in risk/dependency order:

1. contracts, schemas, migrations, interfaces
2. domain/service logic
3. APIs, controllers, jobs, events
4. persistence and integrations
5. UI/state flows
6. tests proving the behavior

Do not ask the user to select slices first. They may skip a claim.

## Per-claim loop

1. State the claim id and exact claim text.
2. Print every implementing changed range as a fenced code block using Cursor's code citation format (`startLine:endLine:path`). Show exact code and at most five surrounding context lines.
3. Explain the code's role in no more than two sentences.
4. Compare code, callers, tests, specialist evidence, and local patterns against the claim.
5. Present surviving findings. For each, include file/range, severity, confidence, concise rationale, and the verbatim GitHub comment body.
6. Ask whether the shown code matches the claim and whether to approve the numbered comments.
7. Wait for the user's response before walking the next claim.
8. Record the user's answer verbatim when it changes or clarifies a business claim.
9. Update `COMMENTS.md`, `HUMAN_REVIEW_PROMPTS.md`, `LOGIC_WALKTHROUGH.md`, `COVERAGE.md`, and `tasks.md`.

## Coverage presentation

Read `../coverage-protocol.md`. A range becomes `human_presented` only when its exact changed lines were printed in the current turn. A path/range mention does not count.

End every per-claim turn with:

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
