---
name: r-antigravity
description: >-
  Antigravity-style workflow for research tools and prototypes. Prefer simple
  researcher-facing interfaces that hide plumbing complexity so analysis stays
  fast. Use when speed and terse plans matter more than production-grade diffs.
disable-model-invocation: true
---

# Antigravity workflow (research / prototypes)

Simulates the antigravity cycle — research, plan, approval, implement, review —
for research tools and prototypes. Prefer deep modules: a small, easy-to-use
interface that reduces researcher load, with plumbing and edge-case complexity
hidden in the implementation. Do not let design polish hinder exploration.

## Rules (priority order)

Apply in this order when they conflict:

1. **Deep modules for researchers**: keep the entrypoint simple; hide data plumbing, retries, formatting, and environment details behind it.
2. **Reduce research load**: optimize for fewer steps, fewer knobs, and less context the researcher must hold — without blocking the analysis itself.
3. **Ship useful prototypes fast**: prefer working research tools over speculative architecture or premature generalization.
4. Prefer **orthogonal helpers** that can be reused across analyses; reshape boundaries when that lowers researcher friction.
5. Keep changes within the approved plan. Larger code changes are allowed when they simplify the researcher interface; no unrelated cleanup.

## Deep-module design standard (research tools)

Treat a module as any script, notebook helper, class, object, package, or CLI entrypoint with a boundary.

- Expose the smallest practical interface for the research task (e.g. one function/CLI that takes intent + inputs and returns usable results).
- Keep connection setup, path wrangling, retries, schema quirks, joins, formatting, and caching behind the boundary.
- Favor a few deep helpers over many shallow wrappers that force the researcher to orchestrate steps.
- Co-locate related plumbing when that reduces what the researcher must know or copy between analyses.
- Avoid interfaces that leak warehouse/config/file internals through excessive parameters or required ceremony.
- Judge an abstraction by how much friction it removes from the research loop, not by elegance. A simple call may legitimately wrap substantial plumbing.
- Prefer defaults that make the common research path work; expose knobs only when the analysis needs them.
- Larger refactors are justified when they shorten the path from question → result, remove duplicated setup, or make the next analysis cheaper. Do not use deep-module design to justify productization or speculative frameworks.

## Tasks
**use the TODO tool to track tasks**

### 1. Review request & Research
- Standardize a unique `{task}` slug as a lowercase kebab-case identifier (e.g., `fix-auth-bug`). Create parent directory `.working_items/` if missing.
- **Resuming Tasks**: If resuming, read existing `implementation_plan_{task}.md` and `tasks_{task}.md`, skip completed phases, and post a concise chat summary of remaining checklist items and resumption point.
- **Research codebase**: Find relevant files, trace logical flows, and build a full understanding of the scope of changes, potential impacts, risks, and side-effects.
- **Evaluate researcher load**: Identify the intended entrypoint, ceremony currently forced on the researcher (setup, parameters, sequencing), duplicated plumbing across analyses, and what complexity should move behind a simple interface.

### 2. Develop an implementation plan
Write a highly concise, terse plan to `.working_items/implementation_plan_{task}.md` and a progress checklist to `.working_items/tasks_{task}.md`.

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

1. {questions - brief list with options}

## Proposed changes

{change description - terse bulleted list of impacted files and logic changes}

## Deep-module design (research load)

- **Researcher interface**: {simple entrypoint / call surface}
- **Hidden plumbing**: {setup, joins, retries, formatting, env details moved behind it}
- **Load reduction**: {steps, knobs, or context removed from the researcher's path}
- **Speed tradeoff**: {what stays rough / deferred so exploration is not hindered}

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
- Implement the approved plan. To avoid cluttering the main thread, the actual coding and testing must be delegated to a subagent.
- Use the `Task` tool (subagent) to perform the implementation.
- **Subagent prompt MUST include** (verbatim constraints — do not omit):
  - Path to `implementation_plan_{task}.md` and `tasks_{task}.md`
  - The **Rules (priority order)** block from this skill
  - The **Deep-module design standard (research tools)** block from this skill
  - Instruct: stay within the approved plan; optimize for a simple researcher interface; do not productize or over-abstract beyond what reduces research load
- Instruct the subagent to return a clean summary of changes and test results when finished.
- As each step completes, change `- [ ]` to `- [x]` in `.working_items/tasks_{task}.md`.
- Maintain exact indentation/formatting; avoid placeholder code.

### 5. Verification
- Update `phase: verification` in `tasks_{task}.md`.
- Execute all automated verification checks.
- Verify the researcher can reach results through the intended simple interface without coordinating hidden plumbing steps.
- Verify the change did not add ceremony that slows the common research path.
- If checks fail: increment `verification_attempts`, record test/linter error in `last_error` field of `tasks_{task}.md` frontmatter, apply fixes, and re-run.
- If unresolved after **3 attempts**, halt, report logs, and ask for user guidance.
- **DO NOT proceed to review changes until all Automated Verification checks pass.**

### 6. Review changes
- Create `.working_items/walkthrough_{task}.md`.
- Provide a very brief summary in the chat including:
  - **Summary of Changes**: A 1-2 sentence high level overview.
  - **Test Status**: Show the tests that were failing and now pass.
  - **Code Overview**: A numbered list of completed logical steps.
  - **User Review**: A relative link to the walkthrough file.

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
