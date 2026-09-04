# Phase 1 — Intake and business claims

## Intake

1. Accept a GitHub PR URL/number. If omitted, resume from the review workspace or ask for it.
2. Fetch with `gh`: title, body, author, state, draft status, base/head branches and SHAs, commits, changed files, full diff, review threads/comments, and checks.
3. Create the review workspace and initialize the artifacts required by `SKILL.md`. Do not search Jira or other ticket trackers for product intent.
4. Run:

   `gh pr diff <n> | python3 <skill-dir>/scripts/init_coverage.py --head-sha <head_sha> > <workspace>/COVERAGE.md`

5. Identify:
   - core change: the few files/hunks that can make the stated product intent true or false
   - incidental changes: generated files, lockfiles, formatting, styling, boilerplate, and unrelated mechanical edits
   - supporting core hunks that matter to the implementation but need not become separate claims
   - change intent in three sourced sentences
   - `review_risk`: `low`, `medium`, or `high`, with concrete reasons from changed surfaces and affected boundaries
6. Persist `review_risk` and `review_risk_reasons` on `tasks.md`. Repeat the classification and reasons in `PR_BRIEF.md` so a cold resume does not re-derive them.
7. Write `PR_CONTEXT.md` and `PR_BRIEF.md`. Mark an incidental hunk `agent_reviewed_not_shown / peripheral_change` only after enough inspection to justify it.

## Review risk

Classify from the diff, not the PR’s self-description. If unsure, use `medium`.

Higher-risk surfaces (any one can raise above `low`; several, or a trust/data/money boundary, usually mean `high`):

- authentication / authorization
- security or trust boundaries
- persistence, schemas, migrations, or destructive data changes
- concurrency / state coordination
- public APIs, external contracts, or compatibility-sensitive boundaries
- money, billing, permissions, tenant isolation, or sensitive data
- broad cross-module orchestration

**low**: docs, copy, isolated styling, lockfile-only, or a small self-contained change with no higher-risk surface.

**medium**: default. Typical product logic without the high list, or mixed incidental + moderate core.

**high**: one or more higher-risk surfaces above, especially across modules.

Do not lower a rating to save work. Risk controls specialist depth in phase 2; it does not skip claims, walkthrough, or submit gates.

## Business claims

Read `../business-claims.md`, then write `BUSINESS_CLAIMS.md`.

- Draft 1–3 claims for the entire PR. Claims must state observable product behavior: actor, trigger/state, result, and important invariant.
- Source each claim from the PR or user. Never infer product intent from implementation. Never fetch Jira.
- Attach the implementing hunks that can make each claim true or false. Do not create claims to account for every diff region; classify other hunks as supporting core code, incidental, or unexplained coverage.
- Print every drafted claim in chat. Never require the user to open `BUSINESS_CLAIMS.md` to review them.
- Ask extra questions only when the PR and user do not provide enough intent to form the claims, and only when the answers materially change the verdict.
- Start phase 2 against the draft claims while waiting for confirmation (depth follows `review_risk`). If the user edits a claim, remap findings and rerun a specialist only when the edit materially changes its scope.
- Stop the logic walkthrough until the user confirms the claims or answers every blocking gap. Then set `claims_confirmed: true` in `tasks.md`.

## Output

In at most four bullets, show the core change, PR intent, `review_risk` plus reasons, all 1–3 claims verbatim, CI status, and initial hunk coverage (`changed_hunks`, `added_lines`, `deleted_lines`). Ask for a short confirmation or edits.
