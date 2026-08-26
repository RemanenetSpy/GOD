"""
========================================================================================
CELLULAR AUTOMATA UNIVERSE: Emergent Dynamic Substrate
========================================================================================
A continuous/discrete living substrate where physics rules emerge from local neighbor interactions.
Supports multiple CA rulesets:
- Conway's Game of Life (B3/S23)
- HighLife (B36/S23) - creates emergent self-replicating Replicators
- Seeds (B2/S) - pure explosive growth
- Day & Night (B3678/S34678) - symmetric pattern dynamics
========================================================================================
"""

import numpy as np
from typing import Tuple, Dict, List
from scipy.signal import convolve2d


class CellularAutomataUniverse:
    """
    Dynamic physical universe where the environment self-organizes according to
    Cellular Automata rules while sovereign agents inhabit and harvest its entropy.
    """
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
        
        # State grids:
        # 0: Empty (vacuum)
        # 1: Nutrient / Energy Cell (active living CA cell)
        # 2: Crystallized Obstacle (dense persistent barrier)
        self.grid = np.zeros(grid_shape, dtype=int)
        self.energy_field = np.zeros(grid_shape, dtype=np.float32)
        
        # Kernel for 8-Moore neighborhood counting
        self.neighbor_kernel = np.array([
            [1, 1, 1],
            [1, 0, 1],
            [1, 1, 1]
        ], dtype=int)
        
        self.reset(density=initial_density)

    def reset(self, density: float = 0.25):
        """Initializes the grid with random living seeds and structural gliders."""
        h, w = self.grid_shape
        raw = self.np_rng.rand(h, w)
        self.grid = np.where(raw < density, 1, 0)
        
        # Insert a few classic gliders / oscillators if space allows
        if h >= 10 and w >= 10:
            # Glider pattern at corner
            self.grid[1:4, 1:4] = np.array([
                [0, 1, 0],
                [0, 0, 1],
                [1, 1, 1]
            ])
            # Pulsar / Blinker oscillator at center
            cy, cx = h // 2, w // 2
            self.grid[cy-1:cy+2, cx] = 1
            
        self.energy_field = self.grid.astype(np.float32) * 2.0

    def step(self, agent_positions: List[Tuple[int, int]]) -> Dict[str, float]:
        """
        Advances the Cellular Automata universe by one physical time step.
        Agents consume nearby living cells for metabolic energy, and living cells evolve.
        """
        h, w = self.grid_shape
        alive = (self.grid == 1).astype(int)
        
        # Count live 8-neighbors with periodic toroidal wrapping
        neighbors = convolve2d(alive, self.neighbor_kernel, mode='same', boundary='wrap')
        
        next_grid = np.zeros_like(self.grid)
        
        # Apply Selected CA Ruleset
        if self.ca_rule == "HighLife (B36/S23)":
            # Born if 3 or 6 neighbors; survives if 2 or 3
            birth = (alive == 0) & ((neighbors == 3) | (neighbors == 6))
            survive = (alive == 1) & ((neighbors == 2) | (neighbors == 3))
        elif self.ca_rule == "Seeds (B2/S)":
            # Born if 2 neighbors; all living die immediately (chaotic explosion)
            birth = (alive == 0) & (neighbors == 2)
            survive = np.zeros_like(alive, dtype=bool)
        elif self.ca_rule == "Day & Night (B3678/S34678)":
            birth = (alive == 0) & np.isin(neighbors, [3, 6, 7, 8])
            survive = (alive == 1) & np.isin(neighbors, [3, 4, 6, 7, 8])
        else:
            # Standard Conway's Game of Life (B3/S23)
            birth = (alive == 0) & (neighbors == 3)
            survive = (alive == 1) & ((neighbors == 2) | (neighbors == 3))
            
        next_grid[birth | survive] = 1
        
        # Density regulation: very dense clusters over time crystallize into obstacles (CellType = 2)
        dense_clusters = (neighbors >= 6) & (next_grid == 1)
        next_grid[dense_clusters] = 2
        
        # Agents interact with substrate: standing on a cell consumes nutrient energy
        rewards = {}
        for idx, (ay, ax) in enumerate(agent_positions):
            if 0 <= ay < h and 0 <= ax < w:
                if next_grid[ay, ax] == 1:
                    # Nutrient absorbed: agent gains vitality, cell temporarily dissipates
                    rewards[f"agent_{idx}"] = 5.0
                    next_grid[ay, ax] = 0
                elif next_grid[ay, ax] == 2:
                    # Friction / obstacle collision penalty
                    rewards[f"agent_{idx}"] = -0.5
                else:
                    rewards[f"agent_{idx}"] = 0.05
                    
        self.grid = next_grid
        self.energy_field = np.clip(self.energy_field * 0.95 + (self.grid == 1) * 1.5, 0.0, 10.0)
        return rewards

    def get_observation_window(self, pos: Tuple[int, int], aperture: int = 3) -> np.ndarray:
        """Returns local observational slice around an agent's coordinates."""
        h, w = self.grid_shape
        py, px = pos
        y0, y1 = max(0, py - aperture), min(h, py + aperture + 1)
        x0, x1 = max(0, px - aperture), min(w, px + aperture + 1)
        return self.grid[y0:y1, x0:x1].copy()
