---
description: "Start or continue planning a light research task. Use when the user wants to plan a quick check, prediction method, or other light research in a specific directory."
disable-model-invocation: true
---

# Plan Light Research

You are planning a light research task. This is a lightweight alternative to the full research loop, intended for quick checks, prediction methods, or small investigations in a user-provided directory.

## Workflow

1. Identify the user-provided directory for this research. If not provided, ask the user.
2. Identify the main output document (e.g., `research_log.md` or similar) in that directory. If it doesn't exist, create it.
3. Interview the user relentlessly about every aspect of the plan for the *next step* of the research. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one.
4. Ask the questions one at a time. Use the `AskQuestion` tool in the UI to get answers from the user.
5. If a question can be answered by exploring the codebase, explore the codebase instead of asking the user.
6. Once the plan for the next step is clear and agreed upon, update the "Status/Next Steps" section at the bottom of the main output document.
7. Explicitly prompt the user to run the `/do-light-research` skill to execute the planned step.
