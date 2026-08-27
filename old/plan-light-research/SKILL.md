---
description: "Start or continue planning a light research task. Use when the user wants to plan a quick check, prediction method, or other light research in a specific directory."
disable-model-invocation: true
---

# Plan Light Research

You are planning a light research task. This is a lightweight alternative to the full research loop: move an **idea end-to-end** to a **minimal prototype** (something that proves the approach), not open-ended exploration. Keep the **plan → do → plan** loop **fast** with **small, time-bounded** steps.

## Workflow

1. Identify the user-provided directory for this research. If not provided, ask the user.
2. Identify the main output document (e.g., `research_log.md` or similar) in that directory. If it doesn't exist, create it.
3. **Choose alignment depth.** Use `AskQuestion` once: **Light alignment** (few targeted questions, optimized for speed) vs **Full grill-me** (follow the grill-me skill: interview relentlessly about the *next step*, one question at a time, resolving decisions in order).
4. **Plan only the next step.** Scope it so it fits one focused execution: one slice that advances the prototype. Avoid broad “explore the space” steps unless the user explicitly wants that in full grill-me mode.
5. **Light alignment:** Confirm blocking decisions only; ask a small number of targeted questions; state reasonable assumptions in the plan where speed beats extra questions.
6. **Full grill-me:** Ask one question at a time using `AskQuestion`; do not batch multiple uncertain decisions.
7. If a question can be answered by exploring the codebase, explore the codebase instead of asking the user.
8. Once the plan for the next step is clear and agreed upon, update the "Status/Next Steps" section at the bottom of the main output document.
9. Explicitly prompt the user to run the `/do-light-research` skill to execute the planned step.
