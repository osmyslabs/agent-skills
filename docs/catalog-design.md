# Catalog boundaries and package maintenance

Decision implemented 29 October 2026 after authorization to add three improvement
skills. This records repository design, not independent approval or a new runtime
platform.

| Outcome | Primary skill | Completion evidence |
| --- | --- | --- |
| Architecture/contract decision | project-architecture-and-blueprint | Observed baseline, decisions, acceptance and roadmap. |
| Reduce maintenance burden | technical-debt-remediation | Characterized behavior, bounded correction or justified retention and checks. |
| Explain/improve performance | performance-evaluation-and-optimization | Representative baseline, cause, comparable results, correctness and uncertainty. |
| Reduce a security risk | security-hardening | Qualified finding, owning control, abuse/legitimate tests and residual risk. |

Choose by requested outcome; categories can overlap. Reuse one finding/backlog
entry and its evidence. Significant boundary/contract changes follow the consumer
repository's decisions. No skill requires another, a provider, external account
or fixed documentation tree. Assessment-only requests remain bounded.

## Standalone packages

Each folder carries its entry point, conditional references, optional OpenAI
metadata, MIT notice, local installer and synthetic evaluation helpers. Relative
links stay within the package. A consumer can copy one folder without this
repository or siblings. Host loading and permissions remain host responsibilities.

The root installer requires an explicit catalog name. Package installers derive
destinations from the validated manifest and preserve their previous CLI.
Different packages can coexist; existing same-name destinations are refused.
The generic installer is maintained in scripts/install.py and copied byte for
byte into packages. This distribution duplication avoids a shared runtime
dependency; validation detects installer drift.

Preparation/inspection helpers and their tests are currently identical copies.
Change them together and run every package's tests. They use the selected manifest
name. Evaluation snapshots retain the license and withhold grading corpus/helpers;
they are deliberately smaller than a full installation.

## Verification and evidence

scripts/check.py discovers every skill directory, verifies package/license/link
containment and catalog routes, validates each corpus and executes each helper
suite in a separate process. Catalog integration tests install complete packages
into all three hosts' project/personal layouts and compare their bytes.

These checks establish packaging and helper behavior. Independent solver runs
need fresh isolated fixtures, actual instructions, no rubric and retained
outcomes. Record failures and limits in the [validation record](validation.md).
Do not infer model behavior, performance gains or security certification from
passing package checks. Native discovery is separate from realistic task execution.
