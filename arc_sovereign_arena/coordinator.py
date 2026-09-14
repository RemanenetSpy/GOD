"""
ARC Sovereign Coordinator (Autopoietic Survival Ecology Edition)
Runs an infinite 24/7 embodied survival world where:
- ARC puzzles are the terrain.
- Correct pixels are food/nutrition; wrong pixels waste energy.
- Organisms survive through hunger ($dH/dt < 0$), birth, and death.
- Zero pre-coded physics rules or hypothesis templates.
- Telemetry and generational lineages are saved permanently to Hugging Face Cloud Vault.
"""

import time
import threading
from typing import Dict, Any, List, Optional
from arc_sovereign_arena.arc_loader import ARCTaskLoader
from arc_sovereign_arena.arc_vault import ARCSovereignVault
from arc_sovereign_arena.autopoietic_world import ArcSurvivalWorld
from arc_sovereign_arena.organism import SensoryMotorConnectome


class SovereignArcCoordinator:
    _instance = None

    def __new__(cls, civilization=None, vault=None):
        if cls._instance is None:
            cls._instance = super(SovereignArcCoordinator, cls).__new__(cls)
            cls._instance._init(civilization, vault)
        elif vault is not None and not getattr(cls._instance, "vault", None):
            cls._instance.vault = vault
            cls._instance._restore_from_vault()
        return cls._instance

    def _init(self, civilization=None, vault=None):
        self.civilization = civilization
        self.loader = ARCTaskLoader()
        self.vault = vault or ARCSovereignVault()
        self.is_running = False
        self._thread: Optional[threading.Thread] = None
        self._last_vault_save = 0.0

        # Initialize the Living Autopoietic World
        self.world = ArcSurvivalWorld(loader=self.loader)
        self.start_time = time.time()

        # Telemetry & State
        self.current_task_id = self.world.current_task_id
        self.live_visual_state: Dict[str, Any] = {
            "mode": "autopoietic_survival",
            "task_id": self.world.current_task_id,
            "generation": 1,
            "organism": self.world.organism,
            "input_grid": self.world.input_canvas.tolist(),
            "working_grid": self.world.working_canvas.tolist(),
            "target_grid": self.world.target_canvas.tolist(),
            "recent_events": [],
            "last_update": time.strftime("%H:%M:%S UTC", time.gmtime())
        }

        # Restore from Hugging Face Cloud Vault if available
        self._restore_from_vault()

    def _restore_from_vault(self):
        """Restores survival lineage and generational memory from Cloud Vault."""
        if not self.vault:
            return
        try:
            saved = self.vault.load("arc_survival_lineage.json")
            if not saved:
                print("[ARC Survival Vault] No prior lineage checkpoint found; starting initial Generation 1.")
                return

            self.world.generation = saved.get("generation", 1)
            self.world.total_births = saved.get("total_births", 1)
            self.world.total_deaths = saved.get("total_deaths", 0)
            self.world.total_food_eaten = saved.get("total_food_eaten", 0)
            self.world.total_puzzles_cleared = saved.get("puzzles_cleared", 0)
            self.world.best_lifespan = saved.get("best_lifespan", 0)

            if "fittest_connectome" in saved and isinstance(saved["fittest_connectome"], dict):
                try:
                    c = SensoryMotorConnectome.from_dict(saved["fittest_connectome"])
                    self.world.fittest_organism.connectome = c
                    self.world.organism = self.world.fittest_organism.spawn_offspring()
                except Exception:
                    pass

            print(f"[ARC Survival Vault Cloud Sync] Restored Generation {self.world.generation} | {self.world.total_deaths} Deaths | {self.world.total_puzzles_cleared} Puzzles Cleared from {getattr(self.vault, 'repo_id', 'cache')}")
        except Exception as e:
            print(f"[ARC Vault Warning] Error restoring lineage: {e}")

    def _save_to_vault(self, force: bool = False):
        """Saves living lineage, generational stats, and best connectome to Cloud Vault."""
        if not self.vault:
            return
        now = time.time()
        if not force and (now - self._last_vault_save < 30.0):
            return
        self._last_vault_save = now

        state = {
            "vault_type": "arc_survival_lineage",
            "generation": self.world.generation,
            "total_births": self.world.total_births,
            "total_deaths": self.world.total_deaths,
            "total_food_eaten": self.world.total_food_eaten,
            "puzzles_cleared": self.world.total_puzzles_cleared,
            "best_lifespan": self.world.best_lifespan,
            "current_task": self.world.current_task_id,
            "fittest_connectome": self.world.fittest_organism.connectome.to_dict(),
            "recent_events": self.world.recent_events[-10:],
            "saved_at": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
            "hf_repo": getattr(self.vault, "repo_id", "local")
        }
        try:
            self.vault.save(
                state,
                filename="arc_survival_lineage.json",
                commit_msg=f"ARC Survival Gen {self.world.generation} | {self.world.total_deaths} Deaths | {self.world.total_puzzles_cleared} Solved",
                async_upload=True
            )
        except Exception as e:
            print(f"[ARC Vault Save Warning]: {e}")

    def start_background_loop(self):
        """Starts the 24/7 Autopoietic Survival Ecology loop."""
        if self.is_running:
            return
        self.is_running = True
        self.start_time = time.time()
        self._thread = threading.Thread(target=self._run_survival_loop, daemon=True)
        self._thread.start()

    def stop_background_loop(self):
        """Halts the background loop."""
        self.is_running = False

    def _run_survival_loop(self):
        """Runs the living ecology: steps the organism, updates UI state, and saves lineages."""
        while self.is_running:
            # 1. Step the living organism in the ARC survival environment
            st = self.world.tick()

            # 2. Synchronize live visual state for UI
            self.current_task_id = st["current_task"]
            self.live_visual_state = {
                "mode": "autopoietic_survival",
                "task_id": st["current_task"],
                "puzzle_idx": st["puzzle_idx"],
                "generation": st["generation"],
                "total_births": st["total_births"],
                "total_deaths": st["total_deaths"],
                "total_food_eaten": st["total_food_eaten"],
                "puzzles_cleared": st["puzzles_cleared"],
                "best_lifespan": st["best_lifespan"],
                "organism": st["organism"],
                "input_grid": st["input_canvas"],
                "working_grid": st["working_canvas"],
                "target_grid": st["target_canvas"],
                "recent_events": st["recent_events"],
                "last_update": time.strftime("%H:%M:%S UTC", time.gmtime())
            }

            # 3. Synchronize with Sovereign Civilization connectome if plugged in
            if self.civilization and hasattr(self.civilization, "fabric") and self.civilization.fabric:
                if st["total_food_eaten"] > 0 and st["tick"] % 20 == 0:
                    self.civilization.fabric.reinforce_synapse("quantum_prime", "classical_prime", amount=0.5)

            # 4. Periodic cloud save
            self._save_to_vault(force=False)

            # Ticking speed: ~12.5 ticks per second (0.08s) for smooth visual observation
            time.sleep(0.08)

    def get_telemetry(self) -> Dict[str, Any]:
        """Returns survival ecology statistics and telemetry."""
        elapsed = time.time() - self.start_time
        return {
            "status": "active" if self.is_running else "ready",
            "mode": "autopoietic_survival",
            "elapsed_time_sec": round(elapsed, 1),
            "elapsed_time_formatted": time.strftime("%H:%M:%S", time.gmtime(elapsed)),
            "current_task": self.world.current_task_id,
            "puzzle_idx": self.world.puzzle_idx,
            "generation": self.world.generation,
            "total_births": self.world.total_births,
            "total_deaths": self.world.total_deaths,
            "total_food_eaten": self.world.total_food_eaten,
            "puzzles_cleared": self.world.total_puzzles_cleared,
            "best_lifespan": self.world.best_lifespan,
            "organism": {
                "r": self.world.organism.r,
                "c": self.world.organism.c,
                "vitality": round(self.world.organism.energy, 1),
                "vitality_pct": round((self.world.organism.energy / self.world.organism.max_energy) * 100, 1),
                "selected_color": self.world.organism.selected_color,
                "is_alive": self.world.organism.is_alive,
                "lifespan": self.world.organism.lifespan_ticks,
                "food_eaten": self.world.organism.food_eaten
            },
            "recent_events": self.world.recent_events[-6:],
            "cloud_vault": {
                "connected": self.vault is not None and bool(getattr(self.vault, "token", None)),
                "repo": getattr(self.vault, "repo_id", "local_only"),
                "total_saved": self.world.total_puzzles_cleared,
                "last_cloud_sync": time.strftime("%H:%M:%S UTC", time.gmtime(self._last_vault_save)) if self._last_vault_save > 0 else "pending"
            }
        }

    def get_live_visual_state(self) -> Dict[str, Any]:
        """Returns the active task's live 2D grids and organism cursor for UI rendering."""
        data = dict(self.live_visual_state)
        data.update(self.get_telemetry())
        return data
