# Coding standards (PR review)

Use this checklist in the LOGIC_QUALITY specialist. Goal: **long-term ease of maintaining the codebase**. Judge the PR by whether it leaves callers simpler, invariants localized, and complexity behind stable boundaries — not by whether the diff is small or stylish.

Do not demand speculative generalization, unrelated cleanup, or an interface migration the PR did not claim. Do not preserve shallow abstractions merely to minimize the diff. Map "approved plan" in the development standard to this PR's confirmed claims and stated intent.

## Maintainability rules (priority order)

Apply in this order when they conflict:

1. **Reduce system complexity**: optimize for simpler callers, fewer concepts, and less coordination—not the smallest diff or fastest implementation.
2. **Deep modules**: prefer small, intent-oriented interfaces that hide substantial cohesive implementation complexity.
3. **Push complexity downward**: keep invariants, sequencing, representation, policy, error handling, and special cases behind the module that owns them.
4. **Prefer clear boundaries**: minimize coupling, information leakage, pass-through layers, and duplicated orchestration. Organize around responsibility and knowledge, not execution order.
5. **Extend/reuse sound code**, but do not preserve shallow abstractions or misplaced responsibilities merely to minimize changes.
6. **Design deliberately**: for important or reshaped boundaries, consider alternative designs. Treat excessive coordination, awkward naming, or difficult-to-describe interfaces as signs the abstraction may be wrong.
7. **Keep the PR's vertical slice**: larger changes are justified when they deepen a module the PR already touches or simplify its boundary; no unrelated cleanup or speculative generalization.
8. **Test restraint**: prefer high-signal contract tests over test volume; do not add tests merely to perform a red/green loop. (LOGIC_QUALITY does not score this — TESTS owns it.)
9. **Comments explain what code cannot**: document non-obvious intent, invariants, or rationale; avoid comments that restate understandable code.

## Deep-module design standard

Treat a module as any file, class, object, package, service, or subsystem with a boundary.

* Expose the smallest practical interface for the capability. Callers should express intent without coordinating internal steps.
* Favor fewer, deeper modules over shallow wrappers, pass-through methods, fragmented helpers, or interfaces that mirror implementation details.
* Co-locate state, policy, invariants, and related complexity when doing so reduces knowledge shared across modules.
* Prefer designs that eliminate invalid states and special cases rather than repeatedly exposing or handling them.
* Judge an abstraction by the complexity it removes from callers, not by its size or line count.
* Preserve public behavior and compatibility unless the PR's claims explicitly include an interface migration.
* New or reshaped public/module boundaries must be named in the PR's claims/intent; private implementation structure may evolve as needed to realize that design.

## Finding bar

A standards miss is a finding only with a concrete trigger (how a future change or caller is harder), the leaked or misplaced knowledge, and a fix direction.

Include as `recommended` when the PR **introduces or worsens**:

- leaked complexity (callers must know sequencing, policy, representation, or special cases)
- a shallow boundary (wrapper, pass-through, fragmented helper, or interface that mirrors internals)
- misplaced responsibility (invariant or orchestration split across modules, or organized by execution order instead of knowledge)
- invalid states or special cases left in callers instead of eliminated behind the owning module
- a hard-to-describe or awkwardly coordinated boundary that will make future change harder
- comments that restate obvious code, or missing comments where a non-obvious invariant/rationale is required

`blocker` only when that smell creates a concrete correctness or security failure mode. Local style, naming, and formatting are `nit` and stay out of the default comment list unless naming is evidence the abstraction itself is wrong. Test-restraint issues belong to the TESTS specialist, not this checklist.
