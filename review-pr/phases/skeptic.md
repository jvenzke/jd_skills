# Phase 3 — Adversarial verification

Run this phase after `SECURITY.md`, `TESTS.md`, and `QUALITY.md` exist, against draft claims. Do not wait for `claims_confirmed`. Surviving findings belong in the walkthrough.

The main agent deduplicates specialist (and integrated-review) candidates by defect (same mechanism, overlapping lines) without judging them, then dispatches a fresh read-only skeptic for each candidate or a small related batch.

If `review_scope` is `incremental`, also skeptic `still_open` / `stale` / `reintroduced` prior comments. Addressed prior items are out of scope unless the update reintroduces them.

## Skeptic contract

The skeptic's job is to disprove findings, not confirm them.

For every candidate:

1. Re-read the actual diff and necessary surrounding code; never score from the candidate summary alone.
2. Confirm the affected path/range and exact quote at `head_sha`, plus the causal changed section for any PR-introduced or worsened finding. An unchanged pre-existing defect may have no changed-line anchor. Missing/mismatched evidence → confidence `0`.
3. Scope and causality: a finding is in scope when the PR introduces, worsens, or newly exposes/makes reachable the failure. A pre-existing defect is outside this PR's slice only when the PR does not materially change its reachability, consequence, contract, or affected callers. Do not call missing confirmed behavior future work, and do not excuse a PR-introduced failure because part of its root cause existed before the PR.
4. State the concrete trigger/input/state, traced execution path, and practical consequence.
5. For business findings, cite the current (usually draft) claim to the main agent. For maintainability, apply `../coding-standards.md` and repository patterns at `base_sha`. Do not draft GitHub-facing bodies.
6. Try to identify guards, callers, validation, tests, or invariants that make the proposed failure impossible.
7. When the candidate is cheaply falsifiable with available repository tools, attempt that falsification before rating `high`. Examples: inspect all relevant call sites; trace the branch and run a narrow test when cheap; read the authoritative schema/type/model; for warehouse SQL, `describe`/`EXPLAIN` via Snowflake MCP (view-only; migrations likely only run in dev); inspect lockfile/resolver or security checks; read workflow selectors and the actual test command; trace trigger to consequence on the concrete path.
8. If neither proven nor disproven, cap confidence at `low`.

Score independently:

- **Confidence**: `high` = concrete trigger + traced execution path + verified practical consequence + attempted falsification using available evidence/tools; `medium` = likely but one material assumption remains, or the defect cannot be fully established; `low` = unconfirmed or disproven.
- **Severity**:
  - `blocker` = the PR introduces, worsens, or newly exposes a concrete failure and merging would materially reduce production correctness, security, availability, data integrity, or required behavior
  - `recommended` = the PR introduces, worsens, or newly exposes a reachable defect, but the verified consequence does not make the merge unsafe
  - `nit` = internal/style only
  - `question` = business intent unresolved; route it to `HUMAN_REVIEW_PROMPTS.md` until the user decides whether the behavior is required in this PR
  - `future_work` = a verified, actionable enhancement beyond the confirmed slice or an unchanged pre-existing defect; it never drives `REQUEST_CHANGES`

Do not rate `high` on a plausible reasoning chain alone.

## Classification examples

| Evidence | Classification | PR effect |
| --- | --- | --- |
| The PR creates or worsens a failure that makes merging unsafe under the blocker definition | `blocker` | May drive `REQUEST_CHANGES` |
| The PR creates or worsens a reachable edge/error-path defect without making the merge unsafe | `recommended` | Non-blocking feedback |
| Confirmed behavior is missing or contradicted | `blocker` or `recommended`, based on verified consequence | Never `future_work` |
| The defect already exists and the PR does not change its reachability, consequence, contract, or affected callers | `future_work` | State explicitly that this PR did not introduce or worsen it |
| The request adds capability beyond the confirmed vertical slice | `future_work` | Describe the later change and why it is outside this PR |
| The evidence does not settle whether behavior belongs in the confirmed slice | `question` | Ask for product intent before classification |
| The concern is style-only with no concrete consequence | `nit` | Excluded unless requested |

A verified pre-existing security-boundary, corruption, tenant-isolation, or data-loss risk remains non-blocking for this PR when unchanged, but call it out prominently as urgent `future_work` and recommend immediate separate remediation. If the PR changes that risk's reachability or consequence, classify the PR-caused effect normally instead.

## Filter

- Apply `../comment-model.md` for what the main agent proposes to the user. Maintainability survivors also need the concrete change-impact path required by `../coding-standards.md`.
- Route unresolved business intent to `HUMAN_REVIEW_PROMPTS.md`, not `COMMENTS.md`.
- Record discarded candidates and the reason in the source artifact so the pass is auditable. Do not discard verified, actionable unchanged defects solely because they pre-date the PR; retain them as `future_work`.
- Main agent independently verifies every surviving finding before presenting it in the walkthrough.

After survivors are verified, start phase 4 immediately.
