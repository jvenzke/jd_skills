---
name: dev-tdd
description: Implement a task using test-driven development (red-green-refactor loop) via a subagent. Summarize changes and commit after user approval. Use when the user wants to implement an issue file or task.
disable-model-invocation: true
---

# Test-Driven Development Implementation

Implement a specific task (e.g., an issue markdown file) using a strict Red-Green-Refactor loop. To avoid cluttering the main thread, the actual coding and testing loop must be delegated to a subagent.

## Process

1. **Read the Task & Tracker**:
   - Read the provided issue markdown file and the sibling `000-index.md` tracker file.
   - Check the status in `000-index.md`. If it is `In Progress`, **stop** and ask for explicit confirmation before proceeding, to avoid stepping on parallel agents.
   - If the issue file contains a `## Review Feedback` section, note that this is a `Needs Fix` task.

2. **Claim the Task**:
   - Update `000-index.md` to mark this task as `In Progress`.

3. **Launch Subagent**:
   - Use the `Task` tool (subagent) to perform the implementation.
   - Provide the subagent with the issue file path, the exact `## Test Command` from the file, and any `## Review Feedback`.
   - Instruct the subagent to follow the Red-Green-Refactor loop:
     - **RED**: Write ONE test that describes the behavior. Run the test command and verify it FAILS.
     - **GREEN**: Write the minimal code needed to make the test PASS. Run the test command and verify it PASSES.
     - **REFACTOR**: Clean up the code. Ensure tests still pass.
   - Instruct the subagent to return a clean summary of changes and test results when finished.

4. **Summary & Review (Main Thread)**:
   Once the subagent completes:
   - Update `000-index.md` to mark the task as `Done`.
   - Present the subagent's summary to the user:
     - **Summary of Changes**: High-level overview of what was built.
     - **Test Status**: Show the tests that were failing and now pass.
     - **Code Overview**: Briefly explain the code changes made.

5. **Commit**:
   - Ask the user for approval to commit the changes.
   - Once approved, stage ONLY the files changed by this specific task.
   - Commit to git with a descriptive message (e.g., `feat: implement <task-name>`).

6. **Next Step**:
   - Instruct the user to run `/dev-tdd` on the next pending issue file, or `/dev-review` if all tasks are complete.
