"""
ARC Sovereign Autopoietic Survival World
A living environment where ARC puzzles are terrain and correct pixels are food.
Zero hardcoded physics rules. The organism survives or starves through embodied action.
"""

import numpy as np
from typing import Dict, Any, List, Optional
from arc_sovereign_arena.organism import ArcLivingOrganism, SensoryMotorConnectome
from arc_sovereign_arena.arc_loader import ARCTaskLoader


class ArcSurvivalWorld:
    """
    The living ARC environment. Orchestrates the puzzle canvas,
    metabolic food dispersion, starvation deaths, and generational births.
    """

    def __init__(self, loader: Optional[ARCTaskLoader] = None):
        self.loader = loader or ARCTaskLoader()
        self.agi1_files = self.loader.get_agi1_tasks()
        self.agi2_files = self.loader.get_agi2_tasks()
        self.all_files = self.agi1_files + self.agi2_files

        # Current Environment State
        self.puzzle_idx: int = 0
        self.current_task_id: str = "genesis"
        self.input_canvas: np.ndarray = np.zeros((3, 3), dtype=int)
        self.working_canvas: np.ndarray = np.zeros((3, 3), dtype=int)
        self.target_canvas: np.ndarray = np.zeros((3, 3), dtype=int)

        # Living Population & Genetics
        self.generation: int = 1
        self.total_births: int = 1
        self.total_deaths: int = 0
        self.total_food_eaten: int = 0
        self.total_puzzles_cleared: int = 0
        self.best_lifespan: int = 0
        self.tick_count: int = 0

        self.organism = ArcLivingOrganism(generation=1)
        self.fittest_organism = self.organism
        self.recent_events: List[Dict[str, Any]] = []

        # Load initial puzzle
        self._load_current_puzzle()

    def _load_current_puzzle(self):
        """Loads the current ARC puzzle terrain."""
        if not self.all_files:
            # Fallback simple 3x3 gravity genesis puzzle if no dataset files found
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
        # Use first training pair as the immediate environment
        pair = task["train"][0]
        self.input_canvas = pair["input"].copy()
        self.target_canvas = pair["output"].copy()

        # If target shape differs from input shape, working canvas matches target dimensions
        if self.target_canvas.shape == self.input_canvas.shape:
            self.working_canvas = self.input_canvas.copy()
        else:
            self.working_canvas = np.zeros_like(self.target_canvas)

        h, w = self.working_canvas.shape
        self.organism.reset_position(h, w)

    def tick(self) -> Dict[str, Any]:
        """Runs one biological tick of the survival ecology."""
        self.tick_count += 1

        # 1. Sensory Perception (Vision + Hunger + Location)
        sensory = self.organism.perceive(self.input_canvas, self.working_canvas)

        # 2. Embodied Action
        action = self.organism.step(sensory)

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
        elif action == ArcLivingOrganism.ACTION_PAINT:
            r, c = self.organism.r, self.organism.c
            target_color = int(self.target_canvas[r, c])
            paint_color = int(self.organism.selected_color)

            if paint_color == target_color:
                # Correct Pixel: NUTRITION!
                if self.working_canvas[r, c] != target_color:
                    food_gain = 15.0
                    self.organism.feed(food_gain)
                    self.total_food_eaten += 1
                    event_msg = f"NUTRITION! Pixel ({r},{c}) set to {paint_color} (+15 Energy)"
                else:
                    self.organism.feed(1.0)
                self.working_canvas[r, c] = paint_color
            else:
                # Wrong Pixel: TOXIC / WASTE
                waste_penalty = 3.0
                self.organism.punish(waste_penalty)
                self.working_canvas[r, c] = paint_color
                event_msg = f"TOXIC! Pixel ({r},{c}) set to {paint_color}, needed {target_color} (-3 Energy)"
        elif action == ArcLivingOrganism.ACTION_REST:
            event_msg = "Resting / Meditating"
        elif 6 <= action <= 15:
            # Tool Color Selection
            self.organism.selected_color = action - 6

        # 4. Check Starvation & Death
        if not self.organism.is_alive:
            self.total_deaths += 1
            if self.organism.lifespan_ticks > self.best_lifespan:
                self.best_lifespan = self.organism.lifespan_ticks
                self.fittest_organism = self.organism

            # Spawn next generation from the fittest survivor
            self.generation += 1
            self.total_births += 1
            self.organism = self.fittest_organism.spawn_offspring()
            self._load_current_puzzle()

            event_msg = f"STARVATION! Organism died at tick {self.tick_count}. Generation {self.generation} spawned."
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

            # Advance to next puzzle
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
            },
            "input_canvas": self.input_canvas.tolist(),
            "working_canvas": self.working_canvas.tolist(),
            "target_canvas": self.target_canvas.tolist(),
            "recent_events": self.recent_events[-8:]
        }
