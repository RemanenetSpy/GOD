# Reward Structure - Balanced for Game Completion

## Current Rewards (Updated)

### Positive Rewards
- **Pellet**: +10
- **Power Pellet**: +50  
- **Eat Ghost (powered)**: +200
- **WIN (all pellets)**: +5000 ⭐ **INCREASED from +1000**

### Negative Penalties
- **Time step**: -0.1
- **Wall hit**: -1.0
- **Death (ghost)**: -1000 ⚠️ **REDUCED from -2000**

## The Balance

### Old System (Too Conservative)
```
Win:  +1000
Death: -2000
Result: Agents too afraid to take risks → Die early instead of trying to win
```

### New System (Balanced)
```
Win:  +5000  ✅
Death: -1000 ⚠️
Result: Winning is 5x better than avoiding death → Agents will take calculated risks
```

## Example Scenarios

### Scenario 1: Play it Safe
- Collect 50 pellets: +500
- Avoid all ghosts: 0
- Time out at 200 steps: -20
- **Total: +480**

### Scenario 2: Go for the Win
- Collect 150 pellets: +1500
- Die once: -1000
- Win bonus: +5000
- **Total: +5500** ⭐ **11x better!**

## Agent Motivation

With this structure, the agent learns:
1. **Winning is the priority** (+5000 is huge!)
2. **Death is acceptable if it leads to winning** (-1000 is manageable)
3. **Playing too safe = low reward** (time penalties add up)

This should encourage agents to **complete games** instead of dying early! 🎯
