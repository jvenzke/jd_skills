# Business claims

Write `BUSINESS_CLAIMS.md` during intake. Claims describe what the diff actually implemented; PR text and the user describe expected results. Phases 2–3 review draft claims. The walkthrough presents claims and asks whether landed behavior matches expectations.

On incremental review, preserve unchanged confirmed claims. Walk added, removed, or materially changed behavior as new or changed claims.

```markdown
---
head_sha: <sha>
status: draft | confirmed
---

# Business claims

## What was done
<product-language bullets from the diff: actor, situation, result, must-not; note differing PR/user expectations. The walkthrough turns these into 2–4 product-named opener `###` headings plus optional Residual. Table cells stay one testable sentence.>

| id | claim (testable) | source | implementing sections | status |
| --- | --- | --- | --- | --- |
| C1 | | diff / pr / user | | draft, confirmed, or gap |

## Gaps
<blocking questions or expected-vs-landed mismatches>

## Non-goals / out of scope
<quoted from PR/user, or clearly unchanged; do not invent>
```

## Rules

- Use the fewest independently testable product assertions—often one. Each claim states actor, trigger/state, observable result, and important invariant or must-not.
- Infer claims from the diff against `base_sha`. Include every silent change to business logic, an existing flow, or a guardrail. Do not hide landed behavior behind the PR description.
- Use separate claims only when behavior could be judged independently. Pure refactors, formatting, generated files, and behavior-preserving support code are not claims.
- Attach only sections that can make a claim true or false. Classify the rest as supporting core, incidental, or unexplained coverage.
- When expected and landed behavior differ, describe landed behavior, record the mismatch under Gaps, and ask the user. `gap` remains potentially blocking until resolved.
- Ask only questions that materially affect judgment and cannot be answered from code. Never search Jira.
- Start specialists once drafts exist. On walkthrough edit/add, set `claims_confirmed: false`; if scope changes materially, rerun only affected specialist and skeptic tracks; otherwise remap evidence.
- After Intent **confirm**, set artifact status and `tasks.md claims_confirmed: true`. Confirmation removes “unexpected change” as a finding; it does not authorize GitHub writes.
