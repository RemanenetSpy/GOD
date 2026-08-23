// VULNERABLE: The Withdrawal Void
function withdraw() public {
    uint256 amount = balances[msg.sender];
    (bool success, ) = msg.sender.call{value: amount}(""); // [!] DENSITY VOID
    // The money is gone, but the 'balance' still exists in the 
    // engine's density map for a split second.
    require(success);
    balances[msg.sender] = 0; 
}
