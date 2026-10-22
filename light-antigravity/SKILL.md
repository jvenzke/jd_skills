---
name: light-antigravity
description: >-
  Single-plan development workflow for maintainable production code. Keeps
  d-antigravity's deep-module design, approval, implementation, and verification
  safeguards while managing the whole task through one flat, resumable plan with
  no phases. Prefer d-antigravity when independently approved vertical slices are
  wanted; prefer r-antigravity for research spikes and throwaway prototypes.
disable-model-invocation: true
---

# Light Antigravity workflow (development)

Ship the whole approved task from one implementation plan with simple, stable
interfaces that hide cohesive implementation complexity. Task size changes the
number of checklist steps, not the artifact shape: unfinished work resumes from
`tasks.md` in a later chat. There are no phase plans, phase folders, phase
checkboxes, or per-phase approvals.

The asked outcome takes the effort. Agent-proposed deepening must relate to that
outcome, appear under **Refactor**, and stay within about 10–20% of the effort.
All artifacts live under `.working_items/{task}/`. Follow **Tasks** in order.

## Artifact layout

```text
.working_items/{task}/
  implementation_plan.md
  tasks.md
  agent_notes.md
  walkthrough.md              # written after verification
```

`{task}` is a lowercase kebab-case slug. A completed task's artifacts are its
history; do not overwrite them for new work. Use a new task slug unless the user
explicitly asks to revise the completed artifacts.

## agent_notes.md (agent code map)

Task-level file for handoff between agents and chats. **Not** a second plan or
walkthrough.

### Purpose
- Durable map of where code lives, entry points, gotchas, commands, and fragile areas
- Only information **not** already in `implementation_plan.md`, `tasks.md`, or `walkthrough.md`
- Written for agents: paths, symbols, commands, one-line facts — no human prose

### Rules
- **Create** the stub at task start. On resume, create the stub if missing; do not block on backfill.
- **Read order**: plan and tasks first (intent), then `agent_notes.md` (code map). Main agent and all subagents follow this order on startup.
- **Write**: any agent that researched or changed code updates it when durable knowledge appears. Edit the relevant section in place; subagents must not rewrite the whole file.
- **Update continuously**, plus checkpoints after research, after implementation, and during Verification.
- **Bullets only**: each bullet is a repo-root-relative path, symbol, command, or one-line verified fact. Prefer symbols over churning line numbers.
- **Banned**: plan/walkthrough duplication; user-facing summaries; approval status; test pass/fail narratives; changelogs; speculative TODOs or design debate.
- **Prune**: prefer no more than about 30 bullets. Keep only facts expensive or non-obvious for a fresh agent to rediscover. Merge duplicates and remove facts now obvious from code or already in other artifacts. Keep still-true gotchas and `Do not touch`.
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

A module is any file, class, object, package, service, or subsystem with a
boundary. Apply these rules in order when they conflict. Rules 1–6 shape the
approved design; they do not authorize work outside the asked task.

