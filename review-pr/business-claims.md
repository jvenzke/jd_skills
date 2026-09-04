# Business claims

Write `BUSINESS_CLAIMS.md` during intake. Draft 1–3 claims, print all of them in chat, and start phase-2 review (risk-adaptive specialists or integrated review) while the user confirms or edits them. The logic walkthrough remains blocked until confirmation.

```markdown
---
head_sha: <sha>
status: draft | confirmed
---

# Business claims

Intent (3 sentences, from PR or user, not inferred from the diff):

1.
2.
3.

| id | claim (testable) | source | implementing hunks | status |
| --- | --- | --- | --- | --- |
| C1 | | pr / user | | draft, confirmed, or gap |

## Gaps

Questions the user must answer before review continues. Empty if claims are confirmed.

## Non-goals / out of scope

Quoted from the PR or user. Do not invent.
```

Rules:

- Use 1–3 claims for the PR. A claim is a product assertion you could be wrong about (who, when, what data, what must not happen). "Code compiles" is not a claim.
- Source every claim from the PR or user. Do not search Jira. If the PR body has no acceptance criteria, do not invent them from the diff. Ask.
- Status `gap` means the change cannot be judged yet. Ask before walking that code.
- Claims describe product intent; they are not an inventory of diff hunks. Attach only the core implementing hunks that can make each claim true or false.
- Classify remaining changes as supporting core code, incidental changes, or unexplained coverage. Do not create another claim merely to map a leftover hunk. Unclear behavior becomes a human prompt.
