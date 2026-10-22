---
name: d-antigravity
description: >-
  Phased development workflow (antigravity-style) for maintainable systems.
  Prefer over r-antigravity when architecture and code quality matter:
  deep-module design, vertical-slice phases, and explicit approval before
  each phase. Optional: a linked /scope-project step as input;
  works unchanged without one.
disable-model-invocation: true
---

# Antigravity workflow (development)

Ship one approved vertical slice at a time with simple, stable interfaces that
hide cohesive implementation complexity. The asked outcome takes the effort.
Agent-proposed deepening must relate to that outcome, appear under **Refactor**,
and stay within about 10–20% of the effort. All artifacts live under
`.working_items/{task}/`. Follow **Tasks** in order.

## Artifact layout

```
.working_items/{task}/
  phase_plan.md                 # optional; once per task
  agent_notes.md                # always; task-level code map for agents
  phase-{N}/                    # one folder per phase (or phase-1 if no phase plan)
    implementation_plan.md
    tasks.md
    walkthrough.md              # written after that phase verifies
    verify.sql | verify.py      # optional; human post-pipeline checks
```

`{N}` is the 1-based phase index from `phase_plan.md` (or `1` when there is no phase plan). **Never overwrite** a completed phase folder — always create a new `phase-{N}/` for the phase this chat is working.

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

## Design rules (priority order)

A module is any file, class, object, package, service, or subsystem with a boundary. Apply in this order when they conflict. Rules 1–6 shape the approved design. They do not authorize work outside the asked task. Agent-proposed deepening must relate to that task, appear in **Refactor**, be approved with the plan, and stay within about 10–20% of the effort. Deepening the user or an attached step already asked for is part of the asked outcome.

1. **Reduce system complexity**: optimize for simpler callers, fewer concepts, and less coordination—not the smallest diff or fastest implementation. Lines that simplify no caller (guards, wrappers, reformatting, redundant tests) are complexity, not thoroughness.
2. **Deep modules**: prefer small, intent-oriented interfaces that hide substantial cohesive implementation. Callers express intent without coordinating internal steps. Favor fewer, deeper modules over shallow wrappers, pass-through methods, fragmented helpers, or interfaces that mirror implementation details.
3. **Push complexity downward**: keep invariants, sequencing, representation, policy, and special cases behind the module that owns them. Owning error handling means the module absorbs or surfaces errors that already arise there — not adding new guards. Co-locate state, policy, invariants, and related complexity when that reduces knowledge shared across modules. Prefer eliminating invalid states and special cases over repeatedly exposing them.
4. **Prefer clear boundaries**: minimize coupling, information leakage, pass-through layers, and duplicated orchestration. Organize around responsibility and knowledge, not execution order.
5. **Judge abstractions by caller complexity removed**, not by size or line count. For important or reshaped boundaries, consider alternative designs. Treat excessive coordination, awkward naming, or difficult-to-describe interfaces as signs the abstraction may be wrong.
6. **Extend/reuse sound code**, but do not preserve shallow abstractions or misplaced responsibilities merely to minimize changes.
7. **Keep the approved vertical slice**: deliver the asked outcome. Related deepening belongs under **Proposed changes** → **Refactor** and is allowed only after **APPROVED**. Private restructuring happens only as that section names it, inside its named files or boundary. With no **Refactor** section, do not move complexity, remove paths, or redesign a boundary. Preserve public behavior and compatibility unless the approved plan includes an interface migration. No unrelated cleanup or speculative generalization.
8. **Trust internal callers**: validate only at trust boundaries named in **Scope limits** (user input, external I/O, warehouse rows, config). Inside the boundary, trust callers and the type system and let existing errors propagate. No new guards, wrappers, re-validation of already-checked data, or new exception types (e.g. `isinstance`, `None` checks, `try/except`) beyond that.
9. **Test restraint**: prefer high-signal contract tests over test volume; do not add tests merely to perform a red/green loop.
10. **Comments explain what code cannot**: document non-obvious intent, invariants, or rationale; avoid comments that restate understandable code.

## Diff hygiene

