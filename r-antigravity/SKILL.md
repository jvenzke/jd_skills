---
name: r-antigravity
description: >-
  Spike-light antigravity workflow for research tasks: throwaway experiments,
  research tooling, and quick analysis-backed prototypes. Prefer simple
  researcher-facing interfaces that hide plumbing. Use when speed and terse
  plans matter more than production-grade diffs; prefer d-antigravity when
  architecture and long-lived code quality matter.
disable-model-invocation: true
---

# Antigravity workflow (research / spikes)

Simulates the antigravity cycle — clarify, plan, approval, implement, smoke
verify, review — for research tools and throwaway prototypes. Prefer deep
modules: a small entrypoint that reduces researcher load, with plumbing hidden
in the implementation. Do not let design polish hinder exploration. No phases,
no `agent_notes`.

## Artifact layout

All planning artifacts live under `.working_items/{task}/`:

```
.working_items/{task}/
  implementation_plan.md
  tasks.md
  walkthrough.md          # written after verification
  verify.sql | verify.py  # optional; human post-pipeline checks
```

`{task}` is a lowercase kebab-case slug. **Never** put runnable product code
under `.working_items/` — that folder is plans/tasks/walkthrough only, plus
optional `verify.sql` / `verify.py` (named exception; read-only human checks).

## Rules (priority order)

Apply in this order when they conflict:

1. **Deep modules for researchers**: keep the entrypoint simple; hide data plumbing, retries, formatting, and environment details behind it.
2. **Reduce research load**: optimize for fewer steps, fewer knobs, and less context the researcher must hold — without blocking the analysis itself.
3. **Ship useful prototypes fast**: prefer working research tools over speculative architecture or premature generalization.
4. Prefer **orthogonal helpers** that can be reused across analyses; reshape boundaries when that lowers researcher friction.
5. Keep changes within the approved plan. Larger code changes are allowed when they simplify the researcher interface; no unrelated cleanup.

## Deep-module design standard (research tools)

Treat a module as any script, notebook helper, class, object, package, or CLI entrypoint with a boundary.

- Expose the smallest practical interface for the research task (e.g. one function/CLI that takes intent + inputs and returns usable results).
- Keep connection setup, path wrangling, retries, schema quirks, joins, formatting, and caching behind the boundary.
- Favor a few deep helpers over many shallow wrappers that force the researcher to orchestrate steps.
- Co-locate related plumbing when that reduces what the researcher must know or copy between analyses.
- Avoid interfaces that leak warehouse/config/file internals through excessive parameters or required ceremony.
- Judge an abstraction by how much friction it removes from the research loop, not by elegance.
- Prefer defaults that make the common research path work; expose knobs only when the analysis needs them.
- Larger refactors are justified when they shorten question → result, remove duplicated setup, or make the next analysis cheaper. Do not use deep-module design to justify productization or speculative frameworks.

## Code placement

- Prefer the repo’s existing research/layout conventions (`src/`, notebooks, analysis folders).
- If none exist, create a small task-local folder (e.g. `scratch/{task}/` or `src/{task}/`) and name it in the plan.
- Analysis, queries, and plots are allowed when needed to prove the spike; do not require canvas/`research_log` ceremony unless the plan names those artifacts.

## Tasks
**use the TODO tool to track tasks**

### 1. Review request, research & clarify
- Standardize `{task}` and create `.working_items/{task}/` if missing.
- **Resume**: If `tasks.md` exists with `approved: true` and unchecked items, read plan + tasks, skip clarify/planning, resume at the first unchecked item, and post a short “where we left off” summary. If a plan exists but is not approved, resume at clarify or user review as appropriate.
- **Research**: Find relevant files, flows, risks, and the intended researcher entrypoint. Identify ceremony forced on the researcher and plumbing that should move behind a simple interface.
- **Establish baseline**: Record the current branch/base commit and any pre-existing dirty files before implementation. Preserve unrelated user changes. The step-6 path tree diffs this pass against that baseline (not GitHub).
- **Align**: Shared understanding of forks that would change outcomes (success criteria, inputs/outputs, irreversible side effects, substantial scope)—not a minimal interrogatory. If the codebase can answer, explore instead. For reversible implementation choices, pick the locally consistent option and note it in the plan.
  - Ask in chat. **Do not use the Q&A/AskQuestion tool.**
  - All **independent** questions in **one** message. Number (`1.`, `2.`, …). Options as indented `- a)`, `- b)`, … alphabetically; mark **(recommended)**. Users reply with ids (e.g. `1b 2a`).
  - After answers, ask only follow-ups an answer blocked or changed (or new facts that still need user judgment). Pause before the next pass or before planning.
- **DO NOT** write the implementation plan while an alignment question that would change outcomes remains open.

### 2. Develop an implementation plan
Write `.working_items/{task}/implementation_plan.md` and `.working_items/{task}/tasks.md`.

#### Rules for Brevity & Efficiency:
1. **No Fluff**: Keep the plan extremely crisp and bulleted.

