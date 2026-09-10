---
head_sha: <full sha>
changed_sections: 0
added_lines: 0
deleted_lines: 0
human_presented: 0
agent_reviewed_not_shown: 0
not_reviewed: 0
not_applicable: 0
---

# Coverage

Initialize with `gh pr diff <n> | python3 <this-skill>/scripts/init_coverage.py --head-sha <sha>`.

When `review_scope` is `incremental`, initialize from the update diff instead (`git diff <prior_review_head_sha>...<head_sha>`). Percents and `not_reviewed` apply to that update, not the full PR. Unchanged sections from the prior review are out of the inventory.

The inventory unit is a **changed section** (one `@@` region). A rename with no remaining sections is one row. Report `added_lines` and `deleted_lines` in frontmatter; do not use an additions-only `total_changed_lines`.

Percents use `changed_sections` as the denominator (exclude `not_applicable`). Presentation counts are not a measure of meaningful human review.

Mark a **product** row `human_presented` only when those exact changed lines were printed as a fenced code block in chat in the same turn. Line-number mentions do not count. `human_presented` means the code was **shown**; it does not mean the user reviewed or understood it. Never label it Human-reviewed.

Changed tests are never `human_presented`. After the agent inspects them, summarize each relevant test in chat (setup, assertion, claim/branch) and mark `agent_reviewed_not_shown` with reason `test_summarized_in_chat`.

The walkthrough is claim- and decision-complete, not section-complete. Show exact product code when it is needed for human judgment (proposed findings, material public/module boundaries, ambiguous intent, user-requested expansion, or a design decision that cannot be confirmed from the traced path). After inspecting other core sections, summarize them in chat and mark `agent_reviewed_not_shown` with reason `covered_by_static_review`. Incidental changes use the most specific agent-only reason.

| path | section | + | - | count | status | reason | shown_in |
| --- | --- | ---: | ---: | ---: | --- | --- | --- |
| | | | | | not_reviewed | | |

## Totals

Recompute from the inventory after every review turn. Percents use `changed_sections` (exclude `not_applicable`).

| status | sections | pct |
| --- | ---: | ---: |
| human_presented | 0 | 0% |
| agent_reviewed_not_shown | 0 | 0% |
| not_reviewed | 0 | 0% |
| not_applicable | 0 | — |

## Human oversight

Separate from presentation counts. Record only explicit user decisions (not displayed sections):

- claims confirmed:
- architecture/boundary decisions reviewed:
- findings approved/rejected/edited:
- unresolved business questions answered:

## Agent-only reasons

`peripheral_change` · `covered_by_tests_or_ci` · `covered_by_pattern_match` · `covered_by_static_review` · `duplicate_or_mechanical` · `superseded_or_unchanged_context` · `low_risk_dependency` · `test_summarized_in_chat`