1. **Reduce system complexity**: optimize for simpler callers, fewer concepts, and less coordination—not the smallest diff or fastest implementation. Lines that simplify no caller are complexity, not thoroughness.
2. **Deep modules**: prefer small, intent-oriented interfaces that hide substantial cohesive implementation. Favor fewer, deeper modules over shallow wrappers, pass-through methods, fragmented helpers, or interfaces that mirror implementation details.
3. **Push complexity downward**: keep invariants, sequencing, representation, policy, and special cases behind the module that owns them. Co-locate state, policy, and related complexity when that reduces knowledge shared across modules. Prefer eliminating invalid states and special cases over repeatedly exposing them.
4. **Prefer clear boundaries**: minimize coupling, information leakage, pass-through layers, and duplicated orchestration. Organize around responsibility and knowledge, not execution order.
5. **Judge abstractions by caller complexity removed**, not by size or line count. For important or reshaped boundaries, consider alternatives. Excessive coordination, awkward naming, or difficult-to-describe interfaces suggest the abstraction may be wrong.
6. **Extend or reuse sound code**, but do not preserve shallow abstractions or misplaced responsibilities merely to minimize changes.
7. **Keep the approved task**: deliver the asked outcome. Related deepening belongs under **Proposed changes** → **Refactor** and is allowed only after **APPROVED**. Private restructuring happens only as that section names it, inside its named files or boundary. With no **Refactor** section, do not move complexity, remove paths, or redesign a boundary. Preserve public behavior and compatibility unless the approved plan includes an interface migration. No unrelated cleanup or speculative generalization.
8. **Trust internal callers**: validate only at trust boundaries named in **Scope limits** (user input, external I/O, warehouse rows, config). Inside the boundary, trust callers and the type system and let existing errors propagate. No new guards, wrappers, re-validation of already-checked data, or new exception types beyond that.
9. **Test restraint**: prefer high-signal public-contract tests over test volume. Do not add tests merely to perform a red/green loop. Do not test private helpers, call counts, mock interaction shape, or duplicate contracts.
10. **Comments explain what code cannot**: document non-obvious intent, invariants, or rationale; avoid comments that restate understandable code.

## Diff hygiene

- Validation follows design rule 8.
- Match surrounding style. Only lines with a semantic change may differ from the recorded baseline.
- Run the repo formatter on a file only when that file was already formatter-clean at baseline and the run adds no churn.
- Never run a whole-file or whole-repo formatter otherwise. Do not reorder imports or alter quotes, trailing commas, or wrapping on untouched lines.

## Tasks

Plans are bullets, not paragraphs. Keep the plan as short as it can be. Omit a
section that adds nothing.

**Trackers**
- **TODO tool**: which skill step this chat is on (`1`, `2`, `3`, `4`, `5`, `6`). Update it when entering a step.
- **`tasks.md`**: the source of truth for the whole task's implementation work. Every numbered **Proposed changes** step must appear in its checklist. Add enough granular checklist items that a later chat can resume from the first unchecked item.

### 1. Review request, research, and clarify

1. Standardize a unique `{task}` slug and create `.working_items/{task}/` if missing.
2. Create `agent_notes.md` from the template if missing.
3. **Parent project — default skip.** Attach only if the user links `.working_items/{project}/scope.md`, `architecture.md`, or `steps/{NN}-*.md`; names `{project}` and its `scope.md` exists; or this task's `tasks.md` already has `project:`.
   - If attached, start from the linked step or the next open/in-progress tracker step; follow its `## Related` links; read project `scope.md`, `architecture.md`, sibling steps, and `agent_notes.md`.
   - If `architecture.md` is missing, create it from leftover `scope.md` `## Deep modules` / `## Quality backlog` content (or `- none`) without a full rewrite.
   - Treat the step as the request. Honor its architecture slice and in-work deepening. Do not explode it into separate project tickets; granular work stays in this task's `tasks.md`.
   - For a new task folder, use `{project}--{step-stem}`. Set the project tracker line to `- [o]` when it was open. Trust on-disk project artifacts over chat memory.
4. **Resume before replanning.** If `implementation_plan.md` or `tasks.md` exists, read them first and then `agent_notes.md`.
   - When `approved: true` and checklist work remains, resume at **4** Implementation or **5** Verification according to `status`. Post a short summary of where work stopped and continue from the first unchecked item.
   - When the plan exists but is unapproved, resolve only outstanding clarification, then return to **3** User review. Do not replace the plan merely because the chat is new.
   - When `status: complete`, do not overwrite the completed workflow for new work.
