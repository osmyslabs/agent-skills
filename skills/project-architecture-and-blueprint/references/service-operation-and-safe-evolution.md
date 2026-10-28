# Service operation and safe evolution

Read the relevant sections when designing an operated service, changing durable
data/protocols, or preparing an authorized release path. Libraries and offline
tools need suitable behavioral/compatibility criteria, not an automatic SRE
organization, network service, canary platform or production SLO.

This reference defines design and verification contracts. It does not authorize
deployment, monitoring integration, provider access, migration or live recovery
tests. Preserve existing operating ownership and approval rules.

## Turn reliability requirements into decisions

Start with the user journey and its observable outcome. For each important
service objective define the applicable fields:

| Field | What it establishes |
| --- | --- |
| Journey and boundary | The user-visible operation, including where timing begins and ends. A fast queue acknowledgment is different from a completed job. |
| SLI | What is measured, numerator/denominator or latency distribution, population, exclusions and evidence source. |
| SLO | Target, measurement window and why it fits the product's consequences and constraints. |
| Ownership | Product/operating roles responsible for accepting and maintaining the objective. |
| Action policy | What investigation, reliability work, change restriction or escalation follows a material miss. |
| Review | When incidents, changed demand or invalidated assumptions trigger reconsideration. |

Label targets as proposed until the relevant owner accepts them. Label compliance
unverified until measurements cover the defined population/window. Do not fill
missing targets with a universal percentage or claim a monitor exists from a
configuration file alone. Justify exclusions; do not hide user-visible failures
because a dependency caused them.

Where useful, define an error budget from the agreed objective and relate it to
prioritization. The policy belongs to the product; do not import another company's
freeze thresholds or choose business consequences without authority. An offline
batch may instead use completion/freshness, deadline and correctness criteria.

## Prepare operation proportionately

For an operated service, keep enough evidence to establish applicable readiness:

- responsible operator/team and a realistic incident/escalation path;
- useful signals and alerts tied to customer impact rather than arbitrary noise;
- a short runbook for common failures, dependency outage and recovery;
- capacity/degraded-mode expectations, including backlog or resource exhaustion;
- data backup/restore and recovery objectives where state matters;
- compatibility, release and recovery controls;
- open acceptance decisions and the evidence needed to close them.

Use roles when people have not been assigned and mark that decision open. Do not
invent an on-call rotation or make a dedicated SRE team a prerequisite for a
small product. A design, local test, hosted test and actual recovery exercise
prove different facts. Run only checks within the current scope/environment.

## Prove compatibility before relying on rollback

An old artifact and its digest do not establish that the old code can read state
or messages produced by the new code. Before a material data/protocol change:

1. Inventory affected readers/writers: services, workers, clients, scheduled jobs,
   persisted records, queued messages, caches and retained backup formats.
2. Build the relevant old/new compatibility matrix for actual write formats,
   read formats, defaults, semantic meaning and error behavior.
3. Identify the safe recovery floor: the oldest version that can still operate
   after activation and the points beyond which earlier rollback is unsafe.
4. Define preparation, activation and retirement with explicit exit evidence.
5. Test mixed-version behavior and recovery with representative synthetic state
   or another authorized environment before claiming the path is safe.

A common sequence is:

```text
prepare readers/compatible schema -> verify all affected consumers ready
 -> activate new writes/behavior -> observe and retain safe recovery version
 -> migrate retained state/messages as needed -> verify retirement conditions
 -> remove obsolete compatibility
```

Expand/contract can implement this for suitable schema changes; other changes
need different protocols. Preparation must include every relevant consumer,
not just the instances counted healthy by a deployment tool. Account for delayed
messages and old records for their whole applicable retention horizon.

Define backfill ownership, idempotency/restart behavior, invariants, concurrency
and reconciliation. Keep runtime rollback, data restoration and forward repair
distinct. If a change is irreversible or rollback would lose accepted writes,
document a reviewed forward-repair or recovery procedure and its data-loss and
downtime implications; never promise a universal reverse migration.

Retire compatibility only when the declared consumers and retained state no
longer require it. A feature flag that disables a function does not undo its
earlier data effects. Record unresolved provider/client compatibility separately
from local fixture success.

## Limit exposure and decide whether to progress

For a service release where staged exposure is feasible, define:

- the initial population/environment and how exposure expands;
- customer-facing health, correctness and capacity metrics;
- comparison baseline, promotion/stop conditions and observation requirements;
- minimum meaningful traffic or workload and handling of inconclusive evidence;
- release/recovery ownership and an authorized stop/rollback/repair mechanism;
- flag ownership and removal condition when flags are used.

Choose controls suited to the estate: one instance, an internal cohort, a
parallel environment, a limited rollout or another supported mechanism. Do not
impose fixed percentages, bake durations, a new orchestrator or automatic rollback
where recovery is unsafe. Separate deployment from feature activation when it
reduces risk without violating business invariants.

Insufficient traffic is inconclusive, not proof of health. A green build or
configuration validation does not establish successful release or operation.
Track states such as proposed, code-verified, limited-release and operating-
accepted using the repository's vocabulary and actual evidence. Open live gates
remain open when the task is only design or local verification.

## Close the learning loop

When operation is actually within scope, connect SLO observations, incidents,
recovery exercises, failed hypotheses and operating effort to the backlog and
architecture records. Record the action owner and next authorized step. Revisit
decisions when the declared trigger occurs rather than waiting for documentation
drift. Scheduling monitors or recurring reviews is a separate user instruction.

## Primary sources

Consulted 28 October 2026; adapt their mechanisms to the project's needs:

- [Google SRE, Implementing SLOs](https://sre.google/workbook/implementing-slos/) and [Example Error Budget Policy](https://sre.google/workbook/error-budget-policy/): measurable objectives, ownership and action. The policy's numbers are examples, not defaults.
- [Google SRE, Production Readiness Reviews](https://sre.google/sre-book/evolving-sre-engagement-model/): service-specific operational review and responsibility.
- [Amazon, Ensuring rollback safety](https://aws.amazon.com/builders-library/ensuring-rollback-safety-during-deployments/): mixed-version compatibility and preparation/activation; includes a DynamoDB experience and distinct hypothetical examples.
- [Meta, Rapid release at massive scale](https://engineering.fb.com/2017/08/31/web/rapid-release-at-massive-scale/): a 2017 report of staged exposure, signals and feature activation; not evidence of a uniform current deployment policy.
