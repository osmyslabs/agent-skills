# Blueprint documents and roadmap

Read when creating or substantially updating project governance, module
specifications or an implementation tracker. Existing repository conventions
take precedence over these example paths. Keep one authoritative home for each
decision rather than introducing duplicate documentation.

## Greenfield structure

When no useful structure exists, this is a starting point:

```text
AGENTS.md
00-governance/
  01-project-charter.md
  02-scope.md
  03-functional-principles.md
  04-non-functional-requirements.md
  05-security-principles.md
  06-data-governance.md
  07-architecture-decisions.md
  08-api-governance.md
  09-development-standards.md
  10-project-roadmap.md
implementation/
  <actual-capability>/
```

Adapt or combine documents to the project's needs. Create only meaningful
project-specific content. Do not generate empty files to fill this tree.

## Governance responsibilities

| Document | Required information when relevant |
| --- | --- |
| Project charter | Mission, users, objectives, product identity, constraints and ownership. |
| Scope | Current phase/MVP, future scope, explicit exclusions and non-goals. Future scope is not implementation authority. |
| Functional principles | Business rules, invariants, actors and critical workflows. |
| Non-functional requirements | Measurable availability/performance/scale needs, reliability, recovery, observability, maintainability, localization and accessibility. Identify unresolved targets. |
| Security principles | Authentication, authorization, roles/permissions, trust boundaries, secrets, encryption, sensitive data and audit. |
| Data governance | Ownership, identifiers, timestamps, consistency/transactions, retention, deletion, archival and migration policy. |
| Architecture decisions | Selected style, boundaries, dependency rules, persistence, APIs, authentication/authorization, asynchronous work, integrations, cache/storage, deployment, security, testing and operations. Cover only applicable concerns. |
| API governance | Versioning, resource/naming semantics, error format, validation, pagination/filtering, authorization, idempotency, rate limits and compatibility. |
| Development standards | Build/run/test commands, supported tooling, dependency rules, CI and review/documentation expectations. Local development must not require production access. |
| Roadmap | Authorized sequence, dependencies, deliverables, acceptance, non-goals and implementation evidence. |

For an existing project, first describe the actual modules, runtime topology,
data flows, persistence, integrations and test coverage. Keep the observed
baseline separate from modernization proposals and migration exceptions.

## Agent entry point

Use the repository's existing agent instruction entry point (`AGENTS.md`,
`CLAUDE.md`, `.github/copilot-instructions.md` or the host's equivalent). Do not
create competing files merely to match a different host's examples.
Keep it concise, containing purpose, required
reading, architectural constraints, repository navigation, development/testing
commands and documentation rules. Link authoritative documents rather than
copying their contents. Preserve applicable instructions already present.

## Decision records

Use a central architecture document for a small new project when appropriate.
Keep a repository's established ADR collection and index when it already has
one. The format is less important than a discoverable, consistent decision
history.

A significant decision should answer:

```text
Status, scope, author and decision owner
Appropriate reviewer, actual approval/review evidence and open objections
Problem and current state
Requirements and constraints
Research: sources, access date, versions and findings
Options considered
Decision or proposed change
Project-specific rationale
Trade-offs, consequences and affected contracts
Verification and migration/rollback criteria
Rejected alternatives, assumptions and reconsideration triggers
```

Separate general industry findings from the project's choice. For example,
separating search indexes from transactional persistence is a pattern; choosing
an external search service still requires project-specific evidence and
operational ownership. Retain enough research to explain the decision without
copying entire external articles.

For a material change outside current authorization, make the impact and
recommendation reviewable before requesting approval. Do not silently change
databases, authentication, service topology or another accepted boundary.

## Capability implementation contracts

Organize specifications around actual business/technical capabilities rather
than every potential future module. Include the applicable parts of:

- purpose, scope, actors and business vocabulary;
- context/model boundaries, invariants and lifecycle transitions;
- use-case inputs/results, authorization and failure semantics;
- persistence, consistency, transactions and migrations;
- API/event schemas, integrations and compatibility;
- security/privacy, operations, observability and rollback;
- dependencies, composition and acceptance checks.

For applicable sensitive or operated capabilities, use the conditional
[threat-analysis contract](threat-analysis.md) and [operation/evolution contract](service-operation-and-safe-evolution.md).
For uncertain or resource-sensitive choices, use the [decision/experiment contract](decision-quality-and-experiments.md).
Link the relevant evidence rather than duplicating these references in every module.

Possible files are `README.md`, `domain.md`, `use-cases.md`, `data-model.md`,
`api.md`, `security.md`, `events.md`, `integration.md` and `testing.md`. Split
only when it improves navigation. Specifications should let a competent
implementer proceed without guessing critical requirements.

## Roadmap and implementation tracking

For each phase define its objective, dependencies, deliverables, affected
capabilities, acceptance criteria and non-goals. Classify additional ideas as
required now, required later, technically possible, nice to have or out of
scope. Do not implement them merely because they are easy.

Use the repository's status vocabulary; otherwise use `not started`,
`in progress`, `blocked` and `complete`. A useful tracker is:

| Item | Status | Evidence | Remaining | Next authorized action |
| --- | --- | --- | --- | --- |
| Actual phase or bounded work item | Current status | Code/test/document/artifact links and results | Open acceptance criteria or blocker | One concrete action, including any authority it requires |

Update the tracker after substantial work. Record evidence against the
acceptance criteria instead of marking the whole phase complete because one
part compiled. Dependency checks, behavioral tests and operational validation
establish different properties. An in-scope migration exception keeps the
corresponding architectural criterion open.

If the repository uses a single global next-action marker, preserve that
convention. Do not create a competing marker for an incidental maintenance
item. State one next action per tracked item and distinguish a requested
maintenance task from the portfolio's existing implementation sequence.

## Completion evidence

Before a substantial feature handoff, check the applicable items:

- requirements and authorized scope are satisfied;
- selected architecture and dependency boundaries are verified in code;
- existing conventions and compatibility commitments are respected;
- meaningful tests/checks pass; skipped or unavailable checks are explicit;
- required migrations and API/implementation documentation are current;
- architecture decisions and registries reflect intentional changes;
- no undocumented major dependency, unrelated change or accidental drift;
- roadmap evidence, remaining work and next action are current.

Where in scope, also check that significant decisions received the required review,
security controls have threat-to-check evidence, state changes have a safe recovery
contract, and service objectives/release progression have their applicable proof.
Keep proposed, locally checked and actually operating acceptance distinct.

Report completed work, verification, remaining work, one next action and any
blocker. Do not claim a phase complete while required evidence, operating
decisions or approvals remain open.
