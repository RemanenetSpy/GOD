"""
ARC Sovereign Autopoietic Survival World
A living environment where ARC puzzles are terrain and correct pixels are food.
Driven directly by the 4 Sovereign Pillars, BinoryCore STDP Plasticity, and Ancestral Causal Memory.
Zero hardcoded physics rules.
"""

import numpy as np
from typing import Dict, Any, List, Optional
from arc_sovereign_arena.organism import ArcLivingOrganism
from arc_sovereign_arena.arc_loader import ARCTaskLoader
from arc_sovereign_arena.ancestral_memory import AncestralCausalMemory

try:
    from binory_core import make_node_id, register_name
except ImportError:
    try:
        from src.binory_core import make_node_id, register_name
    except ImportError:
        def make_node_id(name: str) -> str: return f"node:{name}"
        def register_name(nid: str, name: str) -> None: pass


class ArcSurvivalWorld:
    """
    The living ARC environment. Orchestrates the puzzle canvas,
    metabolic food dispersion, starvation deaths, and generational births
    driven directly by SovereignCivilization, BinoryCore, and Ancestral Causal Memory.
    """

    def __init__(self, loader: Optional[ARCTaskLoader] = None, civilization=None, core=None, ancestral_memory: Optional[AncestralCausalMemory] = None):
        self.loader = loader or ARCTaskLoader()
        self.civilization = civilization
        self.core = core
        self.ancestral_memory = ancestral_memory or AncestralCausalMemory()

        self.agi1_files = self.loader.get_agi1_tasks()
        self.agi2_files = self.loader.get_agi2_tasks()
        self.all_files = self.agi1_files + self.agi2_files

        # Current Environment State
        self.puzzle_idx: int = 0
        self.current_task_id: str = "genesis"
        self.input_canvas: np.ndarray = np.zeros((3, 3), dtype=int)
        self.working_canvas: np.ndarray = np.zeros((3, 3), dtype=int)
        self.target_canvas: np.ndarray = np.zeros((3, 3), dtype=int)

        # Living Population & Generations
        self.generation: int = 1
        self.total_births: int = 1
        self.total_deaths: int = 0
        self.total_food_eaten: int = 0
        self.total_puzzles_cleared: int = 0
        self.best_lifespan: int = 0
        self.tick_count: int = 0

        self.organism = ArcLivingOrganism(
            civilization=self.civilization,
            core=self.core,
            ancestral_memory=self.ancestral_memory,
            generation=1
        )
        self.recent_events: List[Dict[str, Any]] = []

        # Load initial puzzle
        self._load_current_puzzle()

    def _load_current_puzzle(self):
        """Loads the current ARC puzzle terrain."""
        if not self.all_files:
            self.current_task_id = "genesis_falling_seed"
            self.input_canvas = np.array([[0, 1, 0], [0, 0, 0], [0, 0, 0]], dtype=int)
            self.target_canvas = np.array([[0, 0, 0], [0, 0, 0], [0, 1, 0]], dtype=int)
            self.working_canvas = self.input_canvas.copy()
            self.organism.reset_position(3, 3)
            return

        file_path = self.all_files[self.puzzle_idx % len(self.all_files)]
        task = self.loader.parse_task(file_path)
        if not task or not task["train"]:
            self.puzzle_idx += 1
            self._load_current_puzzle()
            return

        self.current_task_id = task["task_id"]
        pair = task["train"][0]
        self.input_canvas = pair["input"].copy()
        self.target_canvas = pair["output"].copy()

        if self.target_canvas.shape == self.input_canvas.shape:
            self.working_canvas = self.input_canvas.copy()
        else:
            self.working_canvas = np.zeros_like(self.target_canvas)

        h, w = self.working_canvas.shape
        self.organism.reset_position(h, w)

    def tick(self) -> Dict[str, Any]:
        """Runs one biological tick: perception, STDP spikes, 4-pillar council action, and metabolic feedback."""
        self.tick_count += 1

        # 1. Sensory Perception & BinoryCore STDP Synaptic Spikes
        self.organism.perceive_and_spike(self.input_canvas, self.working_canvas)

        # 2. Embodied Action via 4-Pillar Council Consensus (Informed by Ancestral Memory)
        action = self.organism.decide_action(self.input_canvas, self.working_canvas, task_id=self.current_task_id)

        event_msg = None
        h, w = self.working_canvas.shape

        # 3. Environmental Execution
        if action == ArcLivingOrganism.ACTION_MOVE_UP:
            self.organism.r = max(0, self.organism.r - 1)
        elif action == ArcLivingOrganism.ACTION_MOVE_DOWN:
            self.organism.r = min(h - 1, self.organism.r + 1)
        elif action == ArcLivingOrganism.ACTION_MOVE_LEFT:
            self.organism.c = max(0, self.organism.c - 1)
        elif action == ArcLivingOrganism.ACTION_MOVE_RIGHT:
            self.organism.c = min(w - 1, self.organism.c + 1)

        if action in (ArcLivingOrganism.ACTION_MOVE_UP, ArcLivingOrganism.ACTION_MOVE_DOWN,
                      ArcLivingOrganism.ACTION_MOVE_LEFT, ArcLivingOrganism.ACTION_MOVE_RIGHT):
            if hasattr(self.organism, "lifespan_memory"):
                self.organism.lifespan_memory.record_visit(self.organism.r, self.organism.c)
        elif action == ArcLivingOrganism.ACTION_PAINT:

            r, c = self.organism.r, self.organism.c
            target_color = int(self.target_canvas[r, c])
            paint_color = int(self.organism.selected_color)

            if paint_color == target_color:
                if self.working_canvas[r, c] != target_color:
                    # Genuine NEW Food ingestion
                    food_gain = 15.0
                    self.organism.feed(food_gain)
                    self.total_food_eaten += 1
                    self.working_canvas[r, c] = paint_color
                    # Register confirmed food source in Ancestral Causal Ledger
                    self.ancestral_memory.record_nutrition(self.current_task_id, r, c, paint_color)
                    event_msg = f"NUTRITION! Pixel ({r},{c}) set to {paint_color} (+15 Energy) [Saved in Ancestral Memory]"

                    # Potentiate STDP node in BinoryCore
                    if self.core is not None and hasattr(self.core, "update"):
                        try:
                            nid_food = make_node_id(f"arc_food_{r}_{c}_{paint_color}")
                            register_name(nid_food, f"food:({r},{c})={paint_color}")
                            self.core.update([nid_food], cpu_load=8.0)
                        except Exception:
                            pass
                else:
                    # Food on this tile has already been eaten! 0 food reward!
                    event_msg = f"DEPLETED! Pixel ({r},{c}) already satisfied (0 Food). Organism must seek another pixel!"
            else:
                # Wrong Pixel: TOXIC / WASTE
                waste_penalty = 3.0
                self.organism.punish(waste_penalty)
                self.working_canvas[r, c] = paint_color
                event_msg = f"TOXIC! Pixel ({r},{c}) set to {paint_color}, needed {target_color} (-3 Energy) [Vetoed in Ledger]"

                # Record toxic choice in Ancestral Causal Ledger
                self.ancestral_memory.record_toxic(self.current_task_id, r, c, paint_color, penalty=waste_penalty)

                # Depress STDP in BinoryCore
                if self.core is not None and hasattr(self.core, "update"):
                    try:
                        nid_tox = make_node_id(f"arc_toxic_{r}_{c}_{paint_color}")
                        register_name(nid_tox, f"toxic:({r},{c})={paint_color}")
                        self.core.update([nid_tox], cpu_load=8.0)
                    except Exception:
                        pass
        elif action == ArcLivingOrganism.ACTION_REST:
            event_msg = "Sovereign Pillars Meditating (Conserving Vitality)"

        # 4. Check Starvation & Generational Transition with Retrograde Death Attribution
        if not self.organism.is_alive:
            self.total_deaths += 1
            if self.organism.lifespan_ticks > self.best_lifespan:
                self.best_lifespan = self.organism.lifespan_ticks

            # RETROGRADE CAUSAL CREDIT ASSIGNMENT:
            # Penalize fatal actions in the death trace so next generation will veto them!
            self.ancestral_memory.record_starvation_death(self.current_task_id, self.organism.episodic_trace)

            # Spike lethal death nodes into BinoryCore
            if self.core is not None and hasattr(self.core, "update"):
                try:
                    nid_death = make_node_id(f"arc_death_{self.current_task_id}")
                    register_name(nid_death, f"death:{self.current_task_id}")
                    death_spikes = [nid_death]
                    for entry in self.organism.episodic_trace[-5:]:
                        if entry.get("action") == "PAINT":
                            pr, pc, pcol = entry["r"], entry["c"], entry["color"]
                            nid_lethal = make_node_id(f"arc_lethal_{pr}_{pc}_{pcol}")
                            register_name(nid_lethal, f"lethal:({pr},{pc})={pcol}")
                            death_spikes.append(nid_lethal)
                    self.core.update(death_spikes, cpu_load=len(death_spikes) * 6.0)
                except Exception:
                    pass

            # Spawn next generation of the Sovereign Civilization
            old_gen = self.generation
            self.generation += 1
            self.total_births += 1
            self.organism = self.organism.spawn_next_generation()
            self._load_current_puzzle()

            event_msg = f"STARVATION! Gen {old_gen} starved at tick {self.tick_count}. Fatal choices permanently vetoed in Ancestral Ledger."
            self._record_event(event_msg, "death")
            return self.get_state()

        # 5. Check Puzzle Mastery (Ecological Feast)
        if np.array_equal(self.working_canvas, self.target_canvas):
            self.total_puzzles_cleared += 1
            self.organism.puzzles_cleared += 1
            feast = 50.0
            self.organism.feed(feast)
            event_msg = f"LEVEL CLEARED! Puzzle {self.current_task_id} completed. (+50 Energy FEAST)"
            self._record_event(event_msg, "clear")

            self.puzzle_idx += 1
            self._load_current_puzzle()

        if event_msg:
            self._record_event(event_msg, "action")

        return self.get_state()

    def _record_event(self, msg: str, event_type: str):
        self.recent_events.append({
            "tick": self.tick_count,
            "gen": self.generation,
            "msg": msg,
            "type": event_type,
            "vitality": round(self.organism.energy, 1),
            "task": self.current_task_id
        })
        if len(self.recent_events) > 25:
            self.recent_events.pop(0)

    def get_state(self) -> Dict[str, Any]:
        """Returns the full live state for web visualization and telemetry."""
        # 4 Pillars status
        pillar_info = {}
        if self.civilization and hasattr(self.civilization, "nodes"):
            for nid, node in self.civilization.nodes.items():
                pillar_info[nid] = {
                    "energy": round(node.state.energy, 1) if hasattr(node, "state") else 100.0,
                    "temperature": round(node.state.temperature, 2) if hasattr(node, "state") else 0.1,
                    "fever": getattr(node.state, "fever_active", False) if hasattr(node, "state") else False
                }

        if self.core and hasattr(self.core, "_synapses"):
            core_synapse_count = len(self.core._synapses)
        elif self.core and hasattr(self.core, "_weights"):
            core_synapse_count = len(self.core._weights)
        else:
            core_synapse_count = 0

        return {
            "tick": self.tick_count,
            "current_task": self.current_task_id,
            "puzzle_idx": self.puzzle_idx,
            "generation": self.generation,
            "total_births": self.total_births,
            "total_deaths": self.total_deaths,
            "total_food_eaten": self.total_food_eaten,
            "puzzles_cleared": self.total_puzzles_cleared,
            "best_lifespan": self.best_lifespan,
            "organism": {
                "r": self.organism.r,
                "c": self.organism.c,
                "vitality": round(self.organism.energy, 1),
                "vitality_pct": round((self.organism.energy / self.organism.max_energy) * 100, 1),
                "selected_color": self.organism.selected_color,
                "is_alive": self.organism.is_alive,
                "lifespan": self.organism.lifespan_ticks,
                "food_eaten": self.organism.food_eaten,
                "visited_tiles_count": self.organism.lifespan_memory.unique_tiles_count() if hasattr(self.organism, "lifespan_memory") else 0,
                "total_steps": self.organism.lifespan_memory.total_steps() if hasattr(self.organism, "lifespan_memory") else 0,
            },
            "input_canvas": self.input_canvas.tolist(),
            "working_canvas": self.working_canvas.tolist(),
            "target_canvas": self.target_canvas.tolist(),
            "pillar_info": pillar_info,
            "core_synapses": core_synapse_count,
            "ancestral_memory": self.ancestral_memory.to_dict(),
            "lifespan_memory": self.organism.lifespan_memory.to_dict() if hasattr(self.organism, "lifespan_memory") else {},
            "recent_events": self.recent_events[-8:]
        }

