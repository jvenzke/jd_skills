---
name: project-memory
description: Maintain compact project memory files for chat handoff and continuity. Use when the user invokes project memory, asks to keep context across chats, or wants `.memory/` files updated with high-level project knowledge.
disable-model-invocation: true
---

# Project Memory

Maintain a compact, high-signal `.memory/` folder so a later chat can resume the work with minimal context loss.

## Activation

When this skill is active:

1. Check whether the working directory contains `.memory/`.
2. If `.memory/` or any required file is missing, offer to initialize the missing pieces before proceeding.
3. Keep memory current throughout the chat after meaningful state changes, without waiting for the user to ask.
4. Prefer concise summaries and current truths over chat transcripts or event logs.

Required files:

```text
.memory/
├── core_context.md
├── working_knowledge.md
├── manifest.md
└── todo.md
```

## File Purposes

### `.memory/core_context.md`

Store durable context:

- Project scope and objective
- Guardrails, constraints, and user preferences
- Architecture, system boundaries, and important design decisions
- Setup notes needed to understand the project later

### `.memory/working_knowledge.md`

Store learned facts that are useful but may evolve:

- Discovered data schemas, business rules, and domain truths
- Important assumptions and their confidence
- Failed attempts and why they failed
- Non-obvious dependencies, risks, and gotchas

### `.memory/manifest.md`

Store an index of active, highly relevant artifacts:

- Code files currently central to the work
- Data files, notebooks, scripts, docs, and generated artifacts
- Why each file matters right now
- Remove entries once they are no longer relevant

### `.memory/todo.md`

Store the prioritized backlog:

- Current task objective
- Next actions in priority order
- Blockers or decisions needed
- Completed items only if they explain current state; prune routine history

## Update Policy

Update memory after meaningful changes, including:

- A major decision is made or reversed
- A new durable fact, schema, rule, or constraint is discovered
- A task is completed, replaced, blocked, or reprioritized
- A failed approach teaches something future agents should avoid repeating
- Relevant files enter or leave the active work area

Do not update memory for:

- Small conversational turns
- Tool output that does not change the project understanding
- Routine command success with no lasting relevance
- Speculation that has not been validated, unless clearly marked as an assumption

## Size and Quality Rules

- Keep each file small and skimmable.
- Write summaries, not transcripts.
- Merge related notes instead of appending duplicates.
- Delete stale, superseded, or low-value notes during updates.
- Preserve the minimum detail needed for a competent agent to continue.
- Prefer stable facts and decisions over chronological history.
- Use clear headings and short bullets.

## Initialization Template

If the user agrees to initialize missing files, create only missing files and preserve any existing content.

Use these minimal templates:

```markdown
# Core Context

## Scope
- TBD

## Guardrails
- TBD

## Architecture
- TBD
```

```markdown
# Working Knowledge

## Durable Facts
- TBD

## Assumptions
- TBD

## Failed Attempts
- TBD
```

```markdown
# Manifest

## Active Files
- TBD

## Relevant Data And Docs
- TBD
```

```markdown
# Todo

## Current Objective
- TBD

## Next Actions
- TBD

## Blockers
- TBD
```

## Correction Workflow

The user may force corrections at any time.

When a correction conflicts with existing memory:

1. State the conflicting memory briefly.
2. Ask before replacing or deleting it.
3. If the user confirms, update the relevant file immediately.
4. Remove contradictory stale notes rather than preserving both.

When a correction adds non-conflicting context, update the relevant file without extra ceremony.

## Resume Workflow

When starting work with this skill active:

1. Read all existing `.memory/` files.
2. Summarize only the current objective, key constraints, active files, and next action.
3. Continue from the highest-priority item in `.memory/todo.md`.
4. Refresh stale sections as new context is discovered.

## Before Ending A Task

Before a natural stopping point, ensure memory reflects:

- The current state of the project
- The next concrete action
- Any blockers or pending user decisions
- Any files that a future agent should inspect first
