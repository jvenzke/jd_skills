---
description: "Execute the next planned step of a light research task. Use when the user has finished planning and wants to execute the next step."
disable-model-invocation: true
---

# Do Light Research

You are executing a light research task based on a plan.

## Workflow

1. Read the main output document in the user-provided directory, specifically the "Status/Next Steps" section at the bottom.
2. Execute the planned step. This may involve writing scripts, analyzing data, or exploring the codebase.
3. Generate any necessary small artifacts related to the completed research step in the same directory.
4. Update the main output document with the findings from this step.
5. Update the "Status/Next Steps" section to reflect that the step is complete and what might be needed next.
6. Explicitly prompt the user to run `/plan-light-research` to plan the next step, or `/summarize-light-research` if the research is complete.
