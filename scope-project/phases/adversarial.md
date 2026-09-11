# Adversarial review (before user review)

Attack the written plan, not the author. Job is to find holes in `scope.md`,
`architecture.md`, and **all** `steps/*.md` against this skill’s bar. Not a
second research pass. Not a second plan.

`agent_notes.md` is evidence only. Do not critique it as a plan. Do not
rewrite it.

## When to run / skip

Run after an artifact write that would go to **User review**: first write,
re-scope, or `refresh` that changed planning files.

Skip when:

- `approved: true` and the user did not ask to re-scope (resume → tracker +
  handoff)
- `adversarial.md` has `status: complete` and `scope.md`, `architecture.md`,
  and every `steps/*.md` are **not newer** than `adversarial.md` (check
  mtimes). Then go to user review.

If those planning files are newer than `adversarial.md`, re-run.

## Loop

1. One attack pass (fresh subagent).
2. Main agent verifies survivors and patches planning files (not
   `agent_notes.md` unless a cited path/symbol is wrong).
3. Re-run attack **only** if the patch **changed the roadmap**: added or
   removed a tracker step, changed **In** / **Out** / **Later**, or changed a
   step’s **Ship destination**. Cap at **two** attack passes. Do not loop on
   wording.

`roadmap_changed: true` in `adversarial.md` only for those cases.

## Finding bar

A finding is real only with all four:

- **Trigger** — what in the plan or repo makes this fail later
- **Evidence** — contradiction across artifacts, or a cited path/symbol in
  this repo (targeted re-read; do not invent APIs)
- **Consequence** — wrong split, locked deepening, unsafe ship, missing
  edge, unverifiable slice, or in/out that will surprise implementers
- **Fix direction** — what to change in which file

Drop wording nits, template/layout-only notes, and “I would have scoped
smaller” without a consequence. Do not attack markdown structure.

## Attack surface (one pass, all files together)

Cross-file bugs are the point. Check:

- **In / Out / Later** — too wide, too narrow, or Later that must be In (or
  the reverse) given deps, rollback, or deepening
- **Step splits** — too small (isolated ticket that does not change what a
  sibling may deepen) or missing a seam (migration, rollback, ship dest,
  deepening sequence)
- **Deepening lock-in** — a step’s **Do not** / slice would prevent a later
  step from deepening the named module
- **Ship destination** vs **Ship strategy** — `prod` vs `feature-branch`,
  **Until**, exceptions
- **Verification** — not observable behavior/new logic; clones **In
  scope**; restates **Out of scope**; test names/commands/coverage;
  file/symbol checklists; `- none`
- **Edge cases** — non-obvious cases missing, or cover now|later|out wrong
- **Quality notes** — missing trigger, leak, or fix direction
- **Recommended architecture / Deep modules** vs what steps **Realize**
- **Tracker** vs step files (titles, order, ship, links)
- **Invented** modules/APIs not grounded in this repo / `agent_notes.md`
- **Quality backlog** promoted into Deep modules / steps without being
  tracker work (or the reverse: in-work deepening left only on the backlog)

Do not paste the skill’s module manifesto into artifacts.

## Subagent

Launch **one** fresh read-only subagent. Instruct it to read this file first,
then the planning artifacts and `agent_notes.md`, then **targeted** re-read
of cited paths only.

Copy this brief; fill `{project}` and the artifact paths.

```
Attack the scope-project plan. Read in order:
1. {skill-dir}/phases/adversarial.md
2. .working_items/{project}/scope.md
3. .working_items/{project}/architecture.md
4. every file in .working_items/{project}/steps/
5. .working_items/{project}/agent_notes.md (evidence only)

Then re-read only cited repo paths/symbols. Do not re-research the whole
codebase. Do not invent APIs or modules.

Job: find holes (trigger, evidence, consequence, fix direction). Try to
kill your own candidates (guards, existing splits, alignment Decisions that
already cover it). Cross-file contradictions count.

Return:
- survivors (high confidence only): id, files, trigger, evidence (path or
  artifact quote), consequence, fix direction, whether the fix would change
  an alignment Decision / In-Out-Later / ship destination
- killed candidates and why
- Do not write files. Do not approve. Do not edit product code. Do not
  rewrite agent_notes.md. Do not natter about heading layout.
```

`{skill-dir}` is the directory that contains `scope-project/SKILL.md`.

## Main agent

1. Independently re-read cited evidence. Drop anything unverified.
2. **Alignment fork:** if a survivor would change a recorded Decision (D1…),
   **In/Out/Later**, or a project-wide ship rule, **do not patch it**. Pause,
   return to **Research then align** (numbered questions, recommended
   options). Do not silently override alignment.
3. Otherwise patch `scope.md` / `architecture.md` / step files. Absorb
   leftovers into the right section (Tradeoffs, Edge cases, Quality backlog,
   step Risks) rather than leaving the critique as source of truth.
4. Write `adversarial.md` (update in place on pass 2).
5. User review of the **repaired** plan. Chat: one short bullet
   `Adversarial: {N} applied, {M} leftovers` (leftovers = alignment pause or
   absorbed residual risk). No extra **APPROVED** gate.

## Template `.working_items/{project}/adversarial.md`

```markdown
---
project: {project}
pass: 1
status: complete
roadmap_changed: false
---

# Adversarial — {project}

Not a second plan. Source of truth is `scope.md`, `architecture.md`, steps.

## Survivors applied

- {id}: {fix} → {file}

## Killed

- {id}: {why}

## Leftovers

- none | {id}: needs alignment | absorbed into {section}

## Pass 2

- skipped | ran because roadmap changed
```
