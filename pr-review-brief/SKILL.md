---
name: pr-brief
description: Performs PR intake and topology mapping for the review workflow. Use first when reviewing a GitHub PR to snapshot metadata, branch-derived Jira context, checks, comments, diff files, and gravity-center files.
disable-model-invocation: true
---

# PR Brief

You are a Lead Architect. Build the mental map that later review phases can resume from in a fresh chat.

## Inputs

Accept a GitHub PR URL/number. If omitted, read the PR identity from `.working_items/pr-review/<pr-id>/STATE.md`.

## Tasks

1. Fetch live PR data with `gh`: title, body, author, base/head branches, `base_sha`, `head_sha`, changed files, diff, review threads, comments, commits, and check/status summary.
2. Discover Jira keys branch-first:
   - head branch name
   - PR title
   - PR body
   - commit messages
3. Fetch linked Jira context when available. Extract acceptance criteria, risk areas, stated non-goals, and status. If multiple primary ticket candidates exist, ask the user to choose.
4. Create `.working_items/pr-review/<owner>-<repo>-<pr-number>/` in the target repo.
5. Write:
   - `STATE.md`: PR URL, repo, PR number, base/head branch, `base_sha`, `head_sha`, phase status, artifact paths.
   - `PR_CONTEXT.md`: PR metadata, ticket context, CI/check summary, existing review comments, unresolved threads.
   - `PR_BRIEF.md`: gravity center, peripheral changes, review plan, risk notes.
   - `COVERAGE.md`: changed-line inventory initialized from the PR diff.
6. Identify:
   - Gravity center: the 1-3 files or modules with the most important behavior changes.
   - Peripheral changes: generated files, styling, boilerplate, config, and low-risk churn.
   - The Why: intent in 3 sentences.
7. For large PRs, propose risk-based file groups and review the gravity center first.
8. Mark obvious peripheral changed lines in `COVERAGE.md` as `agent_reviewed_not_shown` with reason `peripheral_change` only after inspecting enough context to confirm they are low risk.
9. Update `NEXT_CHAT_PROMPT.md`.

## Rules

- GitHub access is required because later phases need diff anchors for inline comments.
- Jira access is enrichment. If unavailable, record the missing context and continue with PR data.
- Do not review deeply in this phase. Map scope, risks, and the recommended next phase.
- If `.working_items/` is not ignored, tell the user and ask before changing `.gitignore`.
- Count changed lines from the PR diff, not full file line counts. Exclude binary files and mark generated files as `not_applicable` or `peripheral_change` with explanation.

## Output

Present the gravity center, peripheral changes, ticket context summary, check summary, initial changed-line count, and recommended next phase. Ask only for required decisions, such as primary ticket selection or large-PR scope.
