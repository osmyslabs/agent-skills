# Feature Blueprint Template

Use this structure selectively. Core concerns are marked **Core** and may be combined for a small capability. Include a conditional section only when applicable; omit empty headings and duplicate inventories.

# <Feature Name>

> Source of truth for the `<feature-slug>` business capability.

## 1. Two-Minute Summary — Core

- **Business purpose:**
- **Trigger(s):**
- **Final outcome:**
- **Primary orchestrator:**
- **Main path:** `<entry>` → `<orchestrator>` → `<effects>`
- **Primary persistence:**
- **External systems:**
- **Highest-risk shared component:**
- **Biggest known risk or evidence gap:**

## 2. Identity and Scope — Core

### In scope

### Out of scope

### Evidence legend

- **Confirmed:** directly supported by repository evidence.
- **Inferred:** supported indirectly; uncertainty is stated.
- **Unverified:** not confirmed by an available path.
- **Not found in repository:** searched for but absent.

## 3. Feature at a Glance — Core

<Compact flow showing actor/trigger, orchestrator, important dependencies, persistent entities, and outcome.>

### Feature effects

| Area | Effect | Evidence |
|---|---|---|
| `<domain/state/system>` | `<created/changed/published/called>` | `<path:line or label>` |

## 4. Entry Points and Execution Paths — Core

### Entry points

| Entry point | Trigger | Initial function | Auth/security | Evidence |
|---|---|---|---|---|

### Path A — `<path name>`

```text
<confirmed significant call or event graph>
```

Narrate decisions, transitions, and boundaries that are not obvious from the graph. Add Path B/C only for materially different behavior. Mark dynamic dispatch, callbacks, queues, and unavailable downstream services explicitly.

## 5. Architecture and Ownership — Core

### Boundaries

| Boundary | Responsibility | What it isolates | Constraint | Evidence |
|---|---|---|---|---|

### Component map

| Component | Type | Location | Responsibility | Ownership | Used by / depends on | Change risk |
|---|---|---|---|---|---|---|
| `<name>` | `<controller/use case/domain/repository/adapter/worker/...>` | `<path>` | `<why it exists>` | `FEATURE-OWNED` / `SHARED` | `<confirmed relationships>` | `LOW` / `MEDIUM` / `HIGH` |

Explain high-risk shared components and non-obvious placement decisions.

## 6. Developer Navigation — Core

### Relevant file map

```text
<feature-relevant files and their significant functions only>
```

### Significant function call graph

```text
<actual calls only; annotate interface, event, queue, webhook, and inferred edges>
```

### Function purpose matrix

| Function | What it does | Why it exists | Evidence |
|---|---|---|---|

## 7. Data, State, and Persistence — Conditional

### Data transformations

| Input | Output | Function | Why | Evidence |
|---|---|---|---|---|

### Domain objects

| Object | Purpose | Important fields/invariants | Created/modified/consumed by | Lifecycle |
|---|---|---|---|---|

### State transitions

| From | To | Trigger/function | Conditions | Persisted change | Evidence |
|---|---|---|---|---|---|

### Persistence map

| Store/table/collection | Purpose | Read by | Written by | Constraints/relationships/migrations | Evidence |
|---|---|---|---|---|---|

## 8. External and Asynchronous Behavior — Conditional

### External dependencies

| Dependency | Used by | Operation/purpose | Timeout/retry/failure | Replaceability/configuration | Evidence |
|---|---|---|---|---|---|

### Events, queues, jobs, and webhooks

| Producer/trigger | Contract | Transport | Consumer | Retry/ordering/duplicates/DLQ | Evidence |
|---|---|---|---|---|---|

Continue the feature trace after the async boundary. Stop at unavailable source and identify the contract as the verification boundary.

### Feature-specific configuration

| Name | Used by | Purpose | Required/default behavior | Evidence |
|---|---|---|---|---|

List configuration names and behavior only; never expose secret values.

## 9. Errors, Invariants, and Security — Core

### Error flow

```text
<low-level error> → <adapter/domain/application translation> → <externally visible result>
```

### Protected invariants

| Invariant | Protected by | Failure consequence | Evidence |
|---|---|---|---|

### Security and authorization

| Check/boundary | Enforced by | Failure behavior | Evidence |
|---|---|---|---|

## 10. Money Movement — Financial Features Only

- **Source of funds:**
- **Destination of funds:**
- **Provider operation:**
- **Internal transaction record:**
- **Ledger and balance impact:**
- **Holds/reservations and fees:**
- **Settlement timing:**
- **Idempotency and duplicate protection:**
- **Callback/webhook and reconciliation:**
- **Rollback/compensation:**
- **Unknown segments:**

Include a compact funds-flow diagram and evidence for every claimed accounting effect.

## 11. Significant Function Registry — Core

Repeat only for functions material to feature behavior.

### `<ClassOrModule.function()>`

- **Location/signature:**
- **Responsibility and actual behavior:**
- **Why it exists / why here:**
- **Confirmed callers / calls:**
- **Meaningful input / output:**
- **Reads / writes / side effects:**
- **Protected invariants:**
- **Failure and error translation:**
- **Transaction/idempotency/concurrency/security:** <only applicable details>
- **Related tests:**
- **Modification point / change impact:**
- **Evidence status:**

## 12. Tests — Core

| Test or suite | Behavior protected | Significant functions exercised | Known gap | Evidence |
|---|---|---|---|---|

Do not claim coverage solely from naming or proximity.

## 13. Change Impact and Modification Recipes — Core

### `<realistic feature-specific change>`

- **Modify:**
- **Potentially affected:**
- **Should remain unchanged:**
- **Tests to update/run:**
- **Risk:** `LOW` / `MEDIUM` / `HIGH`
- **Reasoning:**

### Dangerous couplings and extension points

| Surface | Shared users / variants | Stable contract | Change risk | Evidence |
|---|---|---|---|---|

## 14. Non-Obvious Decisions and Unknowns — Core

### Supported architectural intent

<Explain only intent visible in code/docs or strongly supported by evidence.>

### Unresolved evidence gaps

| Question | Status | Evidence checked | Why it matters | How to verify |
|---|---|---|---|---|

## 15. Start Here — Core

1. Read `<primary orchestrator path>`.
2. Follow `<main path>`.
3. Inspect `<state/persistence/integration hotspot>`.
4. Run `<most relevant tests>`.

Keep the result high-signal. A short feature may need only the core sections and a few compact tables; a complex feature may need multiple execution paths without duplicating shared material.
