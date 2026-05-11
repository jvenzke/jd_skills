---
description: "Execute all atomic tasks in the current step from next_step.md: plots, reproducible Python/SQL, verification canvases, and research_log updates. Confirm with the user after the step is complete."
disable-model-invocation: true
---

# Do Research (execute the planned step)

You are executing the **current research step** defined by planning (`r-plan`). The goal is to move the work forward with **verifiable** artifacts—plots, copy-pasteable **Python/SQL**, and a **canvas dashboard**—not exhaustive exploration.

**Scope of this skill:** run work, produce artifacts, update **`next_step.md`** task status and **`research_log.md`** with links. Do **not** edit **`research_plan.md`** (including its task list and Working Knowledge) during execution—that file is maintained in **`r-plan`**.

**Assumed layout** (from `r-setup`): `input_plan.md`, `research_plan.md`, `research_log.md`, `next_step.md`, `src/`, and **`Canvases/`** — research canvas sources are mirrored here **and** in Cursor’s IDE canvas directory (see **Canvas files** below). If missing, complete `r-setup` first.

## Principles

- **Finish the step before pausing.** Complete **every** atomic task listed for the **current step** in **`next_step.md`** in one `r-do` pass—deliver verification artifacts for each task as you go—then **stop and wait for explicit user confirmation** before starting the next step. Do **not** pause between tasks within the same step unless a task is **blocked** and cannot proceed without user input.
- **Dashboard-style verification.** For quantitative or query-backed work, treat the **canvas** as the primary review surface: important charts/figures, key numbers, and reproducibility (SQL/Python the user can run). Read and follow the **canvas** skill (`skills-cursor/canvas/SKILL.md`) whenever you create or edit a `.canvas.tsx` file.
- **Canvas files (two places, same content):**
  1. **Cursor IDE (presentation)** — Write each `.canvas.tsx` under the workspace-managed path the canvas skill defines (typically `~/.cursor/projects/<workspace>/canvases/<name>.canvas.tsx`). The IDE **only** detects canvases at that Cursor `canvases/` location; resolve `<workspace>` from the active project path (see canvas SKILL if needed).
  2. **Research project (archive)** — Write the **identical** file to **`Canvases/<name>.canvas.tsx`** at the **research project root** (same folder as `README.md` from `r-setup`). Use this path in **`research_log.md`** and planning links so artifacts are portable and version-controlled.
  Always update **both** when you create or change a canvas; keep filenames aligned.
- **Plots + code.** Provide **actionable** snippets: SQL and/or Python that reproduce or extend the analysis, suitable to paste into a notebook or client.
- **Honest scope.** **No canvas** only when the task is purely qualitative (e.g. doc/code exploration) and makes **no quantitative or query-backed claims**—say so briefly in the log.

## Progress tracking

Use the **Todo** feature to track execution: orient, enumerate the step’s tasks, execute each remaining task, log and update `next_step.md` per task, then checkpoint with the user once and hand off when the step is done. Keep todos aligned with atomic tasks in **`next_step.md`** for the current step; mark each complete as you finish it and continue to the next task in the same run.

## Workflow

### 1. Orient

1. Read **`next_step.md`** — this is the source of truth for **what to do now**, task ordering, and where to record **in progress / complete / blocked** for execution.
2. Skim **`input_plan.md`** and **`research_plan.md`** for context only (objective, tables, constraints). Do **not** change **`input_plan.md`** or **`research_plan.md`**.
3. Read **`research_log.md`** so new entries stay consistent with prior wording and links.

### 2. Enumerate tasks for this step

1. Identify **all** atomic tasks for the **current step** that are not yet **complete** (per **`next_step.md`**), in the order the file specifies.
2. If every task for the step is already **complete**, skip to **step 7** (handoff / wrap-up for this step).
3. Do not alter **`research_plan.md`**.

### 3. Execute each remaining task (same run)

For **each** incomplete atomic task, in order:

