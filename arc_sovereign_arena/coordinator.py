"""
ARC Sovereign Coordinator (4-Pillar Council & BinoryCore STDP Edition)
Directly connects the original Sovereign Civilization and BinoryCore STDP plasticity
into the 24/7 ARC Survival Ecology.
Zero hardcoded physics rules.
"""

import time
import threading
from typing import Dict, Any, List, Optional
from arc_sovereign_arena.arc_loader import ARCTaskLoader
from arc_sovereign_arena.arc_vault import ARCSovereignVault
from arc_sovereign_arena.autopoietic_world import ArcSurvivalWorld


class SovereignArcCoordinator:
    _instance = None

    def __new__(cls, civilization=None, vault=None, core=None):
        if cls._instance is None:
            cls._instance = super(SovereignArcCoordinator, cls).__new__(cls)
            cls._instance._init(civilization, vault, core)
        else:
            if civilization is not None and getattr(cls._instance, "civilization", None) is None:
                cls._instance.civilization = civilization
                cls._instance.world.civilization = civilization
                cls._instance.world.organism.civilization = civilization
            if core is not None and getattr(cls._instance, "core", None) is None:
                cls._instance.core = core
                cls._instance.world.core = core
                cls._instance.world.organism.core = core
            if vault is not None and getattr(cls._instance, "vault", None) is None:
                cls._instance.vault = vault
                cls._instance._restore_from_vault()
        return cls._instance

    def _init(self, civilization=None, vault=None, core=None):
        self.civilization = civilization
        self.core = core

        # If core not provided, try to obtain from BinoryCore
        if self.core is None:
            try:
                from binory_core import BinoryCore
                self.core = BinoryCore()
            except ImportError:
                try:
                    from src.binory_core import BinoryCore
                    self.core = BinoryCore()
                except ImportError:
                    self.core = None

        self.loader = ARCTaskLoader()
        self.vault = vault or ARCSovereignVault()
        self.is_running = False
        self._thread: Optional[threading.Thread] = None
        self._last_vault_save = 0.0

        # Initialize the Living Autopoietic World powered directly by the 4 Pillars
        self.world = ArcSurvivalWorld(loader=self.loader, civilization=self.civilization, core=self.core)
        self.start_time = time.time()

    def _get_core_synapse_count(self) -> int:
        if self.core is not None:
            if hasattr(self.core, "_synapses"):
                return len(self.core._synapses)
            elif hasattr(self.core, "_weights"):
                return len(self.core._weights)
        return 0

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
            "pillar_info": {},
            "core_synapses": 0,
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
            if "ancestral_memory" in saved:
                self.world.ancestral_memory.load_dict(saved["ancestral_memory"])

            print(f"[ARC Survival Vault Cloud Sync] Restored Generation {self.world.generation} | {self.world.total_deaths} Deaths | {self.world.total_puzzles_cleared} Puzzles Cleared from {getattr(self.vault, 'repo_id', 'cache')}")
        except Exception as e:
            print(f"[ARC Vault Warning] Error restoring lineage: {e}")

    def _save_to_vault(self, force: bool = False):
        """Saves living lineage, generational stats, and core state to Cloud Vault."""
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
            "core_synapses": self._get_core_synapse_count(),
            "ancestral_memory": self.world.ancestral_memory.to_dict(),
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
        """Runs the living ecology: steps the 4-pillar council, updates UI state, and saves lineages."""
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
                "pillar_info": st["pillar_info"],
                "core_synapses": st["core_synapses"],
                "recent_events": st["recent_events"],
                "last_update": time.strftime("%H:%M:%S UTC", time.gmtime())
            }

            # 3. Periodic cloud save
            self._save_to_vault(force=False)

            # Ticking speed: ~12.5 ticks per second (0.08s)
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
            "core_synapses": self._get_core_synapse_count(),
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
            "ancestral_memory": self.world.ancestral_memory.to_dict(),
            "recent_events": self.world.recent_events[-6:],
            "cloud_vault": {
                "connected": self.vault is not None and bool(getattr(self.vault, "token", None)),
                "repo": getattr(self.vault, "repo_id", "local_only"),
                "total_saved": self.world.total_puzzles_cleared,
                "last_cloud_sync": time.strftime("%H:%M:%S UTC", time.gmtime(self._last_vault_save)) if self._last_vault_save > 0 else "pending"
            }
        }

    def get_live_visual_state(self) -> Dict[str, Any]:
        """Returns the active task's live 2D grids and 4-pillar state for UI rendering."""
        data = dict(self.live_visual_state)
        data.update(self.get_telemetry())
        return data
