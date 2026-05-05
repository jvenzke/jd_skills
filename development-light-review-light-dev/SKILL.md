---
name: review-light-dev
description: Review completed light development work against LIGHT_DEV_PLAN.md and prepare a Pull Request.
disable-model-invocation: true
---

# Review Light Development

You are reviewing a completed light development task and preparing it for a Pull Request.

## Workflow

1. **Verify Completion**: Read `LIGHT_DEV_PLAN.md` to ensure all checklist items are marked as complete.
2. **Gather Context & Diff**: Run `git diff main...HEAD` (or the appropriate base branch) to see all changes made.
3. **Review**: Validate the diff against the scope defined in `LIGHT_DEV_PLAN.md`. Check for missing tests, security risks, or incomplete requirements.
4. **Handle Failures**: If issues are found, update `LIGHT_DEV_PLAN.md` with the missing requirements and prompt the user to run `/do-light-dev` again.
5. **Prepare PR**: If the review passes, draft a PR title and description based on `LIGHT_DEV_PLAN.md` and the actual changes.
6. **Push and Open PR**: Ask the user for approval. Once approved, push the branch (`git push -u origin HEAD`) and use the `gh pr create` command (via the Shell tool) to open the Pull Request. Provide the PR URL to the user.
