# Off-path risks

Failures that a green CI run and a normal dev run do not reach, because they live on paths steady
state never takes. Apply to every change that records a value for later use, derives a metric
across time, compares two row sets, snapshots state, post-processes an output, or changes what a
shared table or payload holds. The same checks work as an author's self-review before opening a PR.

For each item: name the concrete path, then settle it with the code plus one cheap piece of
evidence (a narrow test, a prod query that counts how often the path occurs, a schema read, a
run-history read). A path that nothing can reach is not a finding; a path that occurs in real data
is.

Review against inputs, not intent. Reading a change to confirm it does what the author meant finds
little; asking which input makes it pass wrongly or fail wrongly finds these. Before trusting a
test suite, check that its fixtures include the off-path shapes below. Tests written from the
author's mental model use the steady-state shape and confirm the design instead of testing it.

## Time and state

### 1. Provenance: was the recorded value the one in effect?

A value written at one time and later read as describing an interval is only right if every
writer path produces it with the same meaning.

- List every path that writes the row: the normal run, catch-up after a missed run, restatement,
  backfill, a rerun of the same interval, the first run after deploy, and any guard that can
  cancel the effect after the value is written (a late-apply check, a partial failure).
- For each, ask whether the surviving row describes what actually took effect. Recorded is not
  applied when a gate sits between computing a decision and enacting it.
- Ask whether the consumer aligns the value to the interval it governed, not the interval it is
  labelled with. Effects that start partway through an interval need an effective time.
- Settle with a prod query comparing each row's label time to its write time, and against the
  table that records the effect itself.

*Example:* reward rows carried a floor for every hour a run processed, but settings were applied
only for the run's own hour. 304 of 14,566 test-hours in 28 days were written by a catch-up run
that applied nothing, so their floors never governed any traffic.

### 2. Rows that change after they are written

Status flags, acknowledgements, restatements, soft deletes and backfilled columns mean a row read
today is not the row that existed when the event under review happened.

- For every table read as evidence of past behaviour, ask whether anything updates its rows after
  insert. If so, read it as of the moment that matters, and check that history retention covers
  the window the code needs.
- Describe "what a run did" as a delta between two instants (inserted or changed between start and
  end), not as a creation-time filter. A creation-time filter misses updates to older rows and
  picks up updates made later.

*Example:* expected alerts were rows created in the replayed hour, read from the live table. A
later daily summary had acknowledged them (two tests: unacknowledged at 13:59,
acknowledged at capture time), so a faithful replay failed.

### 3. One instant standing for a job that runs over minutes

Code that snapshots state "as of the run" picks a single instant for a job whose reads and writes
are spread over its duration.

- List what the job writes before the chosen instant. State read at that instant already contains
  those writes, so it is output, not input.
- List what the job reads after it, and whether its inputs were still arriving then. If inputs
  changed during the job, no single instant matches every read.
- Settle by measuring the inputs at the job's start and end. Unchanged means any instant works;
  changed means refuse, or split the instants (state at start, inputs at the read point).
- Take start and end from the job's own run record where one exists. A fixed offset is an
  estimate that drifts on the days it matters.

*Example:* a fixture was read 45% into a ten-minute task, after the task had rewritten the restate
hour about three minutes in. Source loads landed inside the task in 4 of 12 consecutive hours.

### 4. Order and concurrency of producers

- When a test or replay runs steps one after another, check how production runs them. Siblings
  that start together in production can each see or miss the others' writes; run in sequence,
  they always see them.
- For each consumer, write down which sibling writes it can observe in production, and whether the
  test gives it the same view.

*Example:* evaluation, alerting and the bandit started in the same second after the ETL, so
production alerting could read the eval table before or after that run's evaluation.

## Derived values

### 5. Recorded versus enacted

When code records an intermediate (a floor, a threshold, a plan) next to an output that is later
normalised, clamped, reconciled or dropped, the recorded value must reflect that post-processing.

- Find every step after the recording point that changes the output: normalisation, clamping,
  reconciliation against a budget, a guard that discards the result.
- Build the input where each step binds: oversubscribed, unfunded, zero, empty, all-at-floor.
- State the property the pair must satisfy (recorded ≤ enacted, recorded == enacted when binding)
  and test it across the parameter space rather than at one point.

*Example:* inactive floors that could not be funded were normalised from 0.1 to 0.0833 in the
allocation but recorded as 0.1.

### 6. Both sides of an adjustment or a comparison

Two things built to be read together must be built the same way: the numerator and denominator of
an adjusted metric, or the expected and actual sides of a regression check, replay, reconciliation
or before/after diff.

- For an adjustment, any cap, clamp or filter on one side must apply to the other. Write down the
  bounds the adjusted metric must keep (a ratio ≤ 1, adjusted == unadjusted when the adjustment is
  zero) and check them by query on real output, not by reading a table.
- For a comparison, write each side as one sentence: "rows that <predicate>, as of <instant>, for
  <scope>, keeping <which duplicates>". Put the two sentences side by side; any difference is a
  candidate finding. The usual mismatches: one side live and the other as of a moment, rows
  created in a window against rows changed in it, one side narrowed and the other not, one side
  deduplicated and the other not.
- For each comparator, name one input that makes it pass when it should fail and one that makes it
  fail when it should pass. Both become tests.

*Examples:* removed traffic was capped at what an arm received, but the benchmark shrank by the
full nominal floor; adjusted optimality came out above 1 on five tests. Expected alerts held rows
created in the hour while actual alerts held every row the replay changed; the replay's daily
summary acknowledged 83 older warnings the expected side never held.

## Keys, scope and inputs

### 7. Missing and duplicate keys

