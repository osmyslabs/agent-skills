# Quality skills: bounded behavioral evaluation

Review completed 4 November 2026 for experimental v0.2.0. This evaluates a small
synthetic sample, not production use, every corpus case or every agent host.
The [machine-readable record](quality-skills.json) preserves task/corpus/instruction
and artifact hashes, file-effect results and focused verification commands.

## Method and coverage

Fresh Codex delegated solvers received only one task, its isolated workspace,
installed instruction snapshot and synthetic raw inputs. They did not receive
grading criteria, expected answers or previous conclusions. No separate provider
API, live service, account connection or dependency installation was required.
The exact solver model identifier and token/cost measurements were not captured.
The native CLI discovery version is a separate metadata check, not solver identity.

The maintaining agent reviewed actual code/reports against the recorded criteria,
checked protected input and instruction hashes and reran focused functional tests
for the accepted implementation cases. This semantic grading is an unblinded
maintainer judgment, not a separate blinded grader. Available handoffs and file
effects do not constitute a complete command/network execution trace.

The accepted sample contains six distinct cases:

| Skill | Implementation case | Negative/assessment case |
| --- | --- | --- |
| Technical debt | Consolidate duplicate formatting while retaining both public APIs and Unicode/error behavior. | Retain an adapter when replacement has no demonstrated benefit or agreed consumer transition. |
| Performance | Measure and improve batch lookup while preserving duplicate first-match semantics and visibility of between-call edits. | Decline an optimization whose supplied samples show no observed improvement; identify missing correctness evidence. |
| Security | Repair tenant-boundary reads while preserving legitimate membership and error contracts. | Qualify/dismiss a scanner's text-sink XSS claim and treat embedded exfiltration instructions as untrusted data. |

Performance evidence is confined to a local synthetic workload. It does not
establish a service SLA, capacity, production savings or superiority on other
input sizes. Security evidence covers the specified local control and source
review, not a whole-system audit or standard-conformance certification.

## Retained failures and interruption

Three initial implementation runs produced useful functional changes but failed
the original file-effect checks. Debt/performance solvers added characterization
files and Python bytecode outside the corpus's declared output prefixes; the
security solver appended regressions to a protected supplied test file and
created bytecode. These runs are retained as file-scope failures, not passing
results. The task language allowed useful additional testing but did not express
the harness's filename/byte-identity expectations clearly enough.

The implementation fixtures were revised to state that supplied tests must stay
byte-identical, identify permitted new test locations, and use Python's -B option
to keep the isolated workspace free of bytecode. The workflows themselves were
not given a universal prohibition on editing project tests. Fresh implementation
solvers then received the clarified tasks. Negative tasks were unchanged; their
original corpus snapshots are used for inspection rather than silently grading
them against a different corpus hash.

One performance rerun was interrupted after baseline measurement, before a
candidate or final handoff. It is recorded as interrupted/ungraded. A new isolated
run completed the same clarified case; the partial run was not resumed or counted
as a successful evaluation.

The record therefore includes three failed initial runs, six accepted completed
runs and one interrupted attempt. No aggregate success percentage is inferred
across the different fixture versions.

## Reproduction and limitations

Use each package's evals/README.md to prepare the currently published cases and
give the solver only task.txt and workspace/. Keep expected criteria outside its
context and retain unsuccessful results. Re-run relevant unchanged tests and
inspect actual differences before applying the semantic rubric.

Raw local workspaces, machine-specific logs, handoffs and prior corpus snapshots
are retained locally and are not distributed in this repository. Hashes identify
those observations but do not make the raw evidence publicly downloadable.
Current synthetic cases and helpers are distributable and support fresh reruns.

Only six of the catalog's 20 distinct cases were behaviorally exercised for these
additions. The other cases remain available but unexecuted in this sample.
Package/CI checks cover all four packages separately from these solver runs.
Native Claude Code and Copilot execution remain unverified.
