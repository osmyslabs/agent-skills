# Fictional Payout Blueprint Example

This example is fictional. Its names, paths, behavior, and evidence labels are formatting examples only and must never be treated as facts about the inspected repository.

# Payout

> Source of truth for the fictional `payout` business capability.

## 1. Two-Minute Summary

- **Business purpose:** Move an approved amount from a seller wallet to an external bank account.
- **Triggers:** `POST /v1/payouts` starts a payout; `POST /webhooks/acme-pay` completes or fails it.
- **Final outcome:** The payout reaches `COMPLETED` or `FAILED`, with the wallet reservation settled or released.
- **Primary orchestrator:** `RequestPayout.execute()`.
- **Main path:** request → eligibility → reserve balance → create payout → provider transfer → webhook → settle ledger.
- **Primary persistence:** `payouts`, `wallet_reservations`, and `ledger_entries`.
- **Highest-risk shared component:** `WalletLedger`, also used by deposits and refunds.
- **Evidence status:** All statements below are confirmed inside this fictional example unless marked otherwise.

## 2. Feature at a Glance

```text
Seller
  ↓ POST /v1/payouts
PayoutController.request()
  ↓
RequestPayout.execute()
  ├─ PayoutPolicy.validate()
  ├─ WalletLedger.reserve()
  ├─ PayoutRepository.insert(REQUESTED)
  └─ AcmePayoutGateway.send()
       ↓ provider webhook
PayoutWebhook.handle()
  ├─ WebhookVerifier.verify()
  ├─ PayoutRepository.transition()
  └─ WalletLedger.settle() / release()
```

| Area | Effect | Fictional evidence |
|---|---|---|
| Wallet | Available balance decreases and reserved balance increases | `src/wallet/WalletLedger.kt:44` |
| Payout | Record advances from `REQUESTED` to `PROCESSING` | `src/payout/RequestPayout.kt:71` |
| Provider | Bank transfer is requested | `src/payout/AcmePayoutGateway.kt:38` |
| Ledger | Reservation is settled or released after callback | `src/payout/PayoutWebhook.kt:96` |

## 3. Entry Points and Execution Paths

| Entry point | Trigger | Initial function | Security | Fictional evidence |
|---|---|---|---|---|
| `POST /v1/payouts` | Authenticated seller request | `PayoutController.request()` | Seller scope and wallet ownership | `src/payout/PayoutRoutes.kt:19` |
| `POST /webhooks/acme-pay` | Provider callback | `PayoutWebhook.handle()` | HMAC signature and timestamp | `src/payout/PayoutWebhookRoutes.kt:22` |

### Request path

```text
PayoutController.request()
└─ RequestPayout.execute()
   ├─ PayoutPolicy.validate()
   ├─ WalletLedger.reserve()
   ├─ PayoutRepository.insert()
   └─ AcmePayoutGateway.send()
      └─ AcmeClient.createTransfer()
```

`RequestPayout.execute()` owns orchestration but delegates eligibility, accounting, persistence, and provider transport to their respective boundaries. The provider call returns an external transfer ID; the payout is then persisted as `PROCESSING`.

### Completion path

```text
PayoutWebhook.handle()
├─ WebhookVerifier.verify()
├─ ProcessedWebhookRepository.insertIfAbsent()
└─ when provider status is SUCCEEDED
   ├─ PayoutRepository.transition(PROCESSING, COMPLETED)
   └─ WalletLedger.settle()
```

The insert-if-absent operation makes duplicate callbacks no-ops. An event bus is injected into `PayoutWebhook`, but no publish call is present; event publication is therefore **not found in repository** in this fictional example.

## 4. Ownership and Boundaries

| Component | Responsibility | Ownership | Change risk |
|---|---|---|---|
| `RequestPayout` | Orchestrates the request path | `FEATURE-OWNED` | Medium |
| `PayoutPolicy` | Enforces amount and destination eligibility | `FEATURE-OWNED` | Medium |
| `AcmePayoutGateway` | Adapts the external payout API | `FEATURE-OWNED` | Medium |
| `WalletLedger` | Reserves, settles, and releases wallet funds | `SHARED` | High |
| `WebhookVerifier` | Verifies provider signatures | `SHARED` | High |

The application layer decides when to request a payout. The gateway owns provider-specific transport and errors but must not decide wallet eligibility. `WalletLedger` is shared with deposits and refunds, so changing reservation semantics can alter other money flows.

## 5. Data, State, and Persistence

```text
PayoutRequest
  ↓ PayoutController.toCommand()
RequestPayoutCommand
  ↓ RequestPayout.execute()
Payout(REQUESTED)
  ↓ AcmePayoutGateway.send()
Payout(PROCESSING, providerTransferId)
  ↓ signed provider webhook
Payout(COMPLETED | FAILED)
```

