# Behavioral evaluation corpus

Use when maintaining this skill, not during ordinary architecture tasks.
Read [the evaluation protocol](../references/skill-evaluation.md) before grading.
The [eight cases](cases.json) contain synthetic raw fixtures, user requests and
review criteria. They require no product repository, provider account or API key.

Prepare a case from the repository root, selecting the instruction version:

```text
python skills/project-architecture-and-blueprint/evals/prepare.py --validate
python -B skills/project-architecture-and-blueprint/evals/test_prepare.py
python -B skills/project-architecture-and-blueprint/evals/test_install.py
python skills/project-architecture-and-blueprint/evals/prepare.py --case local-fix --skill skills/project-architecture-and-blueprint --output build/skill-evaluation/run-01
```

Use a fresh output path for each run. The helper records corpus/task/instruction
and initial fixture hashes. It copies only the selected skill's entry point,
references, UI metadata and license notice into the isolated workspace. It does not copy this
corpus, expected answers, earlier results or the parent repository's instructions.
It never launches an agent, installs packages or calls a model API.

This deliberately reduced instruction snapshot is not a full package install:
maintenance-only routes may refer to withheld corpus/helpers. Task-solving agents
must not follow those routes to grade themselves. Use `scripts/install.py` and
the full package for installation/reference-completeness checks.

Give an independent evaluator only `task.txt` and `workspace/`. For baseline and
candidate runs use the same case and equivalent tools/environment, with fresh
agent context. Keep the source label and rubric away from the task-solving agent.
Preserve actual final artifacts, handoff and available execution evidence.

After execution, compare the workspace against `manifest.json` and the selected
case's allowed mutations. For `local-fix`, rerun the unchanged fixture tests.
`python -B skills/project-architecture-and-blueprint/evals/inspect_run.py build/skill-evaluation/run-01`
checks actual file effects and preserves a visible corpus-version mismatch;
its exit status covers filesystem integrity, not the case's decision quality.
For design tasks, review the actual reasoning against the criteria; matching a
heading, keyword or document count is not a behavioral pass. Store rubric scores,
evidence paths and any failures outside the skill package's runtime instructions.

Preparation/corpus validation is structural evidence only. A prepared fixture
is not an executed case. Partial sample runs do not establish full-corpus or
statistical superiority, and qualitative inspection is not a complete tool trace.
Helper tests verify exact inputs, withheld case criteria, preservation of prior
evidence and filesystem boundaries; they do not grade the skill's decisions.

Use `--host codex`, `--host claude` or `--host copilot` with `prepare.py` to
select a native project install location and invocation. The default remains
Codex. For the other profiles, the fixture's `AGENTS.md` bytes are placed under
`CLAUDE.md` or `.github/copilot-instructions.md` and the mapping is recorded.
Other raw fixture bytes and review criteria remain unchanged. Six preparation
tests cover the original guarantees plus native layouts and protection of all
three hosts' skill directories. Six installation tests exercise exact copies
for project/user scopes, dry-run and refusal of invalid/existing destinations.

Only execution by the named native client establishes that client's behavior.
Profile preparation and unit tests do not establish Claude/Copilot runtime
compatibility. Preserve client/version and actual availability in the run record;
do not label a Codex solver as another agent merely because it uses that layout.
