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

Both HTML deliverables (`RESEARCH_REVIEW.html` in Step 1 and `RESEARCH_PLAN_PITCH_DECK.html` in Step 2) must follow the [`research-portal`](../research-portal/SKILL.md) rendering spec:

- `RESEARCH_REVIEW.html` is a Tier-1 review index — sectioned tile grid, shared `:root` theme, `.intro` card, `.section-label` bands, `.tile` anchor cards.
- `RESEARCH_PLAN_PITCH_DECK.html` is the Tier-1 deck variant — slide-like sections separated by horizontal rules, no tile grid, prints clean.
- Both files are standalone, hand-authored HTML — no build step, no npm, no CDN frameworks, no external fonts. Plotly via CDN is the only allowed runtime dependency.
- Workflow framing: write a concise summary of planned changes, ask for approval before editing, apply the edits, then end with a short summary of what changed.
- The "no orphan HTML" hard rule and reachability audit from `research-portal` apply — if a task tile is removed, ensure its Tier-3 leaves are either re-linked or archived.

### Task:

1. **Update the human review page**
   - Locate `RESEARCH_REVIEW.html` in the research project working folder. If it does not exist, create it following the Tier-1 review-index conventions in [`research-portal`](../research-portal/SKILL.md).
   - Once `RESEARCH_REVIEW.html` exists, **update `index.html`'s §Review section** to replace the placeholder note with a single prominent link to `RESEARCH_REVIEW.html`. `index.html` is the persistent project entry; `RESEARCH_REVIEW.html` is a child surface linked from it.
   - Apply the `Decisions captured for /publish-research` items that target the review page.
   - Organize similar tasks into Tier-2 sections by research question, hypothesis, data source, experimental method, or decision dependency. Each section header (`.section-label`) explains why the tasks are grouped, how they link to each other, what upstream decision or unknown they address, and the combined takeaway.
   - Each reviewed task gets one `.tile` anchor in its section, populated per the Tier-1 tile contract (icon, title/subtitle, description with headline number, pills for status/task-type/linked-unknown, meta line, CTA verb).
   - Embed compact task summaries inline; link to large artifacts (curated `research_workspace/artifacts/` or original `research_tasks/archive/` paths) instead of inlining them.
   - Interactive controls (section filters, collapsible sections, sortable tables, reviewer note widgets) are allowed *inside* tile descriptions or as supplementary widgets within section bands, but they do not replace the tile grid as the primary navigation surface — see `research-portal` § "Interactive controls inside Tier 1".
   - Run the reachability audit from `research-portal` before declaring this step done; surface any orphan Tier-3 leaves explicitly.
   - End this step with a short summary of what changed in `RESEARCH_REVIEW.html` and which artifacts still need better review coverage.

2. **Update the pitch deck**
   - Locate `RESEARCH_PLAN_PITCH_DECK.html` in the research project working folder. If it does not exist, create it following the Tier-1 deck variant in [`research-portal`](../research-portal/SKILL.md) and the slide-content contract in [`research-plan`](../research-plan/SKILL.md).
   - Apply the `Decisions captured for /publish-research` items that target the deck so it reflects the latest results, decisions, pivots, unresolved risks, convergence status, and next-step asks.
   - Include graphs and diagrams where they improve clarity.
   - Keep the deck presentation-ready: shared `:root` theme, `.intro` card, slide-like `<h2>` sections separated by horizontal rules, prints clean.
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
