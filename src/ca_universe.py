"""
========================================================================================
CELLULAR AUTOMATA UNIVERSE: Emergent Dynamic Substrate
========================================================================================
"""

import numpy as np
from typing import Tuple, Dict, List
from scipy.signal import convolve2d


class CellularAutomataUniverse:
    def __init__(
        self,
        grid_shape: Tuple[int, int] = (25, 25),
        ca_rule: str = "Conway (B3/S23)",
        initial_density: float = 0.25,
        seed: int = 42
    ):
        self.grid_shape = grid_shape
        self.ca_rule = ca_rule
        self.np_rng = np.random.RandomState(seed)
        self.grid = np.zeros(grid_shape, dtype=int)
        self.neighbor_kernel = np.array([
            [1, 1, 1],
            [1, 0, 1],
            [1, 1, 1]
        ], dtype=int)
        self.reset(density=initial_density)

    def reset(self, density: float = 0.25):
        h, w = self.grid_shape
        raw = self.np_rng.rand(h, w)
        self.grid = np.where(raw < density, 1, 0)
        if h >= 10 and w >= 10:
            self.grid[1:4, 1:4] = np.array([
                [0, 1, 0],
                [0, 0, 1],
                [1, 1, 1]
            ])
            cy, cx = h // 2, w // 2
            self.grid[cy-1:cy+2, cx] = 1

    def step(self, agent_positions: Dict[str, Tuple[int, int]]) -> Dict[str, float]:
        h, w = self.grid_shape
        alive = (self.grid == 1).astype(int)
        neighbors = convolve2d(alive, self.neighbor_kernel, mode='same', boundary='wrap')
        
        next_grid = np.zeros_like(self.grid)
        if self.ca_rule == "HighLife (B36/S23)":
            birth = (alive == 0) & ((neighbors == 3) | (neighbors == 6))
            survive = (alive == 1) & ((neighbors == 2) | (neighbors == 3))
        elif self.ca_rule == "Seeds (B2/S)":
            birth = (alive == 0) & (neighbors == 2)
            survive = np.zeros_like(alive, dtype=bool)
        elif self.ca_rule == "Day & Night (B3678/S34678)":
            birth = (alive == 0) & np.isin(neighbors, [3, 6, 7, 8])
            survive = (alive == 1) & np.isin(neighbors, [3, 4, 6, 7, 8])
        else:
            birth = (alive == 0) & (neighbors == 3)
            survive = (alive == 1) & ((neighbors == 2) | (neighbors == 3))
            
        next_grid[birth | survive] = 1
        
        # Dense clusters become obstacles
        dense_obstacles = (neighbors >= 6) & (next_grid == 1)
        next_grid[dense_obstacles] = 2
        
        rewards: Dict[str, float] = {}
        for aid, (py, px) in agent_positions.items():
            py = max(0, min(h - 1, py))
            px = max(0, min(w - 1, px))
            cell_type = next_grid[py, px]
            if cell_type == 1:
                rewards[aid] = 8.0 # Generous feeding reward
                next_grid[py, px] = 0 # Harvested
            elif cell_type == 2:
                rewards[aid] = -0.5 # Collision friction
            else:
                rewards[aid] = 0.02
                
        # Cosmic Nutrient Pulse: If grid runs out of living cells, seed new life
        if np.sum(next_grid == 1) < 4:
            raw = self.np_rng.rand(h, w)
            next_grid[raw < 0.12] = 1
                
        self.grid = next_grid
        return rewards
