# Osmys Agent Skills

Reusable engineering workflows for agents that support the open
[Agent Skills format](https://agentskills.io/specification).

**Status: experimental.** The first skill helps agents create and maintain an
intentional architecture, record decisions and verify implementation without
silently changing a project's scope or authority.

| Skill | Use it for |
| --- | --- |
| [Project Architecture & Blueprint](skills/project-architecture-and-blueprint/SKILL.md) | Architecture baselines, researched decisions, bounded experiments, implementation contracts, drift analysis and evidence-backed roadmaps. |

## What the skill does

The workflow starts from the actual repository and its constraints, investigates
important unknowns, documents decisions, implements only authorized work and
verifies the result. Conditional references cover domain boundaries, security,
capacity/cost, service objectives, safe migrations and infrastructure lifecycle.
Small fixes stay small; the skill does not require a new framework, microservices,
an architecture committee or a fixed documentation tree.

Normal use requires no provider API key, model SDK or Python installation.
The agent needs access to the files and tools appropriate to the requested task.
Unavailable checks stay explicitly unverified. Agent instructions supplement the
host's policies and current user request; they do not grant new permissions.

## Install

Download this repository at a reviewed commit or release, or clone it:

```sh
git clone https://github.com/osmyslabs/agent-skills.git
cd agent-skills
```

Copy the complete `skills/project-architecture-and-blueprint` folder into the
location recognized by your host. Keep its `LICENSE`, references and resources
together. For reproducible use, pin a reviewed commit or release tag and review
upgrades before replacing a local copy.

| Agent | Project location | Personal location | Invocation |
| --- | --- | --- | --- |
| Codex | `.agents/skills/project-architecture-and-blueprint/` | `~/.agents/skills/project-architecture-and-blueprint/` | `$project-architecture-and-blueprint` |
| Claude Code | `.claude/skills/project-architecture-and-blueprint/` | `~/.claude/skills/project-architecture-and-blueprint/` | `/project-architecture-and-blueprint` |
| GitHub Copilot | `.github/skills/project-architecture-and-blueprint/` | `~/.copilot/skills/project-architecture-and-blueprint/` | Ask to use the skill by name or explicit file. |

Alternatively, the local installer uses Python 3.10+ and only the standard library.
Replace the example destination with an existing project directory:

```text
python skills/project-architecture-and-blueprint/scripts/install.py --agent codex --root "<project-directory>" --dry-run
python skills/project-architecture-and-blueprint/scripts/install.py --agent codex --root "<project-directory>"
```

Use `--agent claude` or `--agent copilot` for another host. For personal use,
add `--scope user` and explicitly pass the intended user home as `--root`.
The installer refuses existing destinations and does not download anything,
link accounts or change host configuration. Manual folder copying needs no Python.

Avoid duplicate same-name installations. Native locations, personal/cloud
availability and invocation depend on the host surface and version; see the
[host guide](skills/project-architecture-and-blueprint/references/agent-hosts.md).
OpenAI UI metadata is optional and separate from the common instructions.

## Try it

```text
Use project-architecture-and-blueprint to inspect this repository and prepare
an architecture baseline and implementation roadmap. Preserve the existing
repository instructions and ADR conventions. Do not begin implementation.
```

Use your host's native skill command or identify its installed `SKILL.md` file.
An agent without a skill loader can read the instructions and relevant references
explicitly; automatic discovery and adherence are not guaranteed by the format.

## Verification and limitations

The repository includes 12 offline preparation/installation tests and eight
synthetic task fixtures. They check package copying, scoped destinations,
preservation of existing files and evaluation isolation. They do not execute
models or prove architectural quality. Native Claude Code and Copilot behavior
remain unverified; package placement does not certify every agent or cloud surface.
See the [validation record](docs/validation.md) for the actual evidence scope.

From the repository root, with Python 3.10+:

```text
python -B scripts/verify.py
python -B skills/project-architecture-and-blueprint/evals/prepare.py --validate
python -B skills/project-architecture-and-blueprint/evals/test_prepare.py
python -B skills/project-architecture-and-blueprint/evals/test_install.py
```

The [evaluation guide](skills/project-architecture-and-blueprint/evals/README.md)
explains isolated task preparation and grading. The CI runs offline checks on
Linux and Windows. It never installs an AI client, calls a provider or evaluates
a model's output.

## Contribute and license

Maintained by [Osmys Labs](https://github.com/osmyslabs). Contributions should
address demonstrated behavior or improve portability with reproducible evidence;
see [CONTRIBUTING.md](CONTRIBUTING.md). Support is best effort during the
experimental phase, with no guaranteed response time or production certification.

Code and original instruction text are licensed under [MIT](LICENSE).
The same license is included in the installable skill folder. Linked external
publications retain their own rights; they are references, not relicensed content.
