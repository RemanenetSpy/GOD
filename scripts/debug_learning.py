import numpy as np
from core import WorldModel, CellType

# Create a mock Information Maze scenario
# Rule: Real Pellets have Wall to LEFT. Fake Pellets do not.

grid_size = 10
wm = WorldModel(agent_id="tester", grid_size=grid_size)

# Manually populate history to simulate experience
# Case 1: Real Pellet (Wall on left) -> SUCCESS
# (2, 2) is Pellet. (2, 1) is Wall.
wm.cell_visit_counts[2, 2] = 10
wm.cell_reward_history[(2, 2)] = [10, 10, 10]  # Good reward
wm.grid[2, 1] = CellType.OBSTACLE.value 

# Case 2: Fake Pellet (No Wall on left) -> FAILURE
# (4, 4) is Pellet. (4, 3) is Empty.
wm.cell_visit_counts[4, 4] = 10
wm.cell_reward_history[(4, 4)] = [-50, -50, -50] # Bad reward
wm.grid[4, 3] = CellType.EMPTY.value

# Run Pattern Discovery
patterns = wm.discover_patterns()

print("Discovered Patterns:")
for p in patterns:
    print(p)

# Check if any pattern relates to neighbors
has_relative_rule = any('neighbor' in str(p) for p in patterns)
print(f"\nCan detect relative rules? {has_relative_rule}")
