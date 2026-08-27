# Phase 3 — Adversarial verification

The main agent deduplicates specialist candidates by defect (same mechanism, overlapping lines) without judging them, then dispatches a fresh read-only skeptic for each candidate or a small related batch.

## Skeptic contract

The skeptic's job is to disprove findings, not confirm them.

For every candidate:

1. Re-read the actual diff and necessary surrounding code; never score from the candidate summary alone.
2. Confirm path, changed lines, and exact quote at `head_sha`. Missing/mismatched evidence → confidence `0`.
3. Confirm the defect is introduced or altered by the PR. Pre-existing root cause → confidence `0`.
4. State the concrete trigger/input/state, execution path, and practical consequence.
5. For business findings, cite the confirmed claim. For project guidance, cite policy at `base_sha`, not guidance introduced by the PR.
6. Try to identify guards, callers, validation, tests, or invariants that make the proposed failure impossible.
7. If neither proven nor disproven, cap confidence at `low`.

Score independently:

- **Confidence**: `high` = verified trigger and consequence; `medium` = likely but one material assumption remains; `low` = unconfirmed or disproven.
- **Severity**: `blocker` = data/security boundary loss, crash, corruption, or normal flow broken; `recommended` = reachable edge/error-path defect; `nit` = internal/style only; `question` = business intent unresolved.

## Filter

- Keep only `high` confidence `blocker` or `recommended` findings by default.
- Include `nit` only if the user explicitly requested small findings.
- Route unresolved business intent to `HUMAN_REVIEW_PROMPTS.md`, not `COMMENTS.md`.
- Record discarded candidates and the reason in the source artifact so the pass is auditable.
- Main agent independently verifies every surviving finding before staging it.
