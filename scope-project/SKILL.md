---
name: scope-project
description: >-
  High-level project scoping for large, multi-PR / multi-week changes:
  codebase research, alignment, a durable tracker, architecture notes, and
  coarse step files. Tracks migrations, dependencies, known follow-ups, and
  cross-step refactoring. Planning and tracking only — never implements.
  Use when the user invokes scope-project or wants to roadmap a major
  change before development.
disable-model-invocation: true
---

# Scope project

Research a large change, reach a **shared understanding** with the user, and
write a **project** tracker, **architecture** notes, and coarse **step** files
under `.working_items/{project}/`. Human-review the roadmap, then stop.

This skill tracks the project: migrations, dependencies, edge cases, future
issues, and refactoring/deepening that is only coherent across steps. Prefer
**few** steps. Split on migrations, dependencies, rollback units, and
module-deepening sequence — not on file count or tickets.

On resume, trust on-disk `scope.md` / `architecture.md` over chat memory. Do
not restore an older plan from this conversation.

**Never** change product code, add tests, commit, or open tickets.

## Artifact layout

In the **target repo** (not this skills repo unless that is the target):

```
.working_items/{project}/
  scope.md                 # summary, in/out/later, deps, tracker, tradeoffs
  architecture.md          # map, quality, edge cases, target design, deepening
  agent_notes.md           # project-level code map (paths/symbols/gotchas)
  steps/
    {NN}-{slug}.md         # start-work brief for one coarse vertical slice
```

`{project}` is a lowercase kebab-case slug. `{NN}` is zero-padded order
(`01`, `02`, …). No required step count.

**Write these files as**

- `scope.md` — scope and tracker. Single `approved:` flag. No deep modules,
  quality backlog, or edge cases here.
- `architecture.md` — short design: where the change lives, quality notes,
  non-obvious edge cases, recommended architecture, how steps sequence
  deepening. Keep it short; put paths/symbols/commands in `agent_notes.md`.
- `agent_notes.md` — agent-only code map. Not a second plan.
- `steps/` — start-work brief for that slice. Each step links `scope.md`,
  `architecture.md`, and **every** sibling step so a handoff that names only
  the step can reach the rest.

## When writing architecture and steps

A module is any file, class, object, package, service, or subsystem with a
boundary. Use this list to judge quality notes and how to split or sequence
steps. Do not paste it into artifacts.

- Prefer fewer, deeper modules: small intent-oriented interfaces. Hide
  sequencing, policy, representation, errors, and special cases behind the
  owner. Organize around responsibility and knowledge, not execution order.
- Optimize for simpler callers and less coordination, not the smallest diff.
  Do not keep a shallow wrapper or misplaced responsibility just to minimize
  change.
- Sequence steps so a later step can deepen a module that an earlier step
  opens. Do not lock a later step into a design it cannot deepen.
- Keep the approved slice: larger changes are allowed when they deepen a
  module or simplify its boundary; no unrelated cleanup or speculative
  generalization.
- Name new or reshaped public/module boundaries in the plan. Preserve public
  behavior unless the plan includes an interface migration.
- Judge an abstraction by complexity removed from callers, not by size.
  Compare a few boundary options in alignment chat when the interface is hard
  to describe. Do not add extra design files or diagrams.

## Quality notes

A quality note is real only with all three: a concrete trigger (how a future
change or caller is harder), the leaked or misplaced knowledge, and a fix
direction. Include when research finds:

- leaked complexity (callers must know sequencing, policy, representation, or special cases)
- a shallow boundary (wrapper, pass-through, fragmented helper, or interface that mirrors internals)
- misplaced responsibility (invariant or orchestration split across modules, or organized by execution order instead of knowledge)
- invalid states or special cases left in callers instead of eliminated behind the owning module
- a hard-to-describe or awkwardly coordinated boundary that will make future change harder
- comments that restate obvious code, or missing comments where a non-obvious invariant/rationale is required

Do not dump style, naming, or formatting. Do not promote later/out cleanups
into in-work deepening unless they are tracker steps.

## agent_notes.md

Task-level file for handoff between agents/chats. **Not** a second plan.

