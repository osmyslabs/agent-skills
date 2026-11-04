# Compatibility and characterization

Read before replacing or reorganizing behavior with external or stateful effects.

Find the actual entry points, callers and owners. Characterize successful inputs,
invalid/boundary values, errors, ordering, encoding and observable side effects
where relevant. Preserve the product's authorization and business policy. Do not
infer a generic contract merely because two implementations look similar.

For dependencies inspect the resolved version, public API use, runtime/transitive
requirements, support status and migration notes. A newer major release is not
automatically compatible; a lockfile edit is not runtime validation. Prefer a
targeted supported update with actual consumer checks over a bulk upgrade.

For persistence, concurrency or delivery semantics include transaction boundaries,
idempotency, replay, mixed-version readers/writers and failure recovery. Determine
whether a rollback can read data written by the new version. Preserve the old path
until transition evidence permits retirement; do not migrate real data as an
implicit part of an assessment.

Run the existing relevant checks first, then the changed implementation against
the same contracts. Add missing tests for material affected behavior, not tests
that only assert a new folder layout or implementation detail. Keep fixture tests
and expected outputs independent of the code under refactoring where practical.

Record observed quirks separately from intended requirements. If a request asks to
correct a defect, use a regression test for the intended behavior; do not use a
golden snapshot to make the defect permanent. For a pure refactor, expose unresolved
contract questions before changing externally visible behavior.
