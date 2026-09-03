# Phase 2 — Required specialists

Run both tracks in parallel after `claims_confirmed: true`. They are required sections of every review, though either may record a justified skip when its surface is absent.

## SECURITY specialist

Review gravity-center changes and nearby trust boundaries for:

- hardcoded secrets or credentials
- SQL, command, template, path, XSS, SSRF, deserialization, or unsafe-eval injection
- authentication/authorization bypasses and changed permission boundaries
- sensitive data logging or exposure
- unprotected endpoints, jobs, webhooks, or admin paths
- weakened validation, encryption, rate limiting, tenant isolation, or audit trails
- dependency changes with concrete known or likely risk

Require a concrete exploit/failure path. General hardening advice is not a finding. Use repo-native dependency/security checks before broad external research.

Return candidates with changed path/range, exact quote, trigger, consequence, evidence checked, fix direction, confidence, severity, and claim id where applicable.

The main agent writes `SECURITY.md` with every heading below, even when clean:

```markdown
# Security
## Reviewed files and patterns
## Evidence checked
## Clean areas
## Findings
## Unresolved questions
## Skip reason
```

`Skip reason` is `none` when the scan ran. A skip is allowed only when intake found no security-relevant surface.

## Test coverage specialist

1. Read CI/check results first. Record failing checks and map failures to changed files.
2. Map changed source files and business claims to test files.
3. Inspect whether tests prove:
   - changed conditionals and branches
   - null, empty, min/max, missing-field, permission, and error edges
   - assertion specificity (not merely execution)
   - bug-fix regression behavior
   - each material business claim and invariant
4. Passing CI is evidence, not proof. Do not invent unstated product rules to demand tests.
5. Run targeted local tests only when useful and cheap. Ask before expensive/full suites.

Return candidates with changed path/range, exact quote, uncovered claim/branch, concrete failure that could escape, existing evidence, fix direction, confidence, and severity.

When the main agent presents test coverage in chat, summarize tests in prose. Never paste test source into chat.

The main agent writes `TESTS.md` with every heading below, even when clean:

```markdown
# Test coverage
## CI/check summary
## Failure triage
## Source-to-test and claim map
## Uncovered changed branches
## Weak assertions
## Edge-case and regression gaps
## Local commands and results
## Residual risk
## Skip reason
```

`Skip reason` is `none` when the pass ran. A skip is allowed only when CI is green and there are no changed test files or claim-relevant branches.

## Completion gate

Do not continue until both `SECURITY.md` and `TESTS.md` exist with all required headings. Main agent verifies candidate evidence and updates coverage for inspected lines; specialist output alone does not authorize a comment.
