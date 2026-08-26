# Vulnerability Report: Signature Bypass via Unsigned Destination Address

**Target:** `SolvBTC-Solana-Contract` (Rust/Anchor)
**Severity:** **High / Critical**
**Weakness:** Missing Data integrity Check (Signature Binding)
**Location:** `programs/solvbtc/src/state/withdraw_request.rs`

## Summary
The `WithdrawRequest` signature verification mechanism fails to bind the **destination token account** (`withdraw_token_account`) to the signature. The `hash()` function, which generates the message payload for the ECDSA check, excludes this critical field.

This allows a valid signature intended for a legitimate withdrawal address (e.g., a KYC'd wallet) to be **replayed** to authorize a withdrawal to an arbitrary, unauthorized address, provided the attacker controls the user's signing key to create a new `WithdrawRequest` PDA. This completely bypasses off-chain destination allowlisting or AML checks performed by the signer.

## Technical Details

### The Flaw
In `withdraw_request.rs`, the `hash()` function constructs the data payload for verification:

```rust
pub fn hash(&self) -> [u8;32] {
    solana_nostd_sha256::hashv(&[
        self.user.as_ref(),
        self.withdraw_token.as_ref(),
        self.request_hash.as_ref(), // External ID
        self.shares.to_le_bytes().as_ref(),
        self.nav.to_le_bytes().as_ref()
        // [!] CRITICAL MISSING FIELD: self.withdraw_token_account
    ])
}
```

Because `withdraw_token_account` is missing, two different `WithdrawRequest` accounts (one pointing to Address A, one to Address B) produce the **exact same hash**, provided the other fields (`user`, `amount`, `request_hash`) are identical.

### The Attack Vector (Replay / Substitution)
1.  **Legitimate Request:** User requests withdrawal to **SafeAddress**. Solv Server verifies SafeAddress is whitelisted/safe and returns `Signature_S`.
2.  **Malicious Substitution:** Attacker (or compromised user) initializes a *new* `WithdrawRequest` on-chain (using `open_request_account`) specifying **AttackerAddress**.
3.  **Bypass:** Attacker calls `withdraw_tokens` on the NEW request.
    *   The contract computes `hash()` of the new request.
    *   Since `withdraw_token_account` is ignored in the hash, `Hash(NewRequest) == Hash(OldRequest)`.
    *   **`Signature_S` validates successfully.**
4.  **Result:** Contract transfers funds to **AttackerAddress**.

Note: The attacker must create a new PDA because `vault_withdraw.rs` line 70 enforces that the context `user_withdraw_ta` matches the PDA `withdraw_token_account`. But since `open_request_account` is permissionless (requires only user signature), creating the malicious PDA is trivial.

## Impact
*   **Bypass of Security Controls:** Any off-chain security checks on the destination address (e.g., "Only withdraw to cold wallet", "Sanctions check") are rendered useless. Once a signature is issued for the *amount*, it can be redirected anywhere.
*   **Funds Theft:** If an attacker compromises a user's session *after* a signature is generated but *before* broadcast, they can redirect the funds to themselves.

## Recommendation
Include the `withdraw_token_account` in the hash calculation to cryptographically bind the signature to the specific destination.

```rust
// PATCH
pub fn hash(&self) -> [u8;32] {
    solana_nostd_sha256::hashv(&[
        self.user.as_ref(),
        self.withdraw_token.as_ref(),
        self.request_hash.as_ref(),
        self.shares.to_le_bytes().as_ref(),
        self.nav.to_le_bytes().as_ref(),
        self.withdraw_token_account.as_ref() // <--- ADD THIS
    ])
}
```
