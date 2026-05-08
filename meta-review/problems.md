# Meta Review Problems

Keep entries compact. Store only critical details needed to spot repeated skill failures.

## Active

- 2026-05-01 | skill: review-research (now split into compress-research and publish-research) | symptom: per-step approval gates collapsed in steps 3-6 when user issued a chat-level "continue" | cause: skill text says "ask before editing" but does not require an AskQuestion call, and a single "continue" gets interpreted as blanket approval for the rest of the workflow | fix: either tighten language to require AskQuestion per step or carve out a "blanket continue" exception | decision: logged | evidence: DST-907 review session 2026-05-01, steps 3, 4, 5, 6 all proceeded with plan summaries but no per-step AskQuestion call
- 2026-05-05 | skill: do-research | symptom: generated Plotly review HTML had unreadable overlapping subplot titles and no visible trace legend | cause: skill requires Plotly artifacts but lacks a visual QA check before finalizing review HTML | fix: add visual QA directive for legends, titles, and labels | decision: logged | evidence: Task 029 HTML needed follow-up legend/title fix after user screenshot
- 2026-05-05 | skill: compress-research | symptom: Step 3 closing reply lacked a substantive excerpt from `Research_plan.md` alongside `running_log.md` / `discussion_log.md` snippets and row-coverage estimate | cause: session prioritized ledger paths over quoting aligned plan text | fix: always include at least one anchored excerpt from `Research_plan.md` (or grep-aligned bullet summary) plus stated row-% coverage per Step 3 closing bullets | decision: logged | evidence: DST-907 Task 029 compress session, meta-review 2026-05-05

## Resolved

- 2026-05-08 | skill: logic-walkthrough | fixed: tightened "exact wording" directive at the user-approval gate to require the verbatim PR-comment body (including code blocks/quoted code) alongside summary, so the user no longer has to ask "show me the actual comment text" to see what would post | commit: 3b2743e logic-walkthrough: require verbatim comment body at approval gate | compressed: 0 entries
