# Vulnerability Report: Unsafe Token Handling in Whitechain Bridge

**Program:** `Whitechain Bridge`
**Target:** `Bridge.sol` (Function: `_executeTokenTransfer`)
**Severity:** **Medium** (Potential Funds Loss / State Inconsistency)
**Weakness:** Unchecked Return Value (EIP-20 violation handling)

## 1. Summary
The `Bridge.sol` contract implements a toggle `useTransfer` within `_executeTokenTransfer` and `_executeTokenTransferFrom`. When `useTransfer` is true, the contract calls the standard ERC20 `.transfer()` or `.transferFrom()` methods **without checking their return value**.

While `SafeERC20` is imported and used for the `safeTransfer` branch, the existence of the unsafe branch poses a risk. If a token (e.g., ZRX, various stablecoins) returns `false` on failure instead of reverting, and `Mapper.sol` is misconfigured to use `useTransfer=true` for it, the Bridge will record a successful Deposit/Withdrawal event without actual fund movement.

## 2. Technical Details

### Location
File: `ether/contracts/main/modules/bridge/Bridge.sol`
Lines: 529-535

```solidity
    function _executeTokenTransfer(bool useTransfer, bytes32 tokenAddress, address to, uint256 amount) private {
        if (useTransfer) {
            // [!] UNSAFE: Return value is ignored
            IERC20Upgradeable(address(uint160(uint256(tokenAddress)))).transfer({ to: to, amount: amount });
        } else {
            // SAFE: Uses OpenZeppelin SafeERC20
            IERC20Upgradeable(address(uint160(uint256(tokenAddress)))).safeTransfer({ to: to, value: amount });
        }
    }
```

### The Risk Scenario
1.  **Configuration:** A token that returns `false` on failure (Non-Standard ERC20) is registered in `Mapper` with `useTransfer = true`.
2.  **Failure:** A user attempts to bridge, or the bridge attempts to release tokens.
3.  **Silent Fail:** The token contract returns `false` (e.g., due to insufficient balance or pausable state).
4.  **State Desync:** The Bridge ignores the `false` return, emits the `Deposit`/`Withdrawal` event, and updates internal accounting (e.g., `dailyLimits`).
5.  **Result:** The protocol believes a transfer occurred when it did not.

## 3. Impact
-   **Funds Loss/Lock:** Users may not receive funds on the destination chain if the deposit failed silently.
-   **Accounting Errors:** `dailyLimits` and `gasAccumulated` may be updated based on failed transactions.

## 4. Remediation
**Remove the unsafe path.**
There is no significant gas or logic benefit to using the raw `transfer` over `safeTransfer` in a high-security bridge context. Always use `SafeERC20`.

```diff
    function _executeTokenTransfer(bool useTransfer, bytes32 tokenAddress, address to, uint256 amount) private {
-       if (useTransfer) {
-           IERC20Upgradeable(...).transfer(...);
-       } else {
            IERC20Upgradeable(address(uint160(uint256(tokenAddress)))).safeTransfer({ to: to, value: amount });
-       }
    }
```
