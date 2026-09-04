# Phase 2 — Required specialists

Always write `SECURITY.md`, `TESTS.md`, and `QUALITY.md` with every required heading before adversarial verification. Depth follows `review_risk` on `tasks.md` (and `PR_BRIEF.md`). A written skip is allowed when the surface is absent **or** when low-risk dispatch does not invoke that specialist.

Start the tracks that this risk class requires as soon as the 1–3 draft claims are printed in chat. They may work while the user confirms or edits those claims.

## Risk dispatch

Read stored `review_risk`. Do not reclassify unless `head_sha` changed and the summary of that update shows a new higher-risk surface (then raise, persist, and follow the new class).

### low

Main agent performs integrated logic/quality review and relevant CI/test verification (fill `QUALITY.md` and `TESTS.md`).

Launch a specialist only when intake’s changed surface triggers that track:

- SECURITY: auth, trust, secrets, injection, permissions, tenant isolation, sensitive data, or risky dependencies
- TESTS: changed tests, failing checks, claim-relevant branches, or workflow/path-filter doubt
- LOGIC_QUALITY: non-trivial product logic (not docs/copy/isolated styling/lockfile)

If a track is not triggered, still write its artifact with `Skip reason` stating low-risk + absent surface. `Skip reason` is `none` when that scan ran.

Skeptic (phase 3) still runs on whatever candidates exist, including integrated-review findings.

### medium

Launch **SECURITY**, **test coverage**, and **LOGIC_QUALITY** in parallel (today’s default). Skip a track only when its surface is absent under that specialist’s skip rule below.

### high

Same parallel specialists as medium, plus:

- cheaper extra evidence: inspect authoritative schema/type/model definitions, lockfiles/resolvers, workflow selectors, and relevant call sites for any candidate that needs them
- run a narrow local test or command when it is cheap and would falsify a suspected path
- note material architecture/public/module boundary changes for the walkthrough **Boundary decisions** block (no extra approval gate)

Do not skip high-risk tracks to save time.

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

`Skip reason` is `none` when the scan ran. A skip is allowed when intake found no security-relevant surface, or when low-risk dispatch did not trigger SECURITY.

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
6. Passing CI is evidence, not proof. Do not invent unstated product rules to demand tests. Prefer high-signal contract tests over test volume; do not demand extra cases merely to perform a red/green loop.
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

`Skip reason` is `none` when the pass ran. A skip is allowed when CI is green, the PR's workflows already run this project's impacting tests, and there are no changed test files or claim-relevant branches; or when low-risk dispatch did not trigger TESTS. Always fill `CI workflow scope` and `New-code coverage` (`n/a` plus the skip reason if the rest of the pass is skipped).

## LOGIC_QUALITY specialist

Review core product changes for claim-aligned correctness **and** long-term maintainability. Read `../coding-standards.md` before inspecting code. Do not review tests for coverage (TESTS owns that) or invent product rules the claims do not state.

Correctness:

- wrong branches, inverted conditions, off-by-one, and missed error/empty paths in changed logic
- invariants that the implementation does not actually preserve
- callers, persistence, or UI that contradict a claim
- control-flow or state updates that make a claim false under a concrete trigger

Maintainability (coding-standards.md; same bar as `/d-antigravity`; goal is easier future change, not a small diff):

- leaked complexity: callers coordinate internal steps, policy, representation, or special cases
- shallow boundaries: wrappers, pass-throughs, fragmented helpers, or interfaces that mirror internals
- complexity not pushed downward: invariants, sequencing, policy, or errors handled in callers instead of the owning module
- misplaced responsibility: invariants or orchestration split across modules, or organized by execution order instead of knowledge
- invalid states or special cases left exposed instead of eliminated behind the boundary
- hard-to-describe or awkwardly coordinated new/reshaped boundaries
- comments that restate obvious code; missing comments only where a non-obvious invariant or rationale is required
- unrelated cleanup or speculative generalization (not a finding to *demand* extra refactor; a finding if the PR itself adds drive-by noise or unjustified new abstractions)

Require a concrete trigger, execution or change-impact path, consequence, and fix direction. Naming, formatting, and local style are not findings unless the user asked for nits.

Severity: `blocker` only if the defect or smell creates a concrete correctness or security failure. `recommended` for reachable logic defects and for clear boundary/complexity regressions that will make the codebase harder to maintain. `nit` for local style.

Return candidates with changed path/range, exact quote, trigger, consequence, evidence checked, fix direction, confidence, severity, and claim id where applicable. Tag each candidate `correctness` or `maintainability`.

The main agent writes `QUALITY.md` with every heading below, even when clean:

```markdown
# Logic and quality
## Reviewed files and patterns
## Evidence checked
## Correctness
## Maintainability
## Clean areas
## Findings
## Unresolved questions
## Skip reason
```

`Skip reason` is `none` when the scan ran. A skip is allowed when intake found no core product-code change (docs/config-only, generated/lockfile, or incidental-only), or when low-risk dispatch did not trigger LOGIC_QUALITY. Always fill `Correctness` and `Maintainability` (`n/a` plus the skip reason if skipped).

## Completion gate

Do not begin adversarial verification until `SECURITY.md`, `TESTS.md`, and `QUALITY.md` exist with all required headings. Do not begin the logic walkthrough until the claims are also confirmed. If a claim edit materially changes specialist scope, rerun only the affected track; otherwise remap its evidence. Main agent verifies candidate evidence and updates coverage for inspected hunks; specialist output alone does not authorize a comment.
