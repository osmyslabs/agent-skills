# Behavioral evaluation corpus

Use only when maintaining this skill. Read the [evaluation protocol](../references/skill-evaluation.md).
The [four cases](cases.json) contain synthetic inputs, requests and separate review
criteria, including implementation and negative/assessment-only cases.

From the repository root:

~~~text
python -B skills/technical-debt-remediation/evals/prepare.py --validate
python -B skills/technical-debt-remediation/evals/prepare.py --case compatibility-refactor --output build/technical-debt-remediation/run-01
python -B skills/technical-debt-remediation/evals/inspect_run.py build/technical-debt-remediation/run-01
~~~

Use a fresh output path. Give the solver only task.txt and workspace/ with fresh
context; keep cases.json, expected outcomes, source labels and earlier answers
out of that context. --host codex, claude or copilot selects a native layout and
maps fixture instruction bytes to that host's entry point. Preparation never
runs an agent, installs tools, accesses accounts or calls a model.

The runtime snapshot includes instructions, references, UI metadata and license;
it withholds evaluation helpers and criteria. It is not a complete installation.
Use [the local installer](../scripts/install.py) for the full package.

Preserve raw results outside the workspace and rerun relevant unchanged tests.
The inspector checks file effects and input/task integrity; it does not grade
reasoning, performance gains, security or command/network history. Independently
review artifacts and checks against case criteria. Retain failures and inconclusive
runs, record source/task hashes and publish only sanitized evidence.

Six preparation and six installation tests cover helper invariants. They do not
execute these cases or establish native Claude/Copilot behavior. Run all catalog
checks with python -B scripts/check.py from the repository checkout.
