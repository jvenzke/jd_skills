---
name: prd-to-issue-files
description: Breaks a linked PRD markdown file into vertical-slice issue markdown files in a sibling folder. Use when the user wants to turn a PRD into local issue .md files or implementation plans.
disable-model-invocation: true
---

# PRD to Issue Files

Break a **PRD** (markdown file the user links or paths) into **one markdown file per task** (vertical slice), stored next to the PRD. Since the plan has been deeply discussed, this should be an **AFK (Away From Keyboard)** task.

## Output layout

- **PRD path:** user-provided path to `*.md` (resolve relative to workspace; use absolute paths in frontmatter when helpful).
- **Output directory:** sibling of the PRD: if the PRD is `path/to/feature-prd.md`, write slices under `path/to/feature-prd-issues/`.
- **Filenames:** `NNN-kebab-case-title.md` (zero-padded index, **dependency order**—blockers get lower numbers).
- **Index File:** Always create `000-index.md` in the output directory to track task status (`Pending`, `In Progress`, `Done`, `Needs Fix`).
- **Collisions:** If `feature-prd-issues/` already exists, **stop and ask** whether to merge, use a new name, or replace—unless the user already said to replace/overwrite.

## Process

1. **Gather context**:
   - Read the linked PRD file fully.
   - Extract the tasks from the "Task Breakdown" section.

2. **Draft vertical slices**:
   - Each slice is a **thin vertical slice** through all integration layers end-to-end.
   - Ensure dependencies, testing, and changes are clearly defined.

3. **Write issue markdown files**:
   - Create the output directory if needed.
   - Assign final `NNN-` prefixes consistent with dependency order (blockers first).
   - For each task, write one file using **YAML frontmatter** + **body template** below.
   - In **Blocked by** (body and frontmatter), reference other slices by final filename (e.g. `001-foundation.md`).

4. **Create Tracker**:
   - Create `000-index.md` listing all tasks with a status of `Pending`.

5. **Next Step**:
   - Instruct the user to run `/dev-tdd` on individual issue files to implement them.

**Do not** edit or replace the source PRD.

## Per-file format

**Frontmatter** (all slices):

```yaml
---
title: "Short descriptive name"
type: AFK   # or HITL
prd: path/relative/to/prd.md
blocked_by: []   # e.g. ["001-foundation.md"]
---
```

**Body:**

```markdown
## Parent

Link to PRD: [`prd-relative-path`](relative-or-absolute-path-to-prd.md)

## What to build

Concise end-to-end description of this vertical slice (behavior across layers).

## Implementation Plan

Detailed steps on what needs to be changed in the codebase to implement this task.

## Scope

- **In Scope**: What is explicitly included in this task.
- **Out of Scope**: What is explicitly excluded from this task.

## Testing

What should be tested to verify this task is complete. Include specific test cases or scenarios.

## Test Command

The exact terminal command the agent should use to run the tests for this specific task (e.g., `npm test -- path/to/file.test.ts`).

## Blocked by

- Blocked by [`001-example.md`](001-example.md) (repeat as needed)

Or: **None — can start immediately**
```
