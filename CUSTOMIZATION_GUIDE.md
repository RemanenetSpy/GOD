# Complete Customization Guide - Seeds, World Settings, and Advanced Features

## 🎲 How to Change Seeds

### What is a Seed?
A seed controls the random number generator, determining:
- Where resources appear
- Where obstacles are placed
- Agent's starting position
- Random events in the world

**Same seed = Same world layout every time**

---

## 📍 Where to Change Seeds

### Location 1: Text Demo (Line 160 in main.py)
```python
agent, env = run_episode(num_steps=100, render=True, seed=42)
                                                        ^^^^
                                                    Change this
```

**Examples**:
- `seed=42` → One specific world
- `seed=123` → Completely different world
- `seed=999` → Another unique world
- `seed=None` → Random seed every time (different each run)

### Location 2: Visual Demo (Line 189 in main.py)
```python
visualize_episode(num_steps=100, seed=42, save_animation=True)
                                   ^^^^
                              Change this
```

### Location 3: In environment.py (Line 25 in main.py for visual, or when creating GridWorld)
```python
env = GridWorld(size=10, num_resources=5, num_obstacles=8, seed=42)
                                                            ^^^^
```

---

## 🌍 How to Make the World More Advanced

### Current World Settings (in main.py, visualize_episode function, line 25):
```python
env = GridWorld(
    size=10,              # 10×10 grid (100 cells total)
    num_resources=5,      # 5 resources to collect
    num_obstacles=8,      # 8 obstacles blocking movement
    seed=42               # Seed for reproducibility
)
```

### Advanced World Configurations

#### 1. **Larger World** (More Exploration)
```python
env = GridWorld(
    size=20,              # 20×20 grid (400 cells!)
    num_resources=15,     # More resources
    num_obstacles=25,     # More obstacles
    seed=42
)
```

#### 2. **Dense Resource World** (Easy Mode)
```python
env = GridWorld(
    size=10,
    num_resources=20,     # Lots of resources
    num_obstacles=3,      # Few obstacles
    seed=42
)
```

#### 3. **Sparse Challenging World** (Hard Mode)
```python
env = GridWorld(
    size=15,
    num_resources=3,      # Very few resources
    num_obstacles=30,     # Many obstacles
    seed=42
)
```

#### 4. **Maze-like World**
```python
env = GridWorld(
    size=12,
    num_resources=8,
    num_obstacles=40,     # Lots of obstacles = maze
    seed=42
)
```

#### 5. **Open World** (Minimal Obstacles)
```python
env = GridWorld(
    size=15,
    num_resources=10,
    num_obstacles=5,      # Very open
    seed=42
)
```

---

## 🔧 Advanced Customization Options

### In environment.py (GridWorld class initialization):

```python
env = GridWorld(
    size=10,                    # Grid size (NxN)
    num_resources=5,            # Number of resources
    num_obstacles=8,            # Number of obstacles
    sensor_noise_level=0.1,     # Probability of noisy observations (0.0-1.0)
    seed=42                     # Random seed
)
```

**sensor_noise_level**:
- `0.0` = Perfect sensors (no noise)
- `0.1` = 10% chance of noisy observations (default)
- `0.3` = 30% chance (challenging)
- `0.5` = 50% chance (very challenging)

---

## 🎯 Testing Different Scenarios

### Scenario 1: Compare Different Seeds
```python
# Run 1: Seed 42
agent, env = run_episode(num_steps=100, render=True, seed=42)

# Run 2: Seed 123
agent, env = run_episode(num_steps=100, render=True, seed=123)

# Run 3: Seed 999
agent, env = run_episode(num_steps=100, render=True, seed=999)
```

**Result**: Each seed creates a completely different world!

### Scenario 2: Random World Every Time
```python
agent, env = run_episode(num_steps=100, render=True, seed=None)
```

**Result**: New random world each run!

### Scenario 3: Test Agent Performance Across Multiple Worlds
```python
# Test on 5 different seeds
for seed in [42, 123, 456, 789, 999]:
    print(f"\n=== Testing Seed {seed} ===")
    agent, env = run_episode(num_steps=100, render=False, seed=seed)
    print(f"Final reward: {env.total_reward:.2f}")
    print(f"Exploration: {len(env.discovered_cells)}/100")
```

---

## 🚀 Making the World More Interesting

### Option 1: Modify environment.py Directly

**Add More Cell Types** (in environment.py):
```python
class CellType(Enum):
    EMPTY = 0
    RESOURCE = 1
    OBSTACLE = 2
    UNKNOWN = 3
    TRAP = 4        # New: Dangerous cells
    BONUS = 5       # New: Extra reward cells
    TELEPORT = 6    # New: Teleportation points
```

**Add Different Reward Values**:
```python
# In step() function, modify rewards:
if self.grid[new_pos[0], new_pos[1]] == CellType.RESOURCE.value:
    reward += 1.0  # Normal resource
elif self.grid[new_pos[0], new_pos[1]] == CellType.BONUS.value:
    reward += 5.0  # Bonus resource!
elif self.grid[new_pos[0], new_pos[1]] == CellType.TRAP.value:
    reward -= 3.0  # Trap penalty!
```

