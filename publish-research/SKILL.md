---
name: publish-research
description: Publishes the synthesized findings from /compress-research into the three review surfaces (RESEARCH_REVIEW.html, RESEARCH_PLAN_PITCH_DECK.html, RESEARCH_PLAN.md), then clears the discussion log so the next review session starts fresh. Run after /compress-research.
disable-model-invocation: true
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

- To minimize token usage, do **not** directly read or edit the HTML markup of these files.
- Instead, update structured state files (`research_workspace/review_state.json` and `research_workspace/pitch_deck_state.json`) with the new content, and rely on a local build script to generate the HTML.
- The resulting generated pages must be standalone static HTML files.
- Prefer relative links to `research_workspace/artifacts/` for curated artifacts and `research_tasks/archive/` for original raw task folders.
- Prefer embedded or linked standalone `.html` chart artifacts for plots; use `.png` only as lightweight previews or fallbacks.

### Task:

1. **Update the human review page state**
   - Locate `research_workspace/review_state.json`. If it does not exist, create it with a structured schema for review sections and tasks.
   - Apply the `Decisions captured for /publish-research` items by updating the JSON state.
   - Organize similar tasks into sections in the JSON by research question, hypothesis, or data source.
   - Add a tile object per reviewed task showing task id/name, status, key finding, artifact links, etc.
   - End this step by saving the JSON and providing a shell command or script instruction to regenerate `RESEARCH_REVIEW.html`.

2. **Update the pitch deck state**
   - Locate `research_workspace/pitch_deck_state.json`. If it does not exist, create it.
   - Apply the `Decisions captured for /publish-research` items to the JSON so it reflects the latest pivots, convergence status, and asks.
   - End this step by saving the JSON and providing a shell command or script instruction to regenerate `RESEARCH_PLAN_PITCH_DECK.html`.

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
