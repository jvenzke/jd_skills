---
name: d-antigravity
description: >-
  Phased development workflow (antigravity-style) for maintainable systems.
  Prefer over r-antigravity when architecture and code quality matter:
  deep-module design, vertical-slice phases, and explicit approval before
  each phase.
disable-model-invocation: true
---

# Antigravity workflow (development)

Simulates the antigravity cycle — research, clarify, plan, approval,
implement, review — with bounded vertical slices and a deep-module
design posture. Prefer simple, stable interfaces that hide cohesive
implementation complexity.

## Artifact layout

All artifacts live under `.working_items/{task}/`:

```
.working_items/{task}/
  phase_plan.md                 # optional; once per task
  agent_notes.md                # always; task-level code map for agents
  phase-{N}/                    # one folder per phase (or phase-1 if no phase plan)
    implementation_plan.md
    tasks.md
    walkthrough.md              # written after that phase verifies
```

`{N}` is the 1-based phase index from `phase_plan.md` (or `1` when skipping phases). **Never overwrite** a completed phase folder — always create a new `phase-{N}/` for the next incomplete phase.

## agent_notes.md (agent code map)

Task-level file for handoff between agents/chats. **Not** a second plan or walkthrough.

### Purpose
- Durable map of where code lives, entry points, gotchas, commands, and fragile areas
- Only information **not** already in `phase_plan.md`, `implementation_plan.md`, `tasks.md`, or `walkthrough.md`
- Written for agents: paths, symbols, commands, one-line facts — no human prose

### Rules
- **Create** the stub at task start. On resume, create the stub if missing; do not block on backfill.
- **Read order**: plans/tasks first (intent), then `agent_notes.md` (code map). Main agent and all subagents read it after plans on startup.
- **Write**: any agent that researched or changed code updates it when they learn durable knowledge. Edit the relevant section in place; **subagents must not rewrite the whole file**.
- **Update continuously** whenever durable knowledge appears, plus checkpoints after research, after implementation, and during Verification.
- **Bullets only**: each bullet is a repo-root-relative path, symbol, command, or one-line verified fact. Optional `#L` / symbol anchors when stable; prefer symbols over churning line numbers.
- **Banned**: plan/walkthrough duplication; user-facing summaries; approval status; test pass/fail narratives; phase changelogs; speculative TODOs / design debate.
- **Prune**: prefer ≤~30 bullets total. Keep a note only when it would be expensive or non-obvious for a fresh agent to rediscover from the repository. Merge duplicates; delete anything now obvious from code or already in plans. Keep still-true gotchas and `Do not touch`.
- Always keep all five section headers, even when empty.

#### Template `.working_items/{task}/agent_notes.md`
```markdown
# agent_notes — {task}

Agent-facing code map. Paths/symbols/commands/one-line facts only. No plan duplication.

## Key paths

## Entry points / flows

## Gotchas / invariants

## Commands

## Do not touch
```

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

* Expose the smallest practical interface for the capability. Callers should express intent without coordinating internal steps.
* Favor fewer, deeper modules over shallow wrappers, pass-through methods, fragmented helpers, or interfaces that mirror implementation details.
* Co-locate state, policy, invariants, and related complexity when doing so reduces knowledge shared across modules.
* Prefer designs that eliminate invalid states and special cases rather than repeatedly exposing or handling them.
* Judge an abstraction by the complexity it removes from callers, not by its size or line count.
* Preserve public behavior and compatibility unless the approved plan explicitly includes an interface migration.
* New or reshaped public/module boundaries must be named in the approved plan; private implementation structure may evolve as needed to realize that design.

## Tasks
**use the TODO tool to track tasks**