- Validation follows design rule 8.
- Match surrounding style. Only lines with a semantic change may differ from the recorded baseline. Run the repo formatter on a file only when that file was already formatter-clean at baseline (the format run must add no churn). Never run a whole-file or whole-repo formatter otherwise. No import reordering, quote-style, trailing-comma, or line-wrap edits on untouched lines.

## Tasks

Plans are bullets, not paragraphs. Keep each plan as short as it can be. Omit a section that adds nothing.

**Trackers**
- **TODO tool**: which *skill* step this chat is on (`1`, `2a`, `2b`, `2c`, `3`, `4`, `5`, `6`). Update it as you enter each step.
- **`phase-{N}/tasks.md`**: implementation work for the current phase (source of truth for coding steps).
- **`phase_plan.md` checkboxes**: phase-level `- [ ]` / `- [o]` / `- [x]`. `- [o]` is in progress. A `- [ ]` with a later `- [o]` or `- [x]` is skipped (computed, not stored). Any other `- [ ]` is open.

### 1. Review request, research & clarify

1. Standardize a unique `{task}` slug as a lowercase kebab-case identifier (e.g., `fix-auth-bug`). Create `.working_items/{task}/` if missing.
2. Create `.working_items/{task}/agent_notes.md` from the template if missing (stub with all five section headers).
3. **Parent project — default skip.** Do **not** search for a parent project. Attach only if one of these is true:
   1. The user links `.working_items/{project}/scope.md`, `architecture.md`, or `steps/{NN}-*.md`, **or** names `{project}` and that `scope.md` exists.
   2. A `phase-*/tasks.md` for this `{task}` already has `project:`.
   - If neither: skip the rest of this numbered list.
   - If attached:
     1. Start from the linked **step** (or the next `- [ ]`/`- [o]` tracker step if only `scope.md` / `architecture.md` was named).
     2. Follow that step’s `## Related` links to `{project}/scope.md`, `{project}/architecture.md`, and sibling steps; also read `{project}/agent_notes.md`.
     3. If `architecture.md` is missing, create it from leftover `scope.md` `## Deep modules` / `## Quality backlog` (or `- none`) without a full rewrite — deepening and quality live on `architecture.md`.
     4. Treat the **step** as the request. Honor the architecture slice and in-work deepening named for this step, and put that named deepening in **Refactor** as part of the asked outcome. Do not invent a different project. Do not explode the step into isolation-sized project-tracker tickets — granular checklists stay in this phase’s `tasks.md`.
     5. If creating a new task folder, `{task}` = `{project}--{step-stem}` (step filename without `.md`). Keep that slug if already set.
     6. Set that tracker line to `- [o]` if it was `- [ ]`.
     7. Trust on-disk `{project}/scope.md` and `architecture.md` over chat memory. On resume, include project tracker status in the chat summary.
4. Read existing `.working_items/{task}/phase_plan.md` if the user linked/named it or the file exists. If it exists, resolve `{N}` with **Phase choice** before research, planning, or edits. Then read that phase’s `phase-{N}/implementation_plan.md` and `phase-{N}/tasks.md` if present, then `agent_notes.md`. If phase choice asked a question, stop this step until the user answers. If there is no phase plan, skip phase choice.
5. **Research codebase** (only after `{N}` is resolved): Find the files and flows this task changes, and note impacts on that outcome. Update `agent_notes.md` with durable paths, symbols, gotchas, and commands not already in plans. Related deepening is a **Refactor** proposal, not extra implementation.
6. **Establish baseline**: Record the current branch/base commit and any pre-existing dirty files before implementation. Preserve unrelated user changes.
7. **Evaluate boundaries**: Identify the owning boundary and any related deepening worth proposing under **Refactor**. Evaluation is not approval to change that boundary.
8. **Align**: Shared understanding of forks that would change outcomes (externally observable behavior, architecture/module boundaries, irreversible decisions, significant dependencies, substantial scope)—not a minimal interrogatory. If the codebase can answer, explore instead. For reversible implementation choices, pick the locally consistent option and note it in the plan.
   - Ask in chat. **Do not use the Q&A/AskQuestion tool.**
   - All **independent** questions in **one** message. Number (`1.`, `2.`, …). Options as indented `- a)`, `- b)`, … alphabetically; mark **(recommended)**. Users reply with ids (e.g. `1b 2a`).

     ```
     1. Where should drafts persist?
        - a) Existing documents table
        - b) (recommended) New drafts table
        - c) Local files only
     2. Who can edit drafts?
        - a) (recommended) Author only
        - b) Any project member
     ```

   - After answers, ask only follow-ups an answer blocked or changed (or new facts that still need user judgment). Pause before the next pass or before planning.
