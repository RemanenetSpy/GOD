// VaultManager.sol (2026 Beta)
function executeFlashStake(uint256 amount, address user) external nonReentrant {
    // 1. Initial State Check
    require(amount <= maxFlashAmount, "Exceeds limit");
    
    // 2. Internal Accounting: This "feels" solid.
    // We update the 'staked' mapping before anything else.
    stakedBalances[user] += amount;
    totalSystemLiquidity += amount;

    // 3. The Borrow Call:
    // We call the LendingEngine to issue the debt.
    // The LendingEngine is a trusted internal contract.
    ILendingEngine(lendingEngine).issueDebt(user, amount);

    // 4. Final Sync:
    // Ensure the vault is still balanced.
    updateVaultHealth();
}