1. Mark that task **in progress** in **`next_step.md`** (clear status lines or a small **Task status** subsection—whatever fits the existing file shape).
2. Execute **only** that task before moving on—do not start later tasks in the step until the current one is logged and marked **complete** or **blocked**.

3. Implement in **`src/`** (or the paths the project already uses) as needed.
4. For data/SQL steps: run queries or scripts as appropriate; capture outputs for the dashboard.
5. Produce:
  - **Plots** (saved figures and/or chart sections in the canvas),
  - **Actionable Python/SQL** (the exact snippets someone would rerun),
  - **One canvas** (or more if clearly needed) per the canvas skill: for each dashboard, write **`Canvases/<descriptive-name>.canvas.tsx`** at the research root **and** the matching file under Cursor’s **`.../canvases/`** path (see **Canvas files** above)—same basename. Use it as a **dashboard** for this task’s results (graphs, KPIs, snippet blocks, short verification notes). Do not put `.canvas.tsx` under `src/`, arbitrary repo root, or nested subfolders inside **`Canvases/`**.
6. Complete **steps 4 and 5** for this task, then continue with the **next** incomplete task in the step **without** pausing for user confirmation.

If a task is **blocked**, mark it **blocked** in **`next_step.md`**, note the blocker in **`research_log.md`**, and **stop** the run—do not start later tasks in the step until the user unblocks it.

### 4. Log this task in `research_log.md`

Append under a dedicated subsection for **this execution step** (nested under **Research results**), minimally:

- **Task completed** — one line naming the atomic task.
- **Links** — paths to **`Canvases/`** `.canvas.tsx` file(s), plot files, and scripts/notebooks under `src/` or repo root.
- **Core SQL/Python** — short excerpt or pointer to file + line; keep copy-pasteable units visible or linked.
- **How to verify** — one line (e.g. “rerun `src/...py`” or “execute SQL block on schema X”).

Do **not** use **`research_log.md`** to change **`research_plan.md`** content; planning edits stay in **`r-plan`**.

### 5. Update `next_step.md` for this task only

- Mark the task **complete**, or **blocked** with a short reason and what unblocks it.
- Leave instructions for **remaining** tasks intact so the next run is obvious.

### 6. Checkpoint with the user (required after the step)

When **all** tasks for the current step are **complete** (or the run stopped on a **blocked** task), deliver a **confirmation package**:

1. **Canvas(s)** — open beside chat: main graphs/tables, embedded or summarized key numbers, and **reproducible SQL/Python** sections so the user can validate without rereading the whole chat. Tie together confirmatory views across tasks when helpful.
2. **Short explanation** — what was done across the step and what the artifacts prove or constrain.
3. **Next-step preview** — if the step is fully complete, name what **`r-plan`** should define next (or whether **`r-summarize`** is appropriate). If a task is **blocked**, state what unblocks it.
4. **Explicit gate** — ask whether to continue (planning, execution, or summarize per **step 7**), or to pause / adjust scope.

Do **not** start the **next step** until the user confirms.

### 7. When all tasks for this step are complete

1. Provide a **concise summary** of the work done in this **`r-do`** pass (bullet-level is fine).
2. Provide **canvas(s)** that tie together **confirmatory** views (aggregate dashboards referencing the same paths/snippets as the log).
3. Append **`research_log.md`** with a short **wrap-up** subsection: bullet list of completed tasks, links to canvases and code, and any follow-ups or risks.
4. **Handoff**
   - If more planning or a new step definition is needed before more execution: tell the user to return to **`r-plan`**.
   - If the research thread is ready to close out for handoff: tell the user they may continue to **`r-summarize`**.

## Rules recap

| File | In `r-do` |
|------|-----------|
| **`next_step.md`** | Update task status (**in progress / complete / blocked**); keep step instructions readable. |
| **`research_log.md`** | Append summaries and **links** for this step; include canvas/SQL/Python pointers. |
| **`research_plan.md`** | **Do not edit** — leave tasks and structure for **`r-plan`**. |
| **`input_plan.md`** | Read-only unless the user explicitly asks you to change it. |

---
