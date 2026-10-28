---
name: project-architecture-and-blueprint
license: MIT
description: Create and maintain evidence-backed architecture blueprints, governance documents and implementation roadmaps for new or existing software projects. Use for project initialization, architecture decisions, modernization plans or architecture drift analysis; ordinary local fixes do not require a new blueprint.
---

# Project Architecture & Blueprint

Make substantial implementation follow an intentional, researched and verifiable
architecture:

```text
Understand -> Identify uncertainty <-> Research / bounded experiments
           -> Review and record decision -> Implement incrementally
           -> Verify -> Observe where authorized -> Revise
```

Keep important requirements, decisions, evidence and next actions in the
repository so work can continue without the original conversation.

## Scope and authority

- Follow the user's current scope and applicable repository instructions.
  Reuse existing documentation paths, ADR conventions, architecture choices and
  roadmap identifiers. Do not introduce a parallel governance system.
- A blueprint request authorizes analysis and documentation. Implement only
  when implementation is within the user's request. A roadmap is not authority
  to execute every phase, deploy, link accounts, incur costs or migrate data.
- Resolve local implementation details within approved boundaries. For material
  changes to those boundaries, document the proposal and obtain approval if the
  existing authorization does not already cover it. Prepare the reviewable
  decision and impact assessment first; continue independent authorized work.
- Keep the method proportional. Do not create empty documents, speculative
  infrastructure or a repository-wide redesign for a narrow fix.
- Preserve supplied briefs and historical evidence unless their update is within
  the request; put new analysis in its intended output location instead of
  changing an input merely to add navigation or restate the conclusion.
- Follow an accepted decision directly when the request stays within it. Scale
  research, review and evidence to uncertainty, reversibility and impact; do not
  add a review committee or service-operating requirements to every task.

## 1. Establish the baseline

Read applicable repository instructions in the current agent's conventions
(`AGENTS.md`, `CLAUDE.md`, `.github/copilot-instructions.md` or equivalents),
respecting their declared scope and precedence. Locate the charter/scope,
architecture decisions, roadmap, development standards and implementation contracts.
Inspect actual code, tests and build configuration before trusting documentation.

Classify the project and adapt the work:

| State | Required approach |
| --- | --- |
| Greenfield | Establish a meaningful initial blueprint before substantial implementation. |
| Existing, undocumented | Reverse-engineer the current architecture before proposing a target. |
| Existing, documented | Reuse the blueprint and inspect the affected flows for drift. |
| Existing, inconsistent | Record discrepancies and distinguish observed behavior from the proposed correction. |

Inspect the relevant repository structure, languages, runtimes, dependencies,
composition roots, module graph, persistence/migrations, authentication and
authorization, integrations, CI/deployment configuration and tests. Record paths
and revisions where they support conclusions. Do not copy secret values into
documentation or treat historical test reports as fresh execution evidence.

Identify actors, objectives, workflows, business invariants, current scope,
non-goals, monetization, organization, geographic/regulatory constraints and
operational ownership. Address relevant non-functional requirements:
availability, performance, scale, security/privacy, recovery, observability,
maintainability, localization and accessibility. Mark unknowns and safe
assumptions explicitly; do not invent critical business or operating decisions.

## 2. Research significant decisions

Research the problem, failure modes and alternatives before choosing important
architecture or a non-trivial subsystem. Prefer official documentation,
standards, original engineering publications, maintained reference
implementations and technical papers. Use independent analysis as supporting
evidence and distinguish industry practice from the project's decision.

Compare relevant options by complexity, security, operations, cost, scale,
compatibility and migration impact. Adapt mature practices to the project's
actual team, budget and constraints. Do not copy a large platform's topology
or add a dependency solely because it is popular or saves a small amount of code.

Use fresh official sources for changing vendor capabilities, APIs, limits,
pricing and security guidance. For security-sensitive designs, consult current
authoritative guidance and relevant threat models. Record source URLs, access
dates, applicable versions, findings and limitations. If research is unavailable,
mark the affected decision provisional rather than claiming verification.

Read [Decision quality and experiments](references/decision-quality-and-experiments.md)
when uncertainty can change a design, options need a trade study, or a material
decision needs review. Define the question, discriminating criteria and a bounded
research/experiment budget. Stop when evidence is sufficient or the budget is
reached; record unresolved uncertainty. An isolated prototype may inform the
blueprint before substantial implementation, without becoming approved product code.

## 3. Design enforceable boundaries

Define the selected architectural style, responsibilities, data ownership,
public contracts, allowed dependencies and composition root. Honor a style or
reference explicitly selected by the user. For business applications, evaluate
a modular monolith with bounded contexts and inward dependencies; compare a
transaction-script approach when business complexity does not warrant tactical
DDD. Record the choice and acceptance criteria.

Read [Business boundaries and dependency contracts](references/domain-boundaries-and-dependencies.md)
when designing business contexts, applying DDD/Clean/hexagonal architecture,
reviewing a user-supplied reference or migrating existing boundaries.

For Clean/hexagonal designs, preserve this source dependency direction:

```text
delivery -> application -> domain
infrastructure -> application/domain ports
composition -> delivery + infrastructure + application
```

Keep HTTP types, database rows/connections, provider SDKs and framework errors
at adapters. Inner layers own business invariants and the ports they need.
Define cross-context contracts, transaction boundaries and state ownership;
a shared datastore does not authorize arbitrary cross-context writes. Keep
common contracts small and avoid a universal business model in `shared`.

Address API compatibility/versioning, validation/errors, pagination,
idempotency and rate limiting where applicable. Define deliberate database
migrations, constraints, retention/deletion and transaction semantics; do not
hide schema migration in startup logic. Reuse existing dependencies where
appropriate and assess maintenance, security, licensing and operational impact
before adding another.

Plan realistic failures, timeouts, retries, partial outcomes, observability,
backups and rollback. Avoid distributed systems complexity without demonstrated
requirements and operational ownership.

For security-sensitive changes, read [Threat analysis](references/threat-analysis.md)
and connect the system's assets, trust boundaries and abuse scenarios to controls,
owners, residual risks and checks. Consulting guidance alone does not analyze
the actual system.

For capacity/cost-sensitive choices, use the estimates and uncertainty checks in
the decision-quality reference. For operated services, state/protocol migrations
or release-path work, read [Service operation and safe evolution](references/service-operation-and-safe-evolution.md).
Define applicable SLO/measurement actions, mixed-version recovery and staged
promotion/stop evidence. Keep proposed targets distinct from accepted and measured ones.

Read [Terraform bootstrap and production lifecycle](references/terraform-production-lifecycle.md)
before designing or changing IaC bootstrap, cloud deployment identity or
production rollout. It is an adaptable control pattern, not permission to
provision resources or a mandatory three-state topology.

## 4. Document the contract before implementation

Use [Blueprint documents and roadmap](references/blueprint-documents.md) when
creating or substantially updating governance, implementation specifications
or the implementation tracker. Adapt its example paths to the repository.

For each significant decision record the problem, current state, research,
options, chosen or proposed solution, rationale, trade-offs, consequences and
constraints. Label decisions as proposed, accepted or superseded according to
the repository's convention. Preserve useful rejected alternatives and the
conditions that would justify reconsidering them.

For material decisions, identify the decision owner, appropriate reviewer,
objections/resolution and revisit trigger. Apply existing review authority;
authorization of work and technical review establish different facts. Never
invent named reviewers, approval or independent validation.

Distinguish observed code, proposed contracts, implemented behavior and released
assets. Link evidence to each claim. Update existing ADRs/indexes, registries,
specifications and roadmap entries when their decisions or boundaries change.
Do not describe a future target as the implemented baseline.

## 5. Implement and verify within the authorized phase

Before substantial module work, reconcile the relevant charter, scope,
functional/security/data rules, architecture decisions, roadmap, implementation
contract, actual code and tests. Implement incrementally within that contract.
For legacy work, characterize existing behavior and migrate complete flows
while preserving agreed API/data compatibility. Document scoped exceptions and
their exit criteria; an empty new layer does not complete a migration.

Choose checks that establish the relevant behavior: domain/use-case tests,
adapter/integration/database tests, API/contract/security tests and end-to-end
checks as warranted. Verify dependency boundaries with module visibility or
architecture checks and a known forbidden-dependency probe that must fail.
Compilation, folder layout and HTTP tests alone do not prove DDD, Clean or
hexagonal conformance.

Compare the result with the documented design. Correct accidental drift;
explicitly govern intentional changes. Record exact commands, outcomes, scope
and limitations. Keep local/static, hosted CI and live operating evidence
separate. Do not claim deployment, provider interoperability or production
readiness from static checks.

Where operation is in scope, feed observed SLOs, incidents, failed assumptions
and operational effort back into the decision records and roadmap. Designing
this feedback does not authorize a deployment, monitoring integration or live test.

## 6. Maintain the blueprint and hand off

Before declaring substantial work complete, verify requirements and scope,
architecture boundaries, appropriate passing checks, required migrations/API
documentation and the absence of unrelated changes or undocumented major
dependencies. Synchronize the implementation specification and governance.

Update the roadmap tracker with status, linked evidence, remaining work and
exactly one next authorized action per tracked item. Keep an architectural
criterion open while required boundaries, compatibility or operating decisions
remain unresolved. State when a next action needs additional authority.

End a substantial handoff with these facts, in the user's language:

```text
Completed
Verification
Remaining
Next action
Blocker (when applicable)
```

## Maintaining this skill

For installation, invocation or host capability differences, use
[Agent hosts and portability](references/agent-hosts.md). The common instructions
require no particular provider API, skill installer, model or delegation tool.
Use available file, search and verification tools; disclose unavailable evidence
instead of assuming every host can browse, execute commands or spawn agents.

When changing these instructions, use [the evaluation protocol](references/skill-evaluation.md)
and the [offline case corpus](evals/README.md). Structural validation and executed
behavioral cases are separate evidence; ordinary project work need not load them.
