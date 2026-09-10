---

## name: scope-project
description: >-
  High-level project scoping for large, multi-PR / multi-week changes:
  codebase research, blocking alignment, a durable tracker, and coarse
  step files. Tracks migrations, dependencies, known follow-ups, and
  cross-step refactoring. Planning and tracking only — never implements.
  Use when the user invokes scope-project or wants to roadmap a major
  change before development.
disable-model-invocation: true

# Scope project

Research a large change, align on blocking forks, and write a **project**
tracker plus coarse **step** files under `.working_items/{project}/`.
Human-review the roadmap, then stop.

This skill tracks the project: migrations, dependencies, “we know we need to change this later”, and refactoring/deepening that is only coherent across steps. Prefer **few** steps. Split on migrations,
dependencies, rollback units, and module-deepening sequence — not on
file count or tickets.

**Never** change product code, add tests, commit, or open tickets.

## Artifact layout

In the **target repo** (not this skills repo unless that is the target):

```
.working_items/{project}/
  scope.md                 # summary, scope, quality backlog, tracker
  agent_notes.md           # project-level code map
  steps/
    {NN}-{slug}.md         # one coarse vertical slice per file
```

`{project}` is a lowercase kebab-case slug. `{NN}` is zero-padded order
(`01`, `02`, …). No required step count.

## Rules (priority order)

Apply in this order when they conflict:

1. **Reduce system complexity**: optimize for simpler callers, fewer concepts, and less coordination—not the smallest diff or fastest implementation.
2. **Deep modules**: prefer small, intent-oriented interfaces that hide substantial cohesive implementation complexity.
3. **Push complexity downward**: keep invariants, sequencing, representation, policy, error handling, and special cases behind the module that owns them.
4. **Prefer clear boundaries**: minimize coupling, information leakage, pass-through layers, and duplicated orchestration. Organize around responsibility and knowledge, not execution order.
5. **Extend/reuse sound code**, but do not preserve shallow abstractions or misplaced responsibilities merely to minimize changes.
6. **Design deliberately**: for important or reshaped boundaries, consider alternative designs. Treat excessive coordination, awkward naming, or difficult-to-describe interfaces as signs the abstraction may be wrong.
7. **Keep the approved vertical slice**: larger changes are allowed when required to deepen a module or simplify its boundary; no unrelated cleanup or speculative generalization.
8. **Test restraint**: prefer high-signal contract tests over test volume; do not add tests merely to perform a red/green loop.
9. **Comments explain what code cannot**: document non-obvious intent, invariants, or rationale; avoid comments that restate understandable code.



## Deep-module design standard

Treat a module as any file, class, object, package, service, or subsystem with a boundary.

- Expose the smallest practical interface for the capability. Callers should express intent without coordinating internal steps.
- Favor fewer, deeper modules over shallow wrappers, pass-through methods, fragmented helpers, or interfaces that mirror implementation details.
- Co-locate state, policy, invariants, and related complexity when doing so reduces knowledge shared across modules.
- Prefer designs that eliminate invalid states and special cases rather than repeatedly exposing or handling them.
- Judge an abstraction by the complexity it removes from callers, not by its size or line count.
- Preserve public behavior and compatibility unless the approved plan explicitly includes an interface migration.
- New or reshaped public/module boundaries must be named in the approved plan; private implementation structure may evolve as needed to realize that design.

Use these rules when judging quality opportunities and how to **sequence**
steps so later work can deepen a module that an earlier step opens.
A main goal is refactoring that would not be possible if each step were
scoped in isolation.

## agent_notes.md

Task-level file for handoff between agents/chats. **Not** a second plan.

- Durable map of where code lives, entry points, gotchas, commands, and fragile areas
- Written for agents: paths, symbols, commands, one-line facts — no human prose
- **Create** the stub at project start. On resume, create if missing; do not block on backfill.
- **Write**: update in-section when durable knowledge appears (after research, after re-scope). **Do not rewrite the whole file.**
- **Bullets only**. Optional `#L` / symbol anchors when stable; prefer symbols over churning line numbers.
- **Banned**: plan duplication; user-facing summaries; approval status; speculative TODOs / design debate.
- **Prune**: prefer ≤~30 bullets. Merge duplicates; delete anything now obvious from code or already in `scope.md` / steps.
- Always keep all five section headers, even when empty.



