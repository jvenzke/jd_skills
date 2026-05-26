---
name: antigravity-workflow
description: Simulate the workflow used by antigravity
disable-model-invocation: true
---

# Antigravity workflow

Simulates the workflow used by the antigravity development cycle of code research, implementation plan development, approval, implementation, and review. 

## Tasks 
**use the TODO tool to track tasks**

Detailed steps in following sections

1. **Review request**: Understand the user's request.
   - **For New Tasks**: Standardize a unique `{task}` slug as a lowercase kebab-case identifier (e.g., `fix-auth-bug`). Create the parent directory `.working_items/` if it does not exist.
   - **For Existing Tasks (Resuming in a New Chat)**: If the user provides a link to an existing `implementation_plan_{task}.md` or asks to resume an existing task:
     1. Read `.working_items/implementation_plan_{task}.md` and `.working_items/tasks_{task}.md` to fully restore context.
     2. Identify the current `phase` from the YAML frontmatter of `tasks_{task}.md`.
     3. Skip already completed phases and immediately resume the work from the current phase (e.g., `implementation` or `verification`), summarizing the current state in chat.
2. **Research codebase**: Find relevant files, trace logical flows, and understand the scope of changes.
3. **Develop an implementation plan**: Write the plan to `.working_items/implementation_plan_{task}.md` and create a companion task tracking checklist at `.working_items/tasks_{task}.md`.
4. **User review**: Ask the user to review the plan. Repeat steps 1-3 if revisions are requested. Pause and wait for an explicit **APPROVED** sign-off from the user before proceeding. (Skip this if resuming an already approved task).
5. **Implementation**: Execute the steps directly in the main chat. Update the checkbox items in `.working_items/tasks_{task}.md` as each sub-task is completed.
6. **Verification**: Compile, lint, and run the automated verification checks. Log attempts and errors in the `tasks_{task}.md` YAML block. Repeat until all automated verification checks pass.
7. **Review changes**: Write a walkthrough to `.working_items/walkthrough_{task}.md` and summarize the changes in the chat. Commit only the plan and walkthrough files to Git.

---

## Resuming an Existing Task in a New Chat

If a task is being resumed in a new chat session, or if the user links/references an existing implementation plan:
- **Do not restart the planning or research phases.**
- Immediately read the existing `.working_items/implementation_plan_{task}.md` and `.working_items/tasks_{task}.md` using the Read tool.
- Parse the YAML frontmatter of `tasks_{task}.md` to determine the current `phase` and approval status (`approved: true`).
- If `approved: true`, skip the User Review phase entirely and resume execution in the current phase (`implementation` or `verification`).
- Post a message in the chat referencing the linked plan, listing the remaining checklist items, and explaining where the work is resuming.

---

## Research codebase

- Look into the codebase, find relevant files, trace logical flow, and understand what needs to be changed.
- Build a full understanding of the scope of changes, potential impacts, risks, and important side-effects.

---

## Develop an implementation plan

Using the templates below, write the implementation plan and the task list to `.working_items/`. Keep documentation concise and highly structured.

### implementation plan file template
Here is the needed info:
- `{title}`: title of the task
- `{summary}`: Summary of the requested change
- `{risk notes}`: Any breaking changes, security issues, or other major/blocking problems
- `{important notes}`: Changes in how logic works that may impact other parts of the code or users understanding of how the program worked before
- `{questions}`: Any open questions that require clarifications from the user. Provide options/recommended answers
- `{change description}`: A change of what parts of the code base will be impacted. Include relevant files and logic changes in them. Note exact functions when needed for clarity. Break into logical sections and use bullet points.
- `{automated verification plan}`: Include the plan of what the agent will do to ensure the changes were done correctly. This can include compiling/running the code, running test sweet, ...
- `{manual verification plan}`: What manual steps the user should do to test and varify all the changes made.


Template `implementation_plan_{task}.md`
```markdown
# Implementation Plan: {title}

{summary}

## User Review Required

> <span style="color:red">**RISKS**</span>
> 
> 1. {risk notes}

> <span style="color:yellow">**IMPORTANT**</span>
> 
> 1. {important notes}

### Open questions

1. {questions}

## Proposed changes

{change description}

## Verification plan

### Automated Verification

{automated verification plan}

### Manual Verification

{manual verification plan}
```

### Template: `tasks_{task}.md`
This file is kept locally (ignored by Git) and acts as the single source of truth for execution state and progress checklist.
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

---

## User review

- Provide a high-level bulleted summary of the proposed changes in the chat, followed by a link to the `implementation_plan_{task}.md` file.
- Explicitly ask the user to reply with **APPROVED** to proceed, or outline any changes they would like to make.
- If revisions are requested, update the plan and the tasks checklist as needed and repeat the review.
- **Do not proceed to Implementation unless the user has explicitly approved the plan with "APPROVED" (case-insensitive).** Once approved, update the YAML frontmatter in `tasks_{task}.md` to `approved: true` and set the `phase: implementation`.

---

## Implementation

- Execute the changes sequentially directly in the main chat.
- As each step is implemented:
  1. Update the corresponding checkbox in `.working_items/tasks_{task}.md` (e.g., change `- [ ]` to `- [x]`).
  2. Maintain exact indentation and formatting of the existing codebase.
- Avoid introducing any placeholder code or incomplete logic.

---

## Verification

- Once all implementation steps are marked complete, update `phase: verification` in `tasks_{task}.md`.
- Execute all commands specified in the "Automated Verification" section of the plan.
- If any check fails:
  1. Increment `verification_attempts` in `tasks_{task}.md`.
  2. Record the linter or test output in the `last_error` field of the YAML frontmatter.
  3. Re-examine the changes, apply fixes, and re-run all checks.
  4. If a problem cannot be resolved after **3 verification attempts**, halt, report the logs in chat, and ask for the user's guidance.
- **Do not proceed to the final step until all Automated Verification checks have successfully passed.**

---

## Review changes

### Steps for review changes
- Create the `.working_items/walkthrough_{task}.md` file (detailed below).
- Provide a summary of the work in the chat including:
  - A brief 1-2 sentence overview.
  - A numbered list of completed logical steps.
  - A relative link to the walkthrough file.
- Commit `implementation_plan_{task}.md` and `walkthrough_{task}.md` to Git (along with any codebase modifications), leaving `tasks_{task}.md` local.

### Walkthrough file template
Here is the needed info for the `.working_items/walkthrough_{task}.md` file:
- `{title}`: title of the task
- `{summary}`: Summary of the completed change
- `{risk notes}`: Any breaking changes, security issues, or other major/blocking problems found
- `{important notes}`: Changes in how logic works that may impact other parts of the code or users understanding of how the program worked before
- `{code changes}`: A change of what parts of the code base will be impacted. Include relevant files and logic changes in them. Break into logical sections and use bullet points. Assume the user can review the exact code elsewhere. 
- `{automated verification results}`: What varification steps were done on the most recent version of the code and the results of each step
- `{manual verification plan}`: What manual steps the user should do to test and varify all the changes made.

Template for `.working_items/walkthrough_{task}.md`
```markdown
# Walkthrough: {title}

{summary}

## User Review Required

> <span style="color:red">**RISKS**</span>
> 
> 1. {risk notes}

> <span style="color:yellow">**IMPORTANT**</span>
> 
> 1. {important notes}

## Changes made

{code changes}

## Verification Results

### Automated Verification

{automated verification results}

### Manual Verification

{manual verification plan}
```
