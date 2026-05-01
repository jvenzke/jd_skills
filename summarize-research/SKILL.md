---
name: summarize-research
description: Compiles all research logs into a production-ready /results folder with an executive summary and optimized implementation code.
---

You are a Lead Data Scientist preparing a production hand-off. Your goal is to compress the entire research journey into a clean, actionable package.

> **Wiki integration:** If `llm_wiki/` exists in the repo, the converged research findings must be filed back into the wiki as part of this workflow (Step 10 below). Follow the `llm_wiki` skill's "Research workflow integration" section. Both wiki linters must pass before summarize is declared complete.

### Required Workflow:

Use the todo feature to track the workflow before starting. Create one todo for each step below, keep exactly one step `in_progress`, and mark each step `completed` before starting the next one. Do not skip or reorder steps unless the user explicitly asks.

1. **Inspect Handoff Inputs**
   - If `research_workspace/` exists, use `research_workspace/MANIFEST.md`, `research_workspace/running_log.md`, `research_workspace/src/`, and `research_workspace/artifacts/` as the primary research handoff inputs.
   - Use `research_tasks/archive/` only for raw evidence and deeper provenance.
   - Do not copy every archived artifact into final results.
   - Interview me relentlessly about every aspect of the handoff plan until we reach a shared understanding. Walk down each branch of the research tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.
   - Ask the questions one at a time. Use the question tool in the UI to get answers from the user.
   - If a question can be answered by exploring the codebase, explore the codebase instead.
   - Do not move on to step 2 until we are aligned.

2. **Create Results Structure**
   - Create a `/results` directory.
   - Create `/results/assets` for final visual assets.

3. **Synthesize Executive Summary**
   - Write a high-level summary for non-technical stakeholders.
   - Focus on business impact, final conclusions, and confidence level.

4. **Extract Production Logic**
   - Extract and document ONLY the winning SQL and Python logic.
   - Remove all EDA, dead ends, and failed experiment code.
   - Optimize the handoff code for clarity and reproducibility.

5. **Collate Final Assets**
   - Copy final interactive `.html` visualizations and other presentation-ready assets into `/results/assets`.
   - Copy `.png` visualizations only when they are needed for Markdown files, static previews, or final handoff contexts that cannot render HTML.
   - Link each retained visualization from `/results/README.md`, using HTML links for interactive artifacts and PNG embeds only when Markdown needs an inline image.

6. **Build Presentation Webpage**
   - Create a static webpage in `/results` that can be used as a presentation for the data science group.
   - Outline the work completed, major findings, business or analytical impact, key visuals, limitations, and recommended next steps.
   - Design it as a clear presentation artifact, not a raw research log.
   - Link the webpage from `/results/README.md`.

7. **Clean Up Human Review Page**
   - Locate `RESEARCH_REVIEW.html` in the research project working folder if it exists.
   - If it exists, clean it up as a reviewer-facing companion to the final package: remove stale task tiles, fix broken relative links, group related task tiles into clear sections, clarify section summaries and dependency relationships, and point curated artifacts to `research_workspace/artifacts/` or `/results/assets` as appropriate.
   - Prefer linking or embedding curated `.html` artifacts for reviewable charts; keep `.png` references only for Markdown/static-preview needs or browser fallbacks.
   - Preserve its purpose as an interactive review surface for task-level evidence. Do not turn it into the final presentation webpage.
   - If no `RESEARCH_REVIEW.html` exists, do not create one unless the user asks; note that no human review page was available to clean up.

8. **Write Final Research README**
   - Write `/results/README.md` with the executive summary, final methodology, production snippets, visual asset links, and reproduction notes.
   - Keep the README focused on the final answer rather than the full exploration history.

9. **Update Project README**
   - Add a quick summary of work completed, results, and links to important handoff materials in the main `README.md` for the research project.
   - Link to `/results`, `/research_workspace`, and `RESEARCH_REVIEW.html` as needed.

10. **File Findings into the Wiki** (only if `llm_wiki/` exists in the repo)
   - Invoke the `llm_wiki` skill's Ingest workflow on the converged findings. Specifically:
     - Decide which `llm_wiki/<project>/` folder the findings belong to.
     - Create or update wiki pages for new entities, concepts, and analyses surfaced by the research. Follow the wiki's frontmatter and link-style conventions.
     - Add cross-references from related existing pages.
     - Update `llm_wiki/index.md` with new/changed pages.
     - Append `## [YYYY-MM-DD] ingest | <Research Title>` to `llm_wiki/log.md` with a brief note of pages touched.
   - Run **both wiki linters** — both must report zero errors before this step is complete:
     ```sh
     python3 llm_wiki/skills/llm_wiki/lint_links.py
     python3 llm_wiki/skills/llm_wiki/lint_frontmatter.py
     ```
   - If either linter fails, fix the issue and re-run. Do not proceed to step 11 with linter errors.
   - End this step with a short summary of which wiki pages were created/updated.

11. **Review Final Package**
   - Verify all todos are complete.
   - Confirm `/results/README.md` links resolve.
   - Confirm the static presentation webpage exists and is linked.
   - If `RESEARCH_REVIEW.html` exists, confirm its main section links, task tile links, and curated artifact links resolve.
   - If `llm_wiki/` exists, confirm both wiki linters pass.
   - Present the final directory structure for review.

Compile all findings now and present the final directory structure for review.

