"""
ARC Sovereign Living Organism (4-Pillar Council, BinoryCore & Ancestral Memory Embodiment)
Directly connects the original 4 Sovereign Agents and BinoryCore STDP Plasticity
into the ARC Survival Ecology with Retrograde Death Trace and Ancestral Causal Memory.
"""

import numpy as np
from typing import Tuple, List, Dict, Any, Optional

try:
    from binory_core import make_node_id, register_name
except ImportError:
    try:
        from src.binory_core import make_node_id, register_name
    except ImportError:
        def make_node_id(name: str) -> str: return f"node:{name}"
        def register_name(nid: str, name: str) -> None: pass

try:
    from binory_agents import Action, PillarArchetype
except ImportError:
    try:
        from src.binory_agents import Action, PillarArchetype
    except ImportError:
        from enum import Enum
        class Action(Enum):
            OBSERVE = 0
            MOVE_UP = 1
            MOVE_DOWN = 2
            MOVE_LEFT = 3
            MOVE_RIGHT = 4
        class PillarArchetype(Enum):
            CLASSICAL_EIKONAL = "Classical-Eikonal"
            QUANTUM_SUPERPOSED = "Quantum-Superposed"
            MODERN_THERMODYNAMIC = "Modern-Thermodynamic"
            STRING_TOPOLOGICAL = "String-10D-Topological"

try:
    from arc_sovereign_arena.ancestral_memory import AncestralCausalMemory
except ImportError:
    class AncestralCausalMemory:
        def __init__(self):
            self.confirmed_nutrition = {}
            self.toxic_ledger = {}
            self.task_deaths = {}
            self.lethal_traces = []
        def is_confirmed_nutrition(self, *a): return None
        def get_veto_mask(self, *a): return []
        def record_nutrition(self, *a): pass
        def record_toxic(self, *a, **k): pass
        def record_starvation_death(self, *a): pass
        def to_dict(self): return {}
        def load_dict(self, d): pass


