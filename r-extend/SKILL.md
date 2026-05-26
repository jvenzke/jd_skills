---
name: r-extend
description: Refine and extend the research plan in input_plan.md by grilling the user on proposed next steps, aligning on details, and updating input_plan.md. Use this after completing a research step in r-do and before starting the next step in r-plan when you need to align on new steps or modify the existing research plan.
disable-model-invocation: true
---

# Extend the Research Plan (r-extend)

Your goal is to extend or refine the research plan in `input_plan.md` based on completed research and the user's intent. You must align on these steps through a relentless grilling/interview process, then update `input_plan.md` and only `input_plan.md`.

**Scope of this skill:** planning, alignment, and updates ONLY to `input_plan.md`. No execution of research, no edits to other files (do **not** touch `next_step.md`, `research_plan.md`, `research_log.md`, or any code files).

## Progress tracking

Use the **Todo** feature to track each workflow step below. Create todo items when you begin and mark items completed as you finish each step.

## Workflow (order)

Details of each step are outlined in the following sections.
1. **Gather context** — read `input_plan.md` and check recently completed work.
2. **Formulate & Grill** — formulate the proposed next steps and interview the user relentlessly.
3. **Present proposal** — compile and present the proposed next steps for explicit user approval.
4. **Update input_plan.md** — apply the approved edits to `input_plan.md` (no other files).

---

## 1. Gather context

- Read `input_plan.md`.
- Read `research_log.md` and check what has been completed in the workspace.
- Identify the current state of research and the target area.
- Do not edit any files during this phase.

## 2. Formulate & Grill

- Formulate an initial set of proposed next steps based on what has been done and what the user wants to do next.
- Grill/interview the user relentlessly about every aspect of the design and steps until you reach a shared understanding.
- Walk down each branch of the design tree, resolving dependencies between decisions one-by-one.
- Ask questions **one at a time** directly in the chat and pause for the user's response.
- For each question, provide your recommended answer.
- If a question can be answered by exploring the codebase or existing docs, explore them instead of asking.
- Never guess what is meant by a statement. Confirm anything that is unclear.

## 3. Present proposal

- After the grilling process is over, compile and present the complete proposed next steps to the user.
- If the proposal includes edits/reorganizations of existing steps in `input_plan.md`, explicitly note these changes.
- If the proposal identifies new code files, Snowflake tables, or docs, include them in the proposal.
  - When noting a Snowflake table, follow this exact rule:
    - Write a comment describing the table with the database, schema, and table name in the format `db.schema.table`
    - On the following lines, put each column in the table and the datatype of the table.
- Ask the user for explicit approval to write these changes to `input_plan.md`.
- If the user objects or has feedback, re-trigger the grilling/refinement process to address their concerns.

## 4. Update input_plan.md

- **Only** edit `input_plan.md` after receiving explicit user approval.
- Do not edit any other planning or source files (such as `next_step.md`, `research_plan.md`, or `research_log.md`).
- Update `## Research steps` with the approved steps (appending, updating, or reorganizing as agreed).
- Update the `## Useful files` section with new files, Snowflake tables, or documents, following the specific formatting rules for tables and column data types.

---

## Rules and Guidelines

- **Orthogonality:** Keep your changes strictly confined to `input_plan.md`. Do not touch downstream or upstream planning files such as `next_step.md`, `research_plan.md`, or `research_log.md` under any circumstances.
- **Snowflake Tables:** When working with Snowflake, use the Snowflake MCP to look up tables. Check table sizes to avoid running overly long queries. Use the MCP to pull descriptions, summaries, and samples of less than 50 rows. Use the Python Snowflake connector to pull full datasets.
- **Subagents:** Use subagents whenever a deep dive is needed to avoid cluttering the main thread.
- **No Emojis:** Do not include emojis in files or comments.
