# Skills for Cursor

Author: Joel DeVenzke

Some skills are inspired by Matt Pocock's [Skills for Real Engineers](https://github.com/mattpocock/skills/tree/main).

## References

- [Interesting talk on AI development and the importance of good coding practices](https://youtu.be/v4F1gFy-hqg?si=1opnC2coaZ8HVh7v)
- [Longer walkthrough](https://github.com/jvenzke/jd_skills/tree/main)

## General Skills

- [`/grill-me`](grill-me/SKILL.md): Stress-test a plan or design with one question at a time until the agent and user share a clear understanding.
- [`/caveman`](caveman/SKILL.md): Switch to ultra-compressed communication to reduce token usage.

## Development Workflow (WIP/Not tested)

1. [`/grill-me`](grill-me/SKILL.md): Resolve the design tree for a problem or project.
2. [`/to-prd`](to-prd/SKILL.md): Turn the current conversation and codebase understanding into a PRD under `.working_items/`.
3. [`/prd-to-issue-files`](prd-to-issue-files/SKILL.md): Break an approved PRD into ordered, vertical-slice issue markdown files.

## PR Review Workflow (WIP)

Use this workflow to review GitHub PRs across fresh chats without losing context. Review state is written under `.working_items/pr-review/<owner>-<repo>-<pr-number>/` in the target repo, and each phase updates `NEXT_CHAT_PROMPT.md` so the next chat can resume cleanly.

1. [`/review-pr`](review-pr/SKILL.md): Orchestrate or resume the PR review workflow, choose the next phase, and maintain the shared artifact contract.
2. [`/pr-brief`](pr-brief/SKILL.md): Snapshot PR metadata, branch-first Jira context, CI/check status, comments, diff files, gravity-center files, peripheral changes, and the recommended review plan.
3. [`/scan-security`](scan-security/SKILL.md): Review the diff for evidence-backed security risks, toxic patterns, auth changes, sensitive data exposure, and dependency risk.
4. [`/verify-tests`](verify-tests/SKILL.md): Use GitHub Actions/check results first, then inspect test quality, changed branch coverage, assertion strength, and regression coverage. Run targeted local tests only when useful.
5. [`/logic-walkthrough`](logic-walkthrough/SKILL.md): Walk risk-based story slices, propose actionable inline comments, and create `human_review_prompts` for unclear business logic that needs human judgment.
6. [`/submit-pr-review`](submit-pr-review/SKILL.md): Validate approved comment anchors against the latest diff and submit one GitHub review with inline comments. Use a minimal review body unless blockers or cross-cutting context need a short summary.

Approved comments are staged locally until `/submit-pr-review`; they should become GitHub inline review comments, not a summary-only PR comment. Jira ticket discovery checks the PR branch name first, then title, body, and commits. Unresolved human review prompts are carried forward across chats and are not posted unless they become actionable comments.

The workflow also tracks changed-line review coverage in `COVERAGE.md`. `/submit-pr-review` reports what percent of changed lines were presented to the human reviewer, what percent were reviewed only by the agent, and any unreviewed remainder. Agent-covered lines are grouped by why they were not shown, such as peripheral change, covered by tests/CI, matching an inspected pattern, duplicate mechanical change, static-review-only, or stale/superseded context.

## Research Agent Workflow (WIP)

1. [`/generate-research-project`](generate-research-project/SKILL.md): Start from a Jira ticket or linked README, optionally create a git branch, and build the project scaffold:
   - `README.md`
   - `RESEARCH_PLAN.md`
   - `results/`
   - `research_tasks/`
2. [`/research-plan`](research-plan/SKILL.md): Interview the user and explore the codebase as needed to produce:
   - `RESEARCH_PLAN.md`
   - `RESEARCH_PLAN_PITCH_DECK.html`
3. Repeat the research loop until the plan converges:
   - [`/to-research-tasks`](to-research-tasks/SKILL.md): Convert the current plan and compressed workspace context into the smallest unblocked task set, usually one AFK-ready task and never more than three, including the review artifacts each task must preserve.
   - [`/do-research`](do-research/SKILL.md): Execute one approved task in a scoped task folder, write modular analysis code, generate Plotly PNGs and review artifacts, and log findings in `results_log_{idx}_{name}.md`.
   - [`/review-research`](review-research/SKILL.md): Review the latest task results with the user, decide whether the work has converged, build or update `RESEARCH_REVIEW.html`, compress completed work into `research_workspace/`, archive completed raw task materials, update the pitch deck, and update `RESEARCH_PLAN.md`.
   - Optional [`/commit-research`](commit-research/SKILL.md): Stage only the minimal reviewable and reproducible research files after review checkpoints. Do not commit unless explicitly asked.
4. [`/summarize-research`](summarize-research/SKILL.md): Build the final production handoff in `/results`, including the executive summary, production-ready SQL/Python snippets, final assets, presentation webpage, and project README updates.
