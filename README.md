# Skills for Cursor

Author: Joel DeVenzke

Some skills are inspired by Matt Pocock's [Skills for Real Engineers](https://github.com/mattpocock/skills/tree/main).

## References

- [Interesting talk on AI development and the importance of good coding practices](https://youtu.be/v4F1gFy-hqg?si=1opnC2coaZ8HVh7v)
- [Longer walkthrough](https://youtu.be/-QFHIoCo-Ko?si=d8P-EoPUrC0qJa_L)

## Authoring Principles

The [`/meta-review`](meta-review/SKILL.md) skill is the source of truth for what "good" looks like; it is what evaluates new and existing skills against the criteria below. Run it after any workflow or skill change so issues get logged in `meta-review/problems.md` and the skills evolve.

### Writing a Skill

- The frontmatter `description` is the trigger contract. Make it specific enough that the agent can decide whether to read the skill from the description alone, including cue phrases the user is likely to say.
- Keep each `SKILL.md` under 40 actionable directives. Count numbered steps and bullets; ignore frontmatter, headings, examples, and reference links. If you cannot fit the work in 40 directives after compression, split the skill.
- One skill, one job. Split when a skill has independent triggers or workflows. Merge when two skills are always invoked together, share decision logic, and have no meaningful independent use.
- Stay orthogonal. Communicate with upstream and downstream skills through stable artifacts (named files, sections, manifests), not implicit chat state. A skill should be resumable in a fresh chat by reading those artifacts.
- Don't repeat yourself. If two skills share the same interview, decision tree, or output format, reference the canonical skill instead of duplicating it.
- Be terse. Every bullet should carry weight; cut narration, restatement, and obvious commentary. Compress before adding.
- Gate irreversible work behind explicit user approval (file moves, deletions, commits, pushes, schema changes, network calls).
- Use a consistent shape: short intent statement, numbered workflow, small set of rules, and an explicit out-of-scope or exit section when useful. [`publish-research`](publish-research/SKILL.md) is the reference for multi-step skills; [`grill-me`](grill-me/SKILL.md) is the reference for single-purpose skills.
- Set `disable-model-invocation: true` for skills that should only be invoked explicitly by the user (see [`meta-review`](meta-review/SKILL.md)).

### Developing a Workflow

- Each step in a workflow should map to one skill with one clear output artifact. Skills must not spill into the next step's responsibility.
- Define the artifact contract between steps explicitly (file names, folder layout, section headings, manifests). Downstream skills depend on the artifact, not on chat memory.
- Persist workflow state in a known location so any step can be resumed cold (e.g., `.working_items/`, `research_workspace/`, the research project folder).
- Include a loop step and a convergence/exit criterion when the workflow is iterative (plan → execute → review → compress).
- List the workflow in this README with numbered steps, a `Last updated` date, and an explicit status tag (e.g., `Currently untested`) so consumers know how much to trust it.
- After running a new workflow end-to-end, invoke [`/meta-review`](meta-review/SKILL.md) to capture missed steps, bloat, duplication across skills, and split/merge candidates before the next iteration.

## General Skills

- [`/grill-me`](grill-me/SKILL.md): Stress-test a plan or design with one question at a time until the agent and user share a clear understanding.
- [`/meta-review`](meta-review/SKILL.md): Review how skills performed in the current chat, propose compact improvements, and log approved recurring problems.

## Shared Specs

- [`research-portal`](research-portal/SKILL.md): Rendering spec for every static HTML surface produced by the research workflow (pitch deck, `RESEARCH_REVIEW.html`, leaf review artifacts, final presentation page). Defines the three-tier hierarchy, shared `:root` theme, tile/section components, dual-mode data-loading template, and the no-orphan-HTML hard rule. Referenced by `/research-plan`, `/do-research`, `/to-research-tasks`, `/compress-research`, `/publish-research`, `/summarize-research`, and `/commit-research` instead of being duplicated inline.

## Research Agent Workflow (Last updated: 2026-05-01)

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
   - [`/do-research`](do-research/SKILL.md): Execute one approved task in a scoped task folder, write modular analysis code, generate Plotly HTML review artifacts (Tier-3 leaf views per [`research-portal`](research-portal/SKILL.md)) for `RESEARCH_REVIEW.html`, create PNGs only when Markdown logs or READMEs need inline static images, and log findings in `results_log_{idx}_{name}.md`.
   - [`/compress-research`](compress-research/SKILL.md): Review the latest task results with the user, capture the alignment discussion in `research_workspace/discussion_log.md`, and compress completed work into `research_workspace/` and `research_tasks/archive/`. Does not edit the review surfaces.
   - [`/publish-research`](publish-research/SKILL.md): Read `discussion_log.md`, update `RESEARCH_REVIEW.html`, `RESEARCH_PLAN_PITCH_DECK.html`, and `RESEARCH_PLAN.md` to reflect the captured decisions, then clear the discussion log so the next review cycle starts fresh. Replaces the publication half of the deprecated `/review-research` skill.
   - Optional [`/commit-research`](commit-research/SKILL.md): Stage only the minimal reviewable and reproducible research files after review checkpoints. Do not commit unless explicitly asked.
4. [`/summarize-research`](summarize-research/SKILL.md): Build the final production handoff in `/results`, including the executive summary, production-ready SQL/Python snippets, final assets, presentation webpage, and project README updates.

> The single `/review-research` skill has been split into `/compress-research` (review/discuss/compress) and `/publish-research` (update review HTML, pitch deck, research plan, then reset the discussion log). The old `/review-research` slug is kept as a thin stub that redirects to the two replacements.

## Development Workflow (Last updated: 2026-04-30; Currently untested)

1. [`/grill-me`](grill-me/SKILL.md): Resolve the design tree for a problem or project.
2. [`/to-prd`](to-prd/SKILL.md): Turn the current conversation and codebase understanding into a PRD under `.working_items/`.
3. [`/prd-to-issue-files`](prd-to-issue-files/SKILL.md): Break an approved PRD into ordered, vertical-slice issue markdown files.

## PR Review Workflow (Last updated: 2026-04-30; Currently untested)

Use this workflow to review GitHub PRs across fresh chats without losing context. Review state is written under `.working_items/pr-review/<owner>-<repo>-<pr-number>/` in the target repo, and each phase updates `NEXT_CHAT_PROMPT.md` so the next chat can resume cleanly.

1. [`/review-pr`](review-pr/SKILL.md): Orchestrate or resume the PR review workflow, choose the next phase, and maintain the shared artifact contract.
2. [`/pr-brief`](pr-brief/SKILL.md): Snapshot PR metadata, branch-first Jira context, CI/check status, comments, diff files, gravity-center files, peripheral changes, and the recommended review plan.
3. [`/scan-security`](scan-security/SKILL.md): Review the diff for evidence-backed security risks, toxic patterns, auth changes, sensitive data exposure, and dependency risk.
4. [`/verify-tests`](verify-tests/SKILL.md): Use GitHub Actions/check results first, then inspect test quality, changed branch coverage, assertion strength, and regression coverage. Run targeted local tests only when useful.
5. [`/logic-walkthrough`](logic-walkthrough/SKILL.md): Walk risk-based story slices, propose actionable inline comments, and create `human_review_prompts` for unclear business logic that needs human judgment.
6. [`/submit-pr-review`](submit-pr-review/SKILL.md): Validate approved comment anchors against the latest diff and submit one GitHub review with inline comments. Use a minimal review body unless blockers or cross-cutting context need a short summary.

Approved comments are staged locally until `/submit-pr-review`; they should become GitHub inline review comments, not a summary-only PR comment. Jira ticket discovery checks the PR branch name first, then title, body, and commits. Unresolved human review prompts are carried forward across chats and are not posted unless they become actionable comments.

The workflow also tracks changed-line review coverage in `COVERAGE.md`. `/submit-pr-review` reports what percent of changed lines were presented to the human reviewer, what percent were reviewed only by the agent, and any unreviewed remainder. Agent-covered lines are grouped by why they were not shown, such as peripheral change, covered by tests/CI, matching an inspected pattern, duplicate mechanical change, static-review-only, or stale/superseded context.
