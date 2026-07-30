---
name: d-antigravity
description: >-
  Phased, minimal-diff development workflow (antigravity-style). Prefer over
  r-antigravity when change size and code quality matter: vertical-slice phases,
  reuse-first constraints, and explicit approval before each phase.
disable-model-invocation: true
---

# Antigravity workflow (development)

Simulates the antigravity cycle — research, plan, approval, implement, review —
with hard limits on change size per pass and a reuse-first coding posture.

## Rules (priority order)

Apply in this order when they conflict:

1. **Extend/reuse** existing code over adding new functions or modules.
2. **Minimal diff** that solves the stated problem — no drive-by changes.
3. **Small local refactor** only when it avoids duplication *in this change*.
4. Prefer **reusable, orthogonal units**; no new abstractions unless the approved plan names them.

## Tasks
**use the TODO tool to track tasks**

### 1. Review request & Research
- Standardize a unique `{task}` slug as a lowercase kebab-case identifier (e.g., `fix-auth-bug`). Create parent directory `.working_items/` if missing.
- **Entry / resume (phase plan linked or exists)**: If the user links or names a `phase_plan_{task}.md`, or one already exists under `.working_items/` for this task:
  1. Read `phase_plan_{task}.md`, `implementation_plan_{task}.md` (if present), and `tasks_{task}.md` (if present).
  2. Find the next incomplete phase (`- [ ]` or `- [o]`). Treat `- [o]` as the current in-progress phase.
  3. Skip 2a/2b if `approved: true` in the phase plan frontmatter.
  4. Post a concise chat summary: completed phases, next phase title, and where work resumes — then go to **2c** for that phase (rewrite the implementation plan/checklist for *this* phase only).
- **Resuming mid-phase**: If `tasks_{task}.md` exists with incomplete checklist items for the current phase, skip completed steps and resume at the first unchecked item.
- **Research codebase**: Find relevant files, trace logical flows, and build a full understanding of the scope of changes, potential impacts, risks, and side-effects.

### 2a. Develop a phase plan (optional)
Create a phase plan when **any** of these apply:
- More than **~3 files** are likely to change, **or**
- Work crosses layers (e.g. DB + API + UI), **or**
- A new module/package is required, **or**
- It is unclear which existing code to extend.

Otherwise skip to **2c**. If no phase plan is used, only one **APPROVED** gate is required (step 3).

#### Phase size limits
- Each phase is one **vertical slice** that can ship and verify on its own.
- Soft ceiling: prefer **≤3 files** and a checklist of **≤5 implementation steps** per phase. Split further if either would be exceeded.
- Phases must be vertical slices, not horizontal layers (e.g., "Add DB table" is bad; "Add 'Save Draft' button that writes to DB" is good).

#### Rules for Brevity & Efficiency:
1. **No Fluff**: Keep the phase plan extremely crisp and bulleted. Avoid long-winded paragraphs or verbose descriptions.

#### Template `phase_plan_{task}.md`
```markdown
---
task: {task}
approved: false
---

# Phase Plan: {title}

{summary - 1-2 sentences}

### Open questions

1. {questions - brief list with options and recommended answer}

## Proposed phases

- [ ] Phase 1: {Brief description of phase 1}
   * Details about phase 1 
- [ ] Phase 2: {Brief description of phase 2}
   * Details about phase 2
```

### 2b. Phase plan approval
If a phase document is generated do the following. Otherwise skip to develop an implementation plan.
- Provide a highly concise, high-level summary of proposed phases **(maximum 3-4 bullets total)** in the chat, followed by a relative link to `phase_plan_{task}.md`.
- Ask the user to reply with **APPROVED** to proceed. Repeat if revisions are requested.
- **DO NOT proceed to Implementation plan without explicit "APPROVED" sign-off.** Once approved, set `approved: true` in the `phase_plan_{task}.md` frontmatter.

### 2c. Develop an implementation plan
Write a highly concise, terse plan to `.working_items/implementation_plan_{task}.md` and a progress checklist to `.working_items/tasks_{task}.md`.
If a phase plan is being used, limit scope to the next incomplete phase and change `- [ ]` to `- [o]` in the `phase_plan_{task}.md` file to indicate it’s in progress. Reset `approved: false` and `phase: planning` in `tasks_{task}.md` for the new phase.

#### Rules for Brevity & Efficiency:
1. **No Fluff**: Keep the implementation plan extremely crisp and bulleted. Avoid long-winded paragraphs or verbose descriptions.

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

1. {questions - brief list with options and recommended answer}

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
- Implement a specific task using a strict Red-Green-Refactor loop. To avoid cluttering the main thread, the actual coding and testing loop must be delegated to a subagent.
- Use the `Task` tool (subagent) to perform the implementation.
- **Subagent prompt MUST include** (verbatim constraints — do not omit):
  - Paths to `implementation_plan_{task}.md` and `tasks_{task}.md`
  - The **Rules (priority order)** block from this skill
  - Instruct: stay within the approved plan’s file list; do not start later phases; no new abstractions unless the plan names them
- Instruct the subagent to follow the Red-Green-Refactor loop:
  - **RED**: Write ONE test that describes the behavior. Run the test command and verify it FAILS.
  - **GREEN**: Write the smallest change that makes the test PASS. Extract helpers only if the approved plan requires it. Run the test command and verify it PASSES.
  - **REFACTOR**: Clean up the code. Ensure tests still pass.
- Instruct the subagent to return a clean summary of changes and test results when finished.
- As each step completes, change `- [ ]` to `- [x]` in `.working_items/tasks_{task}.md`.
- Maintain exact indentation/formatting; avoid placeholder code.

### 5. Verification
- Update `phase: verification` in `tasks_{task}.md`.
- Execute all automated verification checks.
- If checks fail: increment `verification_attempts`, record test/linter error in `last_error` field of `tasks_{task}.md` frontmatter, apply fixes, and re-run.
- If unresolved after **3 attempts**, halt, report logs, and ask for user guidance.
- **DO NOT proceed to review changes until all Automated Verification checks pass.**
- If a phase plan is being used, change `- [o]` to `- [x]` in the `phase_plan_{task}.md` file to indicate it’s complete.

### 6. Review changes
- Create `.working_items/walkthrough_{task}.md`.
- Provide a very brief summary in the chat including:
  - **Summary of Changes**: A 1-2 sentence high level overview.
  - **Test Status**: Show the tests that were failing and now pass.
  - **Code Overview**: A numbered list of completed logical steps.
  - **User Review**: A relative link to the walkthrough file.
- **Next phase (new chat)**: If `phase_plan_{task}.md` has remaining `- [ ]` phases, end with a short prompt to start a **new chat** for the next phase, and include a relative link to `phase_plan_{task}.md` (and the next phase title). Do **not** implement the next phase in this chat.

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
