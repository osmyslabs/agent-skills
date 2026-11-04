# Validation record

Public catalog: four independently installable skills, experimental `v0.3.0`.
Updated 4 November 2026, retaining the original 28 October checks below. This is
a bounded verification record, not a claim of universal agent compatibility or
production certification.

## Reproducible offline checks

The commands in [README.md](../README.md#verification-and-limitations) verify:

- Canonical manifest fields, a complete MIT notice inside the installed package,
  UTF-8 source files, Python syntax and local Markdown link containment. Owned
  raw-document URLs in the root llms.txt index are mapped to files in the current
  checkout and checked for existence and containment without network access.
- Twenty-two synthetic evaluation cases and their preparation metadata: ten for
  architecture and four for each improvement skill.
- Six preparation tests per package covering instruction/license preservation,
  isolated output,
  host-specific instruction mapping and exclusion of evaluation answers/helpers
  from the runtime snapshot.
- Six installation tests per package covering full-package copying, all three
  host profiles
  and two scopes, byte identity, dry-run behavior, refusal of overwrites,
  invalid destinations and preservation of existing configuration.

Three catalog integration tests additionally verify selection/refusal of unsafe
names, coexistence and byte identity of all four full packages across all six
host/scope combinations. They execute each installed package's own installer in
dry-run mode outside the source repository. The repository validator rejects
linked filesystem entries; the 48 helper tests do not exercise every operating
system's symlink/junction behavior.

The v0.2.0 catalog checks were rerun with Python 3.13 on Windows on 4 November
2026. The original architecture package was previously checked with Python 3.12
and 3.13. The repository's
[workflow](../.github/workflows/validate.yml) runs the same offline checks on
Linux and Windows with Python 3.10 and 3.13. A workflow result is evidence for
that revision only; inspect the associated commit and run before relying on it.

The [first hosted run](https://github.com/osmyslabs/agent-skills/actions/runs/40780382718)
exposed a Windows test comparison between short and expanded temporary-path
spellings. The expected destination is now resolved before comparison; all
file-preservation and byte-copy assertions remain in place. The failed run is
retained in Actions rather than counted as a passing result.

The validator checks local link targets, not external URL availability or every
Markdown anchor. Helper tests do not execute an AI model or measure its quality.

## Native hosts and behavior

| Verification | Evidence and limits |
| --- | --- |
| Codex local skill discovery | Architecture discovery checked on 28 October and all four skills checked on 29 October 2026 with Codex CLI `0.165.0-alpha.1.2` on Windows in an isolated project via native `skills/list`. All were enabled without package loading errors. No task/model execution was part of this probe. |
| Claude Code | Native client execution has not been tested. Folder placement and fixture preparation are tested offline; they do not establish discovery or adherence. |
| GitHub Copilot | Native client execution has not been tested. Folder placement and fixture preparation are tested offline; they do not establish discovery or adherence. |
| Behavioral evaluation | The [v0.2.0 evaluation report](evaluation/quality-skills.md) records six selected cases from that release's 20-case corpus. The [feature-mode report](evaluation/feature-integration.md) covers two added cases in v0.3.0. The current catalog has 22 cases; these samples do not establish full-corpus coverage. CI does not execute tasks with a model. |

The Codex discovery probe used dedicated runtime state, without linking an
account or starting a conversation. The client may attempt its own background
catalog retrieval; this check is not a strict offline/network-isolation test.
It establishes metadata discovery, not automatic selection, correct tool use or
compliance with every instruction.

The [host guide](../skills/project-architecture-and-blueprint/references/agent-hosts.md)
records the official sources for the installation conventions. Support can vary
by host version, IDE, cloud surface and settings. An agent that reads the files
manually still needs appropriate tools and authorization for the requested task.

## Re-evaluation

Keep discovery, package integrity, model behavior and live operational evidence
separate. When changing authority rules or host loading behavior, prepare an
isolated fixture and record the real client/version, commands, generated outputs
and unperformed checks. Publish sanitized summaries or synthetic reproductions;
do not commit credentials, personal filesystem paths or raw private traces.