- Durable map of where code lives, entry points, gotchas, commands, and fragile areas
- Written for agents: paths, symbols, commands, one-line facts — no human prose
- **Create** the stub at project start. On resume, create if missing; do not block on backfill.
- **Write**: update in-section when durable knowledge appears (after research, after re-scope). **Do not rewrite the whole file.**
- **Bullets only**. Optional `#L` / symbol anchors when stable; prefer symbols over churning line numbers.
- **Banned**: plan duplication; user-facing summaries; approval status; speculative TODOs / design debate.
- **Prune**: prefer ≤~30 bullets. Merge duplicates; delete anything now obvious from code or already in `scope.md` / `architecture.md` / steps.
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

## Align to current document standards

If existing project files do not match the templates in this skill (missing
`architecture.md`, old headings on `scope.md` such as Deep modules / Quality
backlog, old step sections, missing `agent_notes.md` headers), update them to
the current layout.

- Move content into the correct files and sections. Create missing files from
  the templates.
- If a section has no content, use `- none` where the template allows it.
  Still fill **Where this change lives** from `agent_notes.md` / existing
  steps.
- Matching the current layout is **not** a re-scope.
- Changing in-scope refactoring versus already-approved outcomes **is** a
  re-scope — align if needed, then **4. User review**.

## Tasks

Create TODO items for **1. Resume**, **2. Research then align**, **3. Scope
and architecture**, **4. User review**, and **5. Handoff**. Mark each
complete when you finish it. Skip **2** when resuming an approved project
with no re-scope and no `refresh`.

### 1. Resume

- Standardize `{project}` (kebab-case). Create `.working_items/{project}/`
  and `steps/` if missing.
- If files are missing or do not match current templates, apply **Align to
  current document standards**. Do not block on fully backfilling
  `agent_notes.md`.
- Then:

| Condition | Action |
| --- | --- |
| `scope.md` missing | **2. Research then align**, then **3**, **4**. |
| `approved: false` | Finish remaining alignment or **4. User review**. Do not rewrite from scratch. |
| `approved: true`, user did not ask to re-scope | Chat: tracker status + next incomplete step link. Then **5. Handoff**. Stop. Trust on-disk files; do not restore an older plan from chat. |
| User asked to **re-scope** | Read all artifacts. Propose a roadmap diff. Do not overwrite completed steps (`status: done` or tracker `- [x]`). Adjust later steps only. Align / rewrite unapproved later steps / **4**. |
| User said `refresh` (research only) | Keep decisions; re-research; **4** if artifacts change. |

### 2. Research then align

Do this **before** writing `scope.md`, `architecture.md`, or steps.

- **Research the codebase first.** Map owning boundaries, call direction, leaked complexity, blast radius, migrations, dependencies, quality opportunities (Quality notes above), edge cases that may not be obvious, and which modules this work should deepen. High level (systems/modules), not file-level diffs. Ground names in this repo (paths/symbols in `agent_notes.md`). Do not invent APIs or modules from chat or the web. Update `agent_notes.md`.
- **Web search is allowed** to improve recommendations (library pitfalls, established patterns, migration notes). It does not replace tracing this repo. If an external note changes a recommendation, mention it briefly in `architecture.md` when you write that file.
- **Align for a shared understanding** (in/out of scope, which quality items to take now vs later, step order, compatibility/migration). Goal is alignment, not a minimal interrogatory. If the codebase can answer, explore instead of asking.
  - Ask in chat. **Do not use the Q&A/AskQuestion tool.**
  - All **independent** questions in **one** message. Number (`1.`, `2.`, …). Options `a)`, `b)`, … alphabetically; mark **(recommended)**. Users reply with ids (e.g. `1b 2a`). Custom replies allowed.
  - After answers, ask only follow-ups those answers (or new facts that still need user judgment) unlock. Pause before the next pass or before writing artifacts.
- **DO NOT** write `scope.md` / `architecture.md` / steps while an alignment question that would change outcomes remains open.

### 3. Scope and architecture

If writing reveals a gap, research it now. If that unlocks a new fork that still needs user judgment, pause and return to **2**. Do not reopen already-answered decisions.

Write `scope.md`, `architecture.md`, and every step file together.

#### Template `.working_items/{project}/scope.md`

```markdown
---
project: {project}
approved: false
---

# Project: {title}

{summary - 1-2 sentences}

### Decisions from alignment

- D1: {resolved decision - brief; include chosen option}

## Scope

- **In**:
- **Out**:
- **Later**: {migrations / dependencies / known follow-ups}

## Dependencies / migrations

- {A before B; compatibility windows}

## Tracker

- [ ] Step 1: {title} — [steps/01-{slug}.md](steps/01-{slug}.md)

## Tradeoffs / push-outs

- none
```

