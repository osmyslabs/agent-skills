# Terraform Bootstrap and Production Lifecycle

Read this reference when a project uses Terraform or comparable
infrastructure-as-code for cloud bootstrap, CI identity, environment
provisioning, or production deployment. It captures reusable control patterns
that must be verified against the project's cloud, team, risk and existing
estate. Adapt each control to the actual provider and deployment lifecycle.

## 1. First determine the infrastructure state

Classify the project before changing infrastructure:

- **Unprovisioned:** no eligible cloud project/account/subscription or remote
  state backend exists.
- **Bootstrapped:** the root cloud boundary and state backend exist, but the
  durable deployment foundation does not.
- **Foundation-ready:** APIs, registries, identities, CI federation, secret
  containers, and deployment IAM exist.
- **Runtime-ready:** workload infrastructure is applied and post-deployment
  checks pass.
- **Existing/adoption:** resources already exist outside the intended state
  boundaries and require import or state migration.

Do not treat authentication to an unrelated cloud project as authority to use
it. Resolve the exact target and verify ownership, lifecycle state, billing,
region, environment, and repository before any mutation.

For an existing project, inspect actual state backends, Terraform states,
workflow credentials, cloud identities, registries, secrets, and deployed
resources. Do not assume the repository reflects the live estate.

## 2. Identify roots of trust and external prerequisites

Terraform can provision most durable infrastructure, but it cannot safely
invent or self-authorize every prerequisite. Document which items are explicit
roots of trust, for example:

- the organization, account, subscription, project, billing relationship, and
  region;
- initial human/cloud CLI authentication;
- repository ownership and authenticated source-control CLI access;
- production approvers;
- domain registration, DNS delegation, or certificates controlled elsewhere;
- vendor, payment, email, identity, database, and AI-provider accounts;
- secret values and provider-side compliance/retention approvals.

An organization may deliberately manage project/account creation through a
higher-level Terraform bootstrap. Do that only when its parent organization,
billing authority, state backend, and lifecycle ownership are already defined
and the user has authorized those mutations. Otherwise verify an existing
isolated billed boundary and start below it.

Never silently reuse a project because it is the CLI default. Never claim that
Terraform validation proves a project, vendor account, compliance setting, or
live service exists.

## 3. Prefer explicit bootstrap, foundation, and runtime ownership

Use three conceptual layers when their distinct lifecycles solve a real
bootstrap or blast-radius problem. They may be separate states or, for a small
low-risk project, documented logical layers with an equivalent non-circular
control path.

### Layer A — minimal bootstrap

The bootstrap is an idempotent, operator-authorized procedure. It normally:

- verifies the exact existing cloud boundary and billing status;
- enables only the APIs needed to create and access remote state;
- creates or hardens the remote state backend;
- enables encryption, versioning/retention, locking where supported, uniform
  access, and public-access prevention;
- emits the backend identifier and next plan command without credentials.

The bootstrap is not an application deployment. It should not create runtime
services, put secrets in state, or make broad production changes. A remote
backend must exist before Terraform can initialize against it, so this narrow
step cannot always be expressed inside the state it creates.

### Layer B — foundation state

Use an independently reviewed state such as
`foundation/<environment>` for resources ordinary deployments must consume but
must not be able to recreate or mutate casually. Typical ownership includes:

- required cloud service/API activation;
- artifact/container registries;
- runtime, task, scheduler, and deployment identities;
- workload-identity/OIDC federation for CI;
- secret containers, but not secret plaintext;
- optional KMS keys when the project's threat model requires them;
- deployment IAM and narrowly scoped identity-use grants.

The foundation state should output typed, non-secret deployment metadata:
project/account identity, region, registry address, workload identity provider,
deployment identity, runtime identity map, and secret-container identifiers.

Foundation planning should be the default. Foundation apply requires explicit
intent and should be slower and more tightly reviewed than runtime deployment.

### Layer C — runtime state

Use a state such as `runtime/<environment>` for workload resources that change
with application releases. It reads foundation outputs through a supported
remote-state or configuration contract and commonly owns:

- workload storage and access bindings;
- queues, schedulers, jobs, and runtime services;
- secret access plus exact secret-version wiring;
- load balancing, public/private invocation policy, and service networking;
- monitoring, dashboards, alerts, and uptime checks.

Runtime deployment must not own the identity or federation it needs in order to
authenticate. That circular design fails on the first deployment and lets an
ordinary release mutate its own trust boundary.

## 4. Isolate environments and state

