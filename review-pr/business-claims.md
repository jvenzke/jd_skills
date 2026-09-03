# Business claims

Write `BUSINESS_CLAIMS.md` during intake. Specialists and the logic walk do not start until the user confirms the claims or answers the blocking questions.

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

| id | claim (testable) | source | gravity files | status |
| --- | --- | --- | --- | --- |
| C1 | | pr / user | | assumed, confirmed, or gap |

## Gaps

Questions the user must answer before review continues. Empty if claims are confirmed.

## Non-goals / out of scope

Quoted from the PR or user. Do not invent.
```

Rules:

- A claim is a product assertion you could be wrong about (who, when, what data, what must not happen). "Code compiles" is not a claim.
- Source every claim from the PR or user. Do not search Jira. If the PR body has no acceptance criteria, do not invent them from the diff. Ask.
- Status `gap` means the change cannot be judged yet. Ask before walking that code.
- After confirmation, map each gravity-center hunk to a claim id. Unmapped behavior is a prompt, not a silent pass.
