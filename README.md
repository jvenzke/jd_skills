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
- When a skill prepares work for another skill, write the next-step context to a durable Markdown or structured file and name that file in the skill. Include what changed, what remains undecided, and which skill or workflow step should run next.
- Don't repeat yourself. If two skills share the same interview, decision tree, or output format, reference the canonical skill instead of duplicating it.
- Be terse. Every bullet should carry weight; cut narration, restatement, and obvious commentary. Compress before adding.
- Gate irreversible work behind explicit user approval (file moves, deletions, commits, pushes, schema changes, network calls).
- Use a consistent shape: short intent statement, numbered workflow, small set of rules, and an explicit out-of-scope or exit section when useful. [`review-research`](review-research/SKILL.md) is the reference for multi-step skills; [`grill-me`](grill-me/SKILL.md) is the reference for single-purpose skills.
- Set `disable-model-invocation: true` for skills that should only be invoked explicitly by the user (see [`meta-review`](meta-review/SKILL.md)).

### Developing a Workflow

- Each step in a workflow should map to one skill with one clear output artifact. Skills must not spill into the next step's responsibility.
- Define the artifact contract between steps explicitly (file names, folder layout, section headings, manifests). Downstream skills depend on the artifact, not on chat memory.
- Use the README workflow section to explain the next step for each phase, including the handoff file the next chat should read before continuing.
- Persist workflow state in a known location so any step can be resumed cold (e.g., `.working_items/`, `research_workspace/`, the research project folder).
- Include a loop step and a convergence/exit criterion when the workflow is iterative (plan → execute → review → compress).
- List the workflow in this README with numbered steps, a `Last updated` date, and an explicit status tag (e.g., `Currently untested`) so consumers know how much to trust it.
- After running a new workflow end-to-end, invoke [`/meta-review`](meta-review/SKILL.md) to capture missed steps, bloat, duplication across skills, and split/merge candidates before the next iteration.

## General Skills

- [`/grill-me`](grill-me/SKILL.md): Stress-test a plan or design with one question at a time until the agent and user share a clear understanding.
- [`/meta-review`](meta-review/SKILL.md): Review how skills performed in the current chat, propose compact improvements, and log approved recurring problems.

- [`/toggle-html`](toggle-html/SKILL.md): Toggle the generation of HTML review surfaces (RESEARCH_REVIEW.html and RESEARCH_PLAN_PITCH_DECK.html) on or off.


## Light Research Workflow (Last updated: 2026-05-06)

Use this workflow to take an **idea end-to-end** to a **minimal prototype** (proof of approach) with a **fast** plan → do → plan loop—not broad exploratory research. Planning starts with **light alignment vs full grill-me**; execution adds **verification canvases and reproducible SQL** when the step is data-backed.

1. [`/plan-light-research`](plan-light-research/SKILL.md): Plan one **small, time-bounded** next step; update the "Status/Next Steps" section of the main output document.
2. [`/do-light-research`](do-light-research/SKILL.md): Execute the step, add artifacts and (when applicable) a **canvas** with plots and SQL for human verification, update the main document, and prompt for the next action.
3. [`/summarize-light-research`](summarize-light-research/SKILL.md): Compile findings into a handoff document, including pointers to verification artifacts.

## Linear Research Workflow (Last updated: 2026-05-07)

**Artifact chain:** `r-setup` creates the project **`README.md`** (stub), **`input_plan.md`**, **`research_plan.md`**, **`research_log.md`**, **`next_step.md`**, **`Canvases/`**, and **`src/`**. Canvas dashboards are saved under **`Canvases/<name>.canvas.tsx`** for git/handoff **and** mirrored to Cursor’s IDE **`canvases/`** path so they open beside chat (see canvas skill). **`r-plan`** and **`r-do`** update those files across iterations. **`r-summarize`** closes out by **writing the full results into the project `README.md`** (new sections: outcomes, findings, artifacts & verification, implementation handoff, open questions).