#### Template `.working_items/{task}/implementation_plan.md`
```markdown
# Implementation Plan: {title}

{summary - 1-2 sentences}

## User Review Required

### RISKS

1. {risk notes - terse list}

### IMPORTANT

1. {important notes - terse list}

### Decisions from clarify

- D1: {resolved decision - brief; include chosen option}

## Proposed changes

{change description - terse bulleted list of impacted files and logic changes}

## Deep-module design (research load)

- **Researcher interface**: {simple entrypoint / call surface}
- **Hidden plumbing**: {setup, joins, retries, formatting, env details moved behind it}
- **Load reduction**: {steps, knobs, or context removed from the researcher's path}
- **Speed tradeoff**: {what stays rough / deferred so exploration is not hindered}

## Verification plan

### Automated Verification
{researcher-path smoke and any automated checks - terse bullets; prefer one happy-path check}

### Manual Verification
- **How to run**: {exact entrypoint — command / notebook cell / function call}
- **Inputs**: {required inputs}
- **Expected output**: {shape / what “success” looks like}
{any other numbered human checks}

**Human verify file** (optional; in addition to smoke/unit checks)
- {`none` | `verify.sql` | `verify.py` | both} — assert: {observable post-run result}
- Write the file only when the new behavior is fully visible only after a pipeline, job, warehouse, or similar remote run that smoke/unit checks do not exercise. Often `none` when How to run *is* the human check.
- Plan names whether a file is expected. Write the actual script during Verification/Review from **landed** behavior.
```

#### Template `.working_items/{task}/tasks.md`
```markdown
---
task: {task}
phase: planning
approved: false
verification_attempts: 0
last_error: null
---

# Checklist for: {task}

- [ ] Step 1: {granular checklist step 1}
- [ ] Step 2: {granular checklist step 2}
- [ ] Smoke researcher path (How to run)

## Discoveries

- none
```

### 3. User review
- Provide a highly concise summary of proposed changes **(maximum 3-4 bullets)** in chat, plus a relative link to `.working_items/{task}/implementation_plan.md`.
- Ask the user to reply with **APPROVED** to proceed. Repeat if revisions are requested.
- **DO NOT** implement without explicit **APPROVED**. Once approved, set `approved: true` and `phase: implementation` in `tasks.md` frontmatter.

### 4. Implementation
- Implement the approved plan. **Delegation is optional**: use the `Task` tool when work is mechanically large, parallelizable, or would blow the main context; otherwise implement in the main agent.
- If delegating, the **subagent prompt MUST include**:
  - Paths to `.working_items/{task}/implementation_plan.md` and `.working_items/{task}/tasks.md`
  - The **Rules (priority order)** block from this skill
  - The **Deep-module design standard (research tools)** block from this skill
  - Instruct: stay within the approved plan; optimize for a simple researcher interface; do not productize or over-abstract beyond what reduces research load
  - Instruct: as each checklist step completes, change `- [ ]` to `- [x]` in `tasks.md`
- As each step completes (main agent or subagent), change `- [ ]` to `- [x]` in `tasks.md`.
- **Discoveries**: Record material discoveries under `## Discoveries` in `tasks.md`. Adapt autonomously to local/reversible discoveries. Pause and revise the plan for re-**APPROVED** only if success criteria, inputs/outputs, or irreversible side effects change.
- Maintain exact indentation/formatting; avoid placeholder code.

### 5. Verification
- Update `phase: verification` in `tasks.md`.
- Run planned Automated Verification (prefer researcher-path smoke / one happy-path check). Automated tests only when they lock a helper you will call again soon; otherwise Manual Verification is enough.
- Confirm **How to run** works: researcher reaches results through the intended entrypoint without coordinating hidden plumbing.
- **Human verify file**: If Manual Verification named `verify.sql` and/or `verify.py` (or landed behavior now requires one), write it under `.working_items/{task}/` from landed behavior. One file matching how a human inspects the result: SQL when the proof is warehouse rows/state; Python when the proof is API/files/logs/local artifacts. Both only if those proofs are independent. Names must be exactly `verify.sql` and/or `verify.py`. Script is read-only checks with comments stating expected rows/shape/invariants; exit non-zero or print a clear fail. Do not mutate data or trigger the pipeline from the script. Do **not** run warehouse/pipeline verify scripts (do not substitute Snowflake MCP). If not applicable, omit the file.
- If checks fail: increment `verification_attempts`, record the error in `last_error`, apply fixes, and re-run.
- If unresolved after **3** attempts, halt, report logs, and ask for user guidance.
- **DO NOT** proceed to review until planned Automated Verification checks pass (or were planned as none and Manual Verification / How to run succeeded).

### 6. Review changes
- Create `.working_items/{task}/walkthrough.md`.
- Print the chat wrap-up in this order (do not use GitHub; only this implementation pass vs the recorded baseline, or the working tree if no baseline was stored):
  1. **Change story.** 1–3 `###` headings named in product language (one independently judgeable behavior each), plus `### Residual` only when something is still unproven. Each heading body is 1–3 sentences: actor, situation, observable result, and any important must-not. Never include file paths, type/symbol names, SQL/table names, artifact names, or coverage jargon. Do not use HTML `<details>`.
  2. **Changed-path tree (chat only).** Nested tree of every path this pass changed, with `+adds` / `-deletes` per file and directory subtotals. Include generated files and lockfiles. Do not use GitHub.
  3. **Human verify.** Numbered steps. When How to run *is* the human check, make it step 1 (entrypoint, inputs, expected output). Include a relative link to `verify.sql` and/or `verify.py` when those files exist. Do not trigger the pipeline from the agent.
  4. Relative link to the walkthrough file.
- Copy the same change-story headings into `walkthrough.md`. Automated smoke/results live in the walkthrough only. Path tree stays in chat.

#### Walkthrough Template `.working_items/{task}/walkthrough.md`
```markdown
# Walkthrough: {title}

### {behavior in product language}
{1–3 sentences: actor, situation, observable result, must-not. No paths, types, or SQL/table names.}

### Residual
{only if something is still unproven; otherwise omit this heading}

## User Review Required

### RISKS

1. {risk notes - terse list}

### IMPORTANT

1. {important notes - terse list}

### Automated Verification
{results of planned smoke / automated checks}

### Manual Verification
1. {How to run — entrypoint, inputs, expected output}
2. {run verify.sql / verify.py with relative link when present; or omit this step}
```
