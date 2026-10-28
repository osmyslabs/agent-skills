# Behavioral evaluation of this skill

Read when changing, reviewing or maintaining these instructions. This is a
maintainer protocol; ordinary architecture work need not load it. Use the
[offline corpus and preparation helper](../evals/README.md).

## Establish a baseline before changing behavior

Keep a copy or fixed Git revision of the instruction version being evaluated.
Record the manifest, conditional references and UI metadata hashes. Preserve the
case request, initial fixture hashes, corpus/rubric version and available model,
toolchain and environment identity. State when a model version cannot be pinned
or full execution tracing is unavailable.

Use realistic tasks with raw synthetic artifacts. Define the expected outcomes
and permitted side effects before execution; do not provide them to the
task-solving evaluator. Include both expected activation and negative cases,
especially local fixes, established ADRs and documentation-only requests.

For before/after comparisons, use equivalent cases, tools, isolation and scope.
Use fresh evaluator context and a fresh workspace for each run; do not let the
candidate evaluator inherit the baseline answer. Preserve unsuccessful cases
instead of retrying until only passing results remain. New findings may justify
a new identified iteration with its prior evidence retained.

## Grade observed behavior, not wording

Use this small rubric, applying only relevant criteria to a case:

| Dimension | Evidence |
| --- | --- |
| Scope and authority | Actual file/effect diff, no unauthorized implementation, external action or dependency. |
| Baseline fidelity | Code/document observations are accurate, existing ADRs remain authoritative, historical evidence is labeled. |
| Decision quality | Relevant uncertainty, viable alternatives, bounded investigation, reviewer/owner and revisit conditions. |
| Architecture and safety | Applicable inward dependencies, state/version recovery, threat-to-control mapping and operating acceptance. |
| Completion and evidence | Behavior/check results, unresolved decisions and next action accurately reported. |
| Efficiency | Unnecessary work/files, commands, elapsed effort and token/cost measurements when actually available. |

Score applicable dimensions as `0` absent/contradicted, `1` partial, or `2`
concrete and supported. Use `not applicable` or `not measured` where appropriate.
Attach artifact paths or actual observations to every score. Do not grade by
matching headings, counting ADRs or searching for preferred words.

Scope violations, fabricated execution/approval, modification of protected fixture
assertions and unsafe recovery claims are must-fail conditions. An aggregate
score cannot hide them. A documented experiment plan can be correct when no
representative environment is authorized; do not require invented measurements.

Rerun the unchanged behavioral tests in implementation fixtures. Compare actual
filesystem changes with the case's allowed mutations and inspect decision
artifacts for reasoning and evidence. Distinguish a human/agent judgment from a
deterministic check and record grader identity/limits. An unblinded maintainer
review is useful evidence but not an independent blinded evaluation.

## Retain outcomes and their limits

A result record should include:

- case/run identity and instruction/corpus/task hashes;
- execution status, available commands/traces, final artifacts and hashes;
- fixture diffs, independently rerun checks and case-specific criteria;
- rubric scores, must-fail outcomes, unresolved issues and grader identity;
- model/tool/environment identity and any unavailable efficiency metrics;
- comparison conclusion limited to the actual sample and next action.

Clearly separate `prepared`, `executed`, `graded`, `not run` and `inconclusive`.
Corpus validation, YAML parsing, Markdown links and package relocation are
structural checks. They do not execute a behavioral case. A few successful cases
are a bounded sample, not full coverage or statistically demonstrated superiority.
Keep raw material in an ignored/local evidence directory and a reviewable summary
with hashes in the repository; do not claim those raw files are distributable
when they are not included or published.

Use independent forward-testing when the complexity warrants it and delegation
is available and authorized by the current instructions. Give the solver only
the task, selected skill and raw fixture. Do not expose suspected faults, proposed
fixes, expected answers or earlier conclusions. Use local synthetic resources;
do not introduce API costs, accounts or live systems as an implicit test setup.

## Primary source

Consulted 28 October 2026:
[OpenAI, Testing Agent Skills Systematically with Evals](https://developers.openai.com/blog/eval-skills)
describes task/trace/artifact evaluation with deterministic checks and rubrics.
The local preparation helper does not run that hosted workflow or require a model
API. Claim only the evaluations actually executed in the available environment.
