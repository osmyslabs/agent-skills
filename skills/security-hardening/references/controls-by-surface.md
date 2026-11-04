# Controls by surface

Read the relevant surface only; these are investigation prompts, not a universal
checklist or a mandate to install tools and infrastructure.

## Applications and services

Trace identity, resource authorization, tenant context and data exposure through
all adapters. Examine input canonicalization, parameterized database access,
output encoding, safe file/path handling, callback authenticity/replay controls,
session/token lifecycle and limits where grounded in the actual design. Preserve
product ownership of roles, policy, retention and consent. Do not invent a
provider's signing protocol or weaken verification to support an integration.

For web applications/services, select applicable requirements from a reviewed
stable OWASP ASVS version and record exact identifiers only after checking them.
Selected checks establish selected controls; mobile, desktop and infrastructure
surfaces need their own applicable guidance. Do not claim full ASVS conformance
from a small sample or relabel a generic list as a threat model.

## Dependencies and delivery

Inspect resolved dependency identity, advisories, trusted origins and integrity
controls. Keep compatibility and consumer evidence with upgrades. In CI examine
untrusted pull-request inputs, script interpolation, permissions, secret exposure,
third-party actions and artifact trust. Pin immutable action revisions where
appropriate, scope tokens/jobs and separate untrusted code from privileged work.
Do not run untrusted code with secrets as a validation shortcut.

## Runtime and infrastructure configuration

Identify the actual provider/runtime, baseline, environment and operator before
changing access, network exposure, TLS, secrets, logging or container privileges.
Use official provider guidance and applicable versioned configuration benchmarks.
An in-repository setting is not evidence of the deployed setting. Assess lockout,
recovery, dependency and availability consequences before a live change; local
configuration review does not authorize applying it.

## Primary sources

Consulted 29 October 2026:

- [OWASP ASVS](https://asvs.owasp.org/): stable 5.0.0 provides verifiable requirements for web applications and services; recheck versions when applying it.
- [GitHub Actions secure use](https://docs.github.com/en/actions/reference/security/secure-use): delivery trust boundaries, restricted permissions and secret handling. Provider-specific details remain conditional.