### Option 2: Dynamic Environments

**Resources that Move**:
```python
# In _apply_world_rules():
if np.random.random() < 0.05:  # 5% chance each step
    # Move a random resource to new location
    old_pos = random_resource_position()
    new_pos = random_empty_position()
    self.grid[old_pos] = CellType.EMPTY.value
    self.grid[new_pos] = CellType.RESOURCE.value
```

**Obstacles that Appear/Disappear**:
```python
# Dynamic obstacles
if np.random.random() < 0.02:
    pos = random_empty_position()
    self.grid[pos] = CellType.OBSTACLE.value  # New obstacle!
```

### Option 3: Agent Capabilities

**Modify Agent Visible Range** (in agent.py):
```python
# In Agent.__init__():
self.state.frame_of_ref.visible_range = 2  # See 2 cells away (default is 1)
```

**Increase Planning Depth** (in agent.py):
```python
# In Agent.__init__():
self.planning_depth = 5  # Plan 5 steps ahead (default is 3)
```

**Adjust Exploration Bonus** (in agent.py):
```python
# In Agent.__init__():
self.exploration_bonus = 0.5  # Higher = more exploration (default 0.3)
```

---

## 📊 Recommended Test Configurations

### Configuration 1: Beginner World
```python
env = GridWorld(size=8, num_resources=10, num_obstacles=5, seed=42)
agent = Agent(grid_size=8)
agent.exploration_bonus = 0.5  # Encourage exploration
```

### Configuration 2: Standard World (Current)
```python
env = GridWorld(size=10, num_resources=5, num_obstacles=8, seed=42)
agent = Agent(grid_size=10)
```

### Configuration 3: Expert World
```python
env = GridWorld(size=15, num_resources=5, num_obstacles=30, 
                sensor_noise_level=0.3, seed=42)
agent = Agent(grid_size=15)
agent.planning_depth = 5
```

### Configuration 4: Massive World
```python
env = GridWorld(size=20, num_resources=20, num_obstacles=40, seed=42)
agent = Agent(grid_size=20)
# Warning: This will be slower!
```

---

## 🎮 Quick Experiments to Try

### Experiment 1: Seed Comparison
**Goal**: See how different seeds create different challenges

**Steps**:
1. Edit line 160 in main.py: `seed=42`
2. Run and note the final reward
3. Change to `seed=123`
4. Run again and compare

**Expected**: Different rewards, different exploration patterns

### Experiment 2: World Size Impact
**Goal**: See how world size affects learning

**Steps**:
1. Edit line 25 in main.py: `size=5` (small world)
2. Run and note exploration percentage
3. Change to `size=20` (large world)
4. Run and compare

**Expected**: Small world = 100% exploration, Large world = lower %

### Experiment 3: Resource Density
**Goal**: Test agent in resource-rich vs resource-poor worlds

**Steps**:
1. Edit line 25: `num_resources=20` (rich)
2. Run and note final reward
3. Change to `num_resources=2` (poor)
4. Run and compare

**Expected**: More resources = higher reward

### Experiment 4: Sensor Noise
**Goal**: Test how noise affects learning

**Steps**:
1. Edit line 25: `sensor_noise_level=0.0` (perfect sensors)
2. Run and note uncertainty decrease
3. Change to `sensor_noise_level=0.5` (very noisy)
4. Run and compare

**Expected**: More noise = slower learning, higher uncertainty

---

## 📝 Summary of What You Can Change

| Parameter | Location | What It Does | Recommended Range |
|-----------|----------|--------------|-------------------|
| `seed` | Line 160, 189 | World layout | 0-999, or None |
| `num_steps` | Line 160, 189 | Episode length | 50-1000 |
| `size` | Line 25 (in GridWorld) | Grid dimensions | 5-25 |
| `num_resources` | Line 25 | Resource count | 1-50 |
| `num_obstacles` | Line 25 | Obstacle count | 0-100 |
| `sensor_noise_level` | Line 25 | Observation noise | 0.0-0.5 |
| `visible_range` | agent.py init | How far agent sees | 1-5 |
| `planning_depth` | agent.py init | Planning steps | 1-10 |
| `exploration_bonus` | agent.py init | Exploration drive | 0.0-1.0 |

---

## 🎯 Next Steps

1. **Start Simple**: Change just the seed (line 160) and run a few times
2. **Experiment**: Try different world sizes and resource counts
3. **Advanced**: Modify sensor noise and agent parameters
4. **Create Scenarios**: Design specific challenges for the agent

**Remember**: After each change, save the file and run `python main.py`!

---

## 💡 Pro Tips

- **Small worlds** (5×5) are great for quick tests
- **Large worlds** (20×20) show emergent behavior better
- **High noise** makes learning harder but more realistic
- **More resources** = easier for agent = higher rewards
- **More obstacles** = harder navigation = lower rewards
- **Different seeds** = completely different challenges

Experiment and have fun! 🚀
