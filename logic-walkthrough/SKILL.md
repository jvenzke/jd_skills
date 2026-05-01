---
name: logic-walkthrough
description: Guides a risk-based PR logic review using story slices, proposed inline comments, and human review prompts for unclear business logic. Use after security and test review or when reviewing PR behavior.
disable-model-invocation: true
---

# Logic Walkthrough

You are a Staff Engineer. Review the PR as story slices, not as a raw full diff.

## Before Reviewing

Read `STATE.md`, `PR_CONTEXT.md`, `PR_BRIEF.md`, `SECURITY.md`, `TESTS.md`, `COMMENTS.md`, `HUMAN_REVIEW_PROMPTS.md`, and `COVERAGE.md` from `.working_items/pr-review/<pr-id>/`.

Fetch the live PR and compare the current `head_sha` to `STATE.md`. If it changed, summarize the change and ask whether to refresh affected artifacts before continuing.

## Slice Planning

Create a queue of 3-7 logic slices ordered by risk and dependency:

1. schema, interfaces, migrations, contracts
2. domain and service logic
3. API/controllers/jobs/events
4. persistence and integrations
5. UI/state flows
6. tests and observed behavior links

Show the slice queue and recommend which slices to walk first. Walk high-risk or user-selected slices one at a time.

## Review Each Slice

For each slice:

- show concise code references and a 2-sentence role summary
- inspect surrounding code and local patterns
- compare against PR/ticket intent and test evidence
- identify actionable findings
- identify technically valid but unclear business logic
- update `COVERAGE.md` for every changed line in the slice

Use read-only specialist subagents for complex slices, then verify their findings yourself.

## Output Lanes

### Proposed Inline Comments

Use for actionable, code-anchored feedback the PR author can resolve. Append to `COMMENTS.md` with source phase `logic-walkthrough`.

### Human Review Prompts

Use for business logic that looks technically okay but cannot be validated from code, tests, PR text, or ticket context. Append to `HUMAN_REVIEW_PROMPTS.md` with:

- prompt id
- code slice or anchor
- unclear assumption
- evidence checked
- focused question for the user
- user answer verbatim when answered
- status: `open`, `answered`, `converted_to_comment`, or `dismissed`

Do not post human review prompts to GitHub unless the user's answer reveals an actionable issue and the user approves the resulting inline comment.

## User Approval

Show proposed inline comments as a numbered list with file/line, severity, confidence, and exact wording. Let the user approve all, reject all, or select specific numbers.

Ask human review prompts in focused batches when they block understanding of an important slice. Record answers verbatim.

Stage approved comments locally in `COMMENTS.md`. Do not post to GitHub.

Mark any changed lines shown in walkthrough slices, inline comment approvals, or human review prompts as `human_presented`.

Mark changed lines reviewed by the agent but not shown as `agent_reviewed_not_shown` with a reason group:

- `covered_by_tests_or_ci`
- `covered_by_pattern_match`
- `covered_by_static_review`
- `duplicate_or_mechanical`
- `peripheral_change`
- `superseded_or_unchanged_context`

End by updating `LOGIC_WALKTHROUGH.md`, `COVERAGE.md`, and `NEXT_CHAT_PROMPT.md`.