Prefer separate cloud projects/accounts/subscriptions for staging and
production when the provider and budget allow it. At minimum use separate
state paths, identities, secrets, policy, and deployment environments.

Record an ownership table in the project's architecture decision:

| Concern | Bootstrap | Foundation | Runtime | External authority |
|---|---:|---:|---:|---:|
| State backend | Yes | No | No | Cloud root/billing |
| CI federation and deploy identity | No | Yes | Read only | Repository owner |
| Secret containers | No | Yes | Read only | — |
| Secret values/versions | No | Metadata only | Numeric pins only | Authorized operator/vendor |
| Workload services and monitoring | No | No | Yes | — |
| Billing, domains, vendor accounts | No | No | No | Yes unless explicitly governed above |

Use stable backend prefixes rather than implicit local workspaces when distinct
lifecycles and access policies matter. Pin provider versions with committed lock
files. Never commit state, credentials, plaintext variable files, or local
secret inputs.

## 5. Use keyless, tightly constrained CI trust

Prefer short-lived OIDC/workload identity federation over reusable cloud keys.
The trust condition should bind immutable identities where the source provider
offers them, such as numeric repository and owner IDs, plus the exact deployment
environment or protected ref claim. Repository names alone may be mutable.

The CI deployment identity should have only the roles needed by the states it
applies. Grant it explicit permission to use runtime identities; do not make it
an owner merely to avoid working out the contract. Keep foundation mutation out
of ordinary application deployment workflows.

Production deployment should use a protected source-control environment with
required reviewers and self-review prevention. Preserve existing branch rules,
wait timers, and protection when automation updates environment configuration.

Do not store a service-account JSON key or equivalent long-lived cloud
credential in repository secrets when federation is available.

## 6. Automate derived CI environment configuration

Do not ask an operator to copy Terraform outputs one by one into GitHub or
another CI system. Provide an authenticated, redaction-safe bridge that:

1. initializes the exact foundation state;
2. verifies its project, environment, and repository identity;
3. reads typed non-secret foundation outputs;
4. validates a local non-secret environment configuration;
5. creates or updates the CI deployment environment without weakening existing
   protection;
6. publishes derived non-secret variables through the source-control CLI/API;
7. sets an activation flag last, only after the complete configuration passes.

It is valid to keep this bridge outside Terraform. Adding a source-control
Terraform provider solely to publish derived variables introduces another
credential, state dependency, and failure domain. Use such a provider only when
the organization deliberately owns repository configuration in Terraform and
accepts that coupling.

Before activation, deployment workflows should succeed with an explicit
inactive result while skipping checkout/authentication/build/apply steps. This
keeps normal CI usable and prevents an unconfigured environment from failing or
mutating infrastructure. An inactive deployment run is evidence of fail-safe
gating, not evidence of deployment.

## 7. Keep secret plaintext outside Terraform and CI variables

Terraform should generally create secret containers and IAM, not secret
versions containing plaintext. A controlled seeding/rotation procedure should:

- read values from an ignored local file, an approved secret broker, or secure
  operator input;
- validate required keys and reject placeholders/empty values;
- stream values directly to the cloud secret service without printing them;
- resolve the resulting enabled numeric version IDs;
- write or publish only non-secret version metadata.

Runtime configuration must pin positive numeric secret versions. Do not use
`latest` for production services: rotation should be an explicit rollout that
can be reviewed and rolled back. Terraform plans, state, CI variables, command
lines, and logs must never contain secret plaintext.

Whether numeric version-pin manifests are committed or stored as protected
non-secret environment metadata is a project decision. In either case, review
changes and keep the values separate from the secret material they identify.

## 8. Deploy immutable artifacts

Build artifacts may receive human-friendly or commit tags, but deployment must
resolve and pass immutable identifiers such as image digests. Terraform inputs
should validate the immutable form and reject mutable tags.

A mature release flow is:

```text
build artifact
    ↓
push to registry
    ↓
resolve immutable digest
    ↓
plan runtime using exact digests and secret versions
    ↓
apply the saved reviewed plan
    ↓
run post-deployment validation
```

Rollback means redeploying known prior digests and compatible secret-version
pins, not retagging an unknown image.

Those identifiers alone do not establish state/protocol compatibility. Before
relying on application rollback, use the mixed-version, recovery-floor and
retirement checks in [Service operation and safe evolution](service-operation-and-safe-evolution.md).
That reference also defines applicable SLO action policies and staged release
promotion/stop evidence. Read the relevant sections when designing this path;
neither reference authorizes a live rollout or data migration.

## 9. Make apply fail closed