9. **DO NOT** write the phase plan or implementation plan while a phase-choice question or an alignment question that would change outcomes remains open.

#### Phase choice

Run only when `phase_plan.md` exists. Status comes from its checkboxes only. An incomplete `phase-{N}/tasks.md` does not change status. Do not store a skipped mark.

Classify each phase in order:

- `- [x]` — complete. Not a candidate.
- `- [o]` — in progress. Label `[In progress]`.
- `- [ ]` with any later phase `- [o]` or `- [x]` — skipped. Label `[skipped]`.
- Any other `- [ ]` — open. Label `[open]`.

The **next open** phase is the first open phase. Candidates, in phase order, are every in-progress phase, every skipped phase, and the next open phase when one exists. Do not list complete phases, or open phases after the next open one.

- If the user names a phase (its number, its title, or a link to that phase’s files), that phase is `{N}`. Do not ask. If that phase is `- [x]`, do not overwrite its folder; tell the user it is complete.
- If there are no candidates, stop. The phase plan is complete. Do not open another phase.
- If there is one candidate, that phase is `{N}`. Do not ask. A finished `- [x]` prefix followed only by `- [ ]` phases is this case: start the first open phase.
- If there are two or more candidates, ask and stop. Do not research, plan, edit checkboxes, or take the routing table until the user answers. The question is the whole message. No “(recommended)” mark. Each option is the phase title only (`Phase {N}: {title}`), not the slice or `Verify:` clause.

  ```
  1. Which phase should I work on next?
     a. Phase 1 [In progress]: {title}
     b. Phase 2 [open]: {title}
  Respond `1a` to start on phase 1
  ```

  The reply line names option `a` and that option’s phase number. `1a` selects option `a`.

After the answer, `{N}` is the chosen phase. Leave every other phase’s checkbox unchanged.

Use the first matching row. When `phase_plan.md` existed at the start of this step, `{N}` is the phase from **Phase choice**. Otherwise the row sets `{N}`. Create or reuse `phase-{N}/` for *this* phase only; do not reuse or overwrite other phase folders.

| If | `{N}` | After clarify, go to |
| --- | --- | --- |
| `phase-{N}/tasks.md` exists, checklist incomplete, `approved: true` | that phase | **4** Implementation (or **5** if `phase: verification`). Skip remaining clarify/planning. Read plans then `agent_notes.md` before coding. |
| `phase_plan.md` exists (or user linked/named it) | chosen phase | **2c**. Chat-summarize completed phases, next title, resume point. Do not rewrite the phase plan unless the user asked. |
| A phase plan is needed (criteria in **2a**) and `phase_plan.md` is missing | set in 2a | **2a** |
| Else | `1` | **2c** (`phase-1/`). Still maintain `agent_notes.md`. |

### 2a. Develop a phase plan (optional)
Create a phase plan only when one of these applies:
- Work contains multiple independently shippable behaviors, **or**
- A migration or compatibility transition is required, **or**
- The work is likely to span multiple context windows.

A new module, several boundaries, or uncertainty about which code to extend does not by itself require a phase plan. Otherwise skip to **2c** (use `phase-1/`).

#### Phase size limits
- Each phase is one **vertical slice** that can ship and verify on its own.
- Prefer a checklist of **≤5 implementation steps** per phase.
- Scope a phase around one coherent outcome. It may change the files that outcome needs.
- Split a phase when it contains another independently shippable behavior, a separate migration or compatibility transition, or work that needs its own context window.
- Phases must be vertical slices, not horizontal layers (e.g., "Add DB table" is bad; "Add 'Save Draft' button that writes to DB" is good).

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

