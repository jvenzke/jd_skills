---
name: dev-review
description: Perform a compressed review of all changes made during the development cycle, validate against the PRD, and prepare a PR. Use when all tasks for a feature are complete.
disable-model-invocation: true
---

# Development Final Review & PR Preparation

Perform a compressed review of the work completed in the current branch, validate it against the original PRD, and prepare a Pull Request.

## Process

1. **Verify Completion**:
   - Read the `000-index.md` tracker file.
   - Ensure all tasks are marked as `Done`. If any are `Pending` or `In Progress`, warn the user.

2. **Gather Context & Diff**:
   - Read the original PRD file linked in the issue files.
   - Run `git diff main...HEAD` (or the appropriate base branch) to see all changes made during this development cycle.

3. **Compressed Review**:
   Perform a fast, combined review pass over the diff:
   - **Requirements Validation**: Does the diff fulfill the requirements and scope defined in the PRD?
   - **Security & Patterns**: Check for obvious security risks, sensitive data exposure, or toxic patterns.
   - **Test Coverage**: Verify that tests exist for the new logic and that they are meaningful.

4. **Handle Review Failures (Feedback Loop)**:
   If any significant issues, missing tests, or missed requirements are found:
   - Update the specific task's status in `000-index.md` from `Done` to `Needs Fix`.
   - Append the specific review feedback to the bottom of that task's issue markdown file under a `## Review Feedback` heading.
   - **Stop** and prompt the user to run `/dev-tdd` on the failed task again to fix the issues. Do not proceed to PR creation.

5. **Review Summary & Coverage Report (If successful)**:
   If the review passes, present a summary to the user:
   - **What was built**: A brief summary of the feature.
   - **Review Coverage**: Summarize what was shown to the user in the chat vs. what was reviewed by the agent and not shown.
   - **Percentage**: Display a summary of the `% of lines changed` that were explicitly discussed/shown vs. silently reviewed by the agent.

6. **Prepare PR**:
   - Draft a PR title and description based on the PRD and the actual changes.
   - Ask the user for approval to push the branch and open the PR.

7. **Push and Open PR**:
   - Once approved, push the branch to the remote (`git push -u origin HEAD`).
   - Use the `gh pr create` command (via the Shell tool) to open the Pull Request with the drafted title and body.
   - Provide the PR URL to the user.