### 1. Review request, research & clarify
- Standardize a unique `{task}` slug as a lowercase kebab-case identifier (e.g., `fix-auth-bug`). Create `.working_items/{task}/` if missing.
- Create `.working_items/{task}/agent_notes.md` from the template if missing (stub with all five section headers).
- **Entry / resume (phase plan linked or exists)**: If the user links or names a phase plan, or `.working_items/{task}/phase_plan.md` already exists:
  1. Read `.working_items/{task}/phase_plan.md` and, for the next incomplete phase, any existing `phase-{N}/implementation_plan.md` and `phase-{N}/tasks.md`.
  2. Read `.working_items/{task}/agent_notes.md` (create stub first if missing).
  3. Find the next incomplete phase (`- [ ]` or `- [o]`). Treat `- [o]` as the current in-progress phase. Let `{N}` be that phase’s 1-based index.
  4. Skip 2a/2b if `approved: true` in the phase plan frontmatter.
  5. Post a concise chat summary: completed phases, next phase title, and where work resumes — then clarify (below) before planning that phase (**create or reuse** `phase-{N}/` artifacts for *this* phase only; do not reuse or overwrite other phase folders).
- **Resuming mid-phase**: If `phase-{N}/tasks.md` exists with incomplete checklist items and `approved: true`, skip clarify/planning, resume at the first unchecked item, and continue Implementation/Verification as appropriate. Still read plans then `agent_notes.md` before coding.
- **No phase plan**: use `phase-1/` for all implementation artifacts. Still maintain `agent_notes.md`.
- **Research codebase**: Find relevant files, trace logical flows, and build a full understanding of the scope of changes, potential impacts, risks, and side-effects. Update `agent_notes.md` with durable paths/symbols/gotchas/commands not already in plans.
- **Establish baseline**: Record the current branch/base commit and any pre-existing dirty files before implementation. Preserve unrelated user changes.
- **Evaluate boundaries**: Identify the current public interface, complexity leaked to callers, duplicated orchestration, shallow wrappers, and invariants spread across modules. Determine which boundary should own that complexity.
- **Clarify blocking user decisions only**: Resolve uncertainty that materially affects externally observable behavior, architecture/module boundaries, irreversible decisions, significant dependencies, or substantial scope. If a question can be answered by exploring the codebase, explore instead; do not ask it. For reversible implementation choices, choose the locally consistent option and document any material assumption in the plan.
  - Ask all **independent** questions in a **single pass**. Number each with a stable id (`1.`, `2.`, …).
  - For each question, list options alphabetically (`a)`, `b)`, `c)`, …) and mark the recommended one. Users reply with ids (e.g. `1b 2a`).

    ```
    1. Where should drafts persist?
       a) Existing documents table
       b) (recommended) New drafts table
       c) Local files only
    2. Who can edit drafts?
       a) (recommended) Author only
       b) Any project member
    ```

  - After answers, ask only follow-up questions unlocked by those decisions or by new information that still require user judgment. Continue until no **blocking** user decisions remain.
  - Pause for the user's response before the next pass or before planning.
- **DO NOT proceed to phase plan or implementation plan while a blocking user decision remains unresolved**.
- **Next step after clarify**: If `.working_items/{task}/phase_plan.md` exists with `approved: true`, proceed to **2c**. If a phase plan is needed but not yet approved, proceed to **2a**. If no phase plan is needed, skip to **2c**.

### 2a. Develop a phase plan (optional)
Create a phase plan when **any** of these apply:
- Work contains multiple independently verifiable behaviors or slices, **or**
- Work crosses multiple architectural/module boundaries, **or**
- A migration or compatibility transition is required, **or**
- A new module/package is required, **or**
- It is unclear which existing code to extend, **or**
- The work is likely to span multiple context windows or has materially different rollback/risk between parts.

Otherwise skip to **2c** (use `phase-1/`). If no phase plan is used, only one **APPROVED** gate is required (step 3).

#### Phase size limits
- Each phase is one **vertical slice** that can ship and verify on its own.
- Prefer a checklist of **≤5 implementation steps** per phase.
- Scope a phase around one coherent module boundary. It may change many files when needed to move complexity behind that boundary and update its callers atomically.
- Split work when it spans independent behaviors, boundaries, or risk/rollback units, not merely to satisfy a file-count limit.
- Phases must be vertical slices, not horizontal layers (e.g., "Add DB table" is bad; "Add 'Save Draft' button that writes to DB" is good).

#### Rules for Brevity & Efficiency:
1. **No Fluff**: Keep the phase plan extremely crisp and bulleted. Avoid long-winded paragraphs or verbose descriptions.

