# Meta Review Problems

Keep entries compact. Store only critical details needed to spot repeated skill failures.

## Active

- 2026-05-01 | skill: review-research (now split into compress-research and publish-research) | symptom: per-step approval gates collapsed in steps 3-6 when user issued a chat-level "continue" | cause: skill text says "ask before editing" but does not require an AskQuestion call, and a single "continue" gets interpreted as blanket approval for the rest of the workflow | fix: either tighten language to require AskQuestion per step or carve out a "blanket continue" exception | decision: logged | evidence: DST-907 review session 2026-05-01, steps 3, 4, 5, 6 all proceeded with plan summaries but no per-step AskQuestion call

## Resolved

No resolved problems logged.