- [ ] Phase 1: {title} — {one-line vertical slice}. Verify: {how this phase is shown done}
- [ ] Phase 2: {title} — {one-line vertical slice}. Verify: {how this phase is shown done}
```

After drafting the phase plan, proceed to **2b**.

### 2b. Phase plan chat summary
If you wrote `phase_plan.md` in **2a**, do **2b**. Else go to **2c**.
- In the chat, answer: "Brief overview of how each phase fixes the issue." Then add a relative link to `.working_items/{task}/phase_plan.md`.
- **Do not ask for APPROVED** here. The only approval gate is step **3**.
- If the user requests phase-plan revisions, update the plan, then present **2b** again.
- Then proceed to **2c**. Include the phase plan in the implementation-plan review at step 3.

### 2c. Develop an implementation plan
Use `{N}` from **Phase choice**. If this chat just wrote `phase_plan.md` in **2a**, `{N}` is its first `- [ ]` phase (do not ask; a new plan is all open). If there is no phase plan, `{N}` is `1`. Create directory `.working_items/{task}/phase-{N}/` if missing.

**Always write fresh** `implementation_plan.md` and `tasks.md` into that phase folder. Do **not** overwrite or edit artifacts under other `phase-*` folders. If this phase folder already has incomplete work (resume mid-phase), keep existing files and continue; otherwise create new ones. If a parent project is attached, include `project:` and `step:` in `tasks.md` frontmatter.

If a phase plan is being used, limit scope to phase `{N}` and change that phase’s `- [ ]` to `- [o]` in `phase_plan.md`.

Keep the plan as short as it can be while still approving the diff. Product language. One line per item.

Implementation-plan format:
- **Expected diff** is advisory. It estimates product-code size excluding tests: `~{lines} lines across {files} files`. Use `{lines}` and `{files}` here — `{N}` is the phase index. Size does not stop the phase.
- Omit **RISKS** and **IMPORTANT** independently when empty; do not add `none` placeholders. Risks cover possible breaking changes caused by the work. Important covers only non-obvious implications. If an item fits both, put it only under Risks. Behavior belongs under **Proposed changes**.
- **Decisions from clarify**: when `phase_plan.md` or an attached parent step already records them, write `see phase plan` or `see {step}` instead of copying them.
- **Proposed changes**: write the section as the answer to "Walk me through how this fixes the issue step by step." Use numbered steps. Under each step, list the files or functions it touches as sub-bullets. Cover only this phase, and name anything that is deferred.
- **Refactor**: omit unless this phase includes deepening related to the task. Deepening the user or an attached step already asked for is part of the outcome. Agent-proposed deepening stays within about 10–20% of the effort. This section is the only approval for private restructuring. Name what moves behind the boundary, the files or boundary, and the caller simplification.
- **Deep-module design**: three one-sentence bullets. **Scope limits** names what this phase will not change and any new trust-boundary validation. Default validation is `none — trust callers; existing errors propagate`. Anything not named there is unplanned.
- **Verification**: existing coverage, new or extended cases, and manual checks. This is the only authorization for planned new or extended tests. Prefer the minimum cases that distinguish the approved public contracts. Prefer extending an existing case. If none are needed, write `none — reuse existing`. Test bans live in **4** Implementation.
- When a parent project is attached, link the approved step file and `architecture.md`. Do not restate their architecture or decisions. Keep **Proposed changes** (including **Refactor** when this phase deepens), the **Scope limits** bullet, **Expected diff**, and **Verification**. Omit the other sections unless this phase adds a decision the step does not contain.
- **Human verify file**: name `none`, `verify.sql`, `verify.py`, or both, and what it would assert. Step **5** writes the script.

#### Template `.working_items/{task}/phase-{N}/implementation_plan.md`
```markdown
# Implementation Plan: {title} (Phase {N})

## Problem statement

{one sentence: the need, in product language}

**Expected diff** (advisory): ~{lines} lines across {files} files (excluding tests)

## User Review Required

### RISKS

1. {possible breaking change — omit this section when none}

### IMPORTANT

1. {non-obvious implication — omit this section when none}

### Decisions from clarify

- {`see phase plan` / `see {step}` / one brief decision}

## Proposed changes

1. **{step in how this fixes the issue}**
   - {file or function}
2. **{next step}**
   - {file or function}

### Refactor

{omit this whole subsection unless this phase includes related deepening}

1. **{what moves behind the boundary}** — {caller simplification; files or boundary}

## Deep-module design