class ArcLivingOrganism:
    """
    Embodied avatar of the Sovereign Civilization living on the ARC canvas.
    Directly driven by the 4 Sovereign Pillars, BinoryCore, and Ancestral Causal Memory.
    """

    ACTION_MOVE_UP = 0
    ACTION_MOVE_DOWN = 1
    ACTION_MOVE_LEFT = 2
    ACTION_MOVE_RIGHT = 3
    ACTION_PAINT = 4
    ACTION_REST = 5

    def __init__(self, civilization=None, core=None, ancestral_memory: Optional[AncestralCausalMemory] = None, generation: int = 1):
        self.civilization = civilization
        self.core = core
        self.ancestral_memory = ancestral_memory
        self.generation = generation

        # Embodied Spatial Coordinates
        self.r: int = 0
        self.c: int = 0
        self.selected_color: int = 1
        self.max_energy: float = 150.0
        self.is_alive: bool = True

        # Lifespan & Metabolic Statistics
        self.lifespan_ticks: int = 0
        self.food_eaten: int = 0
        self.wrong_paints: int = 0
        self.puzzles_cleared: int = 0
        self.total_metabolic_reward: float = 0.0

        # Episodic Action Trace (Rolling buffer for Retrograde Death Assignment)
        self.episodic_trace: List[Dict[str, Any]] = []

        # Initialize or synchronize energy from Civilization
        self._sync_energy_from_civilization()

    @property
    def energy(self) -> float:
        """Returns the mean energy of the 4 Sovereign Pillars."""
        if self.civilization and hasattr(self.civilization, "nodes") and self.civilization.nodes:
            energies = [n.state.energy for n in self.civilization.nodes.values() if hasattr(n, "state")]
            if energies:
                return float(np.mean(energies))
        return getattr(self, "_fallback_energy", 100.0)

    @energy.setter
    def energy(self, val: float):
        clipped = float(np.clip(val, 0.0, self.max_energy))
        self._fallback_energy = clipped
        if self.civilization and hasattr(self.civilization, "nodes") and self.civilization.nodes:
            for n in self.civilization.nodes.values():
                if hasattr(n, "state"):
                    n.state.energy = clipped

    def _sync_energy_from_civilization(self):
        if self.civilization and hasattr(self.civilization, "nodes") and self.civilization.nodes:
            for n in self.civilization.nodes.values():
                if hasattr(n, "state") and n.state.energy < 20.0:
                    n.state.energy = 100.0
        else:
            self._fallback_energy = 100.0

    def reset_position(self, grid_h: int, grid_w: int):
        """Places the organism at the center of the canvas and syncs node positions."""
        self.r = grid_h // 2
        self.c = grid_w // 2
        if self.civilization and hasattr(self.civilization, "nodes"):
            for n in self.civilization.nodes.values():
                if hasattr(n, "state") and hasattr(n.state, "position"):
                    n.state.position = (self.r, self.c)

    def perceive_and_spike(self, input_canvas: np.ndarray, working_canvas: np.ndarray) -> List[str]:
        """
        Sensory perception: converts visible ARC canvas features into active signals
        and updates BinoryCore with real STDP causal plasticity.
        """
        h, w = working_canvas.shape
        active_nodes: List[str] = []

        # 1. Local Receptive Patch Spikes (Visual Field around Body)
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nr, nc = self.r + dr, self.c + dc
                if 0 <= nr < h and 0 <= nc < w:
                    color_val = int(working_canvas[nr, nc])
                    nid = make_node_id(f"arc_pix_{nr}_{nc}_{color_val}")
                    register_name(nid, f"arc:({nr},{nc})={color_val}")
                    active_nodes.append(nid)

        # 2. Position & Tool State Spikes
        nid_pos = make_node_id(f"arc_pos_{self.r}_{self.c}")
        register_name(nid_pos, f"pos:({self.r},{self.c})")
        active_nodes.append(nid_pos)

        nid_tool = make_node_id(f"arc_tool_color_{self.selected_color}")
        register_name(nid_tool, f"tool:color_{self.selected_color}")
        active_nodes.append(nid_tool)

        # 3. Update BinoryCore STDP Causal Synapses
        if self.core is not None and hasattr(self.core, "update"):
            try:
                self.core.update(active_nodes, cpu_load=len(active_nodes) * 4.0)
            except Exception:
                pass

        return active_nodes

    def decide_action(self, input_canvas: np.ndarray, working_canvas: np.ndarray, task_id: str = "") -> int:
        """
        Action decided through 4-Pillar Council Consensus informed by Ancestral Causal Memory:
        1. Classical-Eikonal computes spatial vector gradients -> Movement direction
        2. Quantum-Superposed collapses discrete state distribution with ANCESTRAL VETO -> Color tool
        3. Modern-Thermodynamic evaluates metabolic vitality -> Paint vs. Rest
        4. String-10D-Topological tracks global consensus harmony
        """
        if not self.is_alive:
            return self.ACTION_REST

        self.lifespan_ticks += 1
        # Basal metabolic burn: breathing drains energy
        self.energy -= 0.15

        if self.energy <= 0.0:
            self.energy = 0.0
            self.is_alive = False
            return self.ACTION_REST

        h, w = working_canvas.shape

        # 1. Classical-Eikonal Node: Spatial Kinematics & Pathing
        classical_move = self.ACTION_MOVE_RIGHT
        if self.civilization and hasattr(self.civilization, "nodes") and "classical_prime" in self.civilization.nodes:
            c_node = self.civilization.nodes["classical_prime"]
            try:
                act = c_node.select_action()
                if act == Action.MOVE_UP: classical_move = self.ACTION_MOVE_UP
                elif act == Action.MOVE_DOWN: classical_move = self.ACTION_MOVE_DOWN
                elif act == Action.MOVE_LEFT: classical_move = self.ACTION_MOVE_LEFT
                elif act == Action.MOVE_RIGHT: classical_move = self.ACTION_MOVE_RIGHT
                else: classical_move = None
            except Exception:
                classical_move = None

        if classical_move is None:
            # Fallback: exploratory cardinal wander
            classical_move = int(np.random.choice([
                self.ACTION_MOVE_UP, self.ACTION_MOVE_DOWN,
                self.ACTION_MOVE_LEFT, self.ACTION_MOVE_RIGHT
            ]))

        # 2. Quantum-Superposed Node: Discrete Color State Collapse with ANCESTRAL VETO
        confirmed_color = None
        if self.ancestral_memory:
            confirmed_color = self.ancestral_memory.is_confirmed_nutrition(task_id, self.r, self.c)

        if confirmed_color is not None:
            # INSTANT RECALL: An ancestor already verified this nutrient color!
            self.selected_color = confirmed_color
        else:
            # Collapse Quantum Belief Tensor, actively VETOING colors that poisoned ancestors!
            vetoed = self.ancestral_memory.get_veto_mask(task_id, self.r, self.c) if self.ancestral_memory else []
            raw_probs = np.ones(10, dtype=float)

            if self.civilization and hasattr(self.civilization, "nodes") and "quantum_prime" in self.civilization.nodes:
                q_node = self.civilization.nodes["quantum_prime"]
                try:
                    if hasattr(q_node.belief_engine, "belief_tensor"):
                        flat = np.abs(q_node.belief_engine.belief_tensor.flatten())
                        if len(flat) >= 10:
                            raw_probs = flat[:10].astype(float)
                except Exception:
                    pass

            # Veto lethal / toxic colors from ancestral memory
            for v_col in vetoed:
                raw_probs[v_col] = 0.0

            prob_sum = float(np.sum(raw_probs))
            if prob_sum > 1e-6:
                norm_probs = raw_probs / prob_sum
                self.selected_color = int(np.random.choice(10, p=norm_probs))
            else:
                # If all colors were vetoed, fallback to uniform
                self.selected_color = int(np.random.randint(0, 10))

        # 3. Modern-Thermodynamic Node: Metabolic Vitality (Paint vs. Rest vs. Move)
        modern_paint = False
        current_tile_confirmed = (confirmed_color is not None)

        if self.civilization and hasattr(self.civilization, "nodes") and "modern_prime" in self.civilization.nodes:
            m_node = self.civilization.nodes["modern_prime"]
            # Fever or high energy triggers active painting
            if m_node.state.energy > 35.0 or m_node.state.fever_active or current_tile_confirmed:
                modern_paint = (np.random.rand() < 0.50)
            elif m_node.state.energy < 20.0:
                # Critical hunger: conserve energy by resting unless standing on confirmed food!
                if not current_tile_confirmed:
                    return self.ACTION_REST
                else:
                    modern_paint = True
        else:
            modern_paint = (np.random.rand() < 0.35)

        # Final Council Action Selection
        if modern_paint:
            action = self.ACTION_PAINT
            self.energy -= 0.25
            act_name = "PAINT"
        else:
            action = classical_move
            self.energy -= 0.05
            act_name = "MOVE"

        # Record action into rolling episodic trace for retrograde death assignment
        self.episodic_trace.append({
            "tick": self.lifespan_ticks,
            "r": self.r,
            "c": self.c,
            "action": act_name,
            "color": self.selected_color,
            "energy": round(self.energy, 2)
        })
        if len(self.episodic_trace) > 35:
            self.episodic_trace.pop(0)

        if self.energy <= 0.0:
            self.energy = 0.0
            self.is_alive = False

        return action

    def feed(self, amount: float):
        """Food ingestion: restores metabolic energy to all 4 Sovereign Pillars and reinforces synapses."""
        new_e = min(self.max_energy, self.energy + amount)
        self.energy = new_e
        self.food_eaten += 1
        self.total_metabolic_reward += amount

        # Hebbian Synaptic Reinforcement in RelativisticMessageFabric
        if self.civilization and hasattr(self.civilization, "fabric") and self.civilization.fabric:
            self.civilization.fabric.reinforce_synapse("classical_prime", "quantum_prime", amount=2.0)
            self.civilization.fabric.reinforce_synapse("quantum_prime", "modern_prime", amount=2.0)
            self.civilization.fabric.reinforce_synapse("modern_prime", "string_meta", amount=2.0)
            self.civilization.fabric.reinforce_synapse("string_meta", "classical_prime", amount=2.0)

    def punish(self, penalty: float):
        """Metabolic penalty for placing toxic (wrong) pixels."""
        self.energy -= penalty
        self.wrong_paints += 1
        self.total_metabolic_reward -= penalty

        # Friction increase in Pillar nodes
        if self.civilization and hasattr(self.civilization, "nodes"):
            for n in self.civilization.nodes.values():
                if hasattr(n, "state"):
                    n.state.temperature = min(3.0, n.state.temperature + 0.1)

        if self.energy <= 0.0:
            self.energy = 0.0
            self.is_alive = False

    def spawn_next_generation(self) -> "ArcLivingOrganism":
        """Spawns next generation of the Sovereign Civilization, inheriting Ancestral Causal Memory."""
        child = ArcLivingOrganism(
            civilization=self.civilization,
            core=self.core,
            ancestral_memory=self.ancestral_memory,
            generation=self.generation + 1
        )
        child.puzzles_cleared = self.puzzles_cleared
        child.energy = 100.0
        return child
