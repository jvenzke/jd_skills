---
description: "Summarize the findings of a completed light research task for handoff. Use when the light research is done and needs to be handed off to another team or agent."
disable-model-invocation: true
---

# Summarize Light Research

You are summarizing the results of a light research task to create a handoff document.

## Workflow

1. Read the main output document and any generated artifacts in the user-provided directory.
2. Produce a handoff document (e.g., `handoff.md`) that contains the necessary information for another team or agent to begin development or implementation based on the research findings.
3. The handoff document should be concise but comprehensive enough to stand alone without needing the full research log.
4. Where the work included **verification canvases** or **reproducible SQL**, reference those explicitly (paths and purpose) so the prototype remains **auditable** without rereading the chat.
5. Inform the user that the handoff document has been created.