- **Boundary**: {owning boundary, who calls it, what this slice does not own}
- **Complexity hidden**: {what moves behind the boundary, or `none`}
- **Scope limits**: {what this phase will not change}. Validation: {named trust boundaries, or `none — trust callers; existing errors propagate`}

## Verification

- **Existing**: {commands / suites, or `none`}
- **New/extended**: {`none — reuse existing`, or `extend|new`: {case} — locks: {public contract}}
- **Test budget**: new: {N} | extended: {M} | reused only: {yes/no}
- **Manual**: {human steps, or `none`}
- **Human verify file**: {`none` | `verify.sql` | `verify.py` | both} — {observable result when a file is expected}
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
# when a /scope-project parent is attached:
# project: {project}
# step: {NN}-{slug}
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
The **only** APPROVED gate. Never treat 2b as approval.
- In the chat, first the plan’s **Boundary** sentence, verbatim. It names the owning boundary, who calls it, and what this slice does not own. When a parent step already defines that boundary, one sentence on what this phase changes is enough.
- Then answer "Walk me through how this fixes the issue step by step." from **Proposed changes**. Show the steps and their related notes; leave out the file and function sub-bullets. If the plan has a **Refactor** section, show it as a labeled step. End with a relative link to `.working_items/{task}/phase-{N}/implementation_plan.md`.
- If a phase plan is being used and its frontmatter is still `approved: false`, include its relative link in the same review (one gate covers both).
- Ask the user to reply with **APPROVED** to proceed. Repeat if revisions are requested.
- If the user requests plan revisions before APPROVED, update the plan/`tasks.md` (and phase plan if needed), then present this review again.
- **DO NOT proceed to Implementation without explicit "APPROVED" sign-off.** Once approved, set `approved: true` and `phase: implementation` in `phase-{N}/tasks.md` frontmatter; if a phase plan is in this same review, also set `approved: true` in its frontmatter.

### 4. Implementation
- Implement via a **Contract-first verify** loop (not mandatory red/green per step).
- Spend the effort on the asked outcome. Agent-proposed complexity reduction beyond that outcome may use at most 10–20% of the effort. Further improvement waits for a plan revision.
- **Refactor**: Do this only when the approved plan has a **Refactor** section. Do only what that section names, inside its named files or boundary. With no **Refactor** section, do not move complexity, remove paths, or redesign a boundary.
- **Delegation is optional**: Use the `Task` tool (subagent) when the work is self-contained, parallelizable, mechanically large, or delegation materially protects the main agent's context budget. Keep implementation in the main agent when success depends heavily on architectural context accumulated during research or the change is tightly coupled.
- If delegating, copy the **subagent brief** below; fill `{task}` and `{N}`. Do not paste **Design rules**, **Diff hygiene**, or the `agent_notes.md` rules into the brief.

#### Subagent brief (copy)
```
Implement the approved phase. Read these files first, in order:
- .working_items/{task}/phase-{N}/implementation_plan.md
- .working_items/{task}/phase-{N}/tasks.md
- .working_items/{task}/agent_notes.md

Follow Design rules, Diff hygiene, and the agent_notes.md rules in the d-antigravity skill.

Stay within the approved plan. Do not start later phases. Do not add a public or module boundary, dependency, or concept the plan does not name. Private restructuring only as the plan’s Refactor section names it, inside that section’s files or boundary. If there is no Refactor section, do not refactor. Deliver the asked outcome. Agent-proposed improvement beyond that outcome may use at most 10–20% of the effort.

Follow the plan’s Verification for tests. Do not invent behavioral requirements. If implementation exposes a concrete regression in an already-approved public contract, a focused new or extended regression case is allowed; record it under ## Discoveries and report it as a verification-plan delta. Stop for re-approval only if the case changes the approved behavior, architecture, or scope.

As each checklist step completes, change `- [ ]` to `- [x]` in .working_items/{task}/phase-{N}/tasks.md. Update agent_notes.md in the relevant section when durable map knowledge is learned; check the notes checklist item when done. Do not rewrite agent_notes.md in full.

Return a clean summary of changes, commands run, discoveries, and Test budget (new: N | extended: M | reused only: yes/no).
```

