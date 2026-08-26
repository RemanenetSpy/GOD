# DoS in `StakingProposal.claimAll()` via Unbounded Loop

**Target:** DeXe Protocol (`StakingProposal.sol`)
**Severity:** Medium (DoS / Temporary Freezing of Funds)
**Weakness:** Unbounded Loop (CWE-835)

## Description
The `StakingProposal` contract contains a `claimAll()` function designed to allow users to claim rewards from all active staking tiers in a single transaction. This function iterates over the `_userClaimableTiers[msg.sender]` EnumerableSet. 

However, this set grows indefinitely as a user participates in more staking rounds. There is no mechanism to remove old tiers from this list within `createStaking` or `stake`. The list is only reduced when `claim` is called. If a user accumulates a significant number of claimable tiers (e.g., by participating in frequent, short-term staking events), the gas cost to iterate through the entire set in `claimAll()` will exceed the block gas limit.

This renders the `claimAll()` function permanently unusable for that user, effectively breaking a core convenience feature and potentially leading to user confusion or temporary fund lockup if they rely solely on this method.

## Code Location
**File:** `contracts/gov/proposals/StakingProposal.sol`
**Function:** `claimAll()` (Lines 119-128)

```solidity
    function claimAll() external {
        EnumerableSet.UintSet storage claimableTiersList = _userClaimableTiers[msg.sender];
        uint256 length = claimableTiersList.length();
        // VULNERABILITY: 'length' is unbounded and grows with user participation
        for (uint i = length; i > 0; i--) {
            uint256 id = claimableTiersList.at(i - 1);
            uint256 deadline = stakingInfos[id].deadline;
            if (block.timestamp <= deadline) continue;
            _claim(id);
        }
    }
```

## Impact
*   **Availability:** The `claimAll` function becomes non-functional for active users.
*   **User Experience:** Funds appear "stuck" if the user interface relies on `claimAll`.
*   **Mitigation:** Users can still fallback to `claim(id)` to withdraw rewards one by one, preventing permanent loss. However, this degradation of service falls under "Smart contract unable to operate due to lack of resources (Gas)" which is often classified as Medium.

## Recommendation
Implement a pagination mechanism for `claimAll` (e.g., `claimBatch(uint256[] ids)`) or limit the loop size to ensure it always fits within the block gas limit.

## References
*   `Devx.md` Line 76: "There is a possibility to hit an 'unbounded loop' here."