For operator wrappers and CI:

- default to plan-only for foundation and manual runtime use;
- save a binary plan and apply that exact plan;
- render plan JSON and summarize creates, updates, deletions, and replacements;
- reject every delete or replacement unless an explicit destruction flag is
  supplied in addition to apply intent;
- require typed confirmation for interactive high-risk applies;
- allow non-interactive approval only inside an already authorized protected
  workflow;
- use deployment concurrency controls and the backend's locking mechanism;
- clean up temporary plans/configuration even on failure;
- never use a broad target or refresh suppression as a routine workaround.

If live resources predate the state split, stop before applying. Design and
review `import`, `moved`, or state-migration operations first. Do not let a new
empty state interpret existing resources as disposable duplicates.

## 10. Separate CI, deployment, and live acceptance evidence

Maintain independent evidence layers:

### Local/static infrastructure evidence

- recursive formatting;
- backend-disabled initialization and validation for every stack;
- validation tests for public configuration, numeric secret pins, immutable
  artifact references, and destructive-plan detection;
- shell/script syntax and workflow YAML parsing;
- documentation and diff checks.

These checks do not prove cloud resources exist.

### Hosted clean-runner evidence

- the same stack validations on a clean runner;
- safety/contract tests and script syntax;
- ordinary application CI kept separate from cloud activation;
- an inactive deployment-path test when the environment is not bootstrapped.

A green inactive deployment proves only that mutation was safely skipped.

### Live environment evidence

- the exact foundation/runtime plans and successful applies;
- cloud service readiness and configuration identity;
- public and authenticated smoke journeys as applicable;
- provider access, monitoring delivery, recovery, security, and compliance
  checks that require actual external systems;
- evidence links, commit/digest/version identities, timestamps, and unresolved
  gates recorded in the repository.

Never mark a production phase complete from `terraform validate`, a workflow
definition, a plan-only run, or an inactive deployment gate.

## 11. Recommended environment progression

For a new environment:

1. Resolve and authorize the exact cloud boundary, billing, region, repository,
   and external prerequisites.
2. Run the minimal backend bootstrap.
3. Generate and review a fresh foundation plan.
4. Apply foundation with explicit approval.
5. Seed/rotate secret versions without exposing values.
6. Run the automated CI environment bridge; set activation last.
7. Build artifacts and resolve immutable identifiers.
8. Generate and review the runtime plan.
9. Apply the exact plan and run post-deployment validation.
10. Record actual evidence and retain all unverified live gates.

Staging should normally exercise this full path first. Production uses a
different cloud boundary/state/identity and a protected approval gate. Promotion
reuses tested release identities where appropriate; it does not copy staging
state or credentials into production.

## 12. Blueprint requirements

When adopting this lifecycle, update the repository before declaring success:

- **Architecture decision:** why the state split exists, exact ownership,
  trust model, external prerequisites, consequences, migration concerns, and
  rejected alternatives.
- **Implementation/deployment specification:** supported commands, input
  schemas, environment progression, recovery/rollback, and what remains
  external.
- **Repository agent instructions/development standards:** relevant validation commands and the rule
  that local development must not require production cloud access.
- **Roadmap/acceptance tracker:** distinguish engineering-complete, hosted-green,
  inactive fail-safe, staging-live, and production-live evidence, with exactly
  one next action.

Useful rejected alternatives to record when applicable:

- runtime state creates the identity needed to authenticate its own first
  deployment;
- long-lived cloud keys in CI;
- manual copying of Terraform outputs into repository settings;
- secret plaintext in Terraform state or CI configuration;
- `latest` secret versions or mutable image tags;
- ordinary releases mutating federation/foundation IAM;
- automatic destructive apply;
- treating plan/validate/inactive runs as live deployment evidence;
- silently reusing the current CLI project or shared credentials;
- duplicating a mature reference project's provider-specific services without
  proving they fit the new project.

## 13. Proportionality and exceptions

This is a control pattern, not a mandatory directory layout. A small disposable
prototype may use one state when all of the following are true:

- there is no circular deployment identity bootstrap;
- the environment is non-production and isolated;
- secret plaintext is still excluded from state and logs;
- destructive changes remain reviewable;
- the simplification is documented with a trigger for separation.

Conversely, regulated or multi-account organizations may need more layers,
policy-as-code, separate security/network states, remote runners, break-glass
controls, and formal change management. Add those only when requirements and
operational ownership justify them.

The reusable lesson is the lifecycle and trust separation—not the names,
provider resources, scripts, regions, or topology of the source projects.
