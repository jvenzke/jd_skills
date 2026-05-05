---
name: research-full-plan
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
- **HTML Generation Preference:** During the interview, ask the user if HTML pages (`RESEARCH_REVIEW.html` and `RESEARCH_PLAN_PITCH_DECK.html`) should be generated. Save this preference in `research_workspace/config.md`. Do not ask this again in future steps. If disabled, do not generate the HTML files.
- **Output:** Once the interview is complete, create the files in the working folder of the project:
    1. `RESEARCH_PLAN.md` - a rigorous handoff plan for a junior data scientist.
    2. `RESEARCH_PLAN_PITCH_DECK.html` - a standalone static HTML pitch deck for a data science group meeting (if HTML generation is enabled).
- **In-Chat Summary:** Extract and present the critical parts of the `RESEARCH_PLAN.md` directly in the chat so the user can quickly read and understand what will happen next in the process without opening the file. After presenting these critical snippets, summarize what sections were left out of the chat (e.g., "table definitions 100 lines of file") and why. Finally, report the percentage of the file's rows that were presented to the user in the chat relative to the total rows in the file.
- **Pitch deck requirements:** The HTML must be self-contained and open directly in a browser without a build step or external dependencies. Make it presentation-ready with slide-like sections, minimal inline CSS, and clear speaker-friendly framing. Include:
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

