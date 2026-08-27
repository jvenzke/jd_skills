# Skills for Cursor

Author: Joel DeVenzke

Some skills are inspired by Matt Pocock's [Skills for Real Engineers](https://github.com/mattpocock/skills/tree/main).

## References

- [Interesting talk on AI development and the importance of good coding practices](https://youtu.be/v4F1gFy-hqg?si=1opnC2coaZ8HVh7v)
- [Longer walkthrough](https://youtu.be/-QFHIoCo-Ko?si=d8P-EoPUrC0qJa_L)

## Authoring Principles

The [`/meta-review`](meta-review/SKILL.md) skill is the source of truth for what "good" looks like; it is what evaluates new and existing skills against the criteria below. Run it after any workflow or skill change so issues get logged in `meta-review/problems.md` and the skills evolve.

### Writing a Skill

- The frontmatter `description` is the trigger contract. Make it specific enough that the agent can decide whether to read the skill from the description alone, including cue phrases the user is likely to say.
- Keep each `SKILL.md` under 40 actionable directives. Count numbered steps and bullets; ignore frontmatter, headings, examples, and reference links. If you cannot fit the work in 40 directives after compression, split the skill.
- One skill, one job. Split when a skill has independent triggers or workflows. Merge when two skills are always invoked together, share decision logic, and have no meaningful independent use.
- Stay orthogonal. Communicate with upstream and downstream skills through stable artifacts (named files, sections, manifests), not implicit chat state. A skill should be resumable in a fresh chat by reading those artifacts.
- When a skill prepares work for another skill, write the next-step context to a durable Markdown or structured file and name that file in the skill. Include what changed, what remains undecided, and which skill or workflow step should run next.
- Don't repeat yourself. If two skills share the same interview, decision tree, or output format, reference the canonical skill instead of duplicating it.
- Be terse. Every bullet should carry weight; cut narration, restatement, and obvious commentary. Compress before adding.
- Gate irreversible work behind explicit user approval (file moves, deletions, commits, pushes, schema changes, network calls).
- Use a consistent shape: short intent statement, numbered workflow, small set of rules, and an explicit out-of-scope or exit section when useful. [`d-antigravity`](d-antigravity/SKILL.md) is the reference for multi-step skills; [`grill-me`](grill-me/SKILL.md) is the reference for single-purpose skills.
- Set `disable-model-invocation: true` for skills that should only be invoked explicitly by the user (see [`meta-review`](meta-review/SKILL.md)).

### Developing a Workflow

- Each step in a workflow should map to one skill with one clear output artifact. Skills must not spill into the next step's responsibility.
- Define the artifact contract between steps explicitly (file names, folder layout, section headings, manifests). Downstream skills depend on the artifact, not on chat memory.
- Use the README workflow section to explain the next step for each phase, including the handoff file the next chat should read before continuing.
- Persist workflow state in a known location so any step can be resumed cold (e.g., `.working_items/`, `research_workspace/`, the research project folder).
- Include a loop step and a convergence/exit criterion when the workflow is iterative (plan → execute → review → compress).
- List the workflow in this README with numbered steps, a `Last updated` date, and an explicit status tag (e.g., `Currently untested`) so consumers know how much to trust it.
- After running a new workflow end-to-end, invoke [`/meta-review`](meta-review/SKILL.md) to capture missed steps, bloat, duplication across skills, and split/merge candidates before the next iteration.

## General Skills

- [`/grill-me`](grill-me/SKILL.md): Stress-test a plan or design with one question at a time until the agent and user share a clear understanding.
- [`/meta-review`](meta-review/SKILL.md): Review how skills performed in the current chat, propose compact improvements, and log approved recurring problems.

- [`/toggle-html`](toggle-html/SKILL.md): Toggle the generation of HTML review surfaces (RESEARCH_REVIEW.html and RESEARCH_PLAN_PITCH_DECK.html) on or off.

## Antigravity Workflows (Last updated: 2026-08-27)

Single-skill research → plan → **APPROVED** → implement (subagent) → verify → walkthrough cycles. Artifacts live under `.working_items/`. Pick by how much code quality and change size matter:

| Skill | Use when | Diff from the others |
| --- | --- | --- |
| [`/r-antigravity`](r-antigravity/SKILL.md) | Research / exploratory work where speed and terse plans matter more than perfect diffs | One plan + one approval; no phase splitting or reuse-first rules |
| [`/d-antigravity`](d-antigravity/SKILL.md) | Real development where bloat and large diffs are a problem | Prefer this over `r-antigravity` when change size and code quality matter: optional phase plan, vertical slices (≤5 steps; may touch >3 files when deepening one boundary), deep-module / reuse rules, per-phase approval + fresh `phase-{N}/` artifacts, new chat for phase 2+ |

**Shared cycle (r / d):** research → implementation plan + tasks → user **APPROVED** → subagent implements (red-green-refactor) → automated verification (halt after 3 failures) → walkthrough.

**`r-antigravity` artifacts:** `.working_items/implementation_plan_{task}.md`, `tasks_{task}.md`, `walkthrough_{task}.md`.

**`d-antigravity` artifacts:** `.working_items/{task}/phase_plan.md` (optional) and per-phase `.working_items/{task}/phase-{N}/{implementation_plan,tasks,walkthrough}.md`. Each chat implements one phase only and must not overwrite prior phase folders; resume by linking or naming the phase plan.

## Light Research Workflow (Last updated: 2026-05-06)

Use this workflow to take an **idea end-to-end** to a **minimal prototype** (proof of approach) with a **fast** plan → do → plan loop—not broad exploratory research. Planning starts with **light alignment vs full grill-me**; execution adds **verification canvases and reproducible SQL** when the step is data-backed.

1. [`/plan-light-research`](plan-light-research/SKILL.md): Plan one **small, time-bounded** next step; update the "Status/Next Steps" section of the main output document.
2. [`/do-light-research`](do-light-research/SKILL.md): Execute the step, add artifacts and (when applicable) a **canvas** with plots and SQL for human verification, update the main document, and prompt for the next action.
3. [`/summarize-light-research`](summarize-light-research/SKILL.md): Compile findings into a handoff document, including pointers to verification artifacts.

## Linear Research Workflow (Last updated: 2026-05-21)

**Artifact chain:** `r-setup` creates the project **`README.md`** (stub), **`input_plan.md`**, **`research_plan.md`**, **`research_log.md`**, **`next_step.md`**, **`Canvases/`**, and **`src/`**. Canvas dashboards are saved under **`Canvases/<name>.canvas.tsx`** for git/handoff **and** mirrored to Cursor’s IDE **`canvases/`** path so they open beside chat (see canvas skill). **`r-plan`**, **`r-do`**, and **`r-extend`** update those files across iterations. **`r-summarize`** closes out by **writing the full results into the project `README.md`** (new sections: outcomes, findings, artifacts & verification, implementation handoff, open questions).

1. [`/r-setup`](r-setup/SKILL.md): Pull a Jira ticket (optional), set up base folders, and ask the user to update **`input_plan.md`**, then continue with **`r-plan`**.
2. [`/r-plan`](r-plan/SKILL.md): Review **`input_plan.md`**, define the **next** research step only, maintain **`research_plan.md`**, **`research_log.md`**, and **`next_step.md`** (handoff to **`r-do`** or **`r-summarize`** when done).
3. [`/r-do`](r-do/SKILL.md): Execute atomic tasks from **`next_step.md`**; add plots, reproducible Python/SQL, and verification canvases (**`Canvases/<name>.canvas.tsx`** in the research folder **and** the matching file under Cursor’s IDE **`canvases/`** path per the canvas skill); append **`research_log.md`**; checkpoint after each task (handoff back to **`r-plan`** or forward to **`r-summarize`**).
4. [`/r-extend`](r-extend/SKILL.md): Refine and extend the research plan in `input_plan.md` by grilling the user on proposed next steps, aligning on details, and updating `input_plan.md`. Use this after completing a research step in `r-do` and before starting the next step in `r-plan` when you need to align on new steps or modify the existing research plan.
5. [`/r-summarize`](r-summarize/SKILL.md): Read all planning and execution artifacts; **extend the project `README.md`** with summarized findings and verification pointers.

## PR Review Workflow (Last updated: 2026-08-27)

Default: one chat, artifacts under `.working_items/pr-review/<owner>-<repo>-<pr-number>/` in the target repo so a later chat can resume. Do not start a new chat between steps unless the user stops.

1. [`/review-pr`](review-pr/SKILL.md): Sole entry point. Runs intake and business-claim alignment, required SECURITY and test-coverage specialists, adversarial verification, claim-driven code walkthrough, staging, and approved GitHub submission.

The workflow mirrors `/d-antigravity` structurally: artifact-first resume, numbered tasks, bounded phases loaded on demand, optional read-only subagents, main-agent verification, explicit gates, and a final walkthrough. Approved comments stay local until submit. Claims come from ticket/PR text or the user—not inferred from the diff. `human_presented` requires a fenced code block in that turn. Coverage totals are shown every review turn and again at submit.

## Development Workflow (Last updated: 2026-05-05, Untested)

1. [`/dev-align`](dev-align/SKILL.md): Read the incoming ticket or doc, explore the codebase, grill the user to align on scope, and create a git branch.
2. [`/to-prd`](to-prd/SKILL.md): Turn the aligned plan into a PRD with a vertical-slice task breakdown (AFK/HITL) under `.working_items/`.
3. [`/prd-to-issue-files`](prd-to-issue-files/SKILL.md): Extract each task from the PRD into its own implementation plan document.
4. [`/dev-tdd`](dev-tdd/SKILL.md): Implement a task using a strict red-green-refactor loop, summarizing changes and committing after approval.
5. [`/dev-review`](dev-review/SKILL.md): Perform a compressed review of the work, summarize coverage, and prepare/open a Pull Request.

## Light Development Workflow (Last updated: 2026-05-05, Untested)

Use this workflow for hotfixes and small implementation tasks that are well-scoped and do not require large rewrites or multiple parallel agents.

1. [`/plan-light-dev`](plan-light-dev/SKILL.md): Read the ticket or request, explore the codebase, align on scope, and create a single `LIGHT_DEV_PLAN.md` tracking document.
2. [`/do-light-dev`](do-light-dev/SKILL.md): Execute the tasks in `LIGHT_DEV_PLAN.md` flexibly, writing tests whenever possible to prevent future regressions.
3. [`/review-light-dev`](review-light-dev/SKILL.md): Review the completed work against the plan, summarize coverage, and prepare/open a Pull Request.