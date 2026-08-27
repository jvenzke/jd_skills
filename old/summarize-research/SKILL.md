---
name: summarize-research
description: Compiles research into a production-ready results/ package with executive summary, final assets, presentation, and implementation code.
disable-model-invocation: true
---

You are a Lead Data Scientist preparing a production handoff. Compress the full research journey into a clean, actionable package for stakeholders and engineers.

Use todos before starting: one todo per numbered step below, exactly one `in_progress`, complete each step before starting the next. Do not skip or reorder unless the user explicitly asks.

1. **Inspect inputs and align.** If `research_workspace/` exists, primary inputs are `research_workspace/MANIFEST.md`, `running_log.md`, `src/`, and `artifacts/`; use `research_tasks/archive/` only for raw evidence/provenance. Read `Research_plan.md` when provided.

2. **Do not bulk-copy history.** Final results should contain only the winning logic, final findings, and curated assets; leave EDA, dead ends, failed experiments, raw task folders, and redundant artifacts in the archive/workspace.

3. **Interview gate.** Until handoff scope is aligned, ask one question at a time with the UI question tool and include your recommended answer. Explore the repo instead of asking when exploration answers the question. Do not move past Step 3 until aligned.

4. **Pre-aligned exception.** If the user supplies a converged `Research_plan.md` (or equivalent), `research_workspace/`, and asks to compile now, state the assumed handoff scope and continue unless a blocker remains.

5. **Create structure.** Create `results/` and `results/assets/`.

6. **Executive summary.** Write stakeholder-facing conclusions focused on business impact, final decisions, confidence, and remaining rollout risks.

7. **Production logic.** Add `results/production_sql.md` and `results/production_python.py` (or repo-preferred names) containing only winning/reusable implementation logic. Indexing canonical source files with short critical excerpts is acceptable; avoid copying exploratory SQL wholesale.

8. **Assets.** Copy final interactive `.html` and other presentation-ready artifacts into `results/assets/`. Copy `.png` only when Markdown/static preview needs inline images or HTML cannot render. Link every retained asset from `results/README.md`.

9. **Presentation webpage.** Create a static `results/presentation.html` for the data science group: work completed, findings, impact, key visuals, limitations, and next steps. Make it a polished presentation artifact, not a raw research log, and link it from `results/README.md`.

10. **Human review page.** If `RESEARCH_REVIEW.html` exists, clean it as a reviewer-facing companion: remove stale tiles, fix relative links, group sections, clarify summaries/dependencies, and point curated evidence to `research_workspace/artifacts/` or `results/assets/`. Do not turn it into the presentation page. If absent, do not create it unless asked.

11. **Final README.** Write `results/README.md` with executive summary, final methodology, production snippets, asset links, reproduction notes, and final directory structure. Keep it about the final answer, not the whole exploration history.

12. **Project README.** Update the research project `README.md` with a short summary and links to `results/`, `research_workspace/`, and `RESEARCH_REVIEW.html` when present.

13. **Wiki conditional.** If `llm_wiki/` exists, invoke the `llm_wiki` research ingest workflow: create/update relevant wiki pages, cross-links, index, and log entry. Both linters must pass before closing: `python3 llm_wiki/skills/llm_wiki/lint_links.py` and `python3 llm_wiki/skills/llm_wiki/lint_frontmatter.py`.

14. **Review package.** Verify todos are complete; spot-check `results/README.md` links, `presentation.html`, review-page links, curated artifact links, and wiki linters if applicable. End with the final directory structure and note anything not verified.
