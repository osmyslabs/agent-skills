Read for the feature-level mode of project-architecture-and-blueprint. Use the
existing project architecture as context; this workflow does not require a
separate skill installation or the project-wide governance sequence.

# Feature Implementation Blueprints

Document a business capability first, then trace only the implementation needed to understand it end to end. The reader already knows the language and framework; explain system-specific behavior, boundaries, and consequences rather than syntax or boilerplate.

## Determine the Deliverable

- Identify the requested business capability and its boundaries. If the name is broad, infer a practical scope from the repository and state it.
- Treat create or update requests as authorization to write the blueprint. For review, explanation, or diagnostic requests, remain read-only unless the user also asks for documentation changes.
- Do not turn a feature blueprint into a project-wide architecture redesign. Use the repository's documented architecture as context, and record discrepancies as evidence or open questions.

## Store the Blueprint by Business Capability

The primary blueprint is organized by business capability, even when its code crosses modules, services, layers, or applications.

1. Inspect the repository for an established documentation convention.
2. When no stronger convention exists, write the entry point to `docs/features/<feature-slug>/README.md`.
3. Use a stable, lowercase, hyphenated slug derived from the capability name.
4. Keep `README.md` as the source of truth. Put optional supporting material under the same feature directory, for example `diagrams/`, `flows/`, `decisions/`, or `examples/`.
5. Do not place the primary blueprint inside a technical module merely because that module contains part of the implementation.
6. A technical module may contain a lightweight link back to the feature blueprint when useful, but do not duplicate or fragment the source of truth.

If the repository already has a documentation convention, integrate with it while preserving business-capability grouping and a clear primary entry point.

## Investigate the Feature

### 1. Establish scope and vocabulary

- Find feature terminology in product documentation, routes, commands, events, state names, persistence names, configuration, and tests.
- Identify the business purpose, trigger, intended outcome, in-scope paths, and explicit exclusions.
- Include frontend behavior only where it triggers, validates, constructs, submits, or handles feature-specific outcomes.

### 2. Reconstruct real execution paths

- Start at each confirmed entry point: HTTP/GraphQL, UI action, CLI, internal call, event, queue, webhook, worker, or scheduled job.
- Follow actual calls through application orchestration, domain behavior, persistence, integrations, and asynchronous continuations.
- Resolve interfaces to concrete implementations only when wiring or runtime selection is visible.
- Distinguish a declared dependency, import, type reference, or co-location from an observed runtime call.
- Continue across services when source is available. When it is not, stop at the contract boundary and mark downstream behavior unverified.
- For large capabilities, document a small set of named execution paths and describe shared functions once.

Use repository search tools such as `rg` and search by business terms, route paths, event names, entity/state values, table or collection names, provider operations, function names, configuration, and tests. Do not rely on filenames alone.

### 3. Select significant functions

Document a function only when changing or removing it could materially affect business behavior, orchestration, state, persistence, invariants, authorization, financial movement, idempotency, retry or reconciliation, external calls, side effects, asynchronous processing, error behavior, or a transaction boundary.

Exclude trivial accessors, obvious mappings, formatting helpers, generic wrappers, constructors without business meaning, and framework boilerplate unless they encode a relevant rule. The function registry is curated, never exhaustive.

For every selected function, capture its responsibility, why it exists, why it belongs at its current boundary when meaningful, confirmed callers and callees, meaningful inputs/outputs, state or persistence effects, invariants, failures, and related tests. Add transaction, idempotency, concurrency, performance, security, or change-impact details only when relevant.

### 4. Follow behavior beyond calls

Trace the material parts of the capability:

- data transformations and where they occur;
- state transitions, triggering functions or events, conditions, and persisted changes;
- reads, writes, transaction boundaries, and constraints;
- external systems, operations, timeouts, retries, and error translation visible in code;
- events, queues, workers, jobs, callbacks, and webhooks, including duplicate and ordering handling;
- side effects and feature-owned versus shared components;
- tests that demonstrably protect the behavior;
- likely modification points, affected surfaces, expected non-changes, and risky shared dependencies.

For financial features, also trace source and destination of funds, provider operation, internal transaction and ledger effects, holds/reservations, fees, settlement, callbacks, reconciliation, compensation, and duplicate or double-spend protection. Never infer accounting behavior merely from names.

## Evidence Discipline

Use code, wiring, configuration, migrations, schemas, contracts, and tests as evidence. Never invent runtime paths, business rules, states, provider behavior, database effects, retries, transaction boundaries, test coverage, or architectural intent.

Apply these labels where evidence quality matters:

- **Confirmed** — directly supported by repository evidence.
- **Inferred** — strongly suggested; state the evidence and remaining uncertainty.
- **Unverified** — plausible but not confirmed by an available path.
- **Not found in repository** — searched for but absent.

Do not use tests as proof of production wiring unless that wiring is independently confirmed. Do not expose secret values; document configuration names and behavior only.

## Compose the Blueprint

Read [feature-blueprint-template.md](feature-blueprint-template.md) before drafting or updating a blueprint. Cover its core concerns, combining sections for a small capability. Omit optional sections that do not apply and avoid empty placeholders or duplicate function inventories. Preserve useful existing content and links when updating an established blueprint.

Use compact text diagrams or tables only when they make paths, mappings, states, or ownership materially easier to understand. Link to repository files with precise paths and line numbers when the output environment supports stable links.

Read [feature-payout-example.md](feature-payout-example.md) only when a financial or asynchronous feature needs a concrete formatting example. It is fictional and must never be treated as repository evidence.

## Quality Check

Before finishing, verify that the blueprint:

- describes one business capability rather than cataloguing technical modules;
- identifies triggers, outcomes, primary orchestrators, and all material execution paths;
- separates confirmed calls from declarations and inference;
- includes only significant functions and explains both what and why;
- traces material data, state, persistence, integrations, async continuations, side effects, failures, invariants, security, and idempotency where applicable;
- distinguishes feature-owned from shared components and explains shared change risk;
- maps tests without overstating coverage;
- gives concrete modification points, likely impact, and expected non-changes;
- records unknowns instead of filling gaps with assumptions;
- keeps the primary entry point in the feature-oriented documentation location;
- is concise enough to serve as a navigation aid rather than a substitute for the source tree.

Report the blueprint path, what was verified, and any important unresolved evidence gaps.
