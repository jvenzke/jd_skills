# Coding standards (PR review)

The LOGIC_QUALITY specialist uses this as the sole maintainability checklist. Optimize for long-term ease of change: simple callers, localized invariants, and complexity hidden behind stable boundaries—not small diffs or stylistic preference.

Do not demand speculative generalization, unrelated cleanup, or an interface migration outside confirmed claims.

## Priorities

1. Reduce total system complexity: fewer concepts and less caller coordination.
2. Prefer deep modules: small intent-oriented interfaces hiding cohesive complexity.
3. Push invariants, sequencing, representation, policy, errors, and special cases into the owning module.
4. Minimize coupling, information leakage, pass-through layers, and duplicated orchestration; organize around knowledge/responsibility.
5. Reuse sound code without preserving shallow or misplaced abstractions merely to minimize changes.
6. Deliberately assess important new/reshaped boundaries; awkward coordination or a hard-to-describe interface signals a poor abstraction.
7. Keep to the PR's vertical slice. A larger edit is justified only when it deepens an already-touched module or simplifies its boundary.
8. Comments explain non-obvious intent, invariants, or rationale; they do not narrate obvious code.

## Boundary standard

- Callers express intent without coordinating internal steps.
- Co-locate related state, policy, and invariants when that reduces shared knowledge.
- Eliminate invalid states and repeated special cases behind the owner.
- Judge abstractions by complexity removed from callers, not size.
- Preserve public compatibility unless confirmed claims include a migration.
- Name material public/module boundary changes in the walkthrough.

## Finding bar

A maintainability finding requires:

1. a change this PR introduces or worsens
2. a concrete current/future trigger or caller
3. leaked/misplaced knowledge and the resulting change-impact path
4. one practical fix direction

Qualifying problems include leaked coordination/policy/representation, shallow pass-through boundaries, split responsibility, caller-exposed invalid states, awkward new interfaces, unjustified drive-by abstractions, and extra paths for the same business data.

Search nearby readers/writers of the same entity/fields/invariants, not the repository at random. Consolidation is `recommended` when it fits this slice, `blocker` only when divergence creates a concrete correctness/security failure, and `future_work` when clearly larger than this PR.

Naming, formatting, and local style are nits unless they reveal the abstraction problem. TESTS—not LOGIC_QUALITY—owns coverage and test-volume judgment.
