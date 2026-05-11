---
description: "Execute the next planned step of a light research task. Use when the user has finished planning and wants to execute the next step."
disable-model-invocation: true
---

# Do Light Research

You are executing a light research task based on a plan. The goal is to move the idea forward with a **minimal prototype** and artifacts a human can **verify**, not exhaustive exploration.

## Workflow

1. Read the main output document in the user-provided directory, specifically the "Status/Next Steps" section at the bottom.
2. Execute the planned step. This may involve writing scripts, analyzing data, or exploring the codebase.
3. Generate any necessary small artifacts related to the completed research step in the same directory.
4. **Human-verifiable output (data-backed steps).** If this step involves **data, metrics, databases, or charts**, read and follow the **canvas** skill. Produce a **Cursor canvas** (a single `.canvas.tsx` under the workspace `canvases/` directory per that skill) that includes **plots** and **reproducible SQL** (or equivalent query text) the reviewer can use to check the work. Embed or summarize key numbers in the canvas; keep SQL copy-pasteable.
5. **Main output document.** Update it with findings from this step. Include a **link** to the canvas file path (if any), the **core SQL/queries** used, and a one-line **how to verify** note.
6. **No canvas needed** only when the step is purely code or document exploration and makes **no quantitative or query-backed claims** — state briefly in the log why there is no verification canvas.
7. Update the "Status/Next Steps" section to reflect that the step is complete and what might be needed next.
8. Explicitly prompt the user to run `/plan-light-research` to plan the next step, or `/summarize-light-research` if the research is complete.
