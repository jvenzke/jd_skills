# Phase 2 — Required specialists

Run both tracks in parallel as soon as the 1–3 draft claims are printed in chat. They may work while the user confirms or edits those claims. They are required sections of every review, though either may record a justified skip when its surface is absent.

## SECURITY specialist

Review core changes and nearby trust boundaries for:

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
2. Identify the project, package, or module this PR belongs to. Read the GitHub workflow files that run on this PR (typically `.github/workflows/*`). Confirm those jobs actually execute the tests that cover that project and its claim-relevant dependents—not a subset skipped by path filters, `if` conditions, a different package selector, or an unrelated job. A workflow that is green because it never ran this project's tests is a finding (changed workflow path/range when the filter lives in the PR; otherwise record it under CI workflow scope and residual risk).
3. Map changed source files and business claims to test files.
4. For **new and changed product code**, record which tests cover it (file, scenario, assertions, claim/branch) and which new ranges, branches, or claims have no covering test.
5. Inspect whether tests prove:
   - changed conditionals and branches
   - null, empty, min/max, missing-field, permission, and error edges
   - assertion specificity (not merely execution)
   - bug-fix regression behavior
   - each material business claim and invariant
6. Passing CI is evidence, not proof. Do not invent unstated product rules to demand tests.
7. Run targeted local tests only when useful and cheap. Ask before expensive/full suites.

Return candidates with changed path/range, exact quote, uncovered claim/branch, concrete failure that could escape, existing evidence, fix direction, confidence, and severity. Include CI-scope misses (relevant tests not invoked by the PR's workflows) the same way.

When the main agent presents test coverage in chat, summarize tests in prose. Never paste test source into chat. After `TESTS.md` is written, print a **Test coverage of new code** block in chat (covering tests vs gaps for new/changed product code) and a **CI workflow scope** block (whether GitHub Actions runs this project's impacting tests). Repeat both in the logic walkthrough. They also go in the GitHub review body at submit.

The main agent writes `TESTS.md` with every heading below, even when clean:

```markdown
# Test coverage
## CI/check summary
## CI workflow scope
## Failure triage
## Source-to-test and claim map
## New-code coverage
## Uncovered changed branches
## Weak assertions
## Edge-case and regression gaps
## Local commands and results
## Residual risk
## Skip reason
```

`CI workflow scope` names the workflows/jobs, the test commands or selectors they run, and whether they include this PR's project. `New-code coverage` maps each new/changed product behavior or claim to covering tests in prose, then lists uncovered new code.

`Skip reason` is `none` when the pass ran. A skip is allowed only when CI is green, the PR's workflows already run this project's impacting tests, and there are no changed test files or claim-relevant branches. Always fill `CI workflow scope` and `New-code coverage` (`n/a` plus the skip reason if the rest of the pass is skipped).

## Completion gate

Do not begin adversarial verification until both `SECURITY.md` and `TESTS.md` exist with all required headings. Do not begin the logic walkthrough until the claims are also confirmed. If a claim edit materially changes specialist scope, rerun only the affected track; otherwise remap its evidence. Main agent verifies candidate evidence and updates coverage for inspected lines; specialist output alone does not authorize a comment.
