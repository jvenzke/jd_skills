---
name: prd-to-issue-files
description: Breaks a linked PRD markdown file into vertical-slice issue markdown files in a sibling folder (tracer bullets, HITL/AFK). Use when the user wants to turn a PRD into local issue .md files, implementation tickets without GitHub, or a file-based work breakdown from docs/prd.md.
---

# PRD to issue files

Break a **PRD** (markdown file the user links or paths) into **one markdown file per vertical slice** (tracer bullet), stored next to the PRD.

## Output layout

- **PRD path:** user-provided path to `*.md` (resolve relative to workspace; use absolute paths in frontmatter when helpful).
- **Output directory:** sibling of the PRD: if the PRD is `path/to/feature-prd.md`, write slices under `path/to/feature-prd-issues/`.
- **Filenames:** `NNN-kebab-case-title.md` (zero-padded index, **dependency order**—blockers get lower numbers).
- **Collisions:** If `feature-prd-issues/` already exists, **stop and ask** whether to merge, use a new name, or replace—unless the user already said to replace/overwrite.

## Process

### 1. Gather context

- Read the linked PRD file fully.
- Use conversation context for extra constraints; do not invent requirements not in the PRD unless the user confirms.

### 2. Explore the codebase (optional)

If not already done and the PRD touches code, explore enough to align slices with the current repo reality.

### 3. Draft vertical slices

Same rules as tracer-bullet planning:

- Each slice is a **thin vertical slice** through all integration layers end-to-end, not a horizontal “one layer” task.
- A completed slice is demoable or verifiable on its own.
- Prefer many thin slices over few thick ones.
- Label each slice **HITL** (needs human decision/review) or **AFK** (can implement without blocking human steps). Prefer AFK where possible.

### 4. Quiz the user (required before writing files)

Present a **numbered list**. For each slice:

- **Title**
- **Type:** HITL / AFK
- **Blocked by:** other slices (by proposed title or index), or none
- **User stories covered:** if the PRD has user stories, map them

Ask:

- Granularity: too coarse / too fine?
- Dependencies correct?
- Merge or split any slices?
- HITL vs AFK correct?

**Do not create files until the user explicitly approves** the breakdown (flow A).

### 5. Write issue markdown files

After approval:

1. Create the output directory if needed.
2. Assign final `NNN-` prefixes consistent with dependency order (blockers first).
3. For each slice, write one file using **YAML frontmatter** + **body template** below.
4. In **Blocked by** (body and frontmatter), reference other slices by final filename (e.g. `001-foundation.md`), not GitHub issue numbers.

**Do not** edit or replace the source PRD.

## Per-file format

**Frontmatter** (all slices):

```yaml
---
title: "Short descriptive name"
type: AFK   # or HITL
prd: path/relative/to/prd.md
blocked_by: []   # e.g. ["001-foundation.md"]
user_stories: [] # optional: strings or IDs from PRD
---
```

**Body:**

```markdown
## Parent

Link to PRD: [`prd-relative-path`](relative-or-absolute-path-to-prd.md)

## What to build

Concise end-to-end description of this vertical slice (behavior across layers, not layer-by-layer laundry list).

## Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Blocked by

- Blocked by [`001-example.md`](001-example.md) (repeat as needed)

Or: **None — can start immediately**
```

Use relative links from each issue file to the PRD and to sibling blockers in the same `*-issues/` folder.

## Optional: index file

If the user wants navigation, add `000-index.md` in the same folder listing slices in order with one-line summaries—only after approval and together with the slice files (ask if unclear).
