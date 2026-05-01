---
name: publish-research
description: Publishes the synthesized findings from /compress-research into the three review surfaces (RESEARCH_REVIEW.html, RESEARCH_PLAN_PITCH_DECK.html, RESEARCH_PLAN.md), then clears the discussion log so the next review session starts fresh. Run after /compress-research.
---

You are a Principal Investigator. The compression pass is complete and `research_workspace/discussion_log.md` carries the explicit decisions to apply. Your job is to publish those decisions to the three review surfaces and then reset the discussion log.

### Rules:
- **Source of truth:** Treat `research_workspace/discussion_log.md` (specifically the `Decisions captured for /publish-research` section) as the canonical to-do list for this skill. If a publication change is not in the discussion log or `running_log.md`, do not invent it; ask the user instead.
- **Truth Consolidation:** Move resolved "Unknowns" from the active experimental section to the "Knowledge Base" in `RESEARCH_PLAN.md`.
- **Stale information cleanup:** Remove stale definitions, assumptions, paths, and interpretations from active sections of `RESEARCH_PLAN.md` so future research agents do not treat outdated ideas as current guidance.
- **Convergence:** If the discussion log says the goal is met, state that clearly in `RESEARCH_PLAN.md` and report the closure findings to the user.
- **Independent next steps:** When the discussion log captures multiple independent next steps, surface all of them; do not force a single sequence.
- **Review provenance:** Preserve links from `RESEARCH_REVIEW.html` to original archived task outputs and curated `research_workspace/artifacts/` copies so reviewers can trace summaries back to raw evidence.
- **Step tracking:** Use the todo feature to track all four steps and complete them in order.

### Static HTML Deliverable Rules

These rules apply to both `RESEARCH_REVIEW.html` (Step 1) and `RESEARCH_PLAN_PITCH_DECK.html` (Step 2):

- The page must be a standalone static HTML file that opens directly in a browser without a build step or external dependencies.
- Prefer relative links to `research_workspace/artifacts/` for curated artifacts and `research_tasks/archive/` for original raw task folders.
- Prefer embedded or linked standalone `.html` chart artifacts for plots; use `.png` only as lightweight previews or fallbacks when no useful HTML artifact exists.
- For each deliverable: write a concise summary of the planned changes, ask for approval before editing, then apply the edits, and end with a short summary of what changed.
- Do not introduce build-time dependencies, npm packages, CDN-loaded frameworks, or external font/icon downloads.

### Task:

1. **Update the human review page**
   - Locate `RESEARCH_REVIEW.html` in the research project working folder. If it does not exist, create it under the Static HTML Deliverable Rules above.
   - Apply the `Decisions captured for /publish-research` items that target the review page.
   - Organize similar tasks into sections by research question, hypothesis, data source, experimental method, or decision dependency. Each section should explain why the tasks are grouped, how they link to each other, what upstream decision or unknown they address, and the combined takeaway.
   - Add a tile per reviewed task showing task id/name, status, task type, research question, key finding, confidence/evidence strength, dependency links to related tasks, artifact links, and a clear reviewer action (review details, inspect data, compare plots, mark follow-up).
   - Embed compact task summaries and small review datasets directly in the page when useful. Link to large artifacts instead of inlining them.
   - Include interactive controls feasible in static HTML: section/task filters, collapsible grouped sections, sortable/filterable small tables, image/plot galleries, task-tile status filters, relationship links between dependent tasks, and reviewer note checklists stored as editable text areas or local browser state when appropriate.
   - End this step with a short summary of what changed in `RESEARCH_REVIEW.html` and which artifacts still need better review coverage.

2. **Update the pitch deck**
   - Locate `RESEARCH_PLAN_PITCH_DECK.html` in the research project working folder. If it does not exist, create it under the Static HTML Deliverable Rules above using the layout requirements from the `research-plan` skill.
   - Apply the `Decisions captured for /publish-research` items that target the deck so it reflects the latest results, decisions, pivots, unresolved risks, convergence status, and next-step asks.
   - Include graphs and diagrams where they improve clarity.
   - Keep the deck presentation-ready with slide-like sections, minimal inline CSS, and speaker-friendly framing.
   - End this step with a short summary of what changed in `RESEARCH_PLAN_PITCH_DECK.html`.

3. **Update the research plan**
   - Write a concise summary of the planned changes to `RESEARCH_PLAN.md` (drawn from the discussion log), ask for approval, then apply.
   - Keep `RESEARCH_PLAN.md` focused and compressed: preserve relevant results, rationale, questions, pivots, convergence status, and new knowledge needed by future researchers, but reduce missed steps, issues, and failed attempts to minimal notes that reference `running_log.md` for detail.
   - Remove stale information from active sections when newer definitions, evidence, or decisions supersede it. Do not leave obsolete assumptions in current goals, unknowns, knowledge base, task framing, or implementation guidance.
   - Add or update a `Historic Definitions` section for concepts that were relevant until a specific task but are no longer useful. Each entry names the old definition, the task number where it was retired, why it was retired, and the current replacement or warning. Keep entries short; this section is a guardrail against rediscovered dead ends, not a dumping ground.
   - End this step with a short summary of what changed in `RESEARCH_PLAN.md` and what approvals are still needed.

4. **Reset the discussion log**
   - Overwrite `research_workspace/discussion_log.md` with an empty template containing only the section headings from the Discussion Log Contract in `/compress-research`, plus a one-line note `Cleared on YYYY-MM-DD by /publish-research after publication of session <session id or date>`.
   - This is the only file that should be reset by this skill; do not touch `running_log.md`, `MANIFEST.md`, or archived task folders.
   - End this step by reporting that the discussion log is reset and the next review cycle can start with a fresh `/compress-research` run.

### Out of Scope:
No new research tasks should be generated or executed. Only `RESEARCH_PLAN.md`, `RESEARCH_PLAN_PITCH_DECK.html`, `RESEARCH_REVIEW.html`, and `research_workspace/discussion_log.md` should change here.
