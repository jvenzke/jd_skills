---
description: "Plan the next research step and maintain planning markdown (input_plan, research_plan, research_log, next_step). No research execution in this skill."
disable-model-invocation: true
---
# Plan the Research

Your goal is to develop a plan for the research that needs to be done and track what has been completed.

**Scope of this skill:** planning, alignment, and edits to the planning markdown files only (`input_plan.md`, `next_step.md`, `research_plan.md`, `research_log.md`). Do **not** execute research here—no running queries, scripts, or analysis as the primary output of this step. Those belong in execution, not in `r-plan`.

**Assumed layout** (from `r-setup`): `input_plan.md`, `research_plan.md`, `research_log.md`, `next_step.md`, `src/`, and **`Canvases/`** (project copies of `.canvas.tsx`; **`r-do`** also writes to Cursor’s IDE `canvases/` path per the canvas skill). If this structure is missing, complete `r-setup` first.

## Progress tracking

Use the **Todo** feature to track each workflow step below (gather context through handoff). Create todo items when you begin and mark items completed as you finish each step.

## Workflow (order)
Details of each step are outlined in the following sections. 
1. **Gather context** — read `input_plan.md` and `research_plan.md`.
2. **Update task status** — reconcile `research_log.md` and `next_step.md` with recent work.
3. **Update working knowledge** — reconcile the **Working Knowledge** section of `research_plan.md`.
4. **Plan alignment** — agree on exactly one next step (discussion and codebase reads only; **no file edits** in this phase). Summarize the agreed next step and tasks in chat, then **pause** until the user approves moving to step 5 (unless they already instructed you to apply planning-file updates in this session).
5. **Update plan for next steps** — propose edits to the four planning files and apply them **only after** step 4’s pause is cleared (same approval exceptions as step 4).
6. **Handoff** — point the user at how to execute the step (see **Handoff** below).

## Rules

- **Canvases:** When you describe dashboard/canvas deliverables in planning files (e.g. **Result Artifacts**, **next_step.md** outputs, or log links), use paths under the research project’s **`Canvases/`** folder (`Canvases/<name>.canvas.tsx`). Execution also mirrors those files to Cursor’s managed **`canvases/`** directory for the IDE—do not point planning at `src/` or other ad-hoc locations for `.canvas.tsx`.
- Focus on **only the next step** of the research plan; plans change as research progresses. A plan can be made up a handful of small atomic tasks.
- Stay inside **planning + markdown maintenance**: no turning this session into "doing the research" beyond reading files for alignment.
- Use the **AskQuestion** tool for decisions that require user input; ask **one question at a time** when practical.

## Gather context

- Read `input_plan.md` and `research_plan.md`.

## Update task status

- Read `research_log.md` and `next_step.md` for work recently marked complete or in progress.
- Ask for user approval *before* marking a task complete in `research_log.md`.

## Update working knowledge

- Review the **Working Knowledge** section of `research_plan.md`.
- For conflicting or incorrect results versus the most recent research:
  - Ask targeted follow-ups until there is a shared understanding (Ask question in chat one question at a time).
  - Walk through each branch of the reasoning to see why there was a misunderstanding and what should change.
- Propose an update to **Working Knowledge** to remove stale/add new knowledge, get user approval, then edit `research_plan.md`.

## Plan alignment (no file edits in this phase)

- **Do not edit** planning markdown files during this phase—only discuss, read the codebase if needed, and align with the user.
- Focus on planning **only the next** step in the research plan. **Do not plan more than one step ahead.**
- Review the plan in `input_plan.md`.
- Confirm the next planned step is correct before proceeding; allow the user to change course.
- Align on scope for that step:
  - Ask questions one at a time in the chat; when helpful, give your recommended answer.
  - Resolve dependencies between decisions one-by-one until the scope is clear.
  - If a question can be answered by exploring the codebase, explore it and summarize findings 
  - Never guess what is meant by a statement. Confirm anything that is unclear.
- Summarize the agreed **next step** and the **list of tasks** needed to complete it (for the proposal phase).

## Update plan for next steps

- Write a proposal for each of the following. Get user approval **before** editing files (unless the user already asked you to apply agreed updates).
  - Update the `input_plan.md` research steps if needed.
  - Update the **Current step** section of `research_plan.md`.
  - Write each step and task as a todo item in the `research_log.md` file's **Task tracking** section.
  - Clear `next_step.md` and write detailed instructions: what should be done in this research step, which tasks to run, scope, and what the final outputs should be. Set the next phase to `r-do` (work to be done) or `r-summarize` (work is complete).

## Handoff

Provide a quick up next summary of the tasks to be worked on. Then tell the user to move onto `r-do` if there is more work to do or `r-summarize` if work is complete.