#### Template `.working_items/{task}/phase_plan.md`
```markdown
---
task: {task}
approved: false
---

# Phase Plan: {title}

{summary - 1-2 sentences}

### Decisions from clarify

- D1: {resolved decision - brief; include chosen option}

## Proposed phases

- [ ] Phase 1: {Brief description of phase 1}
   * Details about phase 1 
- [ ] Phase 2: {Brief description of phase 2}
   * Details about phase 2
```

After drafting the phase plan, proceed to **2b**.

### 2b. Phase plan review
If a phase document is generated do the following. Otherwise skip to develop an implementation plan.
- Provide a highly concise, high-level summary of proposed phases **(maximum 3-4 bullets total)** in the chat, followed by a relative link to `.working_items/{task}/phase_plan.md`.
- If the phase plan itself introduces a major architectural, scope, migration, or irreversible decision that requires separate authorization, ask the user to reply with **APPROVED** before 2c and set `approved: true` once approved.
- If the user requests phase-plan revisions before APPROVED (or before proceeding when no separate gate), update the plan, then present **2b** again.
- Otherwise proceed to **2c** and include the phase plan in the implementation-plan approval at step 3; do not require a second formal gate.

### 2c. Develop an implementation plan
Determine `{N}` (next incomplete phase index, or `1` if no phase plan). Create directory `.working_items/{task}/phase-{N}/` if missing.

**Always write fresh** `implementation_plan.md` and `tasks.md` into that phase folder. Do **not** overwrite or edit artifacts under other `phase-*` folders. If this phase folder already has incomplete work (resume mid-phase), keep existing files and continue; otherwise create new ones.

If a phase plan is being used, limit scope to phase `{N}` and change that phase’s `- [ ]` to `- [o]` in `phase_plan.md`.

#### Rules for Brevity & Efficiency:
1. **No Fluff**: Keep the implementation plan extremely crisp and bulleted. Avoid long-winded paragraphs or verbose descriptions.

#### Template `.working_items/{task}/phase-{N}/implementation_plan.md`
```markdown
# Implementation Plan: {title} (Phase {N})

{summary - 1-2 sentences}

## User Review Required

### RISKS

1. {risk notes - terse list}

### IMPORTANT

1. {important notes - terse list}

### Decisions from clarify

- {D1, D2, ... from phase plan, or resolved decision if no phase plan}

## Proposed changes

{change description - terse bulleted list of impacted files and logic changes}

## Deep-module design

- **System context**: {owning boundary and its role in the system; who calls it, at a high level; what this slice does not own. One sentence default, two max. No file tree. Same sentence as the Step 3 chat line.}
- **Interface**: {small public surface callers will use}
- **Hidden complexity**: {sequencing, invariants, representation, errors, or dependencies moved behind it}
- **Caller impact**: {coordination or concepts removed from callers}
- **Boundary rationale**: {why this module should own the complexity}

## Verification plan

Automated Verification is the **only** place that authorizes planned new or extended tests. Prefer the minimum number of cases that distinguish the approved public contracts and material edge conditions. Prefer extending an existing case over adding a new one. If no new public contract needs locking, write `none — reuse existing` under New/extended cases.

### Automated Verification

**Existing coverage to run**
- {commands / suites / cases already covering this boundary — or `none`}

**New/extended cases** (each must name the public contract; else `none — reuse existing`)
- {extend|new}: {case} — locks: {public contract / observable behavior}
- Ban: private-helper tests, call-count/mock interaction tests, duplicate cases for the same contract, tests whose sole job is to go red then green, snapshot/golden files unless named here

### Manual Verification
{manual verification plan - terse bullet list; OK as primary check for low-risk plumbing when New/extended is none}
```

#### Template `.working_items/{task}/phase-{N}/tasks.md`
```markdown
---
task: {task}
phase_number: {N}
phase: planning
approved: false
verification_attempts: 0
last_error: null
---

# Checklist for: {task} (Phase {N})

- [ ] Step 1: {granular checklist step 1}
- [ ] Step 2: {granular checklist step 2}
- [ ] Update `.working_items/{task}/agent_notes.md` (or confirm no new durable knowledge)

## Discoveries

- none
```

After drafting `implementation_plan.md` and `tasks.md`, proceed to **3**.

