# Business boundaries and dependency contracts

Read when designing or reviewing business contexts, adopting DDD/Clean/hexagonal
architecture, or adapting a user-supplied reference project. Produce a contract
that can be checked against code, not just a preferred directory tree.

## Choose deliberately

Strategic DDD defines where a model and its language apply. Tactical DDD models
behavior and consistency through entities, value objects, aggregates and policies
when their invariants warrant them. Clean Architecture governs source dependency
direction. Hexagonal architecture isolates application behavior through ports
and replaceable adapters. CQRS separates commands and queries; it does not by
itself require a bus, separate databases, or event sourcing.

For a business application with distinct workflows, start by evaluating a modular
monolith with these boundaries. For a simple CRUD capability or technical tool,
a transaction script may be sufficient: state the reasoning and the boundaries
that still apply. Never impose a rich aggregate per table, an interface per
class, or a separate deployment per context. If the user explicitly selected a
style, satisfy it rather than treating proportionality as permission to omit it.

## Required design evidence

In the central architecture decision and relevant implementation specifications,
record the applicable items below. Identify unknown business rules as open;
do not invent them to fill a diagram.

| Artifact | What it must establish |
| --- | --- |
| Context map | Business responsibility, vocabulary, actors, owned model/data, upstream/downstream contracts and source of truth |
| Behavioral model | Actual invariants, lifecycle transitions and consistency/aggregate boundaries; distinguish CRUD/read projections |
| Use-case contract | Input, result, authorization, orchestration, transaction scope, failures and retries/idempotency where relevant |
| Dependency contract | Allowed module/layer edges, public entry points, forbidden imports and composition root |
| Migration and proof | Current violations, first complete vertical slice, compatibility constraints, temporary exceptions and checks needed to close them |

A documentation domain, Gradle module, database table or API route is not
automatically a bounded context. One context may need several technical modules;
one business concept may have different models in different contexts. A database
schema or package boundary is an implementation of an established model boundary,
not a substitute for identifying it.

## Code organization and ports

Organize business capabilities before technical layers. One possible JVM layout:

```text
application-host/                 # bootstrap, HTTP plugins, composition
modules/<business-context>/
    domain/                      # behavior, values, policies, repository contracts
    application/                 # use cases, commands/queries, handlers, output ports
    infrastructure/              # database/provider/storage adapters and mapping
    route/                       # HTTP DTOs, authentication extraction, response mapping
    di/                          # context composition, if useful
shared-contracts/                # deliberately small integration contracts
```

Adapt names and build layout to the repository. Do not create empty layers or
all prospective modules. Use separate build modules when requested or needed to
enforce boundaries; inside one build module, add checks for internal layer edges.
The fact that a context module has a JDBC/HTTP dependency for its adapters does
not permit its domain/application packages to import those APIs.

- The domain expresses business behavior without HTTP/DB/provider/DI types.
- Application use cases orchestrate policies and ports, returning their own
  results/errors. Ports expose the consumer's needs and framework-neutral types.
- Infrastructure implements persistence and provider ports, translating external
  identities, failures, rows and transaction mechanisms at that boundary.
- Routes map wire DTOs to use-case inputs and results/errors back to transport.
- Composition constructs adapters and injects them; inner layers do not find
  dependencies through a global container or the HTTP call context.

Cross-context access uses an explicit public application contract, a consumer
port with an integration adapter, or a documented event/projection. Do not import
another context's concrete repository or mutate its state directly. Define
consistency explicitly: security/revocation/publication invariants must not be
weakened by an asynchronous projection. A modular monolith may coordinate an
explicit shared transaction through owned contracts where required; do not hide
a database connection inside an ostensibly independent domain API.

## Using a reference repository

Inspect actual settings, modules, dependencies and at least one complete flow:
route -> use case/handler -> domain/port -> adapter, plus composition and tests.
Record paths and a commit when available. Use the reference as structural
evidence, not as proof that all its code satisfies every named pattern.

Extract the structure and dependency principles the user selected. Preserve the
target project's stack and authorized decisions unless changing them was also
requested. A reference's DI framework, CQRS code generator, distributed broker,
database or number of modules is not an automatic dependency requirement. Keep
project-specific business names and local paths out of this reusable skill.

## Migrating an existing backend

Record concrete violations first: business SQL inside routes, application code
constructing concrete repositories, HTTP errors in policies, provider types in
the core, global DTOs and helpers crossing every domain, or cyclic module access.

Migrate a complete behavioral slice, including its adapters and composition,
while preserving agreed HTTP/data behavior. Establish the port and domain/use-case
contracts before moving their implementation. Keep API/SQL changes separate
unless the same authorized change requires them. Verify each migrated flow;
renaming folders around the same dependencies does not complete the migration.

Legacy exceptions must name their actual scope, why they remain, the responsible
phase and the condition that removes them. New checks must not silently ignore
all legacy code, unclassified files or modules that have not been migrated yet.
Report migrated and remaining scope separately.

## Verification and completion

- Domain/use-case tests run without a web server, live DB or provider SDK;
  application tests use injected ports and meaningful failure cases.
- Adapter/HTTP/real-DB tests verify mapping, persistence, contracts and permissions.
- Module/build and layer checks enforce inward dependencies and context access;
  a forbidden-dependency fixture or equivalent negative check must be rejected.
- Inspect the wiring and the full flow so an unused pure domain does not conceal
  business logic that still executes in routes or concrete repositories.

Record the checks' scope and limitations. Dependency/import checks do not prove
that the chosen domain model is useful; behavioral tests do not prove dependency
direction. Neither green tests nor a directory tree alone establishes conformance.
Do not close an architectural phase until its required boundaries and migrated
flows are implemented and verified.

## Primary references

Consulted 25 October 2026; summarize their consequences in the project's decision
record when they influence a choice:

- [Eric Evans, DDD Reference](https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf): model/language boundaries and context mapping.
- [Alistair Cockburn, Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture): application isolation through ports and adapters.
- [Robert C. Martin, The Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html): inward source dependencies and framework-independent business rules.
