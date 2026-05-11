# Skills for Cursor I no longer use

## Research Agent Workflow (Last updated: 2026-05-04)
### Issue: this was way to heavy to use for most tasks

> **Token Optimization & Review Rules:** This workflow aggressively minimizes context bloat and keeps the user informed:
> - HTML review surfaces are generated from `review_state.json` and `pitch_deck_state.json` via local scripts; the LLM does not write HTML directly.
> - The `running_log.md` is periodically compressed into `core_context.md` to keep context dense.
> - Raw data artifacts (CSV/JSON rows) are excluded from the LLM context; agents only read summary stats (`df.describe()`) and schemas.
> - Agents provide an in-chat summary of what context was read vs omitted (with percentage of lines reviewed) during planning and review steps.
> - HTML generation is optional and can be toggled at any time using the `/toggle-html` skill.

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
   - [`/do-research`](do-research/SKILL.md): Execute one approved task in a scoped task folder, write modular analysis code, generate Plotly HTML review artifacts for `RESEARCH_REVIEW.html`, create PNGs only when Markdown logs or READMEs need inline static images, and log findings in `results_log_{idx}_{name}.md`.
   - [`/compress-research`](compress-research/SKILL.md): Review the latest task results with the user, capture the alignment discussion in `research_workspace/discussion_log.md`, and compress completed work into `research_workspace/` and `research_tasks/archive/`. Does not edit the review surfaces.
   - [`/publish-research`](publish-research/SKILL.md): Read `discussion_log.md`, update `RESEARCH_REVIEW.html`, `RESEARCH_PLAN_PITCH_DECK.html`, and `RESEARCH_PLAN.md` to reflect the captured decisions, then clear the discussion log so the next review cycle starts fresh. Replaces the publication half of the deprecated `/review-research` skill.
   - Optional [`/commit-research`](commit-research/SKILL.md): Stage only the minimal reviewable and reproducible research files after review checkpoints. Do not commit unless explicitly asked.
4. [`/summarize-research`](summarize-research/SKILL.md): Build the final production handoff in `/results`, including the executive summary, production-ready SQL/Python snippets, final assets, presentation webpage, and project README updates.

> The single `/review-research` skill has been split into `/compress-research` (review/discuss/compress) and `/publish-research` (update review HTML, pitch deck, research plan, then reset the discussion log). The old `/review-research` slug is kept as a thin stub that redirects to the two replacements.
