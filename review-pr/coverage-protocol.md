---
head_sha: <full sha>
total_changed_lines: 0
human_presented: 0
agent_reviewed_not_shown: 0
not_reviewed: 0
not_applicable: 0
---

# Coverage

Initialize with `gh pr diff <n> | python3 <this-skill>/scripts/init_coverage.py --head-sha <sha>`.

Mark a row `human_presented` only when those exact lines were printed as a fenced code block in chat in the same turn. Line-number mentions do not count.

| path | lines | count | status | reason | shown_in |
| --- | --- | ---: | --- | --- | --- |
| | | | not_reviewed | | |

## Totals

Recompute from the inventory after every review turn. Percents use `total_changed_lines` as the denominator (exclude `not_applicable`).

| status | lines | pct |
| --- | ---: | ---: |
| human_presented | 0 | 0% |
| agent_reviewed_not_shown | 0 | 0% |
| not_reviewed | 0 | 0% |
| not_applicable | 0 | — |

## Agent-only reasons

`peripheral_change` · `covered_by_tests_or_ci` · `covered_by_pattern_match` · `covered_by_static_review` · `duplicate_or_mechanical` · `superseded_or_unchanged_context` · `low_risk_dependency`
