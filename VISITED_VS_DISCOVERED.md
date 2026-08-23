# Understanding "Visited Cells" vs "Discovered Cells"

## The Confusion Explained

You noticed:
- **Visited cells**: 26
- **Discovered cells**: 43
- **Exploration %**: Sometimes 26%, sometimes 13%

**Why the difference?** There are **TWO separate tracking systems**!

---

## The Two Tracking Systems

### 1. **Agent's World Model** (visited_cells)
**Location**: `agent.state.world_model.cell_visit_counts`

**What it tracks**: Cells the agent has **physically stepped on**

**How it works**:
```python
# In core.py, WorldModel.update():
pos = observation.position
self.cell_visit_counts[pos[0], pos[1]] += 1  # Only counts where agent STANDS
```

**Example**:
```
Agent path: (5,5) → (5,6) → (5,7) → (6,7)
Visited cells: 4 (only the 4 cells agent stepped on)
```

---

### 2. **Environment's Discovery** (discovered_cells)
**Location**: `env.discovered_cells`

**What it tracks**: All cells the agent has **SEEN** (including neighbors)

**How it works**:
```python
# In environment.py, observe():
for i in range(self.size):
    for j in range(self.size):
        manhattan_dist = abs(i - x) + abs(j - y)
        if manhattan_dist <= visible_range:  # Can see neighbors!
            self.discovered_cells.add((i, j))
```

**Example**:
```
Agent at (5,5) with visible_range=1:
Can see: (5,5), (4,5), (6,5), (5,4), (5,6)
Discovered cells: 5 (center + 4 neighbors)
```

---

## Visual Explanation

### Agent's Perspective (visible_range = 1):

```
. . . . .
. X X X .    X = Can see (discovered)
. X A X .    A = Agent position (visited)
. X X X .
. . . . .
```

**Result**:
- **Visited**: 1 cell (just A)
- **Discovered**: 5 cells (A + 4 neighbors)

### After Agent Moves Right:

```
. . . . .
. X X X X    
. X V A X    V = Previously visited
. X X X X    A = Current position
. . . . .
```

**Result**:
- **Visited**: 2 cells (V and A)
- **Discovered**: 8 cells (all X's)

---

## Why the Numbers Don't Match

### Example from Your Run:

**Agent moved through**: 26 unique cells (visited)
**Agent could see**: 43 unique cells (discovered)

**Why?**
- Agent visits 1 cell at a time
- But sees 5 cells at once (center + 4 neighbors)
- So discovered > visited

**Math**:
```
If agent visits 26 cells:
- Minimum discovered: 26 (if all isolated)
- Maximum discovered: 26 × 5 = 130 (if no overlap)
- Typical discovered: 40-60 (with overlap)
```

---

## The Exploration Percentage Confusion

### In Agent Stats (from agent.py):
```python
'exploration_rate': np.sum(self.state.world_model.cell_visit_counts > 0) / (self.grid_size ** 2)
```

**Uses**: `cell_visit_counts` (VISITED cells only)
**Calculation**: visited_cells / total_cells
**Example**: 26 / 100 = 26%

### In Environment Stats (from environment.py):
```python
'exploration_percentage': len(self.discovered_cells) / (self.size * self.size) * 100
```

**Uses**: `discovered_cells` (SEEN cells)
**Calculation**: discovered_cells / total_cells
**Example**: 43 / 100 = 43%

---

## Why You See Different Percentages

### Text Demo Shows: 26%
**Source**: Agent's `exploration_rate`
**Meaning**: Agent physically visited 26% of cells

### If You Saw 13%:
**Possible reasons**:
1. Different run (different seed/behavior)
2. Halfway through episode (13 visited out of 100)
3. Looking at different metric

### Environment Shows: 43%
**Source**: Environment's `exploration_percentage`
**Meaning**: Agent has seen 43% of cells (including neighbors)

---

## The Code Locations

### Agent's Tracking (core.py, line ~200):
```python
class WorldModel:
    def __init__(self, grid_size: int = 10):
        self.cell_visit_counts = np.zeros((grid_size, grid_size))
    
    def update(self, belief_state, observation):
        pos = observation.position
        self.cell_visit_counts[pos[0], pos[1]] += 1  # Only where agent stands
```

### Environment's Tracking (environment.py, line ~180):
```python
def observe(self, visible_range: int = 1):
    for i in range(self.size):
        for j in range(self.size):
            manhattan_dist = abs(i - x) + abs(j - y)
            if manhattan_dist <= visible_range:
                self.discovered_cells.add((i, j))  # All visible cells
```

---

## Quick Test to See the Difference

Run this in Python:

```python
from environment import GridWorld
from agent import Agent

env = GridWorld(size=10, seed=42)
agent = Agent(grid_size=10)

# Take 5 steps
obs = env.observe()
for i in range(5):
    action, state = agent.act(obs)
    obs, reward, done = env.step(action)

# Check both metrics
agent_visited = np.sum(agent.state.world_model.cell_visit_counts > 0)
env_discovered = len(env.discovered_cells)

print(f"Agent visited: {agent_visited} cells")
print(f"Environment discovered: {env_discovered} cells")
print(f"Difference: {env_discovered - agent_visited} cells")
```

**Expected Output**:
```
Agent visited: 5 cells
Environment discovered: 15-20 cells
Difference: 10-15 cells
```

---

## Summary Table

| Metric | What It Counts | Typical Value | Where It's From |
|--------|----------------|---------------|-----------------|
| **visited_cells** | Cells agent stepped on | Lower | Agent's world model |
| **discovered_cells** | Cells agent has seen | Higher | Environment tracking |
| **exploration_rate** | visited / total | 26% | Agent stats |
| **exploration_percentage** | discovered / total | 43% | Environment stats |

---

## Which One is "Correct"?

**Both are correct!** They measure different things:

- **Visited cells** = "Where have I been?"
  - Useful for: Path planning, coverage
  - More conservative metric

- **Discovered cells** = "What have I seen?"
  - Useful for: Knowledge, mapping
  - More generous metric

**For learning**: Discovered cells is more relevant (agent learns from what it sees)
**For navigation**: Visited cells is more relevant (agent knows where it's been)

---

## The Bottom Line

**Your observation is spot on!**

- Agent **visited** 26 cells (physically stepped on them)
- Agent **discovered** 43 cells (saw them, including neighbors)
- This is **normal and expected** behavior
- The agent can see more than it visits because of `visible_range`

**Think of it like this**:
- Visited = "Footprints" (where you walked)
- Discovered = "What you saw" (including things you saw from a distance)

You can see a mountain without climbing it! 🏔️
