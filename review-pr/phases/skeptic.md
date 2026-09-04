# Phase 3 — Adversarial verification

The main agent deduplicates specialist (and integrated-review) candidates by defect (same mechanism, overlapping lines) without judging them, then dispatches a fresh read-only skeptic for each candidate or a small related batch.

## Skeptic contract

The skeptic's job is to disprove findings, not confirm them.

For every candidate:

1. Re-read the actual diff and necessary surrounding code; never score from the candidate summary alone.
2. Confirm path, changed hunks, and exact quote at `head_sha`. Missing/mismatched evidence → confidence `0`.
3. Scope: a finding is in scope when the PR introduces, alters, or newly exposes/makes reachable the failure. A pre-existing defect is out of scope only when the PR does not materially change its reachability, consequence, contract, or affected callers. Do not drop a PR-introduced failure because part of the root cause existed before the PR. Out of scope → confidence `0`.
4. State the concrete trigger/input/state, traced execution path, and practical consequence.
5. For business findings, cite the confirmed claim. For project guidance and maintainability, cite `review-pr/coding-standards.md` and repo patterns at `base_sha`, not guidance introduced by the PR. A maintainability candidate must show how future change gets harder (leaked complexity, shallow boundary, complexity not pushed downward, or misplaced responsibility) — not merely that a different structure would be nicer.
6. Try to identify guards, callers, validation, tests, or invariants that make the proposed failure impossible.
7. When the candidate is cheaply falsifiable with available repository tools, attempt that falsification before rating `high`. Examples: inspect all relevant call sites; trace the branch and run a narrow test when cheap; read the authoritative schema/type/model; inspect lockfile/resolver or security checks; read workflow selectors and the actual test command; trace trigger to consequence on the concrete path.
8. If neither proven nor disproven, cap confidence at `low`.

Score independently:

- **Confidence**: `high` = concrete trigger + traced execution path + verified practical consequence + attempted falsification using available evidence/tools; `medium` = likely but one material assumption remains, or the defect cannot be fully established; `low` = unconfirmed or disproven.
- **Severity**: `blocker` = data/security boundary loss, crash, corruption, or normal flow broken; `recommended` = reachable edge/error-path defect; `nit` = internal/style only; `question` = business intent unresolved.

Do not rate `high` on a plausible reasoning chain alone.

## Filter

- Keep only `high` confidence `blocker` or `recommended` findings by default. Maintainability survivors need a concrete change-impact path, not style preference.
- Include `nit` only if the user explicitly requested small findings.
- Route unresolved business intent to `HUMAN_REVIEW_PROMPTS.md`, not `COMMENTS.md`.
- Record discarded candidates and the reason in the source artifact so the pass is auditable.
- Main agent independently verifies every surviving finding before presenting it in the walkthrough.
