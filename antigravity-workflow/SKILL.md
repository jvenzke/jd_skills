---
name: antigravity-workflow
description: Simulate the workflow used by antigravity with high emphasis on concise, terse, non-verbose deliverables
disable-model-invocation: true
---

# Antigravity workflow

Simulates the workflow used by the antigravity development cycle of code research, implementation plan development, approval, implementation, and review.

## Tasks
**use the TODO tool to track tasks**

### 1. Review request & Research
- Standardize a unique `{task}` slug as a lowercase kebab-case identifier (e.g., `fix-auth-bug`). Create parent directory `.working_items/` if missing.
- **Resuming Tasks**: If resuming, read existing `implementation_plan_{task}.md` and `tasks_{task}.md`, skip completed phases, and post a concise chat summary of remaining checklist items and resumption point.
- **Research codebase**: Find relevant files, trace logical flows, and build a full understanding of the scope of changes, potential impacts, risks, and side-effects.

### 2. Develop an implementation plan
Write a highly concise, terse plan to `.working_items/implementation_plan_{task}.md` and a progress checklist to `.working_items/tasks_{task}.md`.

#### Rules for Brevity & Efficiency:
1. **No Fluff**: Keep the implementation plan extremely crisp and bulleted. Avoid long-winded paragraphs or verbose descriptions.
2. **Programmatic Notebook Edits**: When editing Jupyter Notebooks (`.ipynb`), write and execute a temporary Python helper script to parse and programmatically inject new cells rather than rewriting raw JSON text directly to save token context and prevent corruption of existing serialized outputs.

#### Template `implementation_plan_{task}.md`
```markdown
# Implementation Plan: {title}

{summary - 1-2 sentences}

## User Review Required

> <span style="color:red">**RISKS**</span>
> 
> 1. {risk notes - terse list}

> <span style="color:yellow">**IMPORTANT**</span>
> 
> 1. {important notes - terse list}

### Open questions

1. {questions - brief list with options}

## Proposed changes

{change description - terse bulleted list of impacted files and logic changes}

## Verification plan

### Automated Verification
{automated verification plan - terse bullet list}

### Manual Verification
{manual verification plan - terse bullet list}
```

#### Template `tasks_{task}.md`
```markdown
---
task: {task}
phase: planning
approved: false
verification_attempts: 0
last_error: null
---

# Checklist for: {task}

- [ ] Step 1: {granular checklist step 1}
- [ ] Step 2: {granular checklist step 2}
```

### 3. User review
- Provide a highly concise, high-level summary of proposed changes **(maximum 3-4 bullets total)** in the chat, followed by a relative link to `implementation_plan_{task}.md`.
- Ask the user to reply with **APPROVED** to proceed. Repeat if revisions are requested.
- **DO NOT proceed to Implementation without explicit "APPROVED" sign-off.** Once approved, set `approved: true` and `phase: implementation` in the `tasks_{task}.md` frontmatter.

### 4. Implementation
- Execute changes sequentially in the main chat.
- As each step completes, change `- [ ]` to `- [x]` in `.working_items/tasks_{task}.md`.
- Maintain exact indentation/formatting; avoid placeholder code.

### 5. Verification
- Update `phase: verification` in `tasks_{task}.md`.
- Execute all automated verification checks.
- If checks fail: increment `verification_attempts`, record test/linter error in `last_error` field of `tasks_{task}.md` frontmatter, apply fixes, and re-run.
- If unresolved after **3 attempts**, halt, report logs, and ask for user guidance.
- **DO NOT proceed to review changes until all Automated Verification checks pass.**

### 6. Review changes
- Create `.working_items/walkthrough_{task}.md`.
- Provide a very brief summary in the chat including:
  - A 1-2 sentence overview.
  - A numbered list of completed logical steps.
  - A relative link to the walkthrough file.

#### Walkthrough Template `.working_items/walkthrough_{task}.md`
```markdown
# Walkthrough: {title}

{summary - 1-2 sentences}

## User Review Required

> <span style="color:red">**RISKS**</span>
> 
> 1. {risk notes - terse list}

> <span style="color:yellow">**IMPORTANT**</span>
> 
> 1. {important notes - terse list}

## Changes made

{code changes - terse bulleted list of completed changes}

## Verification Results

### Automated Verification
{automated verification results - results of verification steps}

### Manual Verification
{manual verification plan - brief steps for the user}
```
