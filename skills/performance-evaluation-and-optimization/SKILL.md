---
name: performance-evaluation-and-optimization
license: MIT
description: Investigate and improve measured software performance using representative workloads, profiling and reproducible before/after comparisons. Use for latency, throughput, resource or cost bottlenecks and performance regressions across applications, databases, builds or services; do not optimize ordinary code speculatively.
---

# Performance Evaluation and Optimization

Explain the actual performance constraint and improve it when evidence supports
a change. A measured lack of benefit or an inconclusive experiment is a valid
result; do not claim an optimization from a plausible-looking code change.

## Define the question and permitted environment

Read repository instructions, relevant architecture, service objectives, code,
existing benchmarks and operational constraints. Identify the affected workflow,
user-visible objective, scale, data shape and resource budget. Distinguish an
accepted target from an assumption. Do not invent an SLA or fabricate telemetry.

Respect analysis-only requests. Use local/synthetic environments for experiments
within scope. A performance request does not implicitly authorize load against a
live endpoint, provider charges, production profiling or infrastructure changes.
Choose permitted local work while missing live evidence remains explicitly open.

## Establish a credible baseline

Read [Measurement and experiments](references/measurement-and-experiments.md)
before a benchmark or a before/after claim. Define the workload, environment,
versions, data, warm/cold state, concurrency, duration, measurements and stop
conditions. Reuse a sound existing harness rather than adding a dependency for
a one-off measurement. Verify the harness returns correct results and measures
the intended work rather than setup, discarded results or an overloaded client.

Select metrics for the problem: latency distribution, throughput with error rate,
CPU, memory/allocations, I/O, query count, build duration or cost per successful
unit. Match sample sizes and measurement resolution to the claim. A mean alone
can hide tail latency; a tiny sample cannot establish a stable p99.

## Find a cause before choosing a fix

Use traces, profiles, query plans, resource counters or bounded instrumentation
to distinguish busy work, waiting, contention, I/O and external latency. Inspect
the load generator as well as the system. Treat source inspection as a hypothesis
when execution evidence is absent. Read [Runtime profiles](references/runtime-profiles.md)
for application, database, browser or build-specific considerations.

Connect the proposed change to an observed limiting factor. Compare the smallest
credible alternatives, including doing nothing when the target is already met.
Caching, batching, parallelism and new indexes each have correctness and resource
costs; choose them from the actual access pattern and failure semantics.

## Change and compare

When implementation is authorized, change one useful cause or keep distinct
changes separately attributable. Preserve outputs, authorization, tenant/data
isolation, ordering, durability and compatibility unless the user authorizes a
changed contract. A faster wrong answer is a regression. Characterize any
intentional trade-off and its accepted owner/limit.

Compare equivalent workloads and environments, repeat sufficiently for observed
variability, and inspect resource/error trade-offs. Retain negative results.
If a proposed patch fails acceptance, do not leave it as a successful optimization;
report the evidence and restore/revise only changes you own, preserving unrelated
user work. Keep output comparison and relevant functional tests independent of
the benchmark. Run focused checks and document what could not be measured.

Do not extrapolate a microbenchmark into service capacity or production savings.
For noisy hosted CI, distinguish correctness checks from performance gates;
use a stable environment, a justified tolerance and ownership before introducing
a blocking regression threshold.

## Report and maintain

Record the exact workload/commands, baseline and candidate data, environment,
observed cause, effect and uncertainty, functional checks, costs and remaining
limits. A source-only investigation should end with hypotheses and a concrete
measurement plan. Update existing performance budgets or architecture decisions
only when their assumptions or accepted contracts actually change.

## Installation and maintenance

Use [Agent hosts and portability](references/agent-hosts.md) for installation and
invocation. No other skill, profiler, provider API or Python runtime is required
by the instructions; actual measurements depend on available tools.

For instruction changes, use the [evaluation protocol](references/skill-evaluation.md)
and [synthetic cases](evals/README.md). Structural checks do not run a benchmark
or prove an improvement; task-solving agents should not read the grading corpus.
