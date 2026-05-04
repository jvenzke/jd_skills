---
name: toggle-html
description: Toggle the generation of HTML review surfaces (RESEARCH_REVIEW.html and RESEARCH_PLAN_PITCH_DECK.html) on or off.
disable-model-invocation: true
---

Your goal is to toggle the user's preference for generating HTML review surfaces during the research workflow.

### Rules:
- **Configuration File:** The preference is stored in `research_workspace/config.md`.
- **Action:** Read the current preference from `research_workspace/config.md`. If it is currently enabled, disable it. If it is disabled, enable it. If the file does not exist, create it and set the preference to the user's requested state (or toggle it to disabled by default if not specified).
- **Output:** Update `research_workspace/config.md` with the new preference.
- **Confirmation:** Inform the user of the new state (e.g., "HTML generation is now disabled. The research workflow will no longer generate `RESEARCH_REVIEW.html` and `RESEARCH_PLAN_PITCH_DECK.html`.").
