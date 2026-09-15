# Phase 1 — Intake and business claims

## Intake

1. Accept a GitHub PR URL/number. If omitted, resume from the review workspace or ask for it.
2. Fetch with `gh`: title, body, author, state, draft status, base/head branches and SHAs, commits, changed files, full diff, review threads/comments, checks, the current GitHub user, and that user’s submitted reviews (`APPROVE` / `REQUEST_CHANGES` / `COMMENT`).
3. Create the review workspace and initialize the artifacts required by `SKILL.md`. Do not search Jira or other ticket trackers for product intent.
4. If this user already submitted a review, read `follow-up.md`, set `review_scope: incremental`, write `PRIOR_REVIEW.md`, and initialize coverage from the update diff. Otherwise `review_scope: full` and run:

   `gh pr diff <n> | python3 <skill-dir>/scripts/init_coverage.py --head-sha <head_sha> > <workspace>/COVERAGE.md`

   Incremental coverage (after fetch of both SHAs):

   `git diff <prior_review_head_sha>...<head_sha> | python3 <skill-dir>/scripts/init_coverage.py --head-sha <head_sha> > <workspace>/COVERAGE.md`

5. Identify:
   - core change: the few files/sections that can make the drafted claims (what the implementation did) true or false
   - incidental changes: generated files, lockfiles, formatting, styling, boilerplate, and unrelated mechanical edits
   - supporting core sections that matter to the implementation but need not become separate claims
   - change intent in three sentences: what the implementation did, plus PR/user expected results when they differ
   - `review_risk`: `low`, `medium`, or `high`, with concrete reasons from changed surfaces and affected boundaries
6. Persist `review_risk` and `review_risk_reasons` on `tasks.md`. Repeat the classification and reasons in `PR_BRIEF.md` so a cold resume does not re-derive them.
7. Write `PR_CONTEXT.md` and `PR_BRIEF.md`. Mark an incidental section `agent_reviewed_not_shown / peripheral_change` only after enough inspection to justify it.

## Review risk

Classify from the coverage inventory’s diff (full PR or update), not the PR’s self-description. If unsure, use `medium`. On `incremental`, recompute from the **update**; raise if new higher-risk surfaces appear; do not lower a stored `high` just because this push is small.

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

- Draft the fewest claims that cover what the implementation did. One is enough when the PR is a single behavior. Add more only for independently testable product assertions. Do not pad to a target count. Claims must state observable product behavior: actor, trigger/state, result, and important invariant.
- Infer those claims from the diff so they describe landed behavior. Use the PR and the user as expected results. Print them so the user can confirm what was done matches what they expected, or edit the claims.
- Cover every silent change to business logic or an existing flow with a drafted claim (including must-nots: no feature regression, no workaround around existing guardrails). Behavior-preserving refactors stay supporting/incidental.
- Never fetch Jira. If implementation and PR/user expected results disagree, draft the claim as what the code did, note the mismatch, and wait for confirmation.
- Attach the implementing sections that can make each claim true or false. Do not create claims to account for every diff region; classify other sections as supporting core code, incidental, or unexplained coverage.
- Print the changed-file tree (below) then every drafted claim in chat. Never require the user to open `BUSINESS_CLAIMS.md` to review them.
- Ask extra questions only when the diff is not enough to state the behavior that changed, or when expected vs done conflicts, and only when the answers materially change the verdict.
- Start phase 2 against the draft claims while waiting for confirmation (depth follows `review_risk`). If the user edits a claim, remap findings and rerun a specialist only when the edit materially changes its scope.
- Stop the logic walkthrough until the user confirms the claims (done matches expected) or answers every blocking gap. Then set `claims_confirmed: true` in `tasks.md`.
- On `incremental` follow-up: reuse unchanged confirmed claims without a new confirmation gate; print a one-line reminder plus **Prior comments** counts; confirm only new or silently changed behaviors. Classify core vs incidental on the **update** diff.

## Changed-file tree

Immediately **above** the first business claim in the claims-gate chat, print a nested directory tree of every changed path with `+adds` / `-deletes` per file and directory subtotals (from `gh`/`git` numstat). Include lockfiles and generated files so impact is honest; core vs incidental stays in the bullets.

- Full review: entire PR numstat.
- Incremental: **update** since last review only, plus a one-line full-PR totals reminder.

Do not repeat this tree in the walkthrough unless the user asks.

## Output

In at most four bullets, show the core change, what the implementation did vs any PR/user expected results, `review_risk` plus reasons, CI status, and initial section coverage (`changed_sections`, `added_lines`, `deleted_lines`). Then the changed-file tree, then every drafted claim verbatim. Ask the user to confirm the claims match expected results, or to edit them.

On `incremental`, those bullets are the **update since last review** (commits/files/risk delta/claim delta), plus prior-comment addressed vs still-open counts. Do not recap the already-reviewed base. The file tree is the update numstat.
