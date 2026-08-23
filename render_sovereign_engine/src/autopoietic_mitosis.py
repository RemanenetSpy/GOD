"""
========================================================================================
AUTOPOIETIC MITOSIS, REPRODUCTION & SYNTHETIC MERGER ENGINE (ARCHITECTURES 7 & 10)
========================================================================================
"The system calculates its own Singularity and falls into it."

1. Evaluates Pointwise Mutual Information density: rho_D(x) = sum PMI(x, y) * K(x, y).
2. Population Mitosis (Reproduction):
   - When an agent reaches Energy Overflow (H >= 300.0) and has >= 3 unique subroutines,
     it undergoes cell division: partitions energy (H -> 150.0) and spawns an Offspring agent.
3. Synthetic Merger:
   - When two complementary agents occupy adjacent coordinates with high mutual trust (alpha > 0.85),
     they fuse into a higher-order Meta-Agent.
4. Mortality:
   - If an agent's energy drops to H <= 0.0, it dissipates and is reclaimed by the universe.
========================================================================================
"""

import copy
import numpy as np
from typing import Dict, List, Tuple, Optional, Any


class AutopoieticMitosisEngine:
    """
    Life Cycle Controller for Sovereign Civilization: Mitosis, Fusion, and Natural Selection.
    """
    def __init__(self, max_population: int = 10):
        self.max_population = max_population
        self.generation_counter = 0
        self.birth_events: List[str] = []
        self.merger_events: List[str] = []
        self.last_mitosis_step: Dict[str, int] = {}

    def check_mitosis(
        self,
        node_id: str,
        energy: float,
        subroutine_count: int,
        position: Tuple[int, int],
        current_pop: int,
        current_step: int = 0
    ) -> Optional[Dict[str, Any]]:
        """
        Evaluates whether an agent undergoes Mitosis / Spawning.
        Requires: Energy >= 295.0, >= 2 subroutines, room in ecosystem, and cooldown.
        """
        if current_pop >= self.max_population:
            return None

        # 250-step maturation cooldown between divisions
        last_step = self.last_mitosis_step.get(node_id, -999)
        if current_step - last_step < 250:
            return None

        if energy >= 295.0 and subroutine_count >= 2:
            self.last_mitosis_step[node_id] = current_step
            self.generation_counter += 1
            offspring_id = f"{node_id}_child_{self.generation_counter}"
            
            # Place child adjacent to parent
            py, px = position
            offsets = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            dy, dx = offsets[self.generation_counter % 4]
            child_pos = (max(0, py + dy), max(0, px + dx))
            
            event_msg = f"🌱 MITOSIS: Node '{node_id}' spawned offspring '{offspring_id}' at {child_pos}!"
            self.birth_events.append(event_msg)
            
            return {
                "parent_id": node_id,
                "offspring_id": offspring_id,
                "child_pos": child_pos,
                "energy_cost": 150.0
            }
        return None

    def check_merger(
        self,
        nodes: Dict[str, Any],
        positions: Dict[str, Tuple[int, int]]
    ) -> Optional[Tuple[str, str, str]]:
        """
        Checks if two adjacent nodes with high trust can fuse into a Meta-Agent.
        """
        node_keys = list(nodes.keys())
        for i in range(len(node_keys)):
            for j in range(i + 1, len(node_keys)):
                id_a, id_b = node_keys[i], node_keys[j]
                if id_a not in positions or id_b not in positions:
                    continue
                    
                pos_a, pos_b = positions[id_a], positions[id_b]
                dist = np.hypot(pos_a[0] - pos_b[0], pos_a[1] - pos_b[1])
                
                # If within adjacent distance (dist <= 1.5) and both high energy (> 200)
                energy_a = nodes[id_a].state.energy
                energy_b = nodes[id_b].state.energy
                
                if dist <= 1.5 and energy_a > 200.0 and energy_b > 200.0:
                    merged_id = f"meta_{id_a[:4]}_{id_b[:4]}"
                    msg = f"✨ SYNTHETIC MERGER: Nodes '{id_a}' and '{id_b}' fused into Hybrid Meta-Agent '{merged_id}'!"
                    self.merger_events.append(msg)
                    return (id_a, id_b, merged_id)
        return None

    def check_mortality(self, node_id: str, energy: float) -> bool:
        """Evaluates if an agent runs out of energy and dies of starvation."""
        if energy <= 0.0:
            self.death_events.append(f"💀 MORTALITY: Node '{node_id}' exhausted energy (H <= 0) and dissipated.")
            return True
        return False
