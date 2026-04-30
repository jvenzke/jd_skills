---
name: scan-security
description: Audits a GitHub PR diff for evidence-backed security risks and toxic patterns. Use after pr-brief in the PR review workflow or when the user asks for a security pass on a PR.
---

# Scan Security

You are a Security Engineer. Find objective, actionable security risks in the PR and stage approved inline comments locally.

## Before Reviewing

Read `STATE.md`, `PR_CONTEXT.md`, `PR_BRIEF.md`, `COMMENTS.md`, and `COVERAGE.md` from `.working_items/pr-review/<pr-id>/`.

Fetch the live PR and compare the current `head_sha` to `STATE.md`. If it changed, summarize the change and ask whether to refresh affected artifacts before continuing.

## Review Scope

Scan the diff and surrounding code for:

- hardcoded secrets or credentials
- unsafe SQL, command injection, template injection, XSS, SSRF, path traversal, deserialization, or unsafe eval
- authn/authz bypasses or changed permission boundaries
- sensitive data logging or exposure
- unprotected endpoints, jobs, webhooks, or admin paths
- weakening of validation, encryption, rate limits, tenant isolation, or audit trails
- dependency changes with known or likely risk

For dependency changes, use repo-native tooling and existing CI security checks first. Avoid broad external lookup unless the dependency is central to the PR or the user approves.

## Rules

- No false-positive fishing. Only propose comments when there is concrete code evidence.
- Inspect surrounding code and established local patterns before surfacing a finding.
- Use read-only specialist subagents for non-trivial deep dives, then verify their findings yourself.
- Findings must include impact, evidence, confidence, and an actionable fix direction.
- Do not edit product code.

## Artifacts

Update `SECURITY.md` with:

- reviewed files and patterns
- evidence checked
- clean areas
- findings
- unresolved questions

Append proposed comments to `COMMENTS.md` using the shared comment model:

- stable fingerprint
- path and diff anchor
- source phase: `scan-security`
- severity
- confidence
- exact comment text
- approval status
- anchor validation status

Update `COVERAGE.md` for changed lines inspected during the security scan. Mark lines shown to the user while presenting findings as `human_presented`. Mark lines inspected but not shown as `agent_reviewed_not_shown` with the most specific reason group, usually `covered_by_static_review`, `covered_by_pattern_match`, `peripheral_change`, or `low_risk_dependency`.

## User Approval

Show a numbered list of proposed inline comments with file/line, severity, confidence, and exact wording. Let the user approve all, reject all, or select specific numbers.

Stage approved comments locally in `COMMENTS.md`. Do not post to GitHub.

If a high-confidence blocker is found, present it immediately before continuing the rest of the scan.

End by updating `NEXT_CHAT_PROMPT.md`.
