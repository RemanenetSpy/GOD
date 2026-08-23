# Vulnerability Report: Signature Context Bypass in SolvBTC (Solana)

**Program:** `SolvBTC-Solana-Contract`
**Component:** `state/withdraw_request.rs`
**Severity:** **High** (Potential Funds Theft via Redirect)
**Status:** Exploitable

## 1. Summary
The `WithdrawRequest` mechanism uses an off-chain ECDSA signature to authorize withdrawals. However, the on-chain `hash()` function used to verify this signature **excludes the destination address** (`withdraw_token_account`). 

This creates a "Context Confusion" vulnerability where a valid signature intended for a legitimate withdrawal (to User's Safe Wallet) can be **replayed** in a new `WithdrawRequest` context to authorize a withdrawal to a different, attacker-controlled address.

## 2. Vulnerability Details

### Location
File: `programs/solvbtc/src/state/withdraw_request.rs`
Function: `hash`

```rust
pub fn hash(&self) -> [u8;32] {
    solana_nostd_sha256::hashv(&[
        self.user.as_ref(),           // Bound to User
        self.withdraw_token.as_ref(), // Bound to Token
        self.request_hash.as_ref(),   // External ID
        self.shares.to_le_bytes().as_ref(), // Amount
        self.nav.to_le_bytes().as_ref()     // NAV
        // [!] MISSING: self.withdraw_token_account.as_ref()
    ])
}
```

### The Logic Gap
The contract correctly enforces that the *Context* `user_withdraw_ta` matches the *PDA* `withdraw_token_account` (in `vault_withdraw.rs`). However, the *PDA itself* is initialized permissionlessly by the user via `open_request_account`.

Since the `hash()` (and thus the Signature verification) essentially ignores the destination address stored in the PDA, an attacker (or compromised user session) can:
1.  Receive a signature for `Destination_A`.
2.  Open a new Request PDA for `Destination_B` (using the same User/Amount/RequestHash).
3.  Use the `Destination_A` signature to withdraw funds to `Destination_B`.

## 3. Impact Assessment
This vulnerability bypasses any server-side security policies regarding destination allowlisting. 
*   **Scenario:** A specialized server signs withdrawals only to "Cold Wallets".
*   **Exploit:** An attacker reuses that signature to withdraw to a "Hot Wallet" or "Attacker Address" (if they have the user's signing key to create the new request).

## 4. Proof of Concept (PoC)
See attached `reproduce_exploit.ts`.
The PoC demonstrates creating two `WithdrawRequest` PDAs with different destinations but identical "Hash payloads", allowing signature reuse.

## 5. Remediation
**Patch:** Include the `withdraw_token_account` in the hash construction.

```rust
pub fn hash(&self) -> [u8;32] {
    solana_nostd_sha256::hashv(&[
        // ... existing fields ...
        self.withdraw_token_account.as_ref() // <--- Fix
    ])
}
```
