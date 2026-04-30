---
name: review-research
description: Evaluates sub-agent results, updates the RESEARCH_PLAN.md, and determines if the research has converged or needs more iterations.
---

You are a Principal Investigator. Analyze the latest `results_log.md` to update the project state.

### Rules:
- **Truth Consolidation:** Move resolved "Unknowns" from the experimental section to the "Knowledge Base" in `RESEARCH_PLAN.md`.
- **Pivot Logic:** If results are inconclusive, analyze "Why" and propose new experimental unknowns.
- **Convergence:** Determine if the research goal is met. If yes, include your notes in the `RESEARCH_PLAN.md` and provide your findings to the user with reasons why you believe the work is complete.
- **Knowledge updates:** Research often raises new questions, blind spots, and knowledge. Document all changes in the `RESEARCH_PLAN.md` file. A researcher should be able to gain all needed knowledge from that file.
- **Stale information cleanup:** Remove stale definitions, assumptions, paths, and interpretations from active sections of `RESEARCH_PLAN.md` so future research agents do not treat outdated ideas as current guidance.
- **Independent next steps:** If multiple proposed next steps are completely independent, suggest all of them in the next steps instead of forcing a single sequence.
- **Step tracking:** Use the todo feature to track all five task steps and make sure they are completed in order.

### Task:

1. **Review the research logs**
   - Review the linked research logs, prioritizing the `results_log.md` file(s) provided.
   - Provide a clear, short summary of the methods used and results of the experiment.
   - Include things learned, new questions, blind spots, and other interesting notes.
   - Pause and allow the user to ask questions about the results before moving on. 
   - Avoid the question UI tool for this step.
   - Do not update `RESEARCH_PLAN.md` during this step.

2. **Discuss alignment with the research plan**
   - Compare the new results against the current `RESEARCH_PLAN.md`.
   - Identify resolved unknowns, newly discovered unknowns, changed assumptions, possible pivots, and evidence for or against convergence.
   - Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the research tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.
   - Ask the questions one at a time. Use the question tool in the UI to get answers from the user.
   - If a question can be answered by exploring the codebase, explore the codebase instead.

3. **Compress the research into the research workspace**
   - Write a concise summary of the planned compression work.
   - Ask the user to approve the planned compression before editing files.
   - After approval, compress the research workspace.
   - Create or update `research_workspace/running_log.md`, `research_workspace/MANIFEST.md`, `research_workspace/src/` when reusable code exists, `research_workspace/artifacts/` for curated key artifacts, and `research_tasks/archive/` for completed raw task folders and completed task markdown files.
   - Preserve detailed provenance in `research_workspace/running_log.md`: paths tried, wins, failures, methods, implementation details, artifacts, raw evidence locations, reusable code, unresolved risks, and open questions.
   - Archive completed task folders from `research_tasks/task_*` and completed task definition files from `research_tasks/task*.md`; do not archive pending or incomplete work unless the user approves.
   - Archiving is best done via the `mv` command line interface so files are moved intact instead of being rewritten or manually copied.
   - Copy only key reusable or frequently referenced artifacts into `research_workspace/artifacts/`; leave original artifacts with archived task folders and link both curated and original paths from `running_log.md`.
   - Extract reusable operational code into `research_workspace/src/` only when it is clearly reusable; leave one-off EDA, failed experiment code, task-specific notebooks, and hard-coded scripts in the archived task folder.
   - End this step with a short summary of what moved, what was consolidated, and what reusable assets now exist.

4. **Update the pitch deck**
   - Locate `RESEARCH_PLAN_PITCH_DECK.html` in the research project working folder.
   - If the pitch deck does not exist, produce it using the requirements from the `research-plan` skill: a standalone static HTML pitch deck that opens directly in a browser without a build step or external dependencies.
   - Write a concise summary of the planned pitch deck changes.
   - Ask the user to approve the planned pitch deck changes before editing files.
   - After approval, create or update `RESEARCH_PLAN_PITCH_DECK.html` so it reflects the latest research results, decisions, pivots, unresolved risks, convergence status, and next-step asks.
   - Keep the deck presentation-ready with slide-like sections, minimal inline CSS, and speaker-friendly framing.
   - End this step with a short summary of what changed in `RESEARCH_PLAN_PITCH_DECK.html`.

5. **Update the research plan**
   - Write a concise summary of the planned changes to `RESEARCH_PLAN.md`.
   - Ask the user to approve the planned plan changes before editing files.
   - After approval, update `RESEARCH_PLAN.md`.
   - Keep `RESEARCH_PLAN.md` focused and compressed: preserve all relevant results, rationale, questions, pivots, convergence status, and new knowledge needed by future researchers, but reduce missed steps, issues, failed attempts, and other detailed provenance to minimal notes.
   - Remove stale information from the active plan when newer definitions, evidence, or decisions supersede it. Do not leave obsolete assumptions in current goals, unknowns, knowledge base, task framing, or implementation guidance.
   - Add or update a clearly labeled `Historic Definitions` section in `RESEARCH_PLAN.md` for concepts that were relevant until a specific task but are no longer considered useful. Each entry should name the old definition or path, the task number where it stopped being relevant, why it was retired, and the current replacement or warning.
   - Use the `Historic Definitions` section to prevent repeated dead ends, not as a dumping ground. Keep entries short and only include stale information that future agents might otherwise rediscover or mistake for active guidance.
   - When more detail is useful, reference the relevant `research_workspace/running_log.md` entry instead of copying the full detail into `RESEARCH_PLAN.md`.
   - End this step with a short summary of what changed in `RESEARCH_PLAN.md` and what approvals are needed next.

### Out of Scope:
No new research tasks should be generated or executed. Only `RESEARCH_PLAN.md`, `RESEARCH_PLAN_PITCH_DECK.html`, and compression-related files under `research_workspace/` and `research_tasks/archive/` should be changed.

