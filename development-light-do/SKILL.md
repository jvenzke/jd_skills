---
name: development-light-do
description: Execute the steps in LIGHT_DEV_PLAN.md for a hotfix or small task. Includes writing tests whenever possible.
disable-model-invocation: true
---

# Do Light Development

You are executing a light development task based on `LIGHT_DEV_PLAN.md`.

## Workflow

1. **Read the Plan**: Read the `LIGHT_DEV_PLAN.md` file, specifically the checklist and the "Status/Next Steps" section.
2. **Execute**: Implement the next planned step(s) in the codebase.
3. **Write Tests**: Whenever possible, write tests for the changes you make to ensure things continue to work as intended in the future. While strict TDD is not enforced, test coverage is highly encouraged to prevent regressions.
4. **Update the Plan**: Check off completed items in `LIGHT_DEV_PLAN.md`. Update the "Status/Next Steps" section to reflect what was done and what is needed next.
5. **Next Step**: If there are remaining steps, prompt the user to run `/do-light-dev` again. If all steps are complete, explicitly prompt the user to run `/review-light-dev` to review the changes and create a PR.
