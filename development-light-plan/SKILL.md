---
name: plan-light-dev
description: Plan a small implementation task or hotfix. Reads the request, explores the codebase, aligns on scope, and creates a LIGHT_DEV_PLAN.md.
disable-model-invocation: true
---

# Plan Light Development

You are planning a light development task. This is a lightweight alternative to the full development loop, intended for well-scoped hotfixes and small tasks that do not require full PRDs or multiple issue files.

## Workflow

1. **Read the input**: Read the incoming ticket, markdown file, or pasted text.
2. **Explore the codebase**: Search the codebase to understand where this fix or feature will live.
3. **Grill the user**: Interview the user to align on the exact scope of the task. Ask questions one at a time using the `AskQuestion` tool.
4. **Create Tracking Document**: Once aligned, create a `LIGHT_DEV_PLAN.md` file in the root directory. This document should contain:
   - The agreed-upon scope and requirements.
   - A checklist of steps to complete the task.
   - A "Status/Next Steps" section at the bottom.
5. **Create Git Branch**: Create a new git branch for the work (e.g., `<TICKET-NUMBER>_short-description` or `fix/short-description`).
6. **Next Step**: Explicitly prompt the user to run the `/do-light-dev` skill to execute the planned steps.
