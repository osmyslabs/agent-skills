---
name: technical-debt-remediation
license: MIT
description: Assess, prioritize and remediate demonstrated technical debt in an existing repository while preserving required behavior and compatibility. Use for a debt assessment, targeted refactoring, fragile tests or build workflows, obsolete dependencies or an agreed modernization slice; ordinary feature work does not require a debt campaign.
---

# Technical Debt Remediation

Reduce a demonstrated maintenance burden through bounded, verifiable changes.
Keep a valid outcome open: retain an intentional compromise when remediation
cost or compatibility risk exceeds its current benefit.

## Establish the requested outcome

Read applicable repository instructions, accepted architecture/ADRs, current
backlog and relevant code/tests. Reuse their paths and conventions. Distinguish
an assessment, a remediation plan and authorized implementation. An audit-only
request permits analysis and its requested outputs, not runtime edits.

Choose a concrete problem: repeated failure, expensive change, unsupported
dependency, fragile integration, slow feedback or a violated accepted boundary.
An unfamiliar style, old date or low coverage number alone does not establish
debt. Inspect callers and consumers before declaring code dead or duplicated.
When ownership or a critical contract is unknown, record that uncertainty and
continue independent work rather than inventing a replacement contract.

## Establish evidence and priority

Read [Prioritization and remediation](references/prioritization-and-remediation.md)
when assessing multiple items or deciding whether repayment is worthwhile.
Record the evidence path/revision, observed burden, affected consumers, risk of
inaction, expected benefit, remediation cost/risk and confidence. Use available
history or incidents only when actually inspected; do not invent churn or ROI.

Choose fix, contain, investigate, defer or accept with a reason and revisit
condition. Respect product priorities and maintenance capacity. A vulnerability
or performance issue can share the same backlog item; follow its security or
measurement acceptance criteria instead of opening duplicate campaigns.

## Characterize before changing

Read [Compatibility and characterization](references/compatibility-and-characterization.md)
before refactoring behavior, replacing dependencies or changing persisted or
cross-module contracts. Establish representative existing behavior and run the
relevant baseline checks. Identify which quirks are contractual, accidental or
still undecided. Do not preserve a confirmed defect as a desired invariant.

Separate a behavior-preserving refactor from an intentional behavior change.
Use existing tests where they establish the contract; add focused characterization
or regression checks for unprotected behavior that the change can affect. A test
failure already present at baseline is evidence, not an improvement to claim.

## Remediate the smallest useful slice

When implementation is authorized, make a complete bounded change with its tests
and necessary documentation. Resolve routine details within scope without
requesting approval for every edit. Avoid unrelated cleanup, speculative layers,
mass dependency upgrades or a full rewrite to solve one maintenance problem.

Preserve public APIs, serialization, error/ordering semantics, authorization,
transaction and concurrency behavior unless their change is authorized. Follow
accepted architecture decisions. If a solution changes a material boundary or
contract, record the impact and use the repository's decision process; do not
silently redefine it. A reversible code revert may not reverse written data.

Run focused checks, inspect the final diff and verify the original problem is
addressed. Deleting tests, suppressing diagnostics or lowering thresholds does
not repay debt unless that specific policy change is justified and authorized.
If evidence contradicts the proposed fix, revise or stop that fix and report why.

## Close with evidence

Report what changed or was deliberately retained, exact checks and their limits,
remaining risk, owner/revisit condition where known and the next scoped action.
Update existing debt tracking or architectural records when affected. Do not
require a new document tree or a debt register for a single local correction.
Distinguish source quality, tested behavior and observed operating outcomes.

## Installation and maintenance

Use [Agent hosts and portability](references/agent-hosts.md) for local installation
and invocation. No other skill or provider API is required. Use available host
tools and disclose checks that could not run.

For instruction changes, use the [evaluation protocol](references/skill-evaluation.md)
and [synthetic cases](evals/README.md). Package checks are separate from executed
behavioral evaluations; task-solving agents should not read the grading corpus.
