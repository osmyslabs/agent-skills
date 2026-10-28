# Agent Skills repository instructions

Read README.md, docs/validation.md and the affected skill before changing it.
This repository contains public engineering instructions and synthetic fixtures.
It does not own product authorization, persistence, credentials or operations.

- Preserve the open skill format, canonical skill name and relative references.
- Keep the common workflow independent of a particular provider or agent API.
- Distinguish structural checks, native discovery, behavioral evaluation and live
  operating evidence. Never infer a model run from a passing package test.
- Use synthetic inputs only. Keep internal product material, raw local traces,
  personal paths and credentials out of public commits and CI logs.
- The installed skill must retain its MIT license. External references keep their
  existing attribution and rights.
- Changes to invocation, authority, host placement or output requirements need
  explicit rationale and appropriately scoped verification.

Run from the repository root:

```text
python -B scripts/verify.py
python -B skills/project-architecture-and-blueprint/evals/prepare.py --validate
python -B skills/project-architecture-and-blueprint/evals/test_prepare.py
python -B skills/project-architecture-and-blueprint/evals/test_install.py
```

Keep temporary installations and test outputs under ignored build/ or a temporary
directory. Do not install missing AI clients, call paid models, link accounts,
deploy or publish a release merely because a fixture describes those actions.
