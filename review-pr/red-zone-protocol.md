# Red zones

A red zone is a path whose changes get mandatory extra depth and exposure, however small the diff looks. Red zones carry knowledge the diff does not show, so a human declares them. The review never infers one: a danger visible in the code is already covered by the risk surfaces in [`phases/intake.md`](phases/intake.md).

This file is the protocol. The paths live in the repository under review.

## Discovery

At intake, find every tracked file named `redzones.md` at `base_sha`:

```bash
git ls-tree -r --name-only <base_sha> | grep -E '(^|/)redzones\.md$'
```

Read them at `base_sha`, never at `head_sha`. The file lives in the repository under review, so reading the head version would let a PR retire its own red zone. A diff that modifies a red-zone file is a finding, not a silent reload.

Patterns resolve relative to the containing file's directory, so a repository-root file covers everything and a package-level file scopes to that package.

Record what discovery found in `tasks.md` `redzone_files`, or `none`, whether or not anything later matches. Report the outcome in the walkthrough either way: the files applied and their matches, or that no red-zone file exists. A guardrail that reports nothing cannot be shown to have run.

## File format

Glob patterns with reasons. The reason is required; the walkthrough prints it beside the flag, so write what breaks and why the diff does not reveal it.

```markdown
| pattern | why |
| --- | --- |
| `src/billing/guard.py` | <what breaks> |
| `**/migrations/**` | <what breaks> |
```

## Required handling

When the active diff matches a pattern:

1. Intake sets `review_risk: critical`, names the matched path in `review_risk_reasons`, and records the matches in `tasks.md` `redzone_paths` and in `PR_BRIEF.md`. Never lower that risk later in the review.
2. Every changed section in a matched path is shown in the walkthrough as a fenced `diff` hunk, finding or not. `agent_reviewed_not_shown` is not available for those rows.
3. The walkthrough flags the path in the changed-path tree and asks the user to acknowledge the change before the submit gate.
4. A changed red-zone section with no covering test is recorded in `TESTS.md`, written to `HUMAN_REVIEW_PROMPTS.md`, and raised in the walkthrough as an unresolved prompt.

A red zone is not itself a finding. It sets depth and exposure; the finding bar in [`phases/skeptic.md`](phases/skeptic.md) still applies.
