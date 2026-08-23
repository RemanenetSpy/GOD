# Why "Removing Failed Rule" Message Appears in Some Runs

## The Question

You noticed this message appearing in **some** runs but not others:
```
⚠️ Removing failed rule: avoid_location at (2, 7) (failure rate: 100.0%)
```

Why does it show up inconsistently?

---

## The Answer: Rule Learning Cycle! 🔄

### How Rule Learning Works:

**Phase 1: Pattern Discovery (Steps 0-10)**
- Agent discovers patterns like "danger zones" and "safe zones"
- Patterns are based on reward history

**Phase 2: Rule Creation (Steps 10-20)**
- Patterns with confidence >0.5 become **rules**
- Example: "Avoid location (2, 7)" (if it gave negative rewards)

**Phase 3: Rule Validation (Steps 20+)**
- Agent tests rules by visiting those locations
- Tracks: prediction_successes vs prediction_failures
- Calculates failure rate

**Phase 4: Rule Removal (When failure rate >70%)**
- If rule fails too often → **Remove it!**
- Print warning message

---

## Why It's Inconsistent Across Runs

### Run 1: Message Appears ✅
```
Step 60: Agent visits (2, 7)
Expected: Negative reward (danger zone)
Actual: Positive reward (+0.9 - found resource!)
Failure rate: 100% (1/1 predictions wrong)
→ ⚠️ Removing failed rule: avoid_location at (2, 7)
```

### Run 2: No Message ❌
```
Agent never visits (2, 7) in this run
→ Rule is never tested
→ No failure detected
→ No message printed
```

### Run 3: No Message ❌
```
Agent visits (2, 7) but rule hasn't been created yet
→ No rule to test
→ No message printed
```

---

## The Key Factors

### 1. **Agent's Path Varies**
Even with the same seed, the agent's **action selection** can vary slightly due to:
- Random exploration (when stuck)
- Belief state updates
- Curiosity rewards

### 2. **Rule Creation Timing**
Rules are only created **every 10 steps** (see `agent.py` line 290):
```python
if self.state.step_count % 10 == 0:
    patterns = self.learning.discover_patterns(...)
    self.state.world_model = self.learning.update_rules(...)
```

If the agent visits a cell **before** the rule is created, no validation happens.

### 3. **Rule Testing Requires Visiting**
The rule is only tested when the agent **actually visits** that location:
```python
if rule.get('type') == 'avoid_location' and rule.get('target') == pos:
    # Test the rule!
```

If the agent never visits `(2, 7)`, the rule is never tested.

---

## Example Timeline

### Run A (Message Appears):
```
Step 10: Create rule "avoid (2, 7)" based on past negative rewards
Step 60: Agent visits (2, 7)
        Expected: -0.5 (danger)
        Actual: +0.9 (resource!)
        Failure rate: 100%
        → ⚠️ Remove rule
```

### Run B (No Message):
```
Step 10: Create rule "avoid (2, 7)"
Step 100: Episode ends
        Agent never visited (2, 7)
        → Rule never tested
        → No message
```

### Run C (No Message):
```
Step 5: Agent visits (2, 7) - no rule yet
Step 10: Create rule based on that visit
Step 100: Agent never returns to (2, 7)
        → Rule never tested
        → No message
```

---

## Why This is Actually Good! ✅

This behavior shows the agent is **learning correctly**:

1. **Creates hypotheses** (rules) based on limited data
2. **Tests hypotheses** when it revisits locations
3. **Removes bad hypotheses** when they fail
4. **Adapts** its model of the world

This is **scientific method in action**! 🔬

---

## How to See It Consistently

If you want to see the message more often:

### Option 1: Increase Steps
```python
run_episode(num_steps=500, ...)  # More time to revisit cells
```

### Option 2: Force Revisits
Modify the agent to prioritize revisiting cells with rules.

### Option 3: Add Logging
See all rules being created/tested:
```python
# In learning.py, line 184
if not rule_exists and pattern['confidence'] > 0.5:
    print(f"   ✅ Creating rule: {rule['type']} at {rule['target']}")
    world_model.rules.append(rule)
```

---

## Summary

**The message appears when:**
1. ✅ A rule is created (based on pattern)
2. ✅ Agent revisits that location
3. ✅ Rule's prediction fails
4. ✅ Failure rate exceeds 70%

**The message doesn't appear when:**
1. ❌ Agent never revisits the location
2. ❌ Rule hasn't been created yet
3. ❌ Rule's predictions are accurate

**This is normal behavior** - it shows the agent is actively testing and refining its understanding of the world! The inconsistency is due to the **stochastic nature** of exploration and the **timing** of rule creation vs. testing.

---

## What You're Seeing

Looking at your runs:
- **Run 1** (Step 60): Agent visited `(2, 7)`, rule failed → Message
- **Run 2**: Agent stuck at `(5, 2)`, never visited `(2, 7)` → No message
- **Run 3**: Agent stuck at `(6, 1)`, never visited `(2, 7)` → No message

The agent is **getting stuck** in different locations each run, so it doesn't always test all its rules!

**This is why improving exploration (Phase 4 goals) is so important!** 🎯
