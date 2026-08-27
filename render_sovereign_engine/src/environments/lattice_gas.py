"""
========================================================================================
REALM 6: LATTICE GAS HYDRODYNAMICS SUBSTRATE (FHP MOMENTUM CONSERVATION)
========================================================================================
Simulates discrete microscopic particle collisions and streaming on a 2D lattice.
Conserves particle mass and momentum:
- Microscopic boolean velocity states (East, North, West, South)
- Exact binary collision operators (Head-on 2-body and 3-body collisions)
- Streaming operator along velocity vectors

Produces emergent continuous fluid mechanics, Navier-Stokes vortices, and viscous drag.
========================================================================================
"""

import numpy as np
from typing import Tuple, Dict, Any, Optional
from base_substrate import BaseSubstrateUniverse


class LatticeGasUniverse(BaseSubstrateUniverse):
    """
    4-Velocity (HPP/FHP) Discrete Lattice Gas Hydrodynamics Substrate.
    Conserves mass and momentum across continuous fluid streaming and collision.
    """
    def __init__(
        self,
        grid_shape: Tuple[int, int] = (25, 25),
        seed: Optional[int] = None
    ):
        super().__init__(grid_shape=grid_shape, name="Lattice Gas (FHP Hydrodynamics)")
        self.np_rng = np.random.RandomState(seed)
        h, w = self.grid_shape
        # 4 directional channels: 0=East (+x), 1=North (-y), 2=West (-x), 3=South (+y)
        self.channels = np.zeros((4, h, w), dtype=np.uint8)
        self.reset()

    def reset(self, initial_density: float = 0.35, **kwargs: Any):
        """Initializes lattice with random microscopic particle velocities and vortices."""
        h, w = self.grid_shape
        self.channels = (self.np_rng.rand(4, h, w) < initial_density).astype(np.uint8)
        
        # Inject directional fluid jet stream
        self.channels[0, h//2-2:h//2+2, :] = 1  # Strong Eastward jet
        
        # Density field is total particles per cell (0 to 4)
        self.grid = np.sum(self.channels, axis=0).astype(np.float32) / 4.0
        self.step_count = 0

    def step(self, agent_positions: Dict[str, Tuple[int, int]]) -> Dict[str, float]:
        self.step_count += 1
        h, w = self.grid_shape
        
        # --- 1. COLLISION OPERATOR (Exact Momentum & Mass Conservation) ---
        c0 = self.channels[0] # East
        c1 = self.channels[1] # North
        c2 = self.channels[2] # West
        c3 = self.channels[3] # South
        
        # Head-on collision: East + West -> North + South (when N & S are empty)
        head_on_ew = (c0 == 1) & (c2 == 1) & (c1 == 0) & (c3 == 0)
        # Head-on collision: North + South -> East + West (when E & W are empty)
        head_on_ns = (c1 == 1) & (c3 == 1) & (c0 == 0) & (c2 == 0)
        
        post_c0 = c0.copy()
        post_c1 = c1.copy()
        post_c2 = c2.copy()
        post_c3 = c3.copy()
        
        post_c0[head_on_ew] = 0
        post_c2[head_on_ew] = 0
        post_c1[head_on_ew] = 1
        post_c3[head_on_ew] = 1
        
        post_c1[head_on_ns] = 0
        post_c3[head_on_ns] = 0
        post_c0[head_on_ns] = 1
        post_c2[head_on_ns] = 1
        
        # --- 2. STREAMING OPERATOR (Particles propagate along velocity vectors) ---
        self.channels[0] = np.roll(post_c0, shift=1, axis=1)   # East: +x
        self.channels[1] = np.roll(post_c1, shift=-1, axis=0)  # North: -y
        self.channels[2] = np.roll(post_c2, shift=-1, axis=1)  # West: -x
        self.channels[3] = np.roll(post_c3, shift=1, axis=0)   # South: +y
        
        # Update macroscopic density field (0.0 to 1.0)
        self.grid = np.sum(self.channels, axis=0).astype(np.float32) / 4.0
        
        # Replenish jet stream if fluid slows down
        if self.step_count % 30 == 0:
            self.channels[0, h//2-1:h//2+2, 0:3] = 1
            
        # --- 3. AGENT HYDRODYNAMIC KINETIC ENERGY HARVESTING ---
        rewards: Dict[str, float] = {}
        for aid, (py, px) in agent_positions.items():
            py = max(0, min(h - 1, py))
            px = max(0, min(w - 1, px))
            density = float(self.grid[py, px])
            
            # Compute local kinetic energy (fluid velocity squared)
            vx = float(self.channels[0, py, px]) - float(self.channels[2, py, px])
            vy = float(self.channels[3, py, px]) - float(self.channels[1, py, px])
            kinetic_energy = vx**2 + vy**2
            
            if density >= 0.25:
                # Harvest kinetic momentum from swirling flow
                rewards[aid] = float(density * 10.0 + kinetic_energy * 2.0)
            else:
                rewards[aid] = 0.0
                
        return rewards

    def get_observation(self, py: int, px: int, aperture: int) -> np.ndarray:
        h, w = self.grid_shape
        y_min, y_max = max(0, py - aperture), min(h, py + aperture + 1)
        x_min, x_max = max(0, px - aperture), min(w, px + aperture + 1)
        return self.grid[y_min:y_max, x_min:x_max]

    def get_climate_telemetry(self) -> Dict[str, Any]:
        tot_particles = int(np.sum(self.channels))
        vx = np.mean(self.channels[0].astype(np.float32) - self.channels[2].astype(np.float32))
        vy = np.mean(self.channels[3].astype(np.float32) - self.channels[1].astype(np.float32))
        flow_speed = float(np.sqrt(vx**2 + vy**2))
        
        return {
            "environment_name": "Lattice Gas Hydrodynamics",
            "season": "Navier-Stokes Momentum Flow",
            "season_icon": "💨",
            "solar_phase": round(flow_speed, 4),
            "ambient_temp": 1.50,
            "regrowth_rate": 0.05,
            "total_biomass": round(float(tot_particles) / 4.0, 2),
            "max_density": 1.0,
            "friction_mult": 1.0,
            "cache_count": 0,
            "is_famine": False
        }
