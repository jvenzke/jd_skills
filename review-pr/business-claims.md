# Business claims

Write `BUSINESS_CLAIMS.md` during intake. Draft the fewest claims that cover **what the implementation did**, print all of them in chat, and start phase-2 review (risk-adaptive specialists or integrated review) while the user confirms they match expected results or edits them. The logic walkthrough remains blocked until confirmation.

On an `incremental` follow-up, keep confirmed claims that still match the update’s behavior. Print a one-line reminder; do not re-open the claims gate unless the update adds, drops, or silently changes business logic or an existing flow (confirm only those deltas).

```markdown
---
head_sha: <sha>
status: draft | confirmed
---

# Business claims

What was done (3 sentences, inferred from the diff; note PR/user expected results when they differ):

1.
2.
3.

| id | claim (testable) | source | implementing sections | status |
| --- | --- | --- | --- | --- |
| C1 | | diff / pr / user | | draft, confirmed, or gap |

## Gaps

Questions the user must answer before review continues (including expected vs done mismatches). Empty if claims are confirmed.

## Non-goals / out of scope

Quoted from the PR or user, or inferred as unchanged when the diff clearly does not touch them. Do not invent unrelated non-goals.
```

Rules:

- Use as few claims as possible to cover what the implementation did. Prefer one claim. Add another only when it is an independently testable product assertion (different actor, trigger, result, or must-not) that would be judged separately if it failed. Do not split a single feature into several claims, pad toward a count, or invent claims to occupy leftover diff sections. A claim is a product assertion you could be wrong about (who, when, what data, what must not happen). "Code compiles" is not a claim.
- Infer claims from the implementation (diff vs `base_sha`) so they describe what actually landed. Use the PR body and the user as expected results. The claims gate is where the user confirms that what was done matches what they expected. Do not search Jira.
- Every silent change to business logic or an existing flow must appear as a drafted claim (source `diff`) so the user can accept, rewrite, or reject it. That includes must-nots: no unintended feature regression, and no workaround around existing guardrails (validation, permissions, flags, invariants). Pure refactors, formatting, generated files, and comments that preserve behavior stay supporting or incidental and do not get their own claims.
- If the PR/user expected results and the implementation disagree, draft the claim as what the code did, call out the mismatch in Gaps, and wait. Do not hide the implementation behind the PR description.
- Status `gap` means the change cannot be judged yet. Ask before walking that code. An unconfirmed silent change to business logic, an existing flow, or a guardrail stays a gap and stays eligible as a blocker until the user confirms it is intended. Confirmed claims can drop a “unexpected change” finding; they do not skip walking the path.
- Claims describe observable behavior of this PR; they are not an inventory of diff sections. Attach only the core implementing sections that can make each claim true or false.
- Classify remaining changes as supporting core code, incidental changes, or unexplained coverage. Do not create another claim merely to map a leftover section. Unclear behavior becomes a human prompt.