This agent writes new tracker rows and new step files as pending (`- [ ]`,
`status: pending`). On resume, **read** `- [o]` (in progress) and `- [x]`
(done) and each step file’s `status`. Implementers may set those marks. Do
not set in progress while only scoping.

Do **not** put deep modules, quality backlog, or edge cases on `scope.md`.

#### Template `.working_items/{project}/architecture.md`

```markdown
# Architecture — {project}

Short human map and target design. Paths/symbols/commands live in `agent_notes.md`.

## Where this change lives

{1 short paragraph or a few bullets: owning modules, call direction, what sits next to this work}

## Quality notes

{items that include trigger, leak, and fix direction. `- none` if research found nothing in-scope}

- **{boundary}**: {leaked or misplaced knowledge} → {why future change is harder} → {fix direction}

## Edge cases

Non-obvious cases this work must cover (or explicitly defer). `- none` if nothing beyond the happy path.

- {case}: {why it is easy to miss} — cover now | later | out

## Recommended architecture

Target abstractions, ownership, and call flows to build into this plan.

- **{abstraction / boundary}**: {what it owns; what callers see}
- **Call flow**: {A → B → C in the target design}

## Deep modules

In-work boundary deepening for **this** project. `- none` if this project does not reshape boundaries.

- **{module / boundary}**: {what's shallow or leaked today} → {target: smaller interface; complexity owned here}. Steps: {NN, …}. Do not {what this step must not lock in so a later step can still deepen the module}.

## Quality backlog

- {opportunity} — now | later | out
  - {why sequencing/deepening beats a single isolated step}
```

Keep architecture **short**. Module-level prose is enough. Do not add extra
architecture-decision files or diagrams. Compare a few boundaries in
alignment chat when needed; do not require a parallel bake-off. Judge
deepening by complexity removed from callers, not by diff size. Leave
**later/out** cleanups in Quality backlog; do not promote them into Deep
modules unless they are tracker steps.

Quality items: persist the full backlog on `architecture.md`. Only **now**
items become steps (or bullets on a step). Do not grow the project by default.

#### Template `.working_items/{project}/steps/{NN}-{slug}.md`

```markdown
---
project: {project}
step: {NN}-{slug}
status: pending
---

# Step {NN}: {title}

{intent - 1-2 sentences}

## Related

- Scope: [scope.md](../scope.md)
- Architecture: [architecture.md](../architecture.md)
- Steps: [01-{slug}.md](01-{slug}.md), [02-{slug}.md](02-{slug}.md) (every sibling, including this file)

## In scope

## Out of scope

## Likely owning boundary

## Dependencies

## Risks

## Architecture slice

- Realize: {the piece of Recommended architecture / Deep modules this step owns}
- Do not: {what this step must not lock in so a later step can still deepen the module}
- Read: `scope.md` → `architecture.md` → this file → `agent_notes.md`
```

Keep step files as **start-work briefs**: intent, in/out, likely boundary,
deps, risks, the architecture slice for this step. Name contracts to
preserve. **Do not** list every file or a red/green task list — that is the
implementation plan after handoff (`/d-antigravity`).

A step is too small if it could ship as an isolated ticket without changing
what a sibling may deepen. Fold it, or leave that work for the
implementation-planning chat after handoff. Split when a later step cannot
deepen a module unless an earlier step opens the boundary, or when
rollback/migration/compatibility needs a seam.

If the user pasted ticket/PR URLs, link them on the relevant step or on
`scope.md`. Never create tickets.

### 4. User review

- Chat: **maximum 3–4 bullets** (outcomes, step sequence, in-work deepening vs later).
- Then relative links to `scope.md`, `architecture.md`, and **every** step file.
- If the user pasted ticket/PR URLs, include those links. Never create tickets.
- Ask for **APPROVED**. Revisions → update artifacts → review again.
- **DO NOT** implement or hand off until **APPROVED**. Then set `approved: true` in `scope.md`.

### 5. Handoff (stop)

- Prompt a **new chat** with `/d-antigravity` and a relative link to the
  first incomplete **step** file only. `/d-antigravity` is the
  implementation-planning skill; it writes the implementation plan. This
  skill does not. The step file links scope and architecture.
- Do not implement here.
