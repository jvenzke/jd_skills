# Skills for Cursor

Author: Joel DeVenzke

## General Skills

- `/grill-me`: Stress-test a plan or design with one question at a time until the agent and user share a clear understanding.
- `/caveman`: Switch to ultra-compressed communication to reduce token usage.

## Development Workflow (WIP/Not tested)

1. `/grill-me`: Resolve the design tree for a problem or project.
2. `/to-prd`: Turn the current conversation and codebase understanding into a PRD under `.working_items/`.
3. `/prd-to-issue-files`: Break an approved PRD into ordered, vertical-slice issue markdown files.

## Research Agent Workflow (WIP)

1. `/generate-research-project`: Start from a Jira ticket or linked README, optionally create a git branch, and build the project scaffold:
   - `README.md`
   - `RESEARCH_PLAN.md`
   - `results/`
   - `research_tasks/`
2. `/research-plan`: Interview the user and explore the codebase as needed to produce:
   - `RESEARCH_PLAN.md`
   - `RESEARCH_PLAN_PITCH_DECK.html`
3. Repeat the research loop until the plan converges:
   - `/to-research-tasks`: Convert the current plan and compressed workspace context into the smallest unblocked task set, usually one AFK-ready task and never more than three.
   - `/do-research`: Execute one approved task in a scoped task folder, write modular analysis code, generate Plotly PNGs, and log findings in `results_log_{idx}_{name}.md`.
   - `/review-research`: Review the latest task results with the user, decide whether the work has converged, compress completed work into `research_workspace/`, archive completed raw task materials, update the pitch deck, and update `RESEARCH_PLAN.md`.
   - Optional `/commit-research`: Stage only the minimal reviewable and reproducible research files after review checkpoints. Do not commit unless explicitly asked.
4. `/summarize-research`: Build the final production handoff in `/results`, including the executive summary, production-ready SQL/Python snippets, final assets, presentation webpage, and project README updates.
