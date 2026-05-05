---
name: to-prd
description: Turns conversation context and codebase understanding into a PRD written under .working_items/ at the git repo root. Use when the user wants a PRD from the current chat, to capture requirements locally, or mentions to-prd / product requirements.
disable-model-invocation: true
---

# Conversation to PRD (.working_items)

Synthesize a PRD from the current conversation and any codebase exploration. **Discuss the plan with the user in detail prior to writing the PRD.**

## Git root and ignore rules

- Resolve the **git repository root** for the project (`git rev-parse --show-toplevel` when available; otherwise the workspace folder root for a single-root workspace).
- All PRD output lives under **`.working_items/`** at that root.
- Ensure **`.working_items/`** is listed in **`.gitignore`** at the repo root: if missing, append a dedicated line `.working_items/` (do not remove existing rules). If `.gitignore` does not exist, create it with that entry.

## Process

1. **Discuss the Plan**:
   - Before writing the PRD, discuss the proposed task breakdown with the user.
   - Ensure tasks follow the **vertical-slicing** idea: each task is a minimum amount of functionality that goes vertically through the stack producing a testable feature.
   - Ensure each task can be done independently. Note dependencies if a later task depends on prior tasks.

2. **Write the PRD** using the template below.

3. **Write the file**:
   - Apply **Git root and ignore rules** above first.
   - Ensure `.working_items` exists at the **repository root** (create it if missing).
   - Save as `.working_items/prd-<YYYY-MM-DD>-<short-kebab-slug>.md` where the slug summarizes the feature. If the date is unknown, use the user-provided "today" from context when available; otherwise omit the date segment.
   - If a file with the same name already exists, append a numeric suffix (e.g. `-2`) before `.md` rather than overwriting.

4. **Next Step**:
   - Instruct the user to run `/prd-to-issue-files` to extract the tasks into individual implementation plans.

Do **not** open GitHub issues or use GitHub APIs for this workflow.

## PRD template

Copy this structure into the markdown file (fill every section; use `N/A` only when truly empty):

```markdown
## Problem Statement

The problem that the user is facing, from the user's perspective.

## Solution

The solution to the problem, from the user's perspective.

## Scope

- **In Scope**: Explicitly list what is included.
- **Out of Scope**: Explicitly list what is excluded.

## Task Breakdown (Vertical Slices)

A numbered list of tasks. Each task must be a vertical slice through the stack producing a testable feature.

For each task, include:
- **Title**: Short description.
- **Type**: `AFK` (Away From Keyboard - preferred) or `HITL` (Human In The Loop).
- **Description**: What the task accomplishes.
- **Dependencies**: Which prior tasks must be completed first (if any).
- **Scope**: What is in and out of scope for this specific task.

## Implementation Decisions

A list of implementation decisions that were made. This can include:
- The modules that will be built/modified
- The interfaces of those modules that will be modified
- Technical clarifications inferred from context
- Architectural decisions
- Schema changes
- API contracts

Do NOT include specific file paths or code snippets. They may become outdated quickly.

## Testing Decisions

A list of testing decisions that were made. Include:
- What makes a good test here (focus on external behavior, not implementation details)
- Which modules will be tested
- Prior art for the tests (similar tests or patterns already in the codebase), if any

## Further Notes

Any other notes, open questions, or assumptions.
```

## Quality bar

- Tasks must be vertical slices, not horizontal layers (e.g., "Add DB table" is bad; "Add 'Save Draft' button that writes to DB" is good).
- **Implementation Decisions** and **Testing Decisions** should stand alone for an engineer who did not read the chat.