#### Template `.working_items/{project}/agent_notes.md`

```markdown
# agent_notes — {project}

Agent-facing code map. Paths/symbols/commands/one-line facts only. No plan duplication.

## Key paths

## Entry points / flows

## Gotchas / invariants

## Commands

## Do not touch
```



## Out of scope

- Product code, tests, commits, pushes, GitHub/Jira writes
- File-level implementation plans or per-step task checklists
- Implementing any step in this chat



## Tasks

**use the TODO tool to track tasks**

### 1. Resume, slug, stubs

- Standardize `{project}` (kebab-case). Create `.working_items/{project}/` and `steps/` if missing.
- Create `agent_notes.md` from the template if missing.
- **Resume**
  - `scope.md` exists, `approved: false` → remaining clarify or **4. User review**. Do not rewrite from scratch.
  - `approved: true` and user did **not** ask to re-scope → chat: tracker status + next incomplete step link, then **5. Handoff**. Stop.
  - User asked to **re-scope** → read `scope.md`, steps, and `agent_notes.md`. Propose a roadmap diff. Do not overwrite completed step files (`status: done` or tracker `- [x]`). Adjust later steps only. Then clarify / rewrite unapproved later steps / **4**.
  - User said `refresh` on research only → keep decisions; re-research; then review if artifacts change.



### 2. Research & clarify

- **Research (codebase only)**. Map owning boundaries, call direction, leaked complexity, blast radius, migrations, dependencies, and quality opportunities. High level (systems/modules), not file-level diffs. Update `agent_notes.md`.
- **Clarify blocking user decisions only** (in/out of scope, which quality items to take now vs later, step order, compatibility/migration). If the codebase can answer, explore instead.
  - Ask in chat. **Do not use the Q&A/AskQuestion tool.**
  - All **independent** questions in **one** message. Number (`1.`, `2.`, …). Options `a)`, `b)`, … alphabetically; mark **(recommended)**. Users reply with ids (e.g. `1b 2a`). Custom replies allowed.
  - After answers, ask only follow-ups those answers (or new blocking facts) unlock. Pause before the next pass or before writing the plan.
- **DO NOT** write `scope.md` / steps while a blocking decision remains open.



### 3. Write artifacts



#### Template `.working_items/{project}/scope.md`

```markdown
---
project: {project}
approved: false
---

# Project: {title}

{summary - 1-2 sentences}

### Decisions from clarify

- D1: {resolved decision - brief; include chosen option}

## Scope

- **In**:
- **Out**:
- **Later**: {migrations / dependencies / known follow-ups}

## Quality backlog

- {opportunity} — now | later | out
  - {why sequencing/deepening beats a single isolated step}

## Dependencies / migrations

- {A before B; compatibility windows}

## Tracker

- [ ] Step 1: {title} — [steps/01-{slug}.md](steps/01-{slug}.md)

## Tradeoffs / push-outs

- none
```

Tracker marks: `- [ ]` pending, `- [o]` in progress, `- [x]` done.

#### Template `.working_items/{project}/steps/{NN}-{slug}.md`

```markdown
---
project: {project}
step: {NN}-{slug}
status: pending
---

# Step {NN}: {title}

{intent - 1-2 sentences}

## Parent

[scope.md](../scope.md)

## In scope

## Out of scope

## Likely owning boundary

## Dependencies

## Risks

## Quality / deepening

- {what this step opens for later deepening, or what it must not paint into a corner}
```

Keep step files **coarse**: intent, in/out, likely boundary, deps, risks,
deepening. Not an implementation plan.

Quality items: persist the full backlog on `scope.md`. Only **now** items
become steps (or bullets on a step). Do not grow the project by default.

Optional ticket/PR links if the user provided them; do not create tickets.

### 4. User review

- Chat: **maximum 3–4 bullets** (outcomes, step sequence, quality-now vs later) + relative link to `scope.md`.
- Ask for **APPROVED**. Revisions → update artifacts → review again.
- **DO NOT** implement or hand off until **APPROVED**. Then set `approved: true` in `scope.md`.



### 5. Handoff (stop)

- Prompt a **new chat** with `/d-antigravity` and a relative link to the first incomplete step file.
- Do not implement here.