- Follow **Contract-first verify** whether implementation is performed by the main agent or a subagent:
  - **Default**: Implement the approved change, then run **Existing**. No new test is required for wiring or plumbing.
  - **When New/extended lists a case**: light red→green only for that **net-new or extended public contract** — write or extend the listed case against observable boundary behavior, confirm it fails for the right reason (new) or asserts the new contract (extend), then make the smallest coherent change that passes while following the approved boundary design.
  - **When New/extended is `none — reuse existing`**: do not add planned tests; implement and run existing coverage (plus **Manual** when listed). A focused regression test is still allowed under the discovered-regression rule above.
  - **Ban**: tests for private helpers, call counts, mock interaction shape, duplicates of the same contract, or any test whose sole purpose is to satisfy a red/green ritual.
- **Discoveries**: Record material implementation discoveries in `tasks.md` — plan adjustments, newly discovered invariants, verification deltas, or unexpected scope. A local complexity reduction that relates to the task may be done inside the 10–20% budget for agent-proposed improvement. Pause for user guidance before private restructuring, a new or reshaped boundary, a migration change, a significant dependency, a public-behavior change, or other work the plan does not name.
- **Project report-back (optional)**: If a parent project is attached, write material tradeoffs and work pushed out of this step onto `{project}/scope.md` (`## Tradeoffs / push-outs`, `## Later`, later tracker steps / new last step). If deepening or quality work was dropped or deferred, patch `{project}/architecture.md` (`## Deep modules`, `## Quality backlog`, `## Edge cases` as needed; create the file from leftover scope headings if missing). Prefer deferring widening work over expanding this step. Pause if that changes approved project outcomes, owning boundaries, or drops/replaces a step. If no parent is attached, skip.
- Follow design rule 8 and **Diff hygiene**. Avoid placeholder code.

### 5. Verification
- **Main agent** owns verification and review artifacts (not the implementation subagent).
- Update `phase: verification` in `phase-{N}/tasks.md`.
- Execute all automated verification checks from the approved plan (**Existing** plus any listed **New/extended** cases) plus any focused regression case allowed and recorded under `## Discoveries`.
- Confirm the result matches the plan’s **Test budget** plus any recorded regression delta (`new: N | extended: M | reused only: yes/no`).
- **Soft warn (do not block)**: if tests were added beyond the approved Verification plan and were not a recorded regression delta, note them in the walkthrough and prefer removing or folding into an amended plan next time — still allow phase completion if checks pass.
- **Human verify file**: If the plan names `verify.sql` and/or `verify.py` (or landed behavior now requires one), write it under `phase-{N}/` from landed behavior. One file matching how a human inspects the result: SQL when the proof is warehouse rows/state; Python when the proof is API/files/logs/local artifacts. Both only if those proofs are independent. Names must be exactly `verify.sql` and/or `verify.py`. Script is read-only checks with comments stating expected rows/shape/invariants; exit non-zero or print a clear fail. Do not mutate data or trigger the pipeline from the script. Do **not** run warehouse/pipeline verify scripts (do not substitute Snowflake MCP). Local unit tests still run here as today. If not applicable, write `none` in the walkthrough and omit the file.
- When the plan has a **Refactor** section, verify callers use the interface that section names and that the obsolete paths it names are gone. With no **Refactor** section, do not require path removal or boundary consolidation.
- **Diff-to-plan check**: Review the final git diff against the recorded baseline. Confirm changed files and behavior match the approved vertical slice, unrelated user changes remain intact, and no unplanned public or module boundary, dependency, or private restructuring was introduced.
- **Unplanned validation (hard)**: If the diff adds guards, wrappers, re-validation, or exception types not named in **Scope limits**, remove them before the phase can complete. If one is actually required, stop for re-approval instead of keeping it. Do not count that stop as a repair attempt.
- **Formatting-noise check (hard)**: Compare `git diff` to `git diff -w --ignore-blank-lines` against the recorded baseline. Revert any hunk that disappears under `-w`, and any hunk whose only change is quotes, import order, wrapping, or trailing commas, before the phase can complete.
- **Expected-diff check (advisory)**: If the plan has an **Expected diff** and the actual product diff excluding tests is materially larger, report planned vs actual and what the extra lines are in the walkthrough. Size alone does not stop the phase.
- When the phase completes, list removed unplanned validation, reverted formatting-only hunks, and the advisory size note on the walkthrough **Extras beyond plan** line.
- **agent_notes hard check**: Re-read `.working_items/{task}/agent_notes.md`. Confirm it reflects this phase’s durable map/gotchas (prune superseded bullets; soft cap ~30). Ensure the `tasks.md` notes checkbox is checked. If there was no new durable knowledge, checking the box alone is enough — do **not** add meta status lines into `agent_notes.md`. Do **not** mark the phase complete until this check passes. If a parent project is attached, also patch `{project}/agent_notes.md` in-section for durable facts that outlive this step (same rules; no full-file rewrite).
- If checks fail: increment `verification_attempts`, classify the failure (`environment`, `existing baseline`, `implementation defect`, `verification defect`, or `plan invalidated`), and record the concise error/classification in `last_error` in `phase-{N}/tasks.md` frontmatter. Apply fixes and re-run when the failure is within the approved scope.
- If the same material failure class remains unresolved after **3 repair attempts**, halt and report logs. Halt earlier if resolution requires changing an approved behavioral/architectural decision or substantial scope. Do not treat unrelated sequential failures (e.g. compile, then lint) as the same stuck loop.
- **DO NOT proceed to review changes until Automated Verification passes and the unplanned-validation, formatting-noise, and expected-diff checks are clear.**
- If a phase plan is being used, change `- [o]` to `- [x]` in `phase_plan.md` for phase `{N}`.
- **Project tracker (optional)**: If attached: leave the project step `- [o]` while `phase_plan.md` still has `- [ ]` phases. If this completes the last phase (or there is no phase plan), set that tracker line to `- [x]` and the step file `status: done`.

