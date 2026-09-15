# Red zones

Paths whose changes get mandatory extra depth and exposure, however small the diff looks. Matching is by path prefix against the active changed-file list, so a directory entry covers everything beneath it.

Edit the table to add or retire a red zone. No phase file hardcodes a path.

| path | why |
| --- | --- |
| `yield_optimization/yield-optimization-tools/src/yield_optimization_tools/SafeSpringserveClient.py` | Guard wrapper that blocks raw Springserve write methods and validates every save and duplicate against account and live-connection rules. Weakening a validator lets unintended writes reach production ad-server configuration. |
| `yield_optimization/yield-optimization-tools/src/yield_optimization_tools/yo_safe_springserve_client.py` | Builds the guarded client: environment secrets, account and label constants, and the allowed-name set the guard enforces. A wrong environment, account, or allowed name sends production traffic to the wrong tags. |

## Required handling

When the active diff touches a listed path:

1. Intake sets `review_risk: critical`, names the matched path in `review_risk_reasons`, and records the matches in `tasks.md` `redzone_paths` and `PR_BRIEF.md`. Never lower that risk later in the review.
2. Every changed section in a matched path is shown in the walkthrough as a fenced `diff` hunk, finding or not. `agent_reviewed_not_shown` is not available for those rows.
3. The walkthrough flags the path in the changed-path tree and asks the user to acknowledge the change before the submit gate.
4. A changed red-zone section with no covering test is recorded in `TESTS.md` and raised in the walkthrough as an unresolved prompt.

A red zone is not itself a finding. It sets depth and exposure; the finding bar in [`phases/skeptic.md`](phases/skeptic.md) still applies.
