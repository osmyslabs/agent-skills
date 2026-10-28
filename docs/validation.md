# Validation record

Public package: `project-architecture-and-blueprint`, experimental `v0.1.0`.
Recorded 28 October 2026. This is a bounded verification record, not a claim of
universal agent compatibility or production certification.

## Reproducible offline checks

The commands in [README.md](../README.md#verification-and-limitations) verify:

- Canonical manifest fields, a complete MIT notice inside the installed package,
  UTF-8 source files, Python syntax and local Markdown link containment.
- Eight synthetic evaluation cases and their preparation metadata.
- Six preparation tests covering instruction/license preservation, isolated output,
  host-specific instruction mapping and exclusion of evaluation answers/helpers
  from the runtime snapshot.
- Six installation tests covering full-package copying, all three host profiles
  and two scopes, byte identity, dry-run behavior, refusal of overwrites,
  invalid destinations and preservation of existing configuration.

The complete public package is also copied and byte-compared for all six
host/scope combinations. The repository validator rejects linked filesystem
entries in the distribution; the 12 helper tests do not exercise every operating
system's symlink/junction behavior.

Local checks use Python 3.12 and 3.13 on Windows. The repository's
[workflow](../.github/workflows/validate.yml) runs the same offline checks on
Linux and Windows with Python 3.10 and 3.13. A workflow result is evidence for
that revision only; inspect the associated commit and run before relying on it.

The validator checks local link targets, not external URL availability or every
Markdown anchor. Helper tests do not execute an AI model or measure its quality.

## Native hosts and behavior

| Verification | Evidence and limits |
| --- | --- |
| Codex local skill discovery | Checked with Codex CLI `0.165.0-alpha.1.2` on Windows using an isolated project installation and the native `skills/list` API. The installed skill was enabled and had no package loading errors. No task/model execution was part of this probe. |
| Claude Code | Native client execution has not been tested. Folder placement and fixture preparation are tested offline; they do not establish discovery or adherence. |
| GitHub Copilot | Native client execution has not been tested. Folder placement and fixture preparation are tested offline; they do not establish discovery or adherence. |
| Behavioral evaluation | Eight synthetic tasks and an inspection helper are supplied for independent reruns. CI does not execute them with a model. No portable behavioral success rate is claimed for this public release. |

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
