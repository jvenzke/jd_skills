---
description: "Close out linear research (r-setup → r-plan → r-do): condense working knowledge, logs, and artifacts into the project README and optional handoff. Use when execution is complete and findings need a durable handoff without rereading the chat."
disable-model-invocation: true
---

# Summarize Research (closeout)

You are closing out a **Linear Research** thread and producing a **standalone summary** so another team or agent can implement from artifacts—not chat history.

**Upstream contract:** This skill assumes the research folder layout and files from [`r-setup`](r-setup/SKILL.md), planning updates from [`r-plan`](r-plan/SKILL.md), and execution output from [`r-do`](r-do/SKILL.md): `README.md`, `input_plan.md`, `research_plan.md`, `research_log.md`, `next_step.md`, `src/`, **`Canvases/`** (project `.canvas.tsx` copies), and any plots referenced in the log. Live IDE canvases may also exist under Cursor’s workspace `canvases/` path—treat **`Canvases/`** as the canonical path in summaries when both exist.

## When to run

- **`next_step.md`** points to **`r-summarize`** or the user explicitly says research is complete / ready for handoff.
- If the project is mid-step, send the user back to **`r-plan`** or **`r-do`** instead of summarizing.

## Progress tracking

Use the **Todo** feature to track each step of the workflow below (orient through finish). Create todo items when you start and mark each item completed as you finish it.

## Workflow

1. **Orient** — Read, in the user-provided research directory:
   - **`README.md`** — preserve existing title, Jira links, and folder-layout description from setup; you will **extend** this file, not replace it wholesale.
   - **`input_plan.md`** — objective and original scope (for context and traceability).
   - **`research_plan.md`** — **Main Research Objective**, **Current step**, **Working Knowledge**, **Result Artifacts**.
   - **`research_log.md`** — **Task tracking** and every **Research results** subsection (including wrap-ups).
   - **`next_step.md`** — confirm no remaining execution work; if instructions still say **`r-do`** with incomplete tasks, stop and tell the user to finish **`r-do`** or **`r-plan`** first.
2. **Collect artifact inventory** — From the log and repo tree, list paths to **`Canvases/*.canvas.tsx`** (and any other dashboard entrypoints named in the log), **plots**, **scripts/notebooks/SQL files** under **`src/`** or elsewhere named in the log. Note each artifact’s **purpose** in one line.
3. **Update `README.md`** — Add **new sections below** the setup content (insert headings that fit the project; minimum intent below):
   - **Summary / outcomes** — Short executive summary: what was validated or learned, and whether the original objective was met (partially or fully).
   - **Key findings** — Bullet list distilled from **Working Knowledge** and **`research_log.md`**; remove duplication and stale statements; flag confidence (e.g. validated vs inferred) only when it matters for implementation.
   - **Artifacts & verification** — Table or bullet list: artifact path, what it shows, how to rerun (**SQL/Python/canvas** pointers copied from the log or files). This fulfills the **audit trail** requirement: verifiable without the chat.
   - **Handoff for implementation** — Concrete next actions for engineering or another agent: what to build, data contracts (**`db.schema.table`** where relevant), constraints, and explicit **non-goals** or risks called out in the log/plan.
   - **Open questions / follow-ups** — Only if still relevant; otherwise state “None” or omit if empty.
4. **Finish** — Tell the user **`README.md`** was updated. Point to the **Artifacts & verification** section for auditing canvases and reproducible code.

## Rules

- **Do not invent** findings; every claim must trace to **`research_plan.md`** or **`research_log.md`** or linked artifacts.
- Prefer **paths and titles** over long pasted content; keep the README scannable.
- If **`research_plan.md` Result Artifacts** and the log disagree, prefer the **log** for “what was actually run,” and note discrepancies briefly in **Open questions**.
- Read the **canvas** skill (`skills-cursor/canvas/SKILL.md`) only if you need to describe or link **`.canvas.tsx`** files accurately.

## Out of scope

- Editing **`research_plan.md`** task lists or **Working Knowledge** for planning continuity—that is **`r-plan`**. You may **summarize** that content into README.
- Running new queries or changing **`src/`** analysis—that is **`r-do`**.
