"""
========================================================================================
ENVIRONMENT PLUG-IN 2: NON-STATIONARY SEASONAL SCARCITY CA (OPTION 6)
========================================================================================
Implements a 4-season dynamic thermodynamic climate cycle:
- 🌸 Spring: Moderate regrowth, low friction, mild temperature.
- ☀️ Summer: Maximum abundance, high regrowth, rapid energy synthesis.
- 🍂 Autumn: Cooling climate, decaying replenishment, scarcity onset.
- ❄️ Winter: Total Famine ($P_{regen}=0.0$), harsh metabolic friction, cosmic pulses OFF.

Supports Substrate Energy Caching (Cell Type 3):
- Agents with high surplus energy can construct static crystalline caches.
- Caches persist through the Winter freeze, creating the evolutionary necessity
  for storage and external memory drives.
========================================================================================
"""

import math
import numpy as np
from typing import Tuple, Dict, Any, List
from scipy.signal import convolve2d
from base_substrate import BaseSubstrateUniverse


class SeasonalScarcityCAUniverse(BaseSubstrateUniverse):
    def __init__(
        self,
        grid_shape: Tuple[int, int] = (25, 25),
        ca_rule: str = "Conway (B3/S23)",
        season_length: int = 4000,
        initial_density: float = 0.25,
        seed: int = 42
    ):
        super().__init__(grid_shape=grid_shape, name="SeasonalScarcity-CA")
        self.ca_rule = ca_rule
        self.season_length = season_length
        self.np_rng = np.random.RandomState(seed)
        self.grid = np.zeros(grid_shape, dtype=int)
        self.neighbor_kernel = np.array([
            [1, 1, 1],
            [1, 0, 1],
            [1, 1, 1]
        ], dtype=int)
        self.caches: Dict[Tuple[int, int], float] = {}
        self.reset(density=initial_density)

    def reset(self, density: float = 0.25):
        h, w = self.grid_shape
        raw = self.np_rng.rand(h, w)
        self.grid = np.where(raw < density, 1, 0)
        self.caches.clear()
        if h >= 10 and w >= 10:
            self.grid[1:4, 1:4] = np.array([
                [0, 1, 0],
                [0, 0, 1],
                [1, 1, 1]
            ])
            cy, cx = h // 2, w // 2
            self.grid[cy-1:cy+2, cx] = 1
        self.step_count = 0

    def get_climate_state(self) -> Dict[str, Any]:
        """Calculates current seasonal phase angle and thermodynamic climate properties."""
        year_progress = (self.step_count % self.season_length) / float(self.season_length)
        
        if year_progress < 0.25:
            # 🌸 SPRING: Phase [0.0, 0.25)
            season = "Spring"
            icon = "🌸"
            temp = 1.0 + 0.5 * math.sin(year_progress * 8 * math.pi)
            regrowth = 0.15
            friction_mult = 0.6  # Low basal friction (0.03 H)
            is_famine = False
        elif year_progress < 0.50:
            # ☀️ SUMMER: Phase [0.25, 0.50)
            season = "Summer"
            icon = "☀️"
            temp = 2.0 + 0.5 * math.sin((year_progress - 0.25) * 8 * math.pi)
            regrowth = 0.25
            friction_mult = 1.0  # Standard basal friction (0.05 H)
            is_famine = False
        elif year_progress < 0.75:
            # 🍂 AUTUMN: Phase [0.50, 0.75)
            season = "Autumn"
            icon = "🍂"
            temp = 1.2 - 0.7 * ((year_progress - 0.50) / 0.25)
            regrowth = 0.05
            friction_mult = 1.6  # Rising friction (0.08 H)
            is_famine = False
        else:
            # ❄️ WINTER: Phase [0.75, 1.0)
            season = "Winter"
            icon = "❄️"
            temp = 0.2
            regrowth = 0.00  # ZERO natural regrowth
            friction_mult = 3.0  # Severe freeze friction (0.15 H)
            is_famine = True

        return {
            "environment_name": "Seasonal Scarcity 2D CA",
            "season": season,
            "season_icon": icon,
            "solar_phase": round(year_progress, 4),
            "season_step": self.step_count % self.season_length,
            "ambient_temp": round(temp, 2),
            "regrowth_rate": regrowth,
            "friction_mult": friction_mult,
            "cache_count": len(self.caches),
            "is_famine": is_famine
        }

    def deposit_energy_cache(self, py: int, px: int, amount: float = 15.0) -> bool:
        """Deposit a static crystalline energy cache (Cell Type 3) at coordinates."""
        h, w = self.grid_shape
        py = max(0, min(h - 1, py))
        px = max(0, min(w - 1, px))
        
        # Can only place a cache on an empty or harvested cell
        if self.grid[py, px] != 2:
            self.grid[py, px] = 3
            self.caches[(py, px)] = amount
            return True
        return False

    def step(self, agent_positions: Dict[str, Tuple[int, int]]) -> Dict[str, float]:
        self.step_count += 1
        h, w = self.grid_shape
        climate = self.get_climate_state()
        is_famine = climate["is_famine"]
        regrowth_rate = climate["regrowth_rate"]
        
        # 1. Cellular Automata Physics (Living cells only)
        alive = (self.grid == 1).astype(int)
        neighbors = convolve2d(alive, self.neighbor_kernel, mode='same', boundary='wrap')
        
        next_grid = np.zeros_like(self.grid)
        
        # Standard Conway rules for living matter
        birth = (alive == 0) & (neighbors == 3)
        survive = (alive == 1) & ((neighbors == 2) | (neighbors == 3))
        
        if is_famine:
            # In Winter freeze, birth is severely inhibited and survival decays
            birth = False
            survive = (alive == 1) & (neighbors == 2)  # Narrow survival window
            
        next_grid[birth | survive] = 1
        
        # Dense clusters become obstacles (Type 2)
        dense_obstacles = (neighbors >= 6) & (next_grid == 1)
        next_grid[dense_obstacles] = 2
        
        # Preserve existing Caches (Type 3) through all seasons
        for (cy, cx) in list(self.caches.keys()):
            if 0 <= cy < h and 0 <= cx < w:
                next_grid[cy, cx] = 3

        # 2. Agent Harvesting & Interaction
        rewards: Dict[str, float] = {}
        for aid, (py, px) in agent_positions.items():
            py = max(0, min(h - 1, py))
            px = max(0, min(w - 1, px))
            cell_type = next_grid[py, px]
            
            if cell_type == 1:
                # Harvest natural food
                rewards[aid] = 8.0
                next_grid[py, px] = 0
            elif cell_type == 3:
                # Harvest Stored Energy Cache! Provides massive survival boost in famine
                cache_val = self.caches.pop((py, px), 15.0)
                rewards[aid] = cache_val + 5.0  # +20.0 H
                next_grid[py, px] = 0
            elif cell_type == 2:
                # Collision with dense obstacle
                rewards[aid] = -0.5
            else:
                # Open void movement
                rewards[aid] = 0.02
                
        # 3. Seasonal Regrowth & Cosmic Pulses
        if not is_famine and regrowth_rate > 0:
            # During Spring & Summer, random seeding happens proportional to regrowth_rate
            if np.sum(next_grid == 1) < int(h * w * regrowth_rate * 0.5):
                raw = self.np_rng.rand(h, w)
                mask = (raw < (regrowth_rate * 0.5)) & (next_grid == 0)
                next_grid[mask] = 1
        # In Winter (is_famine == True), NO regrowth and NO cosmic pulse!
        
        self.grid = next_grid
        return rewards

    def get_observation(self, py: int, px: int, aperture: int) -> np.ndarray:
        h, w = self.grid_shape
        y_min, y_max = max(0, py - aperture), min(h, py + aperture + 1)
        x_min, x_max = max(0, px - aperture), min(w, px + aperture + 1)
        return self.grid[y_min:y_max, x_min:x_max]

    def get_climate_telemetry(self) -> Dict[str, Any]:
        return self.get_climate_state()
