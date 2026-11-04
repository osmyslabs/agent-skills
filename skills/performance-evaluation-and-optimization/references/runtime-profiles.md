# Runtime-specific investigation

Read only the part relevant to the affected execution path. Tool names below are
examples; use tools already available and authorized in the actual environment.

## Applications and services

Trace the end-to-end critical path, then separate CPU work, allocation/GC, locks,
queueing, I/O, retries and external calls. Relate samples to realistic traffic and
resource limits. A function's inclusive CPU time is not automatically wall time.
Sampling overhead and instrumentation can change the system under investigation.

Before caching, define identity/tenant-aware keys, freshness, invalidation,
capacity, sensitive-data retention and stampede behavior. Before parallelism,
check ordering, shared state, pool/downstream limits, cancellation and failure
semantics. Before batching, check per-item authorization and partial failure.

## Databases

Inspect query shape/count, representative cardinality, plans, indexes, I/O,
transaction duration, locks and connection-pool waiting. An estimated plan is a
model; an execution plan with analysis may actually execute the statement and
have side effects. Use an eligible local/test dataset for executable analysis.
An index can increase write cost and deployment time. Removing a query predicate
or tenant constraint to improve speed changes correctness and security.

## Browser and client

Separate network transfer, parsing, execution, rendering and user-interaction
delay. Record device/network conditions and distinguish lab runs from real-user
data. A single Lighthouse score or local desktop run does not establish a field
percentile. Keep accessibility, payload correctness and privacy controls intact.

## Builds and developer workflows

Separate clean/incremental work, cache hits/misses, dependency resolution and
actual test/compile time. Compare equivalent change sets and outputs. Skipping
required tests or weakening cache keys is not a legitimate build optimization.
State how available cores, memory and daemon state affect reproducibility.