### 6. Review changes
- **Main agent** creates `.working_items/{task}/phase-{N}/walkthrough.md` (new file for this phase; never overwrite another phase’s walkthrough).
- Print the chat wrap-up in this order (do not use GitHub; only this implementation pass vs the recorded baseline):
  1. **How this fixes the issue.** Answer "Walk me through how this fixes the issue step by step." for what landed in this phase. Name anything that is deferred.
  2. **Changed-path tree (chat only).** Nested tree of every path this pass changed vs the recorded baseline, with `+adds` / `-deletes` per file and directory subtotals. Include generated files and lockfiles. Do not use GitHub or a full-PR diff.
  3. **Human verify.** Numbered steps the user can run to confirm landed behavior after any required pipeline/job. Include a relative link to `verify.sql` and/or `verify.py` when those files exist. Do not trigger the pipeline from the agent.
  4. Relative link to the walkthrough file.
- Do not print Boundary, Summary of Changes, Code Overview, or test-budget/commands in chat.
- Copy the same step-by-step answer into `walkthrough.md`. Automated commands, contracts, test budget, and extras live in the walkthrough only. The path tree stays in chat.
- **Next phase (new chat)**: If `phase_plan.md` has remaining `- [ ]` phases, end with a short prompt to start a **new chat** for the next phase, and include a relative link to `.working_items/{task}/phase_plan.md` (and the next phase title). Do **not** implement the next phase in this chat — the next chat must create a new `phase-{N+1}/` with its own plan, tasks, and walkthrough.
- **Next project step (new chat)**: If a parent project is attached, this step is `- [x]`, and `scope.md` has later `- [ ]` steps, also prompt a **new chat** with `/d-antigravity` and a relative link to the next step file. Do not start that step here.

#### Walkthrough Template `.working_items/{task}/phase-{N}/walkthrough.md`
```markdown
# Walkthrough: {title} (Phase {N})

### How this fixes the issue
{same step-by-step answer as chat}

### Automated Verification
- Commands/suites run: {terse}
- Contracts covered: {terse}
- Test budget: new: {N} | extended: {M} | reused only: {yes/no}
- Regression deltas: {none | list}
- Extras beyond plan (soft warn): {none | extra tests}. Removed before completion: {none | unplanned validation}. Reverted formatting-only hunks: {none | list}. Expected diff (advisory): {planned vs actual, or `within estimate`}

### Manual Verification
1. {trigger pipeline/job or other human action — or `none`}
2. {run verify.sql / verify.py with relative link when present; what pass looks like}
```