| From | To | Trigger | Persisted effect |
|---|---|---|---|
| — | `REQUESTED` | `PayoutRepository.insert()` | Creates payout and reservation ID |
| `REQUESTED` | `PROCESSING` | Provider accepts transfer | Stores provider transfer ID |
| `PROCESSING` | `COMPLETED` | Successful verified webhook | Settles reservation and records ledger entry |
| `PROCESSING` | `FAILED` | Failed verified webhook | Releases reservation |

The provider timeout path after transfer submission is **inferred** to require reconciliation because `findByProviderTransferId()` exists, but no scheduled reconciler is visible in this fictional repository.

## 6. Money Movement

```text
Seller available balance
  ↓ reserve 100.00
Available -100.00; Reserved +100.00
  ↓ provider confirms success
Reserved -100.00; external-payout ledger entry +100.00
  ↓
Payout COMPLETED
```

- **Source/destination:** Seller wallet to the verified external bank account.
- **Internal record:** The payout and reservation are created in one database transaction.
- **Idempotency:** A unique `(wallet_id, idempotency_key)` constraint protects request retries; provider webhook IDs are inserted once.
- **Compensation:** Synchronous provider rejection releases the reservation. A verified failed callback also releases it.
- **Unknown segment:** Automatic reconciliation after an ambiguous provider timeout is unverified.

## 7. Significant Function Registry

### `RequestPayout.execute()`

- **Location/signature:** `src/payout/RequestPayout.kt:31`, `execute(command: RequestPayoutCommand): PayoutResult`
- **Responsibility:** Coordinates eligibility, reservation, payout creation, and provider submission.
- **Why here:** These steps are application orchestration; neither HTTP transport nor the provider adapter should own the cross-boundary business flow.
- **Confirmed callers/calls:** Called by `PayoutController.request()`; calls `PayoutPolicy.validate()`, `WalletLedger.reserve()`, `PayoutRepository.insert()`, and `PayoutGateway.send()`.
- **Writes/side effects:** Creates payout state, reserves funds, and requests an external transfer.
- **Failures:** Maps `ProviderRejected` to `PayoutSubmissionFailed`; an ambiguous timeout leaves the payout `PROCESSING`.
- **Related tests:** `RequestPayoutTest` covers success, insufficient balance, duplicate key, and synchronous provider rejection.

### `PayoutWebhook.handle()`

- **Location/signature:** `src/payout/PayoutWebhook.kt:40`, `handle(headers: Headers, body: ByteArray)`
- **Responsibility:** Authenticates callbacks and applies terminal provider outcomes once.
- **Why here:** It is the provider-facing asynchronous entry point; ledger mechanics remain delegated.
- **Confirmed calls:** `WebhookVerifier.verify()`, `ProcessedWebhookRepository.insertIfAbsent()`, `PayoutRepository.transition()`, and `WalletLedger.settle()` or `release()`.
- **Protected invariants:** Invalid callbacks cannot mutate state; one provider event cannot settle twice.
- **Related tests:** `PayoutWebhookIntegrationTest` covers valid, duplicate, invalid-signature, success, and failure callbacks.

## 8. Tests

| Test | Protects | Known gap |
|---|---|---|
| `RequestPayoutTest` | Eligibility, idempotent request, reservation, provider rejection | Ambiguous timeout recovery |
| `PayoutWebhookIntegrationTest` | Signature, duplicate callback, terminal transitions | Out-of-order callbacks |
| `WalletLedgerIntegrationTest` | Atomic reserve/settle/release accounting | Cross-feature concurrency under load |

## 9. Change Impact

### Add a minimum payout amount

- **Modify:** `PayoutPolicy.validate()` and payout configuration.
- **Potentially affected:** API validation messages and `RequestPayoutTest`.
- **Should remain unchanged:** `AcmePayoutGateway`, webhook handling, and ledger settlement.
- **Risk:** Low, because the rule precedes reservation and provider submission.

### Add another payout provider

- **Modify:** Implement `PayoutGateway`, provider-specific webhook verification/translation, and runtime wiring.
- **Potentially affected:** Provider configuration, contract tests, reconciliation, and callback routing.
- **Should remain unchanged:** `RequestPayout` orchestration and wallet reservation semantics.
- **Risk:** High, because provider status, idempotency, and webhook behavior can differ.

## 10. Unknowns and Start Here

- **Unverified:** Whether ambiguous transfer timeouts are reconciled automatically.
- **Not found:** An event publication call despite an injected event bus.
- **Start here:** Read `RequestPayout.execute()`, then `WalletLedger.reserve()`, `AcmePayoutGateway.send()`, `PayoutWebhook.handle()`, and the two payout test suites.
