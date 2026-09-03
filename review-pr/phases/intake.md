# Phase 1 — Intake and business claims

## Intake

1. Accept a GitHub PR URL/number. If omitted, resume from the review workspace or ask for it.
2. Fetch with `gh`: title, body, author, state, draft status, base/head branches and SHAs, commits, changed files, full diff, review threads/comments, and checks.
3. Create the review workspace and initialize the artifacts required by `SKILL.md`. Do not search Jira or other ticket trackers for product intent.
4. Run:

   `gh pr diff <n> | python3 <skill-dir>/scripts/init_coverage.py --head-sha <head_sha> > <workspace>/COVERAGE.md`

5. Identify:
   - core change: the few files/ranges that can make the stated product intent true or false
   - incidental changes: generated files, lockfiles, formatting, styling, boilerplate, and unrelated mechanical edits
   - supporting core ranges that matter to the implementation but need not become separate claims
   - change intent in three sourced sentences
   - risk areas and affected boundaries
6. Write `PR_CONTEXT.md` and `PR_BRIEF.md`. Mark an incidental range `agent_reviewed_not_shown / peripheral_change` only after enough inspection to justify it.

## Business claims

Read `../business-claims.md`, then write `BUSINESS_CLAIMS.md`.

- Draft 1–3 claims for the entire PR. Claims must state observable product behavior: actor, trigger/state, result, and important invariant.
- Source each claim from the PR or user. Never infer product intent from implementation. Never fetch Jira.
- Attach the implementing ranges that can make each claim true or false. Do not create claims to account for every diff region; classify other ranges as supporting core code, incidental, or unexplained coverage.
- Print every drafted claim in chat. Never require the user to open `BUSINESS_CLAIMS.md` to review them.
- Ask extra questions only when the PR and user do not provide enough intent to form the claims, and only when the answers materially change the verdict.
- Launch SECURITY and test-coverage specialists against the draft claims while waiting for confirmation. If the user edits a claim, remap findings and rerun a specialist only when the edit materially changes its scope.
- Stop the logic walkthrough until the user confirms the claims or answers every blocking gap. Then set `claims_confirmed: true` in `tasks.md`.

## Output

In at most four bullets, show the core change, PR intent, all 1–3 claims verbatim, CI status, and initial coverage. Ask for a short confirmation or edits.