### 3. User review
- In the chat, first a **System context** line (verbatim from the implementation plan’s Deep-module **System context** bullet): one sentence by default, two max. Name the owning boundary and its role so the user can tell what part of the system is changing; who calls it at a high level; what this slice does not own. No file tree. Always include it, even for thin wiring — still name the owning boundary.
- Then a highly concise, high-level summary of proposed changes **(maximum 3-4 bullets total)**, followed by a relative link to `.working_items/{task}/phase-{N}/implementation_plan.md`.
- If an unapproved phase plan is being used, include its relative link in the same review.
- Ask the user to reply with **APPROVED** to proceed. Repeat if revisions are requested.
- If the user requests plan revisions before APPROVED, update the plan/`tasks.md`, then present human review again.
- **DO NOT proceed to Implementation without explicit "APPROVED" sign-off.** Once approved, set `approved: true` and `phase: implementation` in `phase-{N}/tasks.md` frontmatter; if a phase plan is being approved in the same gate, also set `approved: true` in its frontmatter.

### 4. Implementation
- Implement via a **Contract-first verify** loop (not mandatory red/green per step).
- **Delegation is optional**: Use the `Task` tool (subagent) when the work is self-contained, parallelizable, mechanically large, or delegation materially protects the main agent's context budget. Keep implementation in the main agent when success depends heavily on architectural context accumulated during research or the change is tightly coupled.
- If delegating, the **subagent prompt MUST include** (verbatim constraints — do not omit):
  - Paths to `.working_items/{task}/phase-{N}/implementation_plan.md`, `.working_items/{task}/phase-{N}/tasks.md`, and `.working_items/{task}/agent_notes.md`
  - Instruct: read plans/tasks first, then `agent_notes.md`, before coding
  - The **Rules (priority order)** block from this skill
  - The **Deep-module design standard** block from this skill
  - The **agent_notes.md** rules (purpose, write/update, banned content, in-section edits only — no full-file rewrite)
  - Instruct: stay within the approved plan’s scope; do not start later phases; do not introduce a new public/module boundary, dependency, externally visible concept, or major abstraction unless the plan names it. Private implementation structure may evolve when needed to realize the approved design without widening scope.
  - Instruct: follow the approved plan’s **Automated Verification** for planned tests. Do not invent new behavioral requirements. If implementation exposes a concrete regression in an already-approved public contract, a focused new/extended regression case is allowed; record it under `## Discoveries` and report it as a verification-plan delta. Stop for re-approval only if the case changes the approved behavior, architecture, or scope.
  - Instruct: as each checklist step completes, the **subagent** must change `- [ ]` to `- [x]` in `.working_items/{task}/phase-{N}/tasks.md`
  - Instruct: update `agent_notes.md` in-section when durable map knowledge is learned; check the notes checklist item when done (or when intentionally confirming no new durable knowledge)
- Follow **Contract-first verify** whether implementation is performed by the main agent or a subagent:
  - **Default**: Implement the approved change, then run **Existing coverage to run**. No new test required for refactors, wiring, or plumbing.
  - **When New/extended cases lists a case**: light red→green only for that **net-new or extended public contract** — write/extend the listed case against observable boundary behavior, confirm it fails for the right reason (new) or asserts the new contract (extend), then make the smallest coherent change that passes while following the approved boundary design.
  - **When New/extended is `none — reuse existing`**: do not add planned tests; implement and run existing coverage (plus Manual Verification if listed). A focused regression test is still allowed under the discovered-regression rule above.
  - **Refactor**: Move complexity inward, simplify callers, remove obsolete shallow paths, and keep the public interface narrow; keep authorized tests green.
  - **Ban**: tests for private helpers, call counts, mock interaction shape, duplicates of the same contract, or any test whose sole purpose is to satisfy a red/green ritual.
- **Discoveries**: Record only material implementation discoveries in `tasks.md` — plan adjustments, newly discovered invariants, verification deltas, or unexpected scope. Adapt autonomously to local/reversible discoveries. Pause for user guidance if a discovery changes public behavior, an approved architecture/module boundary, migration strategy, significant dependency, or substantial scope.
- If delegated, instruct the subagent to return a clean summary of changes, commands run, discoveries, and Test budget (`new: N | extended: M | reused only: yes/no`) when finished.
- Maintain exact indentation/formatting; avoid placeholder code.

