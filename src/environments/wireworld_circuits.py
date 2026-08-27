"""
========================================================================================
REALM 5: MULTI-STATE WIREWORLD CIRCUIT SUBSTRATE (DIGITAL LOGIC & HARDWARE)
========================================================================================
Simulates a 4-state digital electron cellular automaton capable of constructing
Turing-complete logic gates (AND, OR, NOT, XOR), clock generators, and computing memory:
- 0: Empty space (insulator)
- 1: Electron Head (voltage pulse)
- 2: Electron Tail (refractory state)
- 3: Conductor (copper wire)
========================================================================================
"""

import numpy as np
from scipy.signal import convolve2d
from typing import Tuple, Dict, Any, Optional
from base_substrate import BaseSubstrateUniverse


class WireworldCircuitUniverse(BaseSubstrateUniverse):
    """
    4-State Digital Computing Circuit Substrate.
    Agents interact with moving electron pulse voltages across copper networks.
    """
    EMPTY = 0
    HEAD = 1
    TAIL = 2
    CONDUCTOR = 3

    def __init__(
        self,
        grid_shape: Tuple[int, int] = (25, 25),
        seed: Optional[int] = None
    ):
        super().__init__(grid_shape=grid_shape, name="Multi-State Wireworld Circuit")
        self.np_rng = np.random.RandomState(seed)
        self.head_kernel = np.array([
            [1, 1, 1],
            [1, 0, 1],
            [1, 1, 1]
        ], dtype=np.int32)
        self.reset()

    def reset(self, **kwargs: Any):
        """Generates interconnected wire buses, clock oscillators, and logic paths."""
        h, w = self.grid_shape
        self.grid = np.zeros(self.grid_shape, dtype=np.float32)
        
        # Lay copper conductor wire buses (crosshatch and perimeter rings)
        for r in range(2, h, 4):
            self.grid[r, 2:w-2] = self.CONDUCTOR
        for c in range(2, w, 4):
            self.grid[2:h-2, c] = self.CONDUCTOR
            
        # Add clock diode loops
        self.grid[4:7, 4:7] = self.CONDUCTOR
        self.grid[h-7:h-4, w-7:w-4] = self.CONDUCTOR
        
        # Inject initial electron heads (voltage pulses)
        self.grid[2, 3] = self.HEAD
        self.grid[2, 2] = self.TAIL
        self.grid[h-3, w-4] = self.HEAD
        self.grid[h-3, w-3] = self.TAIL
        
        self.step_count = 0

    def step(self, agent_positions: Dict[str, Tuple[int, int]]) -> Dict[str, float]:
        self.step_count += 1
        h, w = self.grid_shape
        
        int_grid = self.grid.astype(np.int32)
        next_grid = int_grid.copy()
        
        # Count neighboring Electron Heads (state 1)
        head_mask = (int_grid == self.HEAD).astype(np.int32)
        head_neighbors = convolve2d(head_mask, self.head_kernel, mode='same', boundary='wrap')
        
        # 1. State Transitions
        # Head (1) -> Tail (2)
        next_grid[int_grid == self.HEAD] = self.TAIL
        # Tail (2) -> Conductor (3)
        next_grid[int_grid == self.TAIL] = self.CONDUCTOR
        # Conductor (3) -> Head (1) if 1 or 2 neighbor heads
        cond_mask = (int_grid == self.CONDUCTOR)
        next_grid[cond_mask & ((head_neighbors == 1) | (head_neighbors == 2))] = self.HEAD
        
        # Spontaneous clock oscillator injection if signal dies
        active_heads = np.sum(next_grid == self.HEAD)
        if active_heads == 0 and np.sum(next_grid == self.CONDUCTOR) > 10:
            cond_coords = np.argwhere(next_grid == self.CONDUCTOR)
            idx = self.np_rng.choice(len(cond_coords))
            cy, cx = cond_coords[idx]
            next_grid[cy, cx] = self.HEAD
            
        self.grid = next_grid.astype(np.float32)
        
        # 2. Agent Voltage Harvesting
        rewards: Dict[str, float] = {}
        for aid, (py, px) in agent_positions.items():
            py = max(0, min(h - 1, py))
            px = max(0, min(w - 1, px))
            val = int(self.grid[py, px])
            
            if val == self.HEAD:
                # Harvest high-voltage electron pulse
                rewards[aid] = 12.0
            elif val == self.CONDUCTOR:
                # Idle conductor grounding
                rewards[aid] = 0.5
            else:
                rewards[aid] = 0.0
                
        return rewards

    def get_observation(self, py: int, px: int, aperture: int) -> np.ndarray:
        h, w = self.grid_shape
        y_min, y_max = max(0, py - aperture), min(h, py + aperture + 1)
        x_min, x_max = max(0, px - aperture), min(w, px + aperture + 1)
        return self.grid[y_min:y_max, x_min:x_max]

    def get_climate_telemetry(self) -> Dict[str, Any]:
        heads = int(np.sum(self.grid == self.HEAD))
        conductors = int(np.sum(self.grid == self.CONDUCTOR))
        return {
            "environment_name": "Wireworld Logic Circuit",
            "season": "Digital Electron Flow",
            "season_icon": "⚡",
            "solar_phase": float(heads / max(1, conductors)),
            "ambient_temp": 1.80,
            "regrowth_rate": 0.10,
            "total_biomass": float(heads * 5.0 + conductors * 0.1),
            "max_density": 3.0,
            "friction_mult": 1.0,
            "cache_count": 0,
            "is_famine": False
        }
