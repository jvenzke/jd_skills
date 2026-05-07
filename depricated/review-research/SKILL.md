---
name: review-research
description: Deprecated. The review/discuss/compress workflow now lives in /compress-research, and the review-page/pitch-deck/research-plan publication workflow now lives in /publish-research. This stub redirects to the two replacements.
disable-model-invocation: true
---

`/review-research` has been split into two skills:

1. **/compress-research** — review the latest research-task results with the user, capture the alignment discussion in `research_workspace/discussion_log.md`, and compress completed work into the research workspace.
2. **/publish-research** — read `discussion_log.md`, update `RESEARCH_REVIEW.html`, `RESEARCH_PLAN_PITCH_DECK.html`, and `RESEARCH_PLAN.md`, then clear the discussion log.

Run `/compress-research` first, then `/publish-research` once the compression and discussion are complete.

This stub is kept only so old chats and references to `/review-research` resolve cleanly. New work should invoke the two replacement skills directly.
