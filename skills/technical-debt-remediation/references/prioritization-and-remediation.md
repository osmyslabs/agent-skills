# Prioritization and remediation decisions

Read for debt assessments, competing remediation items or an uncertain payoff.

Record only facts that support a decision. A useful item names the current
constraint, evidence, affected consumer, consequence of waiting, remediation
option, compatibility risk, cost estimate/confidence, owner and revisit trigger.
Separate the one-time repayment effort from recurring maintenance cost. Do not
turn ordinal estimates into a precise financial ROI without measured inputs.

Compare the smallest credible options: leave/accept, document/contain, repair a
local boundary, replace a dependency incrementally, or investigate first. Existing
code that is rarely changed and has a required stable interface may reasonably
remain. Explain which future change or failure would alter that decision.

Prioritize demonstrated impact and urgency alongside effort and disruption.
Examples include build failures blocking releases, repeated manual work, an
unsupported dependency actually used at runtime or a frequently changed boundary
whose coupling causes defects. Check timestamps, scope and attribution before
using incidents or historical reports as current evidence.

Choose one bounded slice with acceptance criteria and a recovery path. For a
large migration, preserve working consumer paths and define the order, transition
contract and retirement trigger. Creating empty new layers is not a completed
migration. A consumer test or representative use case is more useful than a
generic reduction in line count.

If an item is already tracked as a security finding or performance investigation,
link the evidence and keep one owner/acceptance record. Routing does not require
installation of another skill or execution of every quality workflow.

## Primary source

Consulted 29 October 2026:
[Google Research, Defining, Measuring, and Managing Technical Debt](https://research.google/pubs/defining-measuring-and-managing-technical-debt/)
frames debt as both a human and technical management problem. The decision record
above is this skill's adaptable method, not a claim to reproduce Google's process.