5. **Research codebase**: find the files, flows, risks, and owning boundary this task changes. Record durable paths, symbols, gotchas, and commands in `agent_notes.md`. Related deepening is a **Refactor** proposal, not extra implementation.
6. **Establish baseline**: capture the current branch, base commit, and pre-existing dirty files. Record them in `tasks.md` frontmatter when step 2 creates that file and before implementation begins. Preserve unrelated user changes.
7. **Evaluate boundaries**: identify the owning boundary and related deepening worth proposing under **Refactor**. Evaluation is not approval to change it.
8. **Align in a grill-me style**: reach shared understanding of every branch that changes outcomes—externally observable behavior, architecture/module boundaries, irreversible decisions, significant dependencies, or substantial scope.
   - Explore the codebase instead of asking anything it can answer. Choose locally consistent reversible implementation details and note them in the plan.
   - Ask all independent questions in one message. Number them (`1.`, `2.`, …), give alphabetized indented options, and mark a recommended answer. Users reply with ids such as `1b 2a`.
   - Resolve dependencies between decisions. Ask a follow-up pass only when an answer blocked or changed another decision, or research exposed a new outcome-changing fork.
   - Do not write or revise the implementation plan while an outcome-changing question remains open.

### 2. Develop an implementation plan

Create or resume `.working_items/{task}/implementation_plan.md` and
`.working_items/{task}/tasks.md`. Do not overwrite completed task artifacts.
When a parent project is attached, include `project:` and `step:` in
`tasks.md` frontmatter.

Implementation-plan rules:
- **Expected diff** is advisory and estimates product-code size excluding tests: `~{lines} lines across {files} files`.
- Omit **RISKS** and **IMPORTANT** independently when empty. Risks are possible breaking changes; Important is only non-obvious implications. Put an item in only one.
- **Decisions from clarify**: link the parent step when it already records them; otherwise record each resolved decision briefly.
- **Proposed changes** answers “Walk me through how this fixes the issue step by step.” Use numbered steps with touched files or functions as sub-bullets. Every numbered step must have one or more corresponding `tasks.md` checklist items.
- **Refactor**: omit unless task-related deepening is proposed. Name what moves behind the boundary, the affected files or boundary, and the caller simplification. Agent-proposed deepening stays within about 10–20% of the effort.
- **Deep-module design** has exactly three one-sentence bullets. **Scope limits** names what the task will not change and any trust-boundary validation. Default validation is `none — trust callers; existing errors propagate`.
- **Verification** authorizes tests. List existing coverage, new or extended public-contract cases, the test budget, and manual checks. Prefer the minimum cases that distinguish approved contracts and extend an existing case where possible. If no new coverage is needed, write `none — reuse existing`.
- When a parent project is attached, link its approved step and `architecture.md`; do not restate their architecture or decisions.

#### Template `.working_items/{task}/implementation_plan.md`

```markdown
# Implementation Plan: {title}

## Problem statement

{one sentence: the need, in product language}

**Expected diff** (advisory): ~{lines} lines across {files} files (excluding tests)

## User Review Required

### RISKS

1. {possible breaking change — omit this section when none}

### IMPORTANT

1. {non-obvious implication — omit this section when none}

### Decisions from clarify

- {`see {step}` or one brief resolved decision}

## Proposed changes

1. **{step in how this fixes the issue}**
   - {file or function}
2. **{next step}**
   - {file or function}

### Refactor

{omit this whole subsection unless the task includes related deepening}

1. **{what moves behind the boundary}** — {caller simplification; files or boundary}

## Deep-module design

- **Boundary**: {owning boundary, who calls it, what this task does not own}
- **Complexity hidden**: {what moves behind the boundary, or `none`}
- **Scope limits**: {what this task will not change}. Validation: {named trust boundaries, or `none — trust callers; existing errors propagate`}

## Verification

- **Existing**: {commands / suites, or `none`}
- **New/extended**: {`none — reuse existing`, or `extend|new`: {case} — locks: {public contract}}
- **Test budget**: new: {N} | extended: {M} | reused only: {yes/no}
- **Manual**: {human steps, or `none`}
```

#### Template `.working_items/{task}/tasks.md`

