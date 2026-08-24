r"""
========================================================================================
ENVIRONMENT PLUG-IN 3: CONTINUOUS WAVE LENIA (UNIVERSE 3)
========================================================================================
Implements the continuous space, continuous state, and continuous time formulation
of Lenia (Bert Wang-Chak Chan, 2019):

A^{t + \Delta t} = clip( A^t + \Delta t * G(K * A^t), 0.0, 1.0 )

- State Field: psi(x, y) in [0.0, 1.0] (Real-valued continuous biomass/energy density)
- Perception: Concentric continuous ring kernel K(r)
- Growth Mapping: Unimodal Gaussian mapping G(u) = 2 * exp(-(u - mu)^2 / 2*sigma^2) - 1
- Infinite Degrees of Freedom: Continuous differential wave dynamics
========================================================================================
"""

import numpy as np
from typing import Tuple, Dict, Any, List
from scipy.signal import convolve2d
from base_substrate import BaseSubstrateUniverse


class LeniaContinuousUniverse(BaseSubstrateUniverse):
    def __init__(
        self,
        grid_shape: Tuple[int, int] = (25, 25),
        R: float = 5.0,
        T: float = 10.0,
        mu: float = 0.15,
        sigma: float = 0.015,
        seed: int = 42,
        ca_rule: str = "Lenia-Continuous",
        **kwargs: Any
    ):
        super().__init__(grid_shape=grid_shape, name="Continuous-Lenia")
        self.ca_rule = ca_rule
        self.R = R
        self.dt = 1.0 / T
        self.mu = mu
        self.sigma = sigma
        self.np_rng = np.random.RandomState(seed)
        
        # 1. Build Precomputed Continuous Concentric Ring Kernel K(r)
        self.kernel = self._build_lenia_kernel(R)
        
        # 2. Continuous State Field psi(x, y) in [0.0, 1.0]
        self.grid = np.zeros(grid_shape, dtype=np.float32)
        self.reset()

    def _build_lenia_kernel(self, R: float) -> np.ndarray:
        """Constructs a normalized continuous concentric ring convolution kernel."""
        rad = int(np.ceil(R))
        size = 2 * rad + 1
        y, x = np.ogrid[-rad:rad+1, -rad:rad+1]
        dist = np.sqrt(x**2 + y**2) / R
        
        # Unimodal continuous Gaussian ring centered at r = 0.5
        kernel = np.zeros((size, size), dtype=np.float32)
        valid = (dist > 0.0) & (dist < 1.0)
        kernel[valid] = np.exp(-((dist[valid] - 0.5) ** 2) / (2.0 * (0.15 ** 2)))
        
        total_sum = float(np.sum(kernel))
        if total_sum > 0:
            kernel /= total_sum
        return kernel

    def reset(self, initial_droplets: int = 3, **kwargs: Any):
        """Initializes continuous fluid field with localized Gaussian soliton seeds."""
        h, w = self.grid_shape
        self.grid = np.zeros(self.grid_shape, dtype=np.float32)
        
        # Seed smooth Gaussian droplets (potential soliton seeds)
        for _ in range(initial_droplets):
            cy = self.np_rng.randint(4, h - 4)
            cx = self.np_rng.randint(4, w - 4)
            y, x = np.ogrid[:h, :w]
            dist_sq = (y - cy)**2 + (x - cx)**2
            self.grid += np.exp(-dist_sq / (2.0 * 2.5**2)).astype(np.float32) * 0.8
            
        self.grid = np.clip(self.grid, 0.0, 1.0)
        self.step_count = 0

    def step(self, agent_positions: Dict[str, Tuple[int, int]]) -> Dict[str, float]:
        self.step_count += 1
        h, w = self.grid_shape
        
        # 1. Continuous Convolution Operator: U(x, y) = (K * psi)(x, y)
        potential = convolve2d(self.grid, self.kernel, mode='same', boundary='wrap')
        
        # 2. Continuous Gaussian Growth Mapping: G(u)
        growth = 2.0 * np.exp(-((potential - self.mu) ** 2) / (2.0 * (self.sigma ** 2))) - 1.0
        
        # 3. Continuous Time Differential Integration: psi_{t+1} = clip(psi + dt * G(u), 0, 1)
        next_grid = np.clip(self.grid + self.dt * growth, 0.0, 1.0)
        
        # 4. Spontaneous Soliton Maintenance (Cosmic Wave Pulse)
        total_biomass = float(np.sum(next_grid))
        if total_biomass < 3.0:
            cy = self.np_rng.randint(4, h - 4)
            cx = self.np_rng.randint(4, w - 4)
            y, x = np.ogrid[:h, :w]
            dist_sq = (y - cy)**2 + (x - cx)**2
            next_grid += np.exp(-dist_sq / (2.0 * 2.0**2)).astype(np.float32) * 0.7
            next_grid = np.clip(next_grid, 0.0, 1.0)

        # 5. Agent Interaction with Continuous Wave Density
        rewards: Dict[str, float] = {}
        for aid, (py, px) in agent_positions.items():
            py = max(0, min(h - 1, py))
            px = max(0, min(w - 1, px))
            density = float(next_grid[py, px])
            
            if density >= 0.35:
                # Harvest continuous biomass: reward proportional to fluid wave density
                rewards[aid] = float(density * 12.0)
                # Diminish harvested peak locally
                next_grid[py, px] = max(0.0, density - 0.20)
            elif density >= 0.85:
                # Dense vortex resistance / fluid drag
                rewards[aid] = -0.5
            else:
                rewards[aid] = 0.02

        self.grid = next_grid
        return rewards

    def get_observation(self, py: int, px: int, aperture: int) -> np.ndarray:
        """Extracts local continuous sensory patch."""
        h, w = self.grid_shape
        y_min, y_max = max(0, py - aperture), min(h, py + aperture + 1)
        x_min, x_max = max(0, px - aperture), min(w, px + aperture + 1)
        return self.grid[y_min:y_max, x_min:x_max]

    def get_climate_telemetry(self) -> Dict[str, Any]:
        """Telemetry on the continuous Lenia wave state."""
        biomass = float(np.sum(self.grid))
        max_density = float(np.max(self.grid))
        mean_density = float(np.mean(self.grid))
        
        return {
            "environment_name": "Continuous Wave Lenia",
            "season": "Continuous Fluid Dynamics",
            "season_icon": "🌊",
            "solar_phase": round(mean_density, 4),
            "ambient_temp": round(1.0 + max_density, 2),
            "regrowth_rate": round(mean_density, 3),
            "total_biomass": round(biomass, 2),
            "max_density": round(max_density, 3),
            "friction_mult": 1.0,
            "cache_count": 0,
            "is_famine": False
        }
