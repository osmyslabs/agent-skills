# Agent hosts and portability

Read when installing or invoking this package, or adapting its use/evaluation to
a host's available capabilities. These instructions target the open Agent Skills
format. They do not assert support by every agent or every cloud/IDE surface.

## Common contract

`SKILL.md` contains the name/description and workflow; relative references carry
conditional detail. Keep the whole folder together. Other directories such as
`evals/` and `scripts/` support maintenance and local installation. Normal
architecture work requires no Python, provider API key or vendor-specific tool.

Read the repository's actual instruction entry points and scoped rules using
the host's precedence. `AGENTS.md`, `CLAUDE.md` and
`.github/copilot-instructions.md` are examples, not mutually interchangeable
configuration. Do not rename them or create parallel governance without need.
When files conflict, expose the conflict and follow the applicable instruction
hierarchy; the skill does not supersede host policy or the user's current scope.

Required capabilities depend on the task: reading repository files for analysis,
writing for deliverables, and execution tools for actual test claims. Web access
is useful for current research but may be unavailable; keep such evidence open.
Do not simulate missing tools, bypass host permissions, or obtain credentials
just to make a workflow appear complete. Independent evaluation remains optional
and conditional on delegation availability and authorization.

## Local installation profiles

Each path below is relative to an explicitly selected project root or user home.
The selected host/version/session must support loading that location.

| Host | Project folder | Personal folder | Invocation |
| --- | --- | --- | --- |
| Codex | `.agents/skills/project-architecture-and-blueprint` | `.agents/skills/project-architecture-and-blueprint` | `$project-architecture-and-blueprint` or explicit file reference. |
| Claude Code | `.claude/skills/project-architecture-and-blueprint` | `.claude/skills/project-architecture-and-blueprint` | `/project-architecture-and-blueprint` or explicit file reference. |
| GitHub Copilot | `.github/skills/project-architecture-and-blueprint` | `.copilot/skills/project-architecture-and-blueprint` | Ask to use `project-architecture-and-blueprint` and identify its file if needed. Invocation UI depends on the surface. |

Claude's personal filesystem location does not make a skill available in every
Cowork/cloud session. Copilot locations also depend on the surface and settings.
For a team repository, select one supported project location where practical;
Copilot can also recognize `.agents/skills` and `.claude/skills` on supported
surfaces. Do not install duplicate same-name copies without understanding which
one the host loads. No global configuration or account linking is needed by this
package's local copy workflow.

The optional `agents/openai.yaml` contains OpenAI UI metadata and a Codex example
prompt. Common instructions never require it to be interpreted. There is no
MCP dependency, tool allowlist or permission bypass in this package. Hosts may
ignore metadata they do not recognize; the supported common entry point is
`SKILL.md`, not a plugin manifest.

## Install from a reviewed local checkout

The [local installer](../scripts/install.py) uses Python 3.10+ and the standard
library. From this repository checkout, substitute an actual destination:

```text
python skills/project-architecture-and-blueprint/scripts/install.py --agent codex --root <project-directory> --dry-run
python skills/project-architecture-and-blueprint/scripts/install.py --agent claude --root <project-directory>
python skills/project-architecture-and-blueprint/scripts/install.py --agent copilot --scope user --root <user-home-directory>
```

Default scope is `project`. `--root` must already exist. Use `--scope user` only
with the intended user home explicitly selected. Without `--dry-run`, the script
copies the package into the host's selected folder. It performs no downloads,
account access, environment changes or host configuration edits. It refuses any
existing skill destination, even an empty one; upgrades require a deliberate
review/restoration plan rather than silently overwriting local customizations.

Review the planned path and source revision first. For manual installation,
copy the complete package to the chosen folder; Python is unnecessary for that
operation. Clone/download a reviewed commit or release tag before copying.
Host-specific installers are optional alternatives, not dependencies.

An agent without native Agent Skills support may read `SKILL.md` and its needed
references explicitly. That is manual instruction use; it does not establish
automatic discovery or guaranteed adherence.

## Verification levels

Keep these claims distinct:

1. Common format and internal links checked.
2. Exact package copy, destination and reference resolution checked per profile.
3. Native host lists/loads the skill using its own installed client.
4. The host executes a realistic task and its artifacts/side effects are graded.

An isolated test that checks `.claude/skills` paths is level 2, not a Claude
runtime test. A Codex evaluator reading a Claude-shaped fixture is still Codex.
Record host/version, scope, entry point, commands/results and unperformed levels.
Do not install a missing client, link an account or call a paid model implicitly
as a portability check. The [evaluation corpus](../evals/README.md) can prepare
native instruction files and installation layouts for the three profiles.

## Official sources

Checked 28 October 2026; recheck before changing loading behavior:

- [Agent Skills specification](https://agentskills.io/specification): common manifest and relative resources.
- [OpenAI, Build skills](https://learn.chatgpt.com/docs/build-skills): Codex discovery, invocation and optional metadata.
- [Claude Code, Skills](https://code.claude.com/docs/en/skills) and [project instructions](https://code.claude.com/docs/en/memory): native skill locations, commands and scoped instruction behavior.
- [GitHub, Agent skills](https://docs.github.com/en/copilot/concepts/customizations/agent-skills) and [adding skills](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills): Copilot locations and surface-dependent loading.