```markdown
---
task: {task}
status: planning
approved: false
verification_attempts: 0
last_error: null
baseline_branch: {branch}
baseline_commit: {sha}
baseline_dirty_files: {list or `none`}
# when a /scope-project parent is attached:
# project: {project}
# step: {NN}-{slug}
---

# Checklist for: {task}

- [ ] Step 1: {implements Proposed changes step 1}
- [ ] Step 2: {implements Proposed changes step 2}
- [ ] Run approved verification
- [ ] Update `.working_items/{task}/agent_notes.md` (or confirm no new durable knowledge)

## Discoveries

- none
```

Proceed to **3** after drafting both files.

### 3. User review

- In chat, first print the plan's **Boundary** sentence verbatim. When a parent step already defines it, one sentence about what this task changes is enough.
- Answer “Walk me through how this fixes the issue step by step” from **Proposed changes**. Show the numbered steps and their related notes, but omit file/function sub-bullets. Show **Refactor** as a labeled step when present.
- End with a relative link to `.working_items/{task}/implementation_plan.md`.
- Ask the user to reply with **APPROVED** to proceed. If revisions are requested, update the plan and mirrored `tasks.md` checklist, then present the review again.
- Do not implement without explicit **APPROVED**. Once approved, set `approved: true` and `status: implementation` in `tasks.md`.

### 4. Implementation

- Implement through a **Contract-first verify** loop.
- Spend effort on the asked outcome. Agent-proposed complexity reduction beyond it may use at most 10–20% of the effort and must be approved under **Refactor**.
- Perform private restructuring only when the approved plan has a **Refactor** section, and only within the named files or boundary. Without that section, do not move complexity, remove paths, or redesign a boundary.
- **Delegation is optional** when work is self-contained, parallelizable, mechanically large, or delegation materially protects the main agent's context. Keep tightly coupled architectural work with the main agent.
- If delegating, use this brief with `{task}` filled in:

```text
Implement the approved task. Read these files first, in order:
- .working_items/{task}/implementation_plan.md
- .working_items/{task}/tasks.md
- .working_items/{task}/agent_notes.md

Follow Design rules, Diff hygiene, and the agent_notes.md rules in the light-antigravity skill.

Stay within the approved plan. Do not add a public or module boundary, dependency, or concept the plan does not name. Private restructuring only as the plan's Refactor section names it, inside that section's files or boundary. If there is no Refactor section, do not refactor. Agent-proposed improvement beyond the asked outcome may use at most 10–20% of the effort.

Follow the plan's Verification. Do not invent behavioral requirements. If implementation exposes a concrete regression in an approved public contract, a focused new or extended regression case is allowed; record it under ## Discoveries and report it as a verification-plan delta. Stop for re-approval only if it changes approved behavior, architecture, dependencies, or scope.

As each checklist item completes, change `- [ ]` to `- [x]` in tasks.md. Update agent_notes.md in the relevant section when durable map knowledge appears; do not rewrite it in full.

Return changes, commands, discoveries, and Test budget (new: N | extended: M | reused only: yes/no).
```

- **Contract-first verify**:
  - Default: implement the approved change, then run **Existing** coverage. Wiring or plumbing does not require a new test.
  - When **New/extended** lists a case, use light red→green for that public contract: create or extend the named case, confirm it fails for the intended reason or asserts the new contract, then implement the smallest coherent change that passes within the approved boundary.
  - When **New/extended** is `none — reuse existing`, add no planned tests. A focused regression case remains allowed under the discovery rule.
- Check off each `tasks.md` item as it completes. A future chat resumes the same plan at the first unchecked item.
- Record material discoveries in `tasks.md`: plan adjustments, new invariants, verification deltas, or unexpected scope. Adapt autonomously to local reversible findings. Pause for revised plan approval before a public-behavior change, new or reshaped boundary, migration change, significant dependency, private restructuring, or substantial unplanned scope.
- When a parent project is attached, report material tradeoffs and pushed-out work in project `scope.md`; put deferred deepening or quality work in `architecture.md`. Prefer deferral over widening the approved task. Pause if that changes approved project outcomes, owning boundaries, or replaces a project step.
- Follow design rule 8 and **Diff hygiene**. Avoid placeholder code.