### 5. Verification
- **Main agent** owns verification and review artifacts (not the implementation subagent).
- Update `phase: verification` in `phase-{N}/tasks.md`.
- Execute all automated verification checks from the approved plan (Existing coverage + any listed New/extended cases) plus any focused regression case allowed and recorded under `## Discoveries`.
- Confirm Test budget matches the approved plan plus any recorded regression delta (`new: N | extended: M | reused only: yes/no`).
- **Soft warn (do not block)**: if tests were added beyond the approved Verification plan and were not a recorded regression delta, note them in the walkthrough and prefer removing or folding into an amended plan next time — still allow phase completion if checks pass.
- Verify callers use the intended simple interface and do not depend on newly private implementation details.
- Verify the refactor removed obsolete paths and did not leave duplicate orchestration across the old and new boundaries.
- **Diff-to-plan check**: Review the final git diff against the recorded baseline. Confirm changed files and behavior match the approved vertical slice, unrelated user changes remain intact, and no unplanned public/module boundary or dependency was introduced.
- **agent_notes hard check**: Re-read `.working_items/{task}/agent_notes.md`. Confirm it reflects this phase’s durable map/gotchas (prune superseded bullets; soft cap ~30). Ensure the `tasks.md` notes checkbox is checked. If there was no new durable knowledge, checking the box alone is enough — do **not** add meta status lines into `agent_notes.md`. Do **not** mark the phase complete until this check passes.
- If checks fail: increment `verification_attempts`, classify the failure (`environment`, `existing baseline`, `implementation defect`, `verification defect`, or `plan invalidated`), and record the concise error/classification in `last_error` in `phase-{N}/tasks.md` frontmatter. Apply fixes and re-run when the failure is within the approved scope.
- If the same material failure class remains unresolved after **3 repair attempts**, halt and report logs. Halt earlier if resolution requires changing an approved behavioral/architectural decision or substantial scope. Do not treat unrelated sequential failures (e.g. compile, then lint) as the same stuck loop.
- **DO NOT proceed to review changes until all Automated Verification checks pass.**
- If a phase plan is being used, change `- [o]` to `- [x]` in `phase_plan.md` for phase `{N}`.

### 6. Review changes
- **Main agent** creates `.working_items/{task}/phase-{N}/walkthrough.md` (new file for this phase; never overwrite another phase’s walkthrough).
- Provide a very brief summary in the chat including:
  - **System context**: The same sentence as the implementation plan (copy into the walkthrough). Owning boundary and role in the system — what part of the system changed. No file tree.
  - **Summary of Changes**: A 1-2 sentence high level overview.
  - **Verification**: Commands/suites run and contracts covered; **Test budget** `new: N | extended: M | reused only: yes/no` (must match the approved plan plus any recorded regression delta). Mention new/extended cases only if the plan listed them or they were a recorded regression delta. Soft-warn if other extras were added.
  - **Code Overview**: A numbered list of completed logical steps.
  - **User Review**: A relative link to the walkthrough file.
- **Next phase (new chat)**: If `phase_plan.md` has remaining `- [ ]` phases, end with a short prompt to start a **new chat** for the next phase, and include a relative link to `.working_items/{task}/phase_plan.md` (and the next phase title). Do **not** implement the next phase in this chat — the next chat must create a new `phase-{N+1}/` with its own plan, tasks, and walkthrough.

#### Walkthrough Template `.working_items/{task}/phase-{N}/walkthrough.md`
```markdown
# Walkthrough: {title} (Phase {N})

{summary - 1-2 sentences}

- **System context**: {same sentence as implementation plan Deep-module **System context**}

## User Review Required

### RISKS

1. {risk notes - terse list}

### IMPORTANT

1. {important notes - terse list}

## Changes made

{code changes - terse bulleted list of completed changes}

## Verification Results

### Automated Verification
- Commands/suites run: {terse}
- Contracts covered: {terse}
- Test budget: new: {N} | extended: {M} | reused only: {yes/no}
- Regression deltas: {none | list}
- Extras beyond plan (soft warn): {none | list}

### Manual Verification
{manual verification plan - brief steps for the user}
```
