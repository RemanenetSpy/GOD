// PATCHED: Checks-Effects-Interactions
function withdraw() public {
    uint256 amount = balances[msg.sender];
    balances[msg.sender] = 0; // [✓] VOID FILLED: State updated first.
    (bool success, ) = msg.sender.call{value: amount}("");
    require(success);
}
