# Phase 1 — Intake and business claims

## Intake

1. Accept a GitHub PR URL/number. If omitted, resume from the review workspace or ask for it.
2. Fetch with `gh`: title, body, author, state, draft status, base/head branches and SHAs, commits, changed files, full diff, review threads/comments, and checks.
3. Discover ticket keys in this order: head branch, PR title, PR body, commit messages. If a Jira tool is available, fetch the primary ticket. Ask the user to choose only when multiple keys are credible.
4. Create the review workspace and initialize the artifacts required by `SKILL.md`.
5. Run:

   `gh pr diff <n> | python3 <skill-dir>/scripts/init_coverage.py --head-sha <head_sha> > <workspace>/COVERAGE.md`

6. Identify:
   - gravity center: 1–3 files/modules carrying the behavior change
   - peripheral changes: generated files, lockfiles, formatting, styling, boilerplate
   - change intent in three sourced sentences
   - risk areas and affected boundaries
7. Write `PR_CONTEXT.md` and `PR_BRIEF.md`. Mark a peripheral range `agent_reviewed_not_shown / peripheral_change` only after enough inspection to justify it.

## Business claims

Read `../business-claims.md`, then write `BUSINESS_CLAIMS.md`.

- Claims must state observable product behavior: actor, trigger/state, result, and important invariant.
- Source each claim from the ticket, PR, or user. Never infer product intent from implementation.
- Map each gravity-center hunk to at least one claim. Record unmapped behavior as a gap.
- Ask all independent blocking questions in one batch. Ask only questions whose answers materially change the review verdict.
- Stop until the user confirms the claims or answers every gap. Then set `claims_confirmed: true` in `tasks.md`.

## Output

In at most four bullets, show gravity center, ticket/intent, claim summary, CI status, and initial coverage. Ask for claim confirmation when required.