1. [`/r-setup`](r-setup/SKILL.md): Pull a Jira ticket (optional), set up base folders, and ask the user to update **`input_plan.md`**, then continue with **`r-plan`**.
2. [`/r-plan`](r-plan/SKILL.md): Review **`input_plan.md`**, define the **next** research step only, maintain **`research_plan.md`**, **`research_log.md`**, and **`next_step.md`** (handoff to **`r-do`** or **`r-summarize`** when done).
3. [`/r-do`](r-do/SKILL.md): Execute atomic tasks from **`next_step.md`**; add plots, reproducible Python/SQL, and verification canvases (**`Canvases/<name>.canvas.tsx`** in the research folder **and** the matching file under Cursor’s IDE **`canvases/`** path per the canvas skill); append **`research_log.md`**; checkpoint after each task (handoff back to **`r-plan`** or forward to **`r-summarize`**).
4. [`/r-summarize`](r-summarize/SKILL.md): Read all planning and execution artifacts; **extend the project `README.md`** with summarized findings and verification pointers.

## PR Review Workflow (Last updated: 2026-05-04)

Use this workflow to review GitHub PRs across fresh chats without losing context. Review state is written under `.working_items/pr-review/<owner>-<repo>-<pr-number>/` in the target repo, and each phase updates `NEXT_CHAT_PROMPT.md` so the next chat can resume cleanly.

1. [`/review-pr`](review-pr/SKILL.md): Orchestrate or resume the PR review workflow, choose the next phase, and maintain the shared artifact contract.
2. [`/pr-brief`](pr-brief/SKILL.md): Snapshot PR metadata, branch-first Jira context, CI/check status, comments, diff files, gravity-center files, peripheral changes, and the recommended review plan.
3. [`/scan-security`](scan-security/SKILL.md): Review the diff for evidence-backed security risks, toxic patterns, auth changes, sensitive data exposure, and dependency risk.
4. [`/verify-tests`](verify-tests/SKILL.md): Use GitHub Actions/check results first, then inspect test quality, changed branch coverage, assertion strength, and regression coverage. Run targeted local tests only when useful.
5. [`/logic-walkthrough`](logic-walkthrough/SKILL.md): Walk risk-based story slices, propose actionable inline comments, and create `human_review_prompts` for unclear business logic that needs human judgment.
6. [`/submit-pr-review`](submit-pr-review/SKILL.md): Validate approved comment anchors against the latest diff and submit one GitHub review with inline comments. Use a minimal review body unless blockers or cross-cutting context need a short summary.

Approved comments are staged locally until `/submit-pr-review`; they should become GitHub inline review comments, not a summary-only PR comment. Jira ticket discovery checks the PR branch name first, then title, body, and commits. Unresolved human review prompts are carried forward across chats and are not posted unless they become actionable comments.

The workflow also tracks changed-line review coverage in `COVERAGE.md`. `/submit-pr-review` reports what percent of changed lines were presented to the human reviewer, what percent were reviewed only by the agent, and any unreviewed remainder. Agent-covered lines are grouped by why they were not shown, such as peripheral change, covered by tests/CI, matching an inspected pattern, duplicate mechanical change, static-review-only, or stale/superseded context.

## Development Workflow (Last updated: 2026-05-05, Untested)

1. [`/dev-align`](dev-align/SKILL.md): Read the incoming ticket or doc, explore the codebase, grill the user to align on scope, and create a git branch.
2. [`/to-prd`](to-prd/SKILL.md): Turn the aligned plan into a PRD with a vertical-slice task breakdown (AFK/HITL) under `.working_items/`.
3. [`/prd-to-issue-files`](prd-to-issue-files/SKILL.md): Extract each task from the PRD into its own implementation plan document.
4. [`/dev-tdd`](dev-tdd/SKILL.md): Implement a task using a strict red-green-refactor loop, summarizing changes and committing after approval.
5. [`/dev-review`](dev-review/SKILL.md): Perform a compressed review of the work, summarize coverage, and prepare/open a Pull Request.

## Light Development Workflow (Last updated: 2026-05-05, Untested)

Use this workflow for hotfixes and small implementation tasks that are well-scoped and do not require large rewrites or multiple parallel agents.

1. [`/plan-light-dev`](plan-light-dev/SKILL.md): Read the ticket or request, explore the codebase, align on scope, and create a single `LIGHT_DEV_PLAN.md` tracking document.
2. [`/do-light-dev`](do-light-dev/SKILL.md): Execute the tasks in `LIGHT_DEV_PLAN.md` flexibly, writing tests whenever possible to prevent future regressions.
3. [`/review-light-dev`](review-light-dev/SKILL.md): Review the completed work against the plan, summarize coverage, and prepare/open a Pull Request.

## Depricated (see depricated folder)

 - Research Agent Workflow (Last updated: 2026-05-07)