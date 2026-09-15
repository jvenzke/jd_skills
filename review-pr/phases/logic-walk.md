# Phase 4 — Intent-complete logic walkthrough

Run after adversarial verification, against current (usually draft) claims. Walk all applicable claims in one turn, ordered by risk and dependency:

1. contracts, schemas, migrations, interfaces
2. domain/service logic
3. APIs, controllers, jobs, events
4. persistence and integrations
5. UI/state flows
6. tests proving behavior (prose only)

If incremental, apply [`follow-up.md`](follow-up.md): walk update-affected claims and still-open/reintroduced items, show update diffs only, note unchanged claims as already reviewed, and include prior-comment statuses before new comments.

Do not ask the user to select slices. Split only if requested or if more than about four core files plus comment ranges would be unreadable; explain the split and end with Next actions for the remaining walk.

## Walkthrough

Before walking claims, print:

1. At most four bullets covering core change, landed vs expected behavior, risk/reasons, CI state, and section totals.
2. A nested tree of every changed path with `+adds` / `-deletes` per file and directory subtotal. Include generated files and lockfiles.

For incremental review, describe only the update: commits/files, risk delta, claim delta, and prior-comment counts. Use update numstat and add a one-line full-PR totals reminder.

Do not dump a separate claims list; each walked claim prints its id and exact text. Present gaps and expected-vs-landed mismatches as unresolved prompts in this turn. Do not require the user to open `BUSINESS_CLAIMS.md`.

For every walked claim, print its id and exact text, then:

- traced implementation path: files, symbols, callers, and flow
- supporting evidence and tests; summarize test setup, assertions, and covered branch without pasting test source
- material architecture/boundary changes
- other readers/writers of the same business data and whether responsibility is consolidated
- residual uncertainty
- surviving findings

Compare the traced path, callers, tests, specialist evidence, and local patterns against the claim. For high risk—or medium risk that reshapes a public/module boundary—add **Boundary decisions** describing the changed boundary, why it matters, and residual risk.

Show only the product `@@` hunks that need human judgment as unified diffs from `git diff <coverage_base>...<head_sha> -- <path>` (`coverage_base` is `base_sha`, or `prior_review_head_sha` when incremental):

- a proposed finding (inside that numbered comment; [`comment-model.md`](../comment-model.md))
- a material public/module boundary
- ambiguous intent
- a user-requested expansion
- a design decision the traced path cannot settle

Include removed lines and at most five context lines. Do not dump the PR or file diff, and do not use Cursor path citations (they hide deletions). Source the diff from the stored SHAs, not a dirty tree. If a hunk is unreadable, split the walk or summarize mechanical parts. Do not paste large spans to increase presentation counts. Summarize tests unless the user asks for a test diff.

Reprint **Test coverage of new code** and **CI workflow scope** from `TESTS.md`; do not recompute them. Summarize remaining inspected core sections and their disposition.

Present all surviving findings as one numbered list. For each show path/range, the comment-model chat snippet, severity, confidence, concise local rationale, and the exact GitHub body. Apply [`../comment-model.md`](../comment-model.md); do not restate its template or eligibility rules here.

Present unresolved product intent as questions and record it in `HUMAN_REVIEW_PROMPTS.md`. Apply [`../coverage-protocol.md`](../coverage-protocol.md), print its footer and Human oversight, then end with **Next actions**.

Apply [`../business-claims.md`](../business-claims.md) for Intent confirm/edit/add. After a retrigger, re-present affected walks and changed findings; unchanged walks stay already presented. Re-ask Intent.

After the user resolves every action, record decisions in `COMMENTS.md`, `HUMAN_REVIEW_PROMPTS.md`, `LOGIC_WALKTHROUGH.md`, `COVERAGE.md`, and `tasks.md`, then begin phase 5. Re-ask only missing decisions.

## Next actions

Include only decisions needed this turn:

- **Intent** (always): confirm the shown implementation matches all claims, or edit/add claims (retriggers as above). For incremental review, refer to the update and affected claims.
- **Boundary decisions:** include only when that block was shown.
- **Each proposed comment:** approve, reject, or edit.
- **Each unresolved prompt:** answer or leave unresolved.
- **Additional** (always): other inline comments or product questions.

Do not ask for the review type. Number items contiguously. Each item names the decision, gives **Recommended:** and alternatives, then the block ends with a paste-ready example using actual recommendations.

```markdown
## Next actions
Needed to start the submit gate (review type comes later). Reply by number or shorthand.

1. Intent — confirm the shown implementation matches all claims, or edit/add them.
   Recommended: **confirm** · other: **edit** (what to change) · **add** (new claim)
2. Comment 1 — approve, reject, or edit.
   Recommended: **approve** · other: **reject** · **edit**
3. Additional comments or product questions?
   Recommended: **none** · other: provide the comment or question

Example reply (recommended):
1. confirm
2. approve
3. none
```

Omit optional rows that do not apply and keep the example numbering aligned.

## Output lanes

- Actionable anchored issue → `COMMENTS.md`
- Unclear business behavior → `HUMAN_REVIEW_PROMPTS.md`
- Concrete work beyond this PR → `future_work`
- Missing required migration/deploy-order note → `blocker`
- Clean code → coverage disposition; do not manufacture feedback
