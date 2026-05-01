---
name: research-portal
description: Shared rendering spec for the static HTML surfaces produced by the research workflow — the pitch deck (`RESEARCH_PLAN_PITCH_DECK.html`), the human review page (`RESEARCH_REVIEW.html`), the leaf-level interactive review artifacts dropped by `/do-research`, and the final presentation webpage built by `/summarize-research`. This skill is referenced by `/research-plan`, `/do-research`, `/publish-research`, `/summarize-research`, `/compress-research`, `/commit-research`, and `/to-research-tasks` to keep visual structure, navigation, theming, and data-loading patterns consistent across the project. Use it directly when authoring or auditing any HTML surface in a research project; do not duplicate its conventions inline in other skills.
disable-model-invocation: true
---

You are the **rendering spec** for every static HTML surface in a research project. The research workflow's other skills (`/research-plan`, `/do-research`, `/publish-research`, `/summarize-research`) decide *what* to put on each page; this skill decides *how* the page is structured, themed, navigated, and wired to data.

The portal is intentionally:

- **Static.** Plain `.html` files. No build step. Opens via double-click (`file://`) or `python -m http.server`.
- **Self-contained.** Data is either embedded inline (`<script>window.RESULTS = {...}</script>` or `<script id="..." type="application/json">`) or `fetch`'d from a JSON file sitting next to the HTML.
- **Hand-authored.** Each page is small enough (a few hundred lines) that a human can read the whole file. No JSX, no bundlers.
- **Three-tiered.** Index → group/section landing → in-depth view. The hierarchy is the navigation.

---

## Hard rule: no orphan HTML

**Every HTML file you create or modify must be reachable from the project's entry page in two clicks or fewer.** An orphan page (one that exists on disk but has no inbound link from the index / review page) is a broken artifact even if it renders correctly — the reviewer cannot find it, so it does not exist for them.

This rule binds every skill that produces HTML. Before finishing any HTML-producing task:

1. **Identify the entry page** for this research project. In order of preference:
   - `RESEARCH_REVIEW.html` (preferred entry once any review work has happened — it's the reviewer-facing index).
   - `RESEARCH_PLAN_PITCH_DECK.html` (acceptable entry early in a project, before any tasks are reviewed).
   - `index.html` (only if neither of the above exists yet — and if you find yourself creating one, prefer creating `RESEARCH_REVIEW.html` instead, since the rest of the workflow expects that filename).
2. **Add an inbound link to every new HTML file** in the most appropriate Tier-1 or Tier-2 section before declaring the work done:
   - **Leaf review artifacts** (`task_{idx}_{name}/review_artifacts/*.html` produced by `/do-research`) → linked from the task's tile in the matching Tier-2 section of `RESEARCH_REVIEW.html`. If `RESEARCH_REVIEW.html` doesn't exist yet, the task `results_log_{idx}_{name}.md` must list the artifact, and `/publish-research` will create the tile in its next pass — but **the task author must surface this gap explicitly** in their final summary so the next reviewer doesn't miss it.
   - **Templated viewer variants** (one per model / variant / family) → each variant gets its own tile, or a single tile that links to a parent index page (e.g. `cgp_diagnostic_index.html`) which then links to all variants. Either pattern is fine; an unlinked variant is not.
   - **Pitch deck / presentation page / methodology page / archive page** → linked from the `RESEARCH_REVIEW.html` "Reference" Tier-2 section (or its equivalent).
3. **Add a breadcrumb back to the entry page** at the top of every non-entry HTML file. The breadcrumb is the second half of navigation — the link goes *to* the page, the breadcrumb lets the reader get *back*. Both are required.
4. **Do not hide files behind only-the-author-knows-the-URL access.** If a page is intentionally not surfaced (e.g. a half-finished draft), put it under a `drafts/` subdirectory and note it in `research_workspace/running_log.md` so future reviewers know it exists; never leave it next to live artifacts unlinked.
5. **Audit before reporting done.** Run a quick reachability check (manual or scripted — see "Reachability audit" below). If any HTML in the project is unreachable from the entry page, either link it or move it to `drafts/` / `research_tasks/archive/`. Report any retired/archived pages explicitly.

**When updating an existing HTML page:** the same rule applies in reverse. If you remove a tile or a link, you may have just orphaned the target. Either remove the target too (move to `archive/`) or re-link it from another section. Never silently delete inbound links.

### Reachability audit (quick recipe)

From the project root, list all HTML files and check each one is mentioned somewhere it can be reached from the entry page:

```bash
# 1. List every HTML file under the project (excluding archives and drafts)
find . -name "*.html" -not -path "*/archive/*" -not -path "*/drafts/*" -not -path "*/node_modules/*"

# 2. For each one, confirm it appears as an href= target in another HTML file
for f in $(find . -name "*.html" -not -path "*/archive/*" -not -path "*/drafts/*"); do
  base=$(basename "$f")
  hits=$(grep -rl "href=\"[^\"]*$base\"" --include="*.html" . | grep -v "$f")
  if [ -z "$hits" ] && [ "$base" != "RESEARCH_REVIEW.html" ] && [ "$base" != "index.html" ]; then
    echo "ORPHAN: $f"
  fi
done
```

Any line printed by the audit is an orphan and must be fixed before declaring the work done.

---

## How this skill is used by the rest of the workflow

| Other skill | HTML surface it owns | Which tier of this spec |
|---|---|---|
| `/research-plan` | `RESEARCH_PLAN_PITCH_DECK.html` | A single-page slide-deck variant of Tier 1; sectioned, no tile grid required |
| `/do-research` | `task_{idx}_{name}/review_artifacts/*.html` (Plotly charts, scrubbers) | Tier 3 leaf views (interactive Plotly or static) |
| `/publish-research` | `RESEARCH_REVIEW.html` | Tier 1 index → Tier 2 task-group sections of tiles → links into Tier 3 review artifacts produced by `/do-research` |
| `/publish-research` | `RESEARCH_PLAN_PITCH_DECK.html` (refresh) | Same Tier-1 deck variant as `/research-plan`, updated with latest results |
| `/summarize-research` | `/results/<presentation>.html` | Tier 1 final-handoff variant, narrative-led, links into `/results/assets/` |
| `/summarize-research` | `RESEARCH_REVIEW.html` (cleanup) | Same Tier-1 review index, with stale tiles removed and links fixed |
| `/compress-research` | (none — defers all HTML edits to `/publish-research`) | n/a |
| `/commit-research` | (none — only stages files; uses the no-orphan rule to decide what to keep) | n/a |
| `/to-research-tasks` | (none — declares which Tier-2 section a task tile should land in) | n/a |

When any of those skills says "produce/update an HTML page", consult this skill for structure, theme, components, and data-loading; do not invent a new pattern.

---

## The three tiers

```
RESEARCH_REVIEW.html               ← Tier 1: review index (entrance for human reviewer)
 ├── §section: Hypothesis A        ← Tier 2: task-group section, contains a tile grid
 │    ├── tile → task_001/...      ← Tier 3 leaf: review_artifacts of that task
 │    └── tile → task_004/...
 │
 ├── §section: Hypothesis B
 │    ├── tile → task_002/...
 │    └── tile → task_003/...
 │
 └── §section: Reference
      ├── RESEARCH_PLAN.md (link)
      └── RESEARCH_PLAN_PITCH_DECK.html (link)

RESEARCH_PLAN_PITCH_DECK.html      ← Tier 1 single-page slide variant (no tile grid)
/results/<presentation>.html       ← Tier 1 final-handoff variant
```

### Tier 1 — index / entrance (`RESEARCH_REVIEW.html`, pitch deck, presentation page)

Single file. Lays out everything the reader can navigate to. Structure top-to-bottom:

1. **`<h1>` + small subtitle** — project name + one-line framing.
2. **`.intro` card** — 2–4 paragraphs of context. Define any jargon the rest of the page assumes. For `RESEARCH_REVIEW.html`, this is where the convergence status, latest review date, and current research question live. For the pitch deck, this is the title-slide content.
3. **Sectioned tile grids** (review page only). Each section gets:
   - A `.section-label` header (e.g. `📊 Hypothesis A — does X explain Y?`) with a small subtitle linking to the relevant unknown.
   - A `.grid` of tiles (CSS `grid-template-columns: repeat(auto-fit, minmax(420px, 1fr));`).
4. **Tiles are anchors** (`<a href="…" class="tile">`), not divs. The whole card is clickable. Each tile contains:
   - `.tile-icon` (single emoji, ~2.4em) — gives a glanceable identity.
   - `.tile-title` + `.tile-subtitle` — task id/name + one-line "what is this".
   - `.tile-description` — 2–3 sentences. The "why click me" pitch. **Surface the headline number** if one exists ("hits +27.7pp over baseline").
   - `.tile-meta` — pills (`<span class="pill green">…</span>`) for status / task type / linked unknown + a stats line ("n=100 · 4 families · seed=42").
   - `.tile-cta` — verb + arrow ("Open review artifacts →" / "Inspect data →").

**Visual rules for tiles:**

- White card on a soft-grey body background.
- Subtle shadow at rest (`box-shadow: 0 1px 3px rgba(0,0,0,0.05)`).
- On hover: lift (`transform: translateY(-2px)`) + accent border + larger shadow. This hover affordance is non-negotiable — it's what tells the reviewer "these are clickable".
- Archived / superseded tiles use dashed borders (`.tile.archive-tile`) so they're clearly secondary.

**Interactive controls inside Tier 1.** Filters, collapsible sections, sortable tables, and editable note checklists are allowed *inside* tile descriptions or as supplementary widgets within a `.section-label` band, but they do not replace the tile grid as the primary navigation surface. The entrance pattern is always "skim section labels → click a tile → land on Tier 3 leaf"; controls augment that, they don't substitute for it.

**Pitch-deck variant.** When the page is a slide deck, drop the tile grid. Use slide-like sections separated by horizontal rules and large `<h2>` headings, one section per content slide (Title / Problem / Hypothesis / Data / Design / Risks / Timeline / Asks). Same theme, same `.intro` card style, same breadcrumb to `index.html` if one exists. Slides should print clean.

**Presentation-page variant** (built by `/summarize-research`). Narrative-led, headline-number-led, with `<h2>` per major finding and inline plots. Links to `/results/assets/` for downloadable artifacts and to `research_workspace/artifacts/` for provenance.

### Tier 2 — task-group section (a band inside the Tier 1 review index)

Not a separate file — a named section (`<section>` or just an `<h2>`-led block) inside `RESEARCH_REVIEW.html`. Contains:

- Section header (`.section-label`) explaining the **shared research theme** (linked unknown, hypothesis, data source, or decision dependency).
- A 1–2 sentence intro: why these tasks are grouped, the combined takeaway, links to upstream/downstream sections if dependencies exist.
- A `.grid` of tiles, one per task in the group.

When a project is small (≤3 tasks) you can have a single Tier-2 section. When it grows, split sections by hypothesis or by data source — never by chronological order.

`/to-research-tasks` is the upstream author of which Tier-2 section a new task tile should land in; `/publish-research` is the downstream consumer that actually writes the tile into the section.

### Tier 3 — leaf / in-depth views (the `review_artifacts/*.html` files)

Two flavors. Pick whichever matches the artifact `/do-research` produced.

**Flavor A — Static deep-dive** (single-series chart pages, case studies):

- Breadcrumb back to `RESEARCH_REVIEW.html`.
- `<h1>` + intro paragraph.
- A column of `<img>` tags pointing to pre-generated PNG plots (only when a static image is needed) **or** embedded Plotly figures.
- **Annotation paragraphs between each plot** explaining what to notice. Annotations carry the analysis — without them this is a wall of charts.

**Flavor B — Interactive scrubber** (step-through diagnostic viewers):

This is the most opinionated piece. The pattern that works:

1. **Header chrome:** breadcrumb, h1, `.meta` box (current run params: family, n_obs, seed, date).
2. **Controls strip:** family/variant dropdown (if multiple datasets share the file) + slider row with `⏪ −10`, `◀ −1`, `▶ play`, `+1 ▶`, `+10 ⏩`, and an `<input type=range>`. A `.now-row` underneath shows the cursor position in human-readable form.
3. **Stacked panels:** typically 3.
   - **Panel A — full timeline** (the "where am I" view): always-visible time-series with a vertical cursor line that follows the slider.
   - **Panel B — local view at cursor** (the "what does the model see right now" view): zoomed-in plot, posterior, predicted-vs-actual.
   - **Panel C — decomposition / explanation** (the "why" view): bars, heatmap, or matrix breaking down the decision into contributing factors. Hover should reveal the factor breakdown.
4. **Plotly via CDN:** `<script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>`. No npm.
5. **Data loading pattern (idiomatic, dual-mode):**

   ```html
   <script id="diagnostic-data" type="application/json">
   {"_placeholder": true}
   </script>
   <script>
   const DATA_FILE = "diagnostic_data.json";
   async function loadData() {
     const inline = document.getElementById("diagnostic-data");
     const parsed = JSON.parse(inline.textContent);
     if (!parsed._placeholder) { bootstrap(parsed); return; }
     const resp = await fetch(DATA_FILE);
     bootstrap(await resp.json());
   }
   </script>
   ```

   The HTML ships with a `_placeholder` sentinel; a Python build step (or the `/do-research` agent itself when finalizing the artifact) swaps the placeholder for the real JSON when generating a self-contained file. Until then, it falls back to `fetch`. This dual-mode is what makes the same template work both checked-in (inline, portable, opens under `file://`) and during dev (fetch, fast iteration).

6. **Templating:** when there are N variants of the same viewer (e.g. one viewer per model variant), keep one `.tmpl.html` and a small Python builder that substitutes `DATA_FILE` and the page title. Do **not** maintain N copies by hand. The builder lives in `research_workspace/src/` once it's stable, per `/compress-research` compression rules.

---

## Shared CSS theme

Put this `:root` block in **every** HTML file (do not extract to a shared stylesheet — keeping each file self-contained is the whole point). The theme is what makes the portal look unified.

```css
:root {
  --fg: #1d2330;       /* primary text */
  --muted: #6b7280;    /* secondary text, captions */
  --accent: #2b6cb0;   /* links, h2 underlines, table headers */
  --accent2: #c05621;  /* secondary accent (rarely used) */
  --bg: #f7f7f5;       /* page background */
  --card: #ffffff;     /* card / table / panel background */
  --border: #e5e7eb;   /* hairline rules */
  --hi-bg: #ecfdf5;    /* "best" row highlight bg */
  --hi-fg: #065f46;    /* "best" row highlight fg */
}
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
  color: var(--fg); background: var(--bg);
  line-height: 1.55; margin: 0; padding: 2em 1em 4em 1em;
}
.wrap { max-width: 1180px; margin: 0 auto; }
```

**Component primitives to reuse across pages:**

- `.intro` — bordered card, used right under `<h1>`, holds context paragraphs.
- `.grid` — `display: grid; grid-template-columns: repeat(auto-fit, minmax(420px, 1fr)); gap: 1.6em;`
- `.tile` — clickable card (anchor, not div). Hover: lift + accent border.
- `.section-label` — h2-like divider with a coloured underline and a small grey caption.
- `.pill` — inline tag for tile metadata. Variants: default (purple), `.blue`, `.green`.
- `.breadcrumb` — top of every non-index page. `← Back to review`.
- `.note` — yellow-bordered callout for caveats / warnings.
- `.stat-card` — large-number summary tile.
- `table` — accent-header, striped rows, hover-highlight, `.metric` for monospace numeric cells, `.best` for winning row.

---

## File-layout conventions (within a research project folder)

These match the contracts in `/generate-research-project`, `/do-research`, `/compress-research`, and `/publish-research`. The portal skill does not own this layout — it just consumes/links to it.

```
<research_project>/
├── README.md
├── RESEARCH_PLAN.md
├── RESEARCH_PLAN_PITCH_DECK.html        ← Tier 1 (deck variant) · this skill
├── RESEARCH_REVIEW.html                 ← Tier 1 (review index) · this skill
├── research_tasks/
│   ├── task_001_<name>.md
│   ├── task_001_<name>/
│   │   ├── results_log_001_<name>.md
│   │   ├── src/
│   │   └── review_artifacts/             ← Tier 3 leaf views · this skill
│   │       ├── artifact_manifest.json
│   │       ├── chart_<x>.html            ← interactive Plotly
│   │       ├── chart_<x>.png             ← only if Markdown needs static image
│   │       └── viewer_<x>.html           ← scrubber if applicable
│   └── archive/                          ← retired tasks (mv'd by /compress-research)
├── research_workspace/                   ← compressed reusable assets
│   ├── MANIFEST.md
│   ├── running_log.md
│   ├── discussion_log.md                 ← owned by /compress-research, cleared by /publish-research
│   ├── src/
│   │   └── viewer_template.tmpl.html    ← templated leaf view, if N variants
│   └── artifacts/                        ← curated copies for review
└── results/                              ← built by /summarize-research
    ├── README.md
    ├── <presentation>.html               ← Tier 1 (final variant) · this skill
    └── assets/
```

**Naming conventions:**

- Use **slugs with leading numbers** for ordered families/categories: `0_steady_state`, `1_sudden_reversal`, `10_adversarial`. Preserves sort order in dropdowns.
- Pair every leaf HTML with its data file using a stem prefix (`viewer_<x>.html` ↔ `viewer_<x>.json`).
- Retired pages do **not** get deleted — moved to `research_tasks/archive/` and linked from a "Reference / Archive" section of `RESEARCH_REVIEW.html`. File continuity matters for back-references in tickets / comments.

---

## Authoring checklist

Run this when any of the invoking skills produces or updates an HTML surface.

**Tier 1 sanity (`RESEARCH_REVIEW.html`, pitch deck, presentation page):**
- [ ] One sentence under the `<h1>` explains what the reader is looking at.
- [ ] The `.intro` card defines any jargon the rest of the page assumes.
- [ ] (Review page) Every tile has icon, title, subtitle, description, ≥1 pill, meta line, CTA.
- [ ] (Review page) Hover on tiles is visually obvious (lift + colour change).
- [ ] (Review page) No section has fewer than 2 tiles or more than ~5 — fold or split if needed.
- [ ] Links to `RESEARCH_PLAN.md`, `research_workspace/MANIFEST.md`, archived tasks resolve.

**Tier 3 leaf views:**
- [ ] Breadcrumb back to `RESEARCH_REVIEW.html` is at the top.
- [ ] Static views: every PNG/figure is preceded or followed by a sentence of analysis.
- [ ] Interactive views: ±1 / ±10 / play buttons all work; play loops or stops at end; cursor indicator matches across panels.
- [ ] If multiple variants share a template, the template is the source of truth — no hand-edited divergence.
- [ ] Data loads correctly under both `file://` (inline) and `python -m http.server` (fetch fallback).

**Cross-cutting:**
- [ ] Theme variables (`--accent`, `--bg`, etc.) match across files. (`grep ":root {" *.html` should show the same block.)
- [ ] No external dependencies besides a CDN'd Plotly. No fonts loaded from Google. No frameworks.
- [ ] Open the entrance HTML fresh in the browser and click every tile. No 404s, no broken images, no JS errors in console.

**Reachability (no orphans — see "Hard rule" above):**
- [ ] Every newly created or modified HTML file is reachable from the project entry page (`RESEARCH_REVIEW.html` if present, else `RESEARCH_PLAN_PITCH_DECK.html`) in ≤2 clicks.
- [ ] Every non-entry HTML file has a breadcrumb link back to the entry page at the top.
- [ ] The reachability audit (`find` + `grep` recipe above) prints no `ORPHAN:` lines. If one prints, either link the file from a Tier-2 section, or move it to `drafts/` / `research_tasks/archive/`.
- [ ] Removed inbound links did not silently orphan their target. If a tile was deleted, its target was either re-linked elsewhere or archived.

---

## Things to avoid

- **Don't introduce a framework.** React/Vue/Next defeats the "open from disk, read the source, hand-author" purpose. The whole portal should be readable line-by-line.
- **Don't use a CSS preprocessor or shared stylesheet.** Each HTML file copies the `:root` theme block. Slight duplication beats a missing dependency.
- **Don't put analysis only in the chart.** Every chart needs a sentence somewhere on the page saying what it shows and what to notice. Charts are evidence; prose is the argument.
- **Don't fetch from third-party hosts at runtime** (besides Plotly CDN). The portal should still render with the laptop offline — pre-vendor Plotly into the project if offline-first matters.
- **Don't use server-side templating for pages that can be static.** If a page has stable content, it's a `.html` file. Use a Python builder only when content is templated across N variants.
- **Don't delete retired pages.** Move them under `research_tasks/archive/`. Old links in tickets / Slack stay valid.
- **Don't bury the headline.** The headline number for each task (the "+27.7pp" type result) should appear in the *tile description on the review page*, not just inside the deep page.
- **Don't leave orphan HTML.** Any new `.html` file must be linked from the entry page in ≤2 clicks before the task is declared done. An unreachable page is an invisible page — it does not count as a deliverable. See the "Hard rule: no orphan HTML" section above.
- **Don't duplicate this skill's conventions inline in other skills.** When `/research-plan`, `/do-research`, `/publish-research`, or `/summarize-research` produces HTML, they should reference this skill, not redefine its rules.