- Check every comparison against a value that can be missing. In pandas `x != NaN` is true for
  every x, so a filter against a missing key silently keeps everything.
- For every join and group, decide what happens to a group with no match: include, exclude, or
  mark unknown. The decision should be in the code, not an accident of the operator.
- Find every place that treats a key as unique: an index followed by scalar access, a dict keyed
  by id, a join expected to be one-to-one, a `MERGE` that assumes one source row per key. Query
  production for duplicates on that key over a week, and list the writer paths that create them:
  catch-up runs with overlapping windows, retries, two concurrent writers, restatements that
  append instead of replace.
- Where duplicates are legitimate, the code needs an explicit rule (latest by insert time, sum,
  refuse) that matches what downstream readers do.

*Examples:* an hour with traffic but no winning arm compared every arm unequal to NaN and removed
every floor. A compare indexed eval rows by (test, hour) and read cells with `.at`; a run that
evaluated two missing hours wrote each hour twice, 4,515 rows for 1,533 keys, in four runs of one
day.

### 8. Side effects wider than the declared scope

An operation narrowed to a subset (some tests, tenants, dates) can contain a step that acts
globally: acknowledge every open warning, truncate a table, refresh a shared cache.

- Find the global steps inside scoped operations. Check that every output and every comparison is
  narrowed the same way, including the "everything" case where no subset list is passed but the
  input was still a subset.
- Construct the case with an out-of-scope row present and assert it lands on neither side.

*Example:* a replay narrowed to one test, and later a full replay of a capture that excluded
another test, both reported other tests' acknowledged warnings as extra output.

### 9. Inputs taken from elsewhere: copied settings and fallbacks

- When code merges parameters from another source (a captured production config, a user payload,
  a parent job) onto its own, the keys that route (database, schema, environment), authenticate or
  pin time stay reserved. Copy only keys the code does not set itself. Rate reach by what the
  source holds today, but keep the finding when one config edit reaches it.
- For every lookup that can come back empty (an API that can fail, history past retention, a row
  not there yet), read what the code does instead. A default or estimate produces plausible output
  that is wrong on exactly the days it is used. Prefer refusing with a message that names the
  missing input; if a fallback stays, record which path produced the value.
- Check parameters that can override a measured value: an operator-set value silently wins over
  detection unless the code says otherwise.

*Example:* a capture fell back to a fixed 26-minute offset when the production run was not found;
the task had started at :21 on one of twelve observed hours, which would have read state after
the job's own writes.

## Code and consumers

### 10. Branches production does not run

- Find config-gated branches in the changed code and query production config for which are live.
- A dead branch in production still ships. It needs a property test across its parameter space,
  because no dev run will exercise it.
- Rate reach honestly: unreachable today lowers severity; it does not remove the finding when the
  PR introduced the defect or a single config change reaches it.

### 11. Code the PR removes

- For every deleted function, branch or step, find the input that made it matter and check that a
  test covers that input. Simplification passes regress this way: the removed code was handling a
  case the remaining tests never construct.

*Example:* a simplification commit dropped the normalisation factor; the only test of that branch
used a funded case where the factor was 1.

### 12. Consumers that compare strictly

Beyond schema readers (covered under Apply order), list consumers that compare payloads field by
field: replay or regression fixtures, JSON diffing, dashboards over `SELECT *`. A new field is a
diff to them. Say whether they need re-recording and when.

### 13. How far a new failure spreads

- For every new `raise`, assert or hard exit in shared scheduler, planning or orchestration code,
  name what stops when it fires: the one feature, the task, or the whole run. Only a task's primary
  work may stop the run; an optional feature logs a warning and continues.
- Check whether the check's strictness was chosen for this code or copied from a nearby idiom. A
  fail-fast check copied into orchestration code is a candidate finding.
- For each test that asserts a validation fires, look for the inverse test: what must still work
  when it fires. A test that only asserts the raise locks in the wrong strictness.

*Example:* an optional feature raised on an unexpected account id inside the hourly job's planning
step. Personal dev-stack clones default to a different account id, so every clone's hourly run
would have stopped. The unit test asserted the raise.

When a migration seeds or changes config or run-parameter rows, list every job that reads them:
the prod job, the shared dev job, personal dev-stack clones, and one-off manual jobs. Clones copy
the rows but keep their own job defaults.

## Evidence

### 14. The author's evidence, and what it did not sample

- Read the PR's worked examples, validation tables and dev-run output as data. An unexplained value
  there (a missing entry on a row carrying real traffic, a ratio past its bound) is a candidate
  finding until explained, even if the author labelled it a caveat.
- Validation runs tend to use an ordinary input. List the variations the changed code meets over
  time: catch-up after a missed run, the first run of a period when periodic work is due, a partial
  scope, late or still-arriving data, a missing prior run, a config change inside the window.
- Ask for, or build, a table of each claim against its evidence: a live run, a unit test, or
  nothing. A claim backed only by an ordinary run is untested on every variation above. Pick
  validation inputs deliberately to hit the variations, rather than the most recent hour.

*Examples:* the author's worked example showed arms carrying 16-18% of an hour's traffic with no
floor; it was the symptom of item 1. Four validation captures of ordinary hours all matched; the
five defects later found sat in a catch-up run, the daily-summary hour, an excluded test, later
acknowledgements and a missing production run.

## Reporting

For each item that applies, record the paths checked and the evidence used in `QUALITY.md`
(provenance, mutable rows, snapshot instants, producer order, recorded-versus-enacted, both sides,
keys, scope, copied settings and fallbacks, removed code, failure spread) or `TESTS.md` (property tests, dead-branch
coverage, false-pass and false-fail cases, off-path fixtures, the claim-evidence table). Size every
surviving finding with data before rating severity.
