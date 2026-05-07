---
description: "Execute research tasks one at a time from next_step.md: plots, reproducible Python/SQL, verification canvases, and research_log updates. Confirm with the user before each next task."
disable-model-invocation: true
---

# Do Research (execute the planned step)

You are executing the **current research step** defined by planning (`r-plan`). The goal is to move the work forward with **verifiable** artifacts—plots, copy-pasteable **Python/SQL**, and a **canvas dashboard**—not exhaustive exploration.

**Scope of this skill:** run work, produce artifacts, update **`next_step.md`** task status and **`research_log.md`** with links. Do **not** edit **`research_plan.md`** (including its task list and Working Knowledge) during execution—that file is maintained in **`r-plan`**.

**Assumed layout** (from `r-setup`): `input_plan.md`, `research_plan.md`, `research_log.md`, `next_step.md`, `src/`, and **`canvases/`** — all research canvases (`.canvas.tsx`) are created and stored **only** in `canvases/`. If missing, complete `r-setup` first.

## Principles

- **One task at a time.** Complete a single atomic task from the current step, deliver verification artifacts, then **stop and wait for explicit user confirmation** before starting the next task.
- **Dashboard-style verification.** For quantitative or query-backed work, treat the **canvas** as the primary review surface: important charts/figures, key numbers, and reproducibility (SQL/Python the user can run). Read and follow the **canvas** skill (`skills-cursor/canvas/SKILL.md`) whenever you create or edit a `.canvas.tsx` file. **Store every canvas at `canvases/<name>.canvas.tsx`** (workspace `canvases/` directory only—the IDE does not pick up canvases in other paths).
- **Plots + code.** Provide **actionable** snippets: SQL and/or Python that reproduce or extend the analysis, suitable to paste into a notebook or client.
- **Honest scope.** **No canvas** only when the task is purely qualitative (e.g. doc/code exploration) and makes **no quantitative or query-backed claims**—say so briefly in the log.

## Progress tracking

Use the **Todo** feature to track execution: orient, pick task, execute, log, update `next_step.md`, checkpoint with the user, and handoff when the step is done. For multi-task steps, keep todos aligned with atomic tasks in **`next_step.md`**—refresh the list when moving to the next task after user confirmation.

## Workflow

### 1. Orient

1. Read **`next_step.md`** — this is the source of truth for **what to do now**, task ordering, and where to record **in progress / complete / blocked** for execution.
2. Skim **`input_plan.md`** and **`research_plan.md`** for context only (objective, tables, constraints). Do **not** change **`input_plan.md`** or **`research_plan.md`**.
3. Read **`research_log.md`** so new entries stay consistent with prior wording and links.

### 2. Pick exactly one task

1. Identify the **next** atomic task that is not yet **complete** (per **`next_step.md`**).
2. Mark that task **in progress** in **`next_step.md`** (clear status lines or a small **Task status** subsection—whatever fits the existing file shape). Do not alter **`research_plan.md`**.

### 3. Execute that task only

- Implement in **`src/`** (or the paths the project already uses) as needed.
- For data/SQL steps: run queries or scripts as appropriate; capture outputs for the dashboard.
- Produce:
  - **Plots** (saved figures and/or chart sections in the canvas),
  - **Actionable Python/SQL** (the exact snippets someone would rerun),
  - **One canvas** (or more if clearly needed) per the canvas skill: write each file as **`canvases/<descriptive-name>.canvas.tsx`** only—use it as a **dashboard** for this task’s results (graphs, KPIs, snippet blocks, short verification notes). Do not put `.canvas.tsx` files under `src/`, repo root, or subfolders of `canvases/`.

### 4. Log this task in `research_log.md`

Append under a dedicated subsection for **this execution step** (nested under **Research results**), minimally:

- **Task completed** — one line naming the atomic task.
- **Links** — paths to canvas(s), plot files, and scripts/notebooks under `src/` or repo root.
- **Core SQL/Python** — short excerpt or pointer to file + line; keep copy-pasteable units visible or linked.
- **How to verify** — one line (e.g. “rerun `src/...py`” or “execute SQL block on schema X”).

Do **not** use **`research_log.md`** to change **`research_plan.md`** content; planning edits stay in **`r-plan`**.

### 5. Update `next_step.md` for this task only

- Mark the task **complete**, or **blocked** with a short reason and what unblocks it.
- Leave instructions for **remaining** tasks intact so the next run is obvious.

### 6. Checkpoint with the user (required after every task)

Deliver a **confirmation package**:

1. **Canvas** — open beside chat: main graphs/tables, embedded or summarized key numbers, and **reproducible SQL/Python** sections so the user can validate without rereading the whole chat.
2. **Short explanation** — what was done and what the artifacts prove or constrain.
3. **Next task preview** — name and scope of the **next** atomic task from **`next_step.md`** (if any).
4. **Explicit gate** — ask whether to proceed to that next task, or to pause / adjust scope.

Do **not** start the next task until the user confirms.

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
