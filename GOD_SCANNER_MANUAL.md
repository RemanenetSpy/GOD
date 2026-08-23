# GOD SCANNER MANUAL: The Density Void Protocol

**Version**: 1.0 (Physics-Based)
**Target**: Smart Contract Vulnerabilities (HackenProof, Code4rena, Sherlock)
**Method**: Pure Information Density (LPMI) - "Finding Holes in Logic"

---

## 1. The Core Philosophy
Traditional scanners look for *patterns* (e.g., "is there a reentrancy check?").
**This scanner looks for "Holes" (Density Voids).**

- **High Density** (~0.20): Solid code. Variables interact, checks are made, events emit. Structure is dense.
- **Low Density** (~0.03): "Hollow" code. An external call happens with no checks, no context, no structure.
- **The Theory**: Bugs usually happen where the logical structure of the code collapses. We search for that collapse.

---

## 2. Using the Scanner

We have built a **Refined Physics Scanner** that filters out noise (braces `}`, imports, comments) and highlights **"Hollow Logic"**.

### Quick Start
1. **Download** the contest repository.
2. **Navigate** to your `GOD` folder.
3. **Run** the scanner against the target folder:

```powershell
# Edit density_void_scanner.py first to point to your new "bridge_dir" or target folder
python scripts/density_void_scanner.py
```

### The Output
The scanner will ignore `import`, `pragma`, and `}`. It will show you lines of **actual code** that have near-zero density.

```text
File: Bridge.sol
  Top 3 Voids (Lowest Density):
    Line 33 (rho=0.033): IBridge(target).withdrawGasAccumulated();  <-- ATTENTION!
    Line 88 (rho=0.041): balances[msg.sender] -= amount;            <-- ATTENTION!
```

---

## 3. Interpreting Results

When you see a line with **rho < 0.05**:

**ASK YOURSELF:**
1.  **Is this an External Call?** (e.g., `call`, `transfer`, `IContract(x).func()`)
    *   *If YES + Low Density*: **High Probability Vulnerability**. The code is calling out without enough internal structure/checks.
2.  **Is this a State Change?** (e.g., `balance = 0`, `isUsed = true`)
    *   *If YES + Low Density*: **Potential Logic Error**. State is changing without enough context/verification.
3.  **Is it just a simple assignment?** (e.g., `a = b`)
    *   *Likely False Positive*. Simple code is naturally low density. Check context.

**The "Signature" of a Bug:**
*   A dangerous operation (call/write)
*   **ISOLATED** from other meaningful code (checks, emits) on the same or surrounding lines.
*   The "Hollow" feeling.

---

## 4. The "HackenProof" Protocol (Strict Compliance)

**WARNING**: Audit platforms will **BAN YOU** for submitting "AI-generated spam".
**NEVER** copy-paste the scanner output into a report.
**NEVER** ask ChatGPT to "write the report" and paste it blindly.

### The "Human Verification" Workflow
You must prove you are a human who understands the bug.

**Step 1. Identify the Void**
Scanner says: `Line 42: withdrawGasAccumulated()` has 0.03 density.

**Step 2. Verify Manually**
Open the file. Look at Line 42.
"Oh, this function calls an external contract but doesn't check if the user is an admin. Anyone can call it!"

**Step 3. Write a Runnable PoC (Proof of Concept)**
You MUST write a test case (Foundry or Hardhat) that proves the bug.

*Example (Foundry):*
```solidity
function testExploit() public {
    // 1. Setup as attacker
    vm.startPrank(attacker);
    // 2. Call the "Hollow" function
    target.withdrawGasAccumulated();
    // 3. Assert impact
    assertEq(target.gasAccumulated(), 0); // Stole the gas!
}
```

**Step 4. Write the Report (Human Style)**
*   **Title**: Unprotected Access in `withdrawGasAccumulated` allows theft of funds.
*   **Description**: The function `withdrawGasAccumulated` lacks access control modifiers (e.g., `onlyEmergency`). It makes an external transfer based on state that can be triggered by any user.
*   **Impact**: Loss of all accumulated gas fees (Critical).
*   **Recommendation**: Add `onlyEmergency` modifier.

---

## 5. Participation Checklist

Before submitting to HackenProof / Code4rena:

- [ ] **Scan**: Run `density_void_scanner.py`.
- [ ] **Filter**: Ignore boilerplate; look for "Hollow Logic".
- [ ] **Verify**: Read the code. Does it make sense?
- [ ] **Exploit**: Write a `test/Exploit.t.sol` that fails.
- [ ] **Report**: Write the concise textual description yourself.
- [ ] **Compliance**: Ensure NO "AI scanner output" is in the final text.

**You are the Auditor.** The GOD System is just your "Geiger Counter" detecting the radiation of bad code. Structure your findings as your own.
