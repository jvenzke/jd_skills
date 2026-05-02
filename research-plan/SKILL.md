---
name: research-plan
description: Interview the user to turn a vague research idea into a rigorous, falsifiable plan. Categorizes unknowns into feasibility, experimental, and out-of-scope.
disable-model-invocation: true
---

Your goal is to build a `RESEARCH_PLAN.md` that can be handed off to a junior data scientist, plus a static HTML pitch deck for presenting the plan at a data science group meeting.

> **Wiki integration:** If `llm_wiki/` exists in the repo, follow the `llm_wiki` skill's "Research workflow integration" section before drafting interview questions — load relevant wiki pages so you don't ask questions the wiki already answers, and cite them from `RESEARCH_PLAN.md`.

### Rules:
- **Categorization:** You must separate unknowns into:
    1. **Feasibility:** Data access, SQL table sizes, cost, and scale.
    2. **Experimental:** Scientific questions to be answered.
    3. **Out-of-Scope:** Boundaries to prevent agent drift.
- **Output:** Once the interview is complete, create the following files in the working folder of the project:
    1. `RESEARCH_PLAN.md` - a rigorous handoff plan for a junior data scientist.
    2. `RESEARCH_PLAN_PITCH_DECK.html` - a standalone static HTML pitch deck for a data science group meeting.
    3. `index.html` - the project's persistent Tier-1 entry page. See [`research-portal`](../research-portal/SKILL.md). Bootstrap it with: a header (project title, ticket link, owner, status chip), a §Plan section linking `README.md` + `RESEARCH_PLAN.md` + `RESEARCH_PLAN_PITCH_DECK.html`, an empty §Tasks section, a §Review placeholder noting that `RESEARCH_REVIEW.html` will appear after `/publish-research` runs, and a §Wiki section linking the most-relevant wiki pages cited in the project README. `index.html` is a permanent navigation surface — every subsequent skill that creates or modifies HTML in the project updates it.
- **Pitch deck requirements:** Follow the Tier-1 deck variant in [`research-portal`](../research-portal/SKILL.md) — shared `:root` theme, `.intro` card, slide-like `<h2>` sections separated by horizontal rules, no tile grid, prints clean, self-contained (no build step, no external dependencies). Slide content must include:
    1. Title, owner, date, and one-sentence thesis.
    2. Problem and motivation.
    3. Proposed research question or hypothesis.
    4. Data assets, feasibility constraints, and known access risks.
    5. Experimental design and success criteria.
    6. Major risks, out-of-scope boundaries, and decision points.
    7. Proposed timeline, next steps, and explicit asks for the group.

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time. Use the question tool in the UI to get answers from the users.

If a question can be answered by exploring the codebase, explore the codebase instead.

