# Skills for Cursor and Claude Code

Author: Joel DeVenzke

## Install

```bash
git clone https://github.com/jvenzke/jd_skills.git
cd jd_skills
./install.sh
```

Copies active skills (everything except [`old/`](old/)) into `~/.cursor/skills/`. Re-run the same command after `git pull` to update.

```bash
./install.sh grill-me review-pr              # named skills only
./install.sh --project                       # current directory (Cursor)
./install.sh --project ~/code/my-app         # a project root (Cursor)
./install.sh --claude                        # Claude Code: ~/.claude/skills/
./install.sh --claude --project ~/code/my-app
```

`--project` installs into `<dir>/.cursor/skills/` (or `<dir>/.claude/skills/` with `--claude`) so only that repo sees them. Named skills can include folders under `old/`. `--claude` does not also write Cursor dests.

## Overview

A collection of skills I use day to day as a data scientist, covering the work
between a rough idea and a reviewed pull request: development, research spikes,
PR review, and design pressure-testing.

Every skill is human-in-the-loop by design. Each one runs a numbered workflow
and asks only the questions the codebase cannot answer. Irreversible work
(implementation, GitHub writes, commits, file deletions, skill-file edits)
waits for the skill's gate: usually an explicit **APPROVED**. `/research-first`,
`/grill-me`, and `/clean-skill` use numbered option replies instead.
`/review-pr` submission is naming the GitHub review type after the exact
payload is shown — not a second **APPROVED**.

Progress lives on disk, not in chat history. Skills write plans, task
checklists, and walkthroughs to `.working_items/` in the target repo, so a
fresh chat resumes by reading those files instead of re-deriving context.

## Active skills

| Skill | Use when |
| --- | --- |
| [`/research-first`](research-first/SKILL.md) | Same-chat prefix: web landscape + alignment before other work |
| [`/scope-project`](scope-project/SKILL.md) | Multi-week project roadmap: migrations, dependencies, cross-step refactoring (no code) |
| [`/d-antigravity`](d-antigravity/SKILL.md) | Real development: architecture, maintainable diffs, vertical slices |
| [`/r-antigravity`](r-antigravity/SKILL.md) | Research spikes, throwaway tooling, analysis-backed prototypes |
| [`/review-pr`](review-pr/SKILL.md) | GitHub pull request quality review |
| [`/grill-me`](grill-me/SKILL.md) | Stress-test a plan or design with one pass of questions |
| [`/meta-review`](meta-review/SKILL.md) | After a session: check whether skills were followed and should change |
| [`/clean-skill`](clean-skill/SKILL.md) | After editing a skill: flag text that is unclear for an implementing agent |

Unused skills live in [`old/`](old/). Do not invoke them; they are archive only.

## How these skills are built

[`/meta-review`](meta-review/SKILL.md) is the quality bar. Run it after a session that used a skill. [`/clean-skill`](clean-skill/SKILL.md) is for editing a skill file itself: flag implementing-agent problems, wait for option replies, then change files only after explicit approval. Log recurring misses in `meta-review/problems.md`.

**One invokable skill per workflow.** Tightly coupled steps stay inside that skill. Do not split a pipeline across slash commands the user must chain in a later chat. [`/research-first`](research-first/SKILL.md) is an optional **same-chat prefix**: landscape + alignment, then continue the user's task (and any other skill attached in that message) from `.working_items/{task}/field_research.md`. Do not require a second invocation in a new chat. [`/scope-project`](scope-project/SKILL.md) is a complete planning skill; it only names `/d-antigravity` at handoff. [`/review-pr`](review-pr/SKILL.md) and [`/d-antigravity`](d-antigravity/SKILL.md) are the models for full workflows: numbered tasks, durable artifacts, resume from disk.

**Progressive disclosure.** `SKILL.md` holds the contract: when to run, artifact layout, ordered rules, task list, gates, and resume. Load detail only for the active task (`review-pr/phases/…`, templates, scripts). Keep references one level deep. Prefer `SKILL.md` well under 500 lines.

