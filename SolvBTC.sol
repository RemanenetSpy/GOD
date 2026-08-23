// SolvBTC.sol - Master Staking Logic (Scope: Jan 2026 Audit)
function subscribe(
    address pool,
    uint256 amount,
    uint256 deadline,
    bytes calldata signature
) external nonReentrant returns (uint256) {
    // 1. Verification Block
    require(block.timestamp <= deadline, "EXPIRED");
    _verifySignature(pool, amount, deadline, signature);

    // 2. Transfer Block (The "Mass" Entry)
    IERC20(btcToken).safeTransferFrom(msg.sender, address(this), amount);

    // 3. Calculation Block (The Potential Void)
    // We calculate the user's share of the pool.
    uint256 shares = _convertToShares(pool, amount);
    
    // [!] DANGER ZONE: 
    // We update the pool's total supply AFTER giving the user shares.
    _mint(msg.sender, shares);
    
    // Potential Temporal Void:
    // If _convertToShares relies on totalSystemLiquidity, 
    // and totalSystemLiquidity is updated here...
    totalSystemLiquidity += amount;
    poolBalances[pool] += amount;

    emit Subscribed(msg.sender, pool, amount, shares);
    return shares;
}