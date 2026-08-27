"""
========================================================================================
REALM 4: REACTION-DIFFUSION SUBSTRATE (GRAY-SCOTT TURING MORPHOGENESIS)
========================================================================================
Simulates continuous multi-chemical Turing pattern morphogenesis:
du/dt = Du * laplacian(u) - u * v^2 + F * (1 - u)
dv/dt = Dv * laplacian(v) + u * v^2 - (F + k) * v

Generates self-replicating chemical spots, labyrinthine Turing waves, and spiral vortices.
========================================================================================
"""

import numpy as np
from scipy.signal import convolve2d
from typing import Tuple, Dict, Any, Optional
from base_substrate import BaseSubstrateUniverse


class ReactionDiffusionUniverse(BaseSubstrateUniverse):
    """
    Continuous 2-chemical Gray-Scott Reaction-Diffusion Substrate.
    Agents interact with spatial morphogen gradients (u, v concentrations).
    """
    def __init__(
        self,
        grid_shape: Tuple[int, int] = (25, 25),
        Du: float = 0.16,
        Dv: float = 0.08,
        feed_rate: float = 0.035,
        kill_rate: float = 0.065,
        dt: float = 1.0,
        seed: Optional[int] = None
    ):
        super().__init__(grid_shape=grid_shape, name="Reaction-Diffusion (Gray-Scott Turing)")
        self.np_rng = np.random.RandomState(seed)
        self.Du = Du
        self.Dv = Dv
        self.F = feed_rate
        self.k = kill_rate
        self.dt = dt
        
        # 5-point discrete Laplace convolution kernel
        self.laplace_kernel = np.array([
            [0.05, 0.20, 0.05],
            [0.20, -1.00, 0.20],
            [0.05, 0.20, 0.05]
        ], dtype=np.float32)
        
        self.u = np.ones(self.grid_shape, dtype=np.float32)
        self.v = np.zeros(self.grid_shape, dtype=np.float32)
        self.reset()

    def reset(self, initial_seeds: int = 3, **kwargs: Any):
        """Initializes uniform U field with localized V chemical seeds."""
        h, w = self.grid_shape
        self.u = np.ones(self.grid_shape, dtype=np.float32)
        self.v = np.zeros(self.grid_shape, dtype=np.float32)
        
        # Seed initial V spots in the center/random points
        for _ in range(initial_seeds):
            cy = self.np_rng.randint(4, h - 4)
            cx = self.np_rng.randint(4, w - 4)
            r = 2
            y_min, y_max = max(0, cy - r), min(h, cy + r + 1)
            x_min, x_max = max(0, cx - r), min(w, cx + r + 1)
            self.u[y_min:y_max, x_min:x_max] = 0.50
            self.v[y_min:y_max, x_min:x_max] = 0.25 + self.np_rng.rand(y_max - y_min, x_max - x_min).astype(np.float32) * 0.10
            
        self.grid = self.v.copy()
        self.step_count = 0

    def step(self, agent_positions: Dict[str, Tuple[int, int]]) -> Dict[str, float]:
        self.step_count += 1
        h, w = self.grid_shape
        
        # 1. 2D Spatial Laplacians
        lap_u = convolve2d(self.u, self.laplace_kernel, mode='same', boundary='wrap')
        lap_v = convolve2d(self.v, self.laplace_kernel, mode='same', boundary='wrap')
        
        # 2. Reaction-Diffusion Equations
        uvv = self.u * (self.v ** 2)
        du = (self.Du * lap_u - uvv + self.F * (1.0 - self.u)) * self.dt
        dv = (self.Dv * lap_v + uvv - (self.F + self.k) * self.v) * self.dt
        
        self.u = np.clip(self.u + du, 0.0, 1.0)
        self.v = np.clip(self.v + dv, 0.0, 1.0)
        
        # Spontaneous seed replenishment if V dies out
        total_v = float(np.sum(self.v))
        if total_v < 1.0:
            cy = self.np_rng.randint(4, h - 4)
            cx = self.np_rng.randint(4, w - 4)
            self.u[cy-1:cy+2, cx-1:cx+2] = 0.50
            self.v[cy-1:cy+2, cx-1:cx+2] = 0.40
            
        self.grid = self.v.copy()
        
        # 3. Agent Harvesting & Metabolic Interaction
        rewards: Dict[str, float] = {}
        for aid, (py, px) in agent_positions.items():
            py = max(0, min(h - 1, py))
            px = max(0, min(w - 1, px))
            v_val = float(self.v[py, px])
            
            if v_val >= 0.20:
                rewards[aid] = float(v_val * 14.0)
                # Consume local V catalyst
                self.v[py, px] = max(0.0, v_val - 0.15)
            else:
                rewards[aid] = 0.0
                
        return rewards

    def get_observation(self, py: int, px: int, aperture: int) -> np.ndarray:
        h, w = self.grid_shape
        y_min, y_max = max(0, py - aperture), min(h, py + aperture + 1)
        x_min, x_max = max(0, px - aperture), min(w, px + aperture + 1)
        return self.grid[y_min:y_max, x_min:x_max]

    def get_climate_telemetry(self) -> Dict[str, Any]:
        tot_v = float(np.sum(self.v))
        max_v = float(np.max(self.v))
        return {
            "environment_name": "Gray-Scott Reaction-Diffusion",
            "season": "Morphogenetic Turing Waves",
            "season_icon": "🧬",
            "solar_phase": self.F,
            "ambient_temp": float(self.k * 25.0),
            "regrowth_rate": float(self.Du),
            "total_biomass": round(tot_v, 2),
            "max_density": round(max_v, 3),
            "friction_mult": 1.0,
            "cache_count": 0,
            "is_famine": False
        }
