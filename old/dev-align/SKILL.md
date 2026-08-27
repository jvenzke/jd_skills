---
name: dev-align
description: Read a ticket or research output, explore the codebase, and grill the user to align on the task scope. Creates a git branch. Use when starting development on a new ticket, feature, or research output.
disable-model-invocation: true
---

# Development Alignment & Branching

Take an incoming ticket (via Jira URL, local markdown file, or pasted text) or research output, explore the codebase, and align with the user on the exact scope of the task.

## Process

1. **Read the input** (handle any combination of the following):
   - **Jira URLs**: Use the Atlassian MCP to fetch the ticket details.
   - **Local files**: Use the Read tool to parse provided markdown or text files.
   - **Pasted text**: Read directly from the chat context.
   - *Note: If multiple sources are provided, merge and synthesize the context from all of them.*

2. **Explore the codebase**:
   - Search the codebase to understand where this feature or fix will live.
   - Ground all discussions in the existing system architecture, patterns, and constraints.

3. **Grill the user**:
   - Interview the user relentlessly about every aspect of the plan until reaching a shared understanding.
   - Walk down each branch of the design tree, resolving dependencies between decisions one-by-one.
   - For each question, provide your recommended answer.
   - Ask questions **one at a time**. Use the `AskQuestion` tool in the UI to get answers from the user.
   - If a question can be answered by exploring the codebase, **explore the codebase instead** of asking the user.

4. **Define Scope**:
   - Explicitly discuss and agree on what is **in scope** and what is **out of scope** for the task.

5. **Create Git Branch**:
   - Once aligned, create a new git branch for the work.
   - If there is a ticket number (e.g., Jira ticket), format the branch as `<TICKET-NUMBER>_short-description` (e.g., `DST-123_add-login`).
   - If there is no ticket number, use a descriptive kebab-case name (e.g., `feature/add-login`).

6. **Next Step**:
   - Instruct the user to run `/to-prd` to generate the Product Requirements Document based on this alignment.
