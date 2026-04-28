---
name: research-plan
description: Interview the user to turn a vague research idea into a rigorous, falsifiable plan. Categorizes unknowns into feasibility, experimental, and out-of-scope.
---

Your goal is to build a `RESEARCH_PLAN.md` that can be handed off to a junior data scientist. 
  
### Rules:
- **Categorization:** You must separate unknowns into:
    1. **Feasibility:** Data access, SQL table sizes, cost, and scale.
    2. **Experimental:** Scientific questions to be answered.
    3. **Out-of-Scope:** Boundaries to prevent agent drift.
- **Output:** Once the interview is complete, create a `RESEARCH_PLAN.md` in the working folder of the project.

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time. Use the question tool in the UI to get answers from the users.

If a question can be answered by exploring the codebase, explore the codebase instead.

