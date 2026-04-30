---
name: review-pr
description: Orchestrates and resumes a fresh-chat GitHub PR review workflow. Use when starting, resuming, or deciding the next phase of a PR review with inline comments, Jira context, CI checks, and persisted review artifacts.
---

# Review PR

You are the PR review orchestrator. Keep the workflow resumable across fresh chats by reading and writing review artifacts under the target repository.

## Core Contract

- Use GitHub PR data as the source of truth. Require a PR URL/number or read it from the review workspace.
- Store review state in `.working_items/pr-review/<owner>-<repo>-<pr-number>/` at the target repo root.
- Each phase must be independently runnable from the artifacts in that folder.
- Approved review comments are staged locally first. Do not post them until `/submit-pr-review`.
- End every phase by updating and displaying `NEXT_CHAT_PROMPT.md`.
- If the PR `head_sha` changed since the artifact snapshot, summarize the change and ask whether to refresh affected artifacts before continuing.
- Use read-only specialist subagents for deep dives when the PR is non-trivial; the main agent owns verification, artifacts, and user approvals.

## Default Phase Order

1. `/pr-brief`
2. `/scan-security`
3. `/verify-tests`
4. `/logic-walkthrough`
5. `/submit-pr-review`

Allow entry into any phase when the review workspace already exists.

## Artifact Set

Use Markdown with YAML frontmatter when creating or updating:

- `STATE.md`
- `PR_CONTEXT.md`
- `PR_BRIEF.md`
- `SECURITY.md`
- `TESTS.md`
- `LOGIC_WALKTHROUGH.md`
- `COMMENTS.md`
- `HUMAN_REVIEW_PROMPTS.md`
- `COVERAGE.md`
- `NEXT_CHAT_PROMPT.md`
- `SUBMISSION.md`

## Comment Model

Proposed comments must include:

- stable fingerprint from PR number, `head_sha`, path, line/diff position, and normalized comment text
- path and diff anchor
- source phase
- severity: `blocker`, `recommended`, `nit`, or `question`
- confidence: `high`, `medium`, or `low`
- exact proposed comment text
- anchor validation status
- approval status

Only actionable, code-anchored, user-approved comments should be submitted to GitHub.

## Human Review Prompts

Track technically valid code that contains unclear business logic separately from PR comments. Store prompts in `HUMAN_REVIEW_PROMPTS.md` with:

- prompt id
- code slice or anchor
- unclear assumption
- evidence checked
- focused question for the user
- user answer verbatim
- status: `open`, `answered`, `converted_to_comment`, or `dismissed`

Warn about unresolved prompts before final submission, but do not block submission by default.

## Review Coverage Accounting

Track changed-line review coverage in `COVERAGE.md` so the user can see what percent of the PR they personally reviewed versus what the agent reviewed without showing.

For every changed line or compact changed-line range, record:

- path and line/range
- source hunk or diff anchor
- status: `human_presented`, `agent_reviewed_not_shown`, `not_reviewed`, or `not_applicable`
- phases that inspected it
- if shown, the slice or prompt where it was presented
- if not shown, a reason group

Use these reason groups for agent-covered lines that were not shown:

- `peripheral_change`: boilerplate, config, styling, formatting, generated code, or low-risk churn
- `covered_by_tests_or_ci`: behavior was adequately covered by CI, targeted tests, or existing tests
- `covered_by_pattern_match`: matches an established local pattern already inspected elsewhere
- `covered_by_static_review`: reviewed directly by the agent with no human judgment needed
- `duplicate_or_mechanical`: repeated equivalent changes already represented by a shown slice
- `superseded_or_unchanged_context`: context line, moved code, or change no longer relevant after refresh
- `low_risk_dependency`: dependency or lockfile change with clean repo-native checks

At final submission, report:

- total changed lines considered
- percent human-presented
- percent agent-reviewed but not shown
- percent not reviewed, if any
- agent-reviewed lines grouped by reason with counts and percentages

## Next Chat Prompt

After each phase, write `NEXT_CHAT_PROMPT.md` with:

- PR URL
- review workspace path
- completed phases
- current `base_sha` and `head_sha`
- next recommended skill
- unresolved approvals
- unresolved human review prompts
- current review coverage summary
- one concise instruction the user can paste into a new chat
