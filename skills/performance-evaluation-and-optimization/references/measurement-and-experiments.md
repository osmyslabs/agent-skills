# Measurement and experiments

Read before producing performance comparisons or designing a benchmark.

State the question and practical acceptance rule before selecting a faster-looking
implementation. Specify the successful work unit, input sizes/distribution,
arrival/concurrency model, environment/resource limits, runtime/dependency versions,
cache/JIT state and instrumentation. Capture raw samples and command/configuration
identity so another engineer can reproduce the comparison.

Check result correctness and work completion. An optimization that omits work,
returns stale data, moves cost outside the timer or increases failures must not be
credited as a win. Measure errors/timeouts alongside throughput. Confirm the client
is not the bottleneck and that closed-loop traffic has not hidden queueing under
saturation. Observe resources while a benchmark runs when tools permit.

Separate setup from steady-state work when that matches the use case; include
cold-start cost when users actually pay it. Use matched workloads and comparable
hardware/process conditions. Repeated runs, alternating order and controlled
background activity can reduce bias. Choose repetition and duration from noise,
budget and risk, rather than imposing a universal sample count.

Report units, number of observations and distribution/variability. Distinguish
run-level variation from request-level percentiles. Small differences within
ordinary variance are inconclusive. Avoid precise confidence claims without a
justified statistical method and representative independent samples.

Keep experiment outputs local unless their publication is requested. Sanitized
synthetic reports can be committed; raw customer traces, machine paths and secret
values must not enter a public result. CPU profiles can carry sensitive labels.

## Primary sources

Consulted 29 October 2026:

- [Brendan Gregg, Active Benchmarking](https://www.brendangregg.com/activebenchmarking.html): inspect the actual limiter while measuring and verify what the harness exercises.
- [Brendan Gregg, USE Method](https://www.brendangregg.com/usemethod.html): examine utilization, saturation and errors for relevant resources; this is one investigative method, not coverage of every performance problem.
