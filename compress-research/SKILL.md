---
name: compress-research
description: Reviews the latest research-task results with the user, captures the alignment discussion to a discussion log, and compresses completed work into the research workspace. Hand off to /publish-research when convergence is good enough to update review surfaces.
disable-model-invocation: true
---

You are a Principal Investigator. Analyze the latest task results to update the project state and prepare the workspace for publication.

### Rules:
- **Truth Consolidation:** Move resolved "Unknowns" from the experimental section to the "Knowledge Base" in `RESEARCH_PLAN.md` only when /publish-research runs. During compression, capture them in the discussion log and `running_log.md` instead.
- **Pivot Logic:** If results are inconclusive, analyze "Why" and propose new experimental unknowns in the discussion log.
- **Independent next steps:** If multiple proposed next steps are completely independent, capture all of them; do not force a single sequence.
- **Step tracking:** Use the todo feature to track all three task steps and complete them in order.
- **No publication side effects:** Do not edit `RESEARCH_PLAN.md`, `RESEARCH_REVIEW.html`, or `RESEARCH_PLAN_PITCH_DECK.html` here. Capture the changes the discussion implies, but defer the edits to /publish-research.

### Discussion Log Contract

Keep `research_workspace/discussion_log.md` as the running record of the current review session. The file is owned jointly by /compress-research (which writes into it) and /publish-research (which clears it at the end of the publication pass).

- File path: `research_workspace/discussion_log.md`.
- Lifecycle: cleared by /publish-research at the end of its run, so each /compress-research session starts on a clean file.
- Required sections, in order: `# Discussion Log`, `## Session metadata` (date, reviewed task ids, links to results logs), `## Methods and results summary`, `## Alignment with research plan`, `## Resolved unknowns`, `## New unknowns and pivots`, `## Closure / convergence read`, `## Decisions captured for /publish-research` (the explicit changes the discussion implies for `RESEARCH_REVIEW.html`, `RESEARCH_PLAN_PITCH_DECK.html`, and `RESEARCH_PLAN.md`).
- Each Q&A or decision should be recorded as a short, dated bullet so /publish-research can apply them mechanically.

### Task:

1. **Review the research logs**
   - Review the linked research logs, prioritizing the `results_log_{idx}_{name}.md` file(s), task artifact manifests, and task review artifacts provided.
   - Provide a clear, short summary of the methods used and results of the experiment.
   - Include things learned, new questions, blind spots, and other interesting notes.
   - Pause and allow the user to ask questions about the results before moving on.
   - Avoid the question UI tool for this step.
   - Do not update `RESEARCH_PLAN.md`, `RESEARCH_REVIEW.html`, or the pitch deck during this step.

2. **Discuss alignment with the research plan and persist the discussion log**
   - Compare the new results against the current `RESEARCH_PLAN.md`.
   - Identify resolved unknowns, newly discovered unknowns, changed assumptions, possible pivots, and evidence for or against convergence.
   - Interview the user relentlessly, walking each branch of the research tree and resolving dependencies one-by-one. For each question, provide your recommended answer.
   - Ask questions one at a time using the question tool.
   - If a question can be answered by exploring the codebase, explore the codebase instead.
   - As the discussion progresses, persist findings to `research_workspace/discussion_log.md` using the structure in the Discussion Log Contract above. Do not wait until the end of the discussion; update the log incrementally so a crash or context reset does not lose the alignment work.
   - End this step with a short summary that points the user at `research_workspace/discussion_log.md` and lists the captured `Decisions captured for /publish-research` bullets.

3. **Compress the research into the research workspace**
   - Write a concise summary of the planned compression work and ask for approval before editing files.
   - After approval, compress the workspace.
   - Create or update `research_workspace/running_log.md`, `research_workspace/MANIFEST.md`, `research_workspace/src/` when reusable code exists, `research_workspace/artifacts/` for curated key artifacts, and `research_tasks/archive/` for completed raw task folders and completed task markdown files.
   - Preserve detailed provenance in `research_workspace/running_log.md`: paths tried, wins, failures, methods, implementation details, artifacts, raw evidence locations, reusable code, unresolved risks, and open questions. Cross-reference the relevant sections of `discussion_log.md` rather than duplicating them.
   - Archive completed task folders from `research_tasks/task_*` and completed task definition files from `research_tasks/task*.md`; do not archive pending or incomplete work unless the user approves. Use the `mv` command line interface so files are moved intact instead of being rewritten or manually copied.
   - Copy review-ready artifacts to `research_workspace/artifacts/`: representative CSV/JSON samples, schema/metadata files, standalone plot HTML files, PNG previews only when required for Markdown/static-preview use, data dictionaries, query files, and artifact manifests.
   - Leave original artifacts with archived task folders and link both curated and original paths from `running_log.md`.
   - Extract reusable operational code into `research_workspace/src/` only when clearly reusable; leave one-off EDA, failed experiment code, task-specific notebooks, and hard-coded scripts in the archived task folder.
   - End this step with a short summary of what moved, what was consolidated, and what reusable assets now exist. Tell the user the next step is `/publish-research`, which will read `discussion_log.md`, update the review HTML, pitch deck, and research plan, and then clear the discussion log.

### Out of Scope:
No new research tasks should be generated or executed. Only compression-related files under `research_workspace/`, `research_tasks/archive/`, and the `discussion_log.md` should change here.
