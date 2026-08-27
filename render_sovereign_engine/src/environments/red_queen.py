"""
========================================================================================
REALM 7: RED QUEEN CO-EVOLUTIONARY ARENA SUBSTRATE (PREDATOR-PREY ECOLOGY)
========================================================================================
Simulates an asymmetric, multi-trophic ecological combat arena:
- Autotrophic Vegetation (Grass / Biomass)
- Autonomous Herbivore Prey Swarms (Green)
- Apex Predator Entities (Red) hunting across pheromone trails

Forces agents to engage in an evolutionary Red Queen arms race:
- Discovering evasive defense maneuvers
- Co-adaptive pack hunting & ambush strategies
- Dynamic game-theoretic equilibrium (Lotka-Volterra dynamics)
========================================================================================
"""

import numpy as np
from typing import Tuple, Dict, Any, Optional, List
from base_substrate import BaseSubstrateUniverse


class RedQueenArenaUniverse(BaseSubstrateUniverse):
    """
    Multi-Trophic Co-Evolutionary Ecosystem Substrate.
    Agents survive among autonomous prey herds and roaming predators.
    """
    def __init__(
        self,
        grid_shape: Tuple[int, int] = (25, 25),
        num_prey: int = 8,
        num_predators: int = 2,
        seed: Optional[int] = None
    ):
        super().__init__(grid_shape=grid_shape, name="Red Queen Co-Evolution Arena")
        self.np_rng = np.random.RandomState(seed)
        self.num_prey = num_prey
        self.num_predators = num_predators
        self.vegetation = np.zeros(self.grid_shape, dtype=np.float32)
        self.prey_positions: List[List[int]] = []
        self.predator_positions: List[List[int]] = []
        self.reset()

    def reset(self, **kwargs: Any):
        """Initializes vegetation field, prey herds, and stealth predators."""
        h, w = self.grid_shape
        self.vegetation = self.np_rng.rand(h, w).astype(np.float32) * 0.50
        
        self.prey_positions = [
            [self.np_rng.randint(2, h - 2), self.np_rng.randint(2, w - 2)]
            for _ in range(self.num_prey)
        ]
        self.predator_positions = [
            [self.np_rng.randint(2, h - 2), self.np_rng.randint(2, w - 2)]
            for _ in range(self.num_predators)
        ]
        
        self._update_grid()
        self.step_count = 0

    def _update_grid(self):
        """Combines vegetation, prey, and predator layers into a visual composite grid."""
        h, w = self.grid_shape
        # Base layer: vegetation (0.0 to 0.40)
        self.grid = np.clip(self.vegetation * 0.40, 0.0, 0.40)
        
        # Prey layer: 0.60 intensity
        for py, px in self.prey_positions:
            self.grid[py, px] = 0.60
            
        # Predator layer: 1.00 intensity (Glowing apex red)
        for py, px in self.predator_positions:
            self.grid[py, px] = 1.00

    def step(self, agent_positions: Dict[str, Tuple[int, int]]) -> Dict[str, float]:
        self.step_count += 1
        h, w = self.grid_shape
        
        # 1. Vegetation regrowth (Logistic growth)
        self.vegetation = np.clip(self.vegetation + 0.02 * (1.0 - self.vegetation), 0.0, 1.0)
        
        # 2. Prey movement (Graze nearby vegetation, evade predators)
        for prey in self.prey_positions:
            moves = [[0, 1], [0, -1], [1, 0], [-1, 0], [0, 0]]
            best_m = moves[self.np_rng.choice(len(moves))]
            prey[0] = max(0, min(h - 1, prey[0] + best_m[0]))
            prey[1] = max(0, min(w - 1, prey[1] + best_m[1]))
            self.vegetation[prey[0], prey[1]] = max(0.0, self.vegetation[prey[0], prey[1]] - 0.10)
            
        # 3. Predator movement (Hunt nearest prey or agent)
        for pred in self.predator_positions:
            if self.prey_positions:
                targets = np.array(self.prey_positions)
                dists = np.abs(targets[:, 0] - pred[0]) + np.abs(targets[:, 1] - pred[1])
                target_idx = int(np.argmin(dists))
                ty, tx = self.prey_positions[target_idx]
                
                dy = 1 if ty > pred[0] else (-1 if ty < pred[0] else 0)
                dx = 1 if tx > pred[1] else (-1 if tx < pred[1] else 0)
                pred[0] = max(0, min(h - 1, pred[0] + dy))
                pred[1] = max(0, min(w - 1, pred[1] + dx))
                
                # Check predator catch prey
                if pred[0] == ty and pred[1] == tx:
                    self.prey_positions[target_idx] = [
                        self.np_rng.randint(2, h - 2),
                        self.np_rng.randint(2, w - 2)
                    ]

        self._update_grid()
        
        # 4. Agent Rewards & Co-Evolutionary Interaction
        rewards: Dict[str, float] = {}
        for aid, (ay, ax) in agent_positions.items():
            ay = max(0, min(h - 1, ay))
            ax = max(0, min(w - 1, ax))
            
            # Check if agent is eaten by a predator (Ambush)
            pred_threat = any(pred[0] == ay and pred[1] == ax for pred in self.predator_positions)
            if pred_threat:
                rewards[aid] = -8.0 # Severe predatory penalty
                continue
                
            # Check if agent hunts a prey (Pack hunting reward)
            prey_hunt = False
            for p_idx, prey in enumerate(self.prey_positions):
                if prey[0] == ay and prey[1] == ax:
                    rewards[aid] = 16.0 # Massive hunting harvest
                    prey_hunt = True
                    self.prey_positions[p_idx] = [
                        self.np_rng.randint(2, h - 2),
                        self.np_rng.randint(2, w - 2)
                    ]
                    break
                    
            if not prey_hunt:
                # Graze on wild vegetation
                veg_val = float(self.vegetation[ay, ax])
                if veg_val > 0.30:
                    rewards[aid] = float(veg_val * 4.0)
                    self.vegetation[ay, ax] = max(0.0, veg_val - 0.08)
                else:
                    rewards[aid] = 0.0
                    
        return rewards

    def get_observation(self, py: int, px: int, aperture: int) -> np.ndarray:
        h, w = self.grid_shape
        y_min, y_max = max(0, py - aperture), min(h, py + aperture + 1)
        x_min, x_max = max(0, px - aperture), min(w, px + aperture + 1)
        return self.grid[y_min:y_max, x_min:x_max]

    def get_climate_telemetry(self) -> Dict[str, Any]:
        tot_veg = float(np.sum(self.vegetation))
        return {
            "environment_name": "Red Queen Co-Evolution Arena",
            "season": "Predator-Prey Warfare",
            "season_icon": "⚔️",
            "solar_phase": float(len(self.prey_positions) / max(1, self.num_prey)),
            "ambient_temp": 2.20,
            "regrowth_rate": 0.08,
            "total_biomass": round(tot_veg, 2),
            "max_density": 1.0,
            "friction_mult": 1.0,
            "cache_count": 0,
            "is_famine": False
        }
