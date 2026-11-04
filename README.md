# Osmys Agent Skills

Reusable engineering workflows for agents that support the open
[Agent Skills format](https://agentskills.io/specification).

**Status: experimental.** These skills support architecture and evidence-backed
improvements within the requested scope. The four-skill catalog is distributed
in the experimental v0.3.0 release. v0.2.0 added the improvement skills; v0.3.0
integrates feature implementation blueprints into the architecture skill.

| Skill | Use it for |
| --- | --- |
| [Project Architecture & Blueprint](skills/project-architecture-and-blueprint/SKILL.md) | Project architecture, governance and roadmaps, or an end-to-end implementation blueprint for one business feature. |
| [Technical Debt Remediation](skills/technical-debt-remediation/SKILL.md) | Prioritize demonstrated debt, preserve contracts and remediate a bounded slice or justify retention. |
| [Performance Evaluation and Optimization](skills/performance-evaluation-and-optimization/SKILL.md) | Measure representative workloads, find bottlenecks and verify correctness-preserving improvements. |
| [Security Hardening](skills/security-hardening/SKILL.md) | Triage findings, strengthen controls and verify abuse rejection and legitimate behavior. |

The root [llms.txt](llms.txt) provides a concise documentation index with links to
raw Markdown for AI tools that choose to use it. This follows the optional
[llms.txt proposal](https://llmstxt.org/), originally intended for websites. In
this GitHub repository it is a navigational aid; automatic discovery or search
indexing is not guaranteed. The skill entry point remains `SKILL.md`, and
repository contributor instructions remain in `AGENTS.md`.

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

Copy the complete `skills/<skill-name>` folder for the selected skill into the
location recognized by your host. Keep its `LICENSE`, references and resources
together. For reproducible use, pin a reviewed commit or release tag and review
upgrades before replacing a local copy.

| Agent | Project location | Personal location | Invocation |
| --- | --- | --- | --- |
| Codex | `.agents/skills/<skill-name>/` | `~/.agents/skills/<skill-name>/` | `$<skill-name>` |
| Claude Code | `.claude/skills/<skill-name>/` | `~/.claude/skills/<skill-name>/` | `/<skill-name>` |
| GitHub Copilot | `.github/skills/<skill-name>/` | `~/.copilot/skills/<skill-name>/` | Ask to use the skill by name or explicit file. |

Alternatively, the local installer uses Python 3.10+ and only the standard library.
Replace the example destination with an existing project directory:

```text
python scripts/install.py --skill technical-debt-remediation --agent codex --root "<project-directory>" --dry-run
python scripts/install.py --skill technical-debt-remediation --agent codex --root "<project-directory>"
```

Select any catalog name with `--skill`. Each package also retains its own
standalone scripts/install.py, usable without the repository checkout.
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

For one feature, ask the same skill to trace that business capability end to end.
Its [feature workflow](skills/project-architecture-and-blueprint/references/feature-implementation-blueprint.md)
reuses existing architecture and documentation conventions, curates significant
functions and follows asynchronous/data boundaries. This mode needs no separate
feature-implementation skill. Explanation-only requests stay read-only unless
writing documentation is requested.

Choose the primary skill by the requested outcome and reuse existing finding
records when categories overlap. Each skill is independently usable; see the
[catalog design](docs/catalog-design.md) for boundaries and maintenance.

## Verification and limitations

The repository includes 48 offline preparation/installation tests, three catalog
integration tests and 22 synthetic task fixtures. They check package copying, scoped destinations,
preservation of existing files and evaluation isolation. They do not execute
models or prove architectural quality. Native Claude Code and Copilot behavior
remain unverified; package placement does not certify every agent or cloud surface.
See the [validation record](docs/validation.md) for the actual evidence scope.

From the repository root, with Python 3.10+:

```text
python -B scripts/verify.py
python -B scripts/check.py
```

Each package's evals/README.md explains isolated task preparation and grading.
The CI discovers every skill and runs offline checks on
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
