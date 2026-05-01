---
name: to-prd
description: Turns conversation context and codebase understanding into a PRD written under .working_items/ at the git repo root. Use when the user wants a PRD from the current chat, to capture requirements locally, or mentions to-prd / product requirements.
disable-model-invocation: true
---

# Conversation to PRD (.working_items)

Synthesize a PRD from the current conversation and any codebase exploration. **Do not interview the user** — use what is already known; put uncertainties in **Further Notes**.

## Git root and ignore rules

- Resolve the **git repository root** for the project (`git rev-parse --show-toplevel` when available; otherwise the workspace folder root for a single-root workspace).
- All PRD output lives under **`.working_items/`** at that root.
- Ensure **`.working_items/`** is listed in **`.gitignore`** at the repo root: if missing, append a dedicated line `.working_items/` (do not remove existing rules). If `.gitignore` does not exist, create it with that entry (and a short comment if helpful).

## Process

1. **Explore the repo** as needed to understand the current state (if not already clear from context).

2. **Outline major modules** to build or modify. Prefer **deep modules**: simple, stable interfaces that encapsulate substantial behavior and are testable in isolation. Record module boundaries and interfaces in **Implementation Decisions** (no file paths or code). Record which modules merit tests and why in **Testing Decisions**. Do not pause for user approval on modules or tests unless the user explicitly asked for a review pass.

3. **Write the PRD** using the template below.

4. **Write the file**:
   - Apply **Git root and ignore rules** above first.
   - Ensure `.working_items` exists at the **repository root** (create it if missing).
   - Save as `.working_items/prd-<YYYY-MM-DD>-<short-kebab-slug>.md` where the slug summarizes the feature (e.g. `.working_items/prd-2026-04-27-sent-request-targeting.md`). If the date is unknown, use the user-provided “today” from context when available; otherwise omit the date segment and use `.working_items/prd-<short-kebab-slug>.md`.
   - If a file with the same name already exists, append a numeric suffix (e.g. `-2`) before `.md` rather than overwriting.

Do **not** open GitHub issues or use GitHub APIs for this workflow.

## PRD template

Copy this structure into the markdown file (fill every section; use `N/A` only when truly empty):

```markdown
## Problem Statement

The problem that the user is facing, from the user's perspective.

## Solution

The solution to the problem, from the user's perspective.

## User Stories

A LONG, numbered list of user stories. Each user story should be in the format of:

1. As an <actor>, I want a <feature>, so that <benefit>

This list should be extensive and cover all aspects of the feature.

## Implementation Decisions

A list of implementation decisions that were made. This can include:

- The modules that will be built/modified
- The interfaces of those modules that will be modified
- Technical clarifications inferred from context
- Architectural decisions
- Schema changes
- API contracts
- Specific interactions

Do NOT include specific file paths or code snippets. They may become outdated quickly.

## Testing Decisions

A list of testing decisions that were made. Include:

- What makes a good test here (focus on external behavior, not implementation details)
- Which modules will be tested
- Prior art for the tests (similar tests or patterns already in the codebase), if any

## Out of Scope

What is explicitly out of scope for this PRD.

## Further Notes

Any other notes, open questions, or assumptions.
```

## Quality bar

- User stories should be numbered and cover happy paths, edge cases, observability, and operational concerns where relevant.
- **Implementation Decisions** and **Testing Decisions** should stand alone for an engineer who did not read the chat.
