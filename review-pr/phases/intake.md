# Phase 1 — Intake

1. Accept a GitHub PR URL/number. If omitted, resume from the review workspace or ask for it.
2. Fetch with `gh`: title, body, author, state, draft status, base/head branches and SHAs, commits, changed files, full diff, review threads/comments, checks, current GitHub user, and that user's submitted reviews.
3. Create the review workspace, `tasks.md`, required artifact stubs, and an `agent_notes.md` containing only durable paths, flows, commands, and invariants.
4. If this user has a submitted review, set `review_scope: incremental` and apply [`follow-up.md`](follow-up.md). Otherwise set `review_scope: full` even if others reviewed. Explicit “full re-review” uses `full`.
5. Initialize `COVERAGE.md` as directed by [`../coverage-protocol.md`](../coverage-protocol.md).
6. From the active diff, identify:
   - core files/sections that make product behavior true or false
   - supporting core sections
   - incidental/generated/mechanical sections
   - change intent in at most three sentences: landed behavior and any differing PR/user expectation
7. Apply [`../red-zone-protocol.md`](../red-zone-protocol.md): discover the repository's red-zone files, match every changed path against their patterns, and record both in `tasks.md` `redzone_files` and `redzone_paths` and in `PR_BRIEF.md`, or `none`.
8. Write `PR_CONTEXT.md` and `PR_BRIEF.md`. Mark incidental coverage only after enough inspection to justify it.
9. Classify and persist review risk, then apply [`../business-claims.md`](../business-claims.md). Start phase 2 as soon as draft claims exist; do not wait.

## Review risk

Classify from the active coverage diff, not the PR description. If unsure use `medium`.

Higher-risk surfaces:

- authentication, authorization, security, or trust boundaries
- persistence, schemas, migrations, or destructive data changes
- concurrency or state coordination
- public APIs, external contracts, or compatibility-sensitive boundaries
- money, billing, permissions, tenant isolation, or sensitive data
- broad cross-module orchestration

Use:

- **low:** docs, copy, isolated styling, lockfile-only, or a small self-contained change without a higher-risk surface
- **medium:** normal product logic or mixed incidental and moderate core changes
- **high:** one or more higher-risk surfaces, especially across modules or trust/data/money boundaries
- **critical:** the diff matches a glob in a red-zone file discovered per [`../red-zone-protocol.md`](../red-zone-protocol.md)

Persist the rating and concrete reasons in `tasks.md` and `PR_BRIEF.md`. On incremental review, classify the update; never lower a stored `high` or `critical`, and raise risk if the update adds a higher-risk surface. Risk controls specialist depth but never skips claims, walkthrough, or submission gates.