**`description` is the trigger.** Third person. State what the skill does and when to use it. Set `disable-model-invocation: true` unless the skill should auto-attach from ambient context. These skills are explicit (`/name`) only.

**Artifact-first, not chat-memory.** Persist under `.working_items/` in the target repo. A later chat resumes by reading those files. Typical pieces:

- `tasks.md` — checklist plus frontmatter (`approved`, current phase, SHAs)
- `implementation_plan.md` / `phase_plan.md` — intent the user approved
- `agent_notes.md` — agent-only code map (paths, symbols, gotchas); not a second plan
- `walkthrough.md` — what shipped and how it was verified
- `field_research.md` — web landscape + alignment decisions (`/research-first`)
- `scope.md` + `architecture.md` + `steps/` — project tracker, target design, and start-work slices (`/scope-project`)

**Gates.** Ask only blocking questions. Implementation, GitHub writes, skill-file edits, and similar irreversible work wait for an explicit **APPROVED** (or the skill's named equivalent — `/research-first` logs option-id replies in `field_research.md`; `/review-pr` submits when the user names `APPROVE` / `REQUEST_CHANGES` / `COMMENT`). The main agent owns verification, artifacts, and presentation. Subagents are optional, read-constrained, and do not approve or post.

**Shape.** Short intent, numbered workflow, small rule set, named artifacts, explicit out-of-scope. [`/d-antigravity`](d-antigravity/SKILL.md) is the multi-step reference. [`/grill-me`](grill-me/SKILL.md) is the single-purpose reference. Be terse. Gate file moves, deletions, commits, and pushes behind user approval.

Do not treat “one README step = one skill” as a rule. That produced the old split review and research pipelines now in `old/`.

## `/research-first` (Last updated: 2026-09-03)

Optional same-chat prefix when field context matters. Thin local orientation → sourced web landscape (last ~2–3 years) → numbered alignment questions with recommended options → log answers → continue the original task. Follow `/d-antigravity` or `/r-antigravity` only if that skill is also in the chat.

Artifact: `.working_items/{task}/field_research.md` (Orientation, Landscape, Questions, Decisions). Resume from disk; refresh only if asked.

## `/scope-project` (Last updated: 2026-09-11)

Standalone planning/tracking for large changes that span chats, PRs, or weeks. Use when you need a durable map of migrations, dependencies, known follow-ups, and refactoring/deepening that only works if steps are sequenced. KPI is easier future change, not spec-kit-style isolated tickets. Never implements. Artifacts stay under `.working_items/{project}/` (not Spec Kit / Kiro / MCP boards). `scope.md` owns in/out/later, deps, and the living tracker. `architecture.md` owns the short human map, quality notes (finding bar), non-obvious edge cases, recommended architecture, and in-work deepening vs later/out backlog. Legacy projects missing `architecture.md` get it created from leftover scope headings, not a full rewrite. Implement chats patch the tracker when they defer work.

Cycle: resume notes → codebase research (web allowed) + `agent_notes.md` → alignment for a shared understanding → `scope.md` + `architecture.md` + `steps/{NN}-*.md` → **APPROVED** → handoff prompt for a **new chat** with `/d-antigravity` and the next step file only (that file links the rest).

Artifacts: `.working_items/{project}/scope.md`, `architecture.md`, `agent_notes.md`, `steps/`.

## `/d-antigravity` (Last updated: 2026-09-11)

Phased development when architecture and long-lived quality matter. Prefer over `/r-antigravity` for product code. Works with no `/scope-project` output.

Cycle: research and blocking clarify → optional phase plan → implementation plan + `tasks.md` → **APPROVED** → implement (delegation optional) → main-agent verification → walkthrough. One phase per chat when a phase plan exists; never overwrite a completed `phase-{N}/`.

Optional project attach: only if the user links `scope.md` / `architecture.md` / a step file (or `tasks.md` already has `project:`). Treat the step as the request (follow its links to architecture and sibling steps); still write phase and implementation plans. Report tradeoffs to `scope.md` and dropped/deferred deepening to `architecture.md`; update the project tracker when the step finishes.

Artifacts: `.working_items/{task}/phase_plan.md` (optional), `agent_notes.md`, and `.working_items/{task}/phase-{N}/{implementation_plan,tasks,walkthrough}.md`.

Clarify is blocking: independent questions in one numbered pass with recommended options; do not plan while user decisions remain open. Deep-module rules apply: small interfaces, complexity behind the boundary, contract-first tests (no red/green ritual).

## `/r-antigravity` (Last updated: 2026-08-27)

Spike-light cycle for research tools and throwaway prototypes. Same clarify → plan → **APPROVED** → implement → smoke verify → walkthrough shape, without phases or `agent_notes`.

Artifacts: `.working_items/{task}/{implementation_plan,tasks,walkthrough}.md`. Runnable code stays in repo conventions (`src/`, notebooks, `scratch/{task}/`), not under `.working_items/`.

Optimize for a simple researcher entrypoint and hidden plumbing. Prefer `/d-antigravity` once the work should live as maintained software.

## `/review-pr` (Last updated: 2026-09-11)

Single-chat GitHub PR review. Resume from artifacts in the reviewed repo at `.working_items/pr-review/<owner>-<repo>-<number>/`. If this user already submitted approve / request changes / comment, later runs are **incremental**: only the update since that review, plus prior-comment status.

Tasks: intake (fewest business claims that cover the PR + `low`/`medium`/`high` review risk) → risk-adaptive SECURITY, test-coverage, and LOGIC_QUALITY review → adversarial verification → claim-and-decision walkthrough → submit. Claims come from PR text or the user—not inferred from the diff, and not from Jira. Claims are printed in chat. Always write `SECURITY.md`, `TESTS.md`, and `QUALITY.md` (findings or a written skip) before the walk continues; low risk uses integrated logic/quality plus CI/tests unless a surface triggers a specialist. LOGIC_QUALITY checks claim-aligned correctness and deep-module maintainability (easier future change, not a small diff). Tests report new-code coverage and whether GitHub Actions runs this project’s tests.

Coverage inventory is **changed sections** (`@@` regions, with added and deleted line counts), not additions-only. `human_presented` means exact product code was shown; it is not “human-reviewed.” Tests are summarized in prose, never pasted. Submit keeps presentation metrics and human-oversight bullets in chat/`SUBMISSION.md`; the GitHub body is product language only (no claim ids or local artifact names). Walkthrough units are claims, material boundaries, ambiguities, and surviving findings; paste product code when judgment needs it. High confidence requires cheap falsification when tools can do it. Gates: claims, walkthrough Next actions, then naming the review type after the exact payload. A new `head_sha` is summarized then processed without a pause. Submit posts one GitHub review with event `APPROVE`, `REQUEST_CHANGES`, or `COMMENT`.

## `/grill-me`, `/meta-review`, and `/clean-skill`

`/grill-me`: one pass of questions, recommended answer on each, then pause for a reply. Repeat a pass only if an answer blocked or changed later questions. Explore the codebase instead of asking what it can answer. (from [Matt Pocock's Skills for Real Engineers](https://github.com/mattpocock/skills/tree/main)). `/research-first` is the landscape/alignment prefix; `/grill-me` is design interrogation.

`/meta-review`: compare this chat to the skill text. Propose compact edits. Do not change skills, the problem log, or git without an explicit decision on each issue.

`/clean-skill` (Last updated: 2026-09-11): review a skill the user names, in isolation, for text that is unneeded or unclear for an **implementing agent**. Output a numbered problem list; each problem has a recommended solution plus two lettered alternatives so replies look like `1a {notes} …`. Stop for those replies. After answers, summarize intended edits in chat and wait for explicit approval before changing any skill file.

## Archive

[`old/`](old/) holds workflows that are no longer used (linear research, light research, ticket-to-PRD development, light-dev, and related helpers). Keep them for history. Do not list them as active steps, and do not teach new skills to call them. (includes some skills from [Matt Pocock's Skills for Real Engineers](https://github.com/mattpocock/skills/tree/main))