### 5. Verification

- Set `status: verification` in `tasks.md`.
- The main agent owns verification and review artifacts, even when implementation was delegated.
- Run all **Existing** and **New/extended** checks from the approved plan plus any focused regression case recorded under **Discoveries**.
- Confirm the actual test budget matches the plan plus recorded regression deltas. Extra unapproved tests are a soft warning: note them in the walkthrough and prefer removing or folding them into a revised plan next time.
- Execute the approved manual checks that are locally available.
- If the plan has a **Refactor** section, verify callers use the named interface and named obsolete paths are gone. Without a **Refactor** section, do not require path removal or boundary consolidation.
- **Diff-to-plan check (hard)**: compare the final diff to the recorded baseline. Confirm files and behavior match the approved task, unrelated changes remain intact, and no unplanned public/module boundary, dependency, or private restructuring appeared.
- **Unplanned validation (hard)**: remove guards, wrappers, re-validation, or exception types not named in **Scope limits**. If one is required, stop for re-approval.
- **Formatting-noise check (hard)**: compare `git diff` with `git diff -w --ignore-blank-lines` against the baseline. Revert hunks that disappear under `-w` and changes limited to quotes, imports, wrapping, or trailing commas.
- **Expected-diff check (advisory)**: when the product diff excluding tests is materially larger than estimated, report planned versus actual and explain the extra lines in the walkthrough. Size alone does not stop completion.
- **agent_notes hard check**: re-read and prune `agent_notes.md`, confirm it reflects durable task knowledge, and check its `tasks.md` item. If nothing durable was learned, check the item without adding meta-status notes. When attached to a parent, update project `agent_notes.md` with facts that outlive this task.
- On failure, increment `verification_attempts`, classify it as `environment`, `existing baseline`, `implementation defect`, `verification defect`, or `plan invalidated`, and record a concise `last_error`. Repair and rerun within approved scope.
- If the same material failure class remains after three repair attempts, stop and report logs. Stop sooner when resolution requires a changed approved behavior, architecture, dependency, or substantial scope.
- Do not proceed to review until automated verification passes and the hard checks are clear.
- When attached to a parent project, mark its tracker step complete and its step file `status: done` after the whole task verifies.

### 6. Review changes

- Create `.working_items/{task}/walkthrough.md`; do not overwrite a completed walkthrough for new work.
- Print the chat wrap-up in this order, using only this task's diff against the recorded baseline:
  1. **How this fixes the issue.** Answer the walkthrough question for what landed and name deferred work.
  2. **Changed-path tree (chat only).** Show every changed path with `+adds` / `-deletes` per file and directory subtotals, including generated files and lockfiles. Do not use GitHub or a full-PR diff.
  3. **Human verify.** Give numbered steps the user can run to confirm the landed behavior. Do not create or link verification scripts.
  4. Link the walkthrough file.
- Copy the same step-by-step answer into `walkthrough.md`. Keep automated commands, contracts, test budget, and extras in the walkthrough; keep the path tree only in chat.
- After the walkthrough is written and every checklist item is complete, set `status: complete` in `tasks.md`.
- There is no next-phase handoff. If the task remains incomplete when a chat ends, a later `/light-antigravity` invocation resumes the same plan. If a parent project has a later open step, prompt a new chat for that step after this task completes.

#### Template `.working_items/{task}/walkthrough.md`

```markdown
# Walkthrough: {title}

### How this fixes the issue
{same step-by-step answer as chat}

### Automated Verification
- Commands/suites run: {terse}
- Contracts covered: {terse}
- Test budget: new: {N} | extended: {M} | reused only: {yes/no}
- Regression deltas: {none | list}
- Extras beyond plan (soft warn): {none | extra tests}. Removed before completion: {none | unplanned validation}. Reverted formatting-only hunks: {none | list}. Expected diff (advisory): {planned vs actual, or `within estimate`}

### Manual Verification
1. {human step and expected result, or `none`}
```
