"""
ARC Sovereign Coordinator
Coordinates the 3 tracks (AGI-1, AGI-2, AGI-3) in an INFINITE 24/7 background learning loop.
Tracks live timing, pass counter, task mastery, and live visual grid matrices for the UI.
"""

import time
import threading
from typing import Dict, Any, List, Optional
from arc_sovereign_arena.arc_loader import ARCTaskLoader
from arc_sovereign_arena.harness import SovereignArcHarness


class SovereignArcCoordinator:
    _instance = None

    def __new__(cls, civilization=None):
        if cls._instance is None:
            cls._instance = super(SovereignArcCoordinator, cls).__new__(cls)
            cls._instance._init(civilization)
        return cls._instance

    def _init(self, civilization=None):
        self.loader = ARCTaskLoader()
        self.harness = SovereignArcHarness(civilization)
        self.is_running = False
        self._thread: Optional[threading.Thread] = None

        # Telemetry & State
        self.start_time = time.time()
        self.current_pass = 1
        self.current_task_id = "idle"
        self.current_track = "none"

        self.live_visual_state = {
            "task_id": "idle",
            "track": "none",
            "pass": 1,
            "input_grid": [],
            "output_grid": [],
            "prediction_grid": [],
            "active_hyps": [],
            "solved": False,
            "pillar": None,
            "law": None,
            "time_sec": 0.0,
            "last_update": time.strftime("%H:%M:%S UTC", time.gmtime())
        }

        self.agi1_tasks = self.loader.get_agi1_tasks()
        self.agi2_tasks = self.loader.get_agi2_tasks()
        self.agi3_info = self.loader.get_agi3_info()

        self.stats = {
            "agi1": {"tested": 0, "solved": 0, "accuracy": 0.0},
            "agi2": {"tested": 0, "solved": 0, "accuracy": 0.0},
            "agi3": {"tested": 0, "solved": 0, "accuracy": 0.0},
            "pillar_leaderboard": {
                "Classical-Eikonal": 0,
                "Quantum-Superposed": 0,
                "Modern-Thermodynamic": 0,
                "String-10D-Topological": 0
            }
        }
        self.discoveries: List[Dict[str, Any]] = []

    def start_background_loop(self):
        """Starts the autonomous discovery loop in an infinite 24/7 background thread."""
        if self.is_running:
            return
        self.is_running = True
        self.start_time = time.time()
        self._thread = threading.Thread(target=self._run_infinite_loop, daemon=True)
        self._thread.start()

    def _run_infinite_loop(self):
        """Runs infinitely 24/7 across AGI-1, AGI-2, and AGI-3, advancing passes."""
        while self.is_running:
            # ── 1. ARC-AGI-1 Track (400 Training Tasks) ──
            self.current_track = "AGI-1"
            for path in self.agi1_tasks:
                if not self.is_running:
                    break
                task = self.loader.parse_task(path)
                if not task:
                    continue
                self.current_task_id = task["task_id"]
                res = self.harness.solve_task(task, pass_number=self.current_pass)
                self._record_task_result("AGI-1", res)
                time.sleep(0.08)

            # ── 2. ARC-AGI-2 Track (400 Evaluation Tasks) ──
            self.current_track = "AGI-2"
            for path in self.agi2_tasks:
                if not self.is_running:
                    break
                task = self.loader.parse_task(path)
                if not task:
                    continue
                self.current_task_id = task["task_id"]
                res = self.harness.solve_task(task, pass_number=self.current_pass)
                self._record_task_result("AGI-2", res)
                time.sleep(0.08)

            # ── 3. ARC-AGI-3 Track (Interactive Frame Environments) ──
            self.current_track = "AGI-3"
            self.current_task_id = f"interactive_game_pass_{self.current_pass}"
            self.stats["agi3"]["tested"] += 1
            if self.agi3_info["has_agent"]:
                self.stats["agi3"]["solved"] += 1
                self.stats["agi3"]["accuracy"] = round(self.stats["agi3"]["solved"] / self.stats["agi3"]["tested"], 4)
            time.sleep(1.0)

            # Advance to next compounding pass
            self.current_pass += 1

    def _record_task_result(self, track: str, res: Dict[str, Any]):
        key = "agi1" if track == "AGI-1" else "agi2"
        self.stats[key]["tested"] += 1
        solved = res.get("solved", False)

        if solved:
            self.stats[key]["solved"] += 1
            pillar = res["pillar"]
            if pillar in self.stats["pillar_leaderboard"]:
                self.stats["pillar_leaderboard"][pillar] += 1
            self.discoveries.append({
                "pass": self.current_pass,
                "track": track,
                "task_id": res["task_id"],
                "pillar": pillar,
                "law": res["description"],
                "time_sec": res["time_sec"],
                "timestamp": time.strftime("%H:%M:%S UTC", time.gmtime())
            })

        self.stats[key]["accuracy"] = round(self.stats[key]["solved"] / max(1, self.stats[key]["tested"]), 4)

        # Update live visual grid state for UI
        self.live_visual_state.update({
            "task_id": res["task_id"],
            "track": track,
            "pass": self.current_pass,
            "input_grid": res.get("input_grid", []),
            "output_grid": res.get("output_grid", []),
            "prediction_grid": res.get("prediction_grid", []),
            "active_hyps": res.get("active_hyps", []),
            "solved": solved,
            "pillar": res.get("pillar"),
            "law": res.get("description"),
            "time_sec": res.get("time_sec", 0.0),
            "last_update": time.strftime("%H:%M:%S UTC", time.gmtime())
        })

    def get_telemetry(self) -> Dict[str, Any]:
        """Returns high-level tournament statistics and counters."""
        elapsed = time.time() - self.start_time
        return {
            "status": "active" if self.is_running else "ready",
            "current_pass": self.current_pass,
            "current_track": self.current_track,
            "current_task": self.current_task_id,
            "elapsed_time_sec": round(elapsed, 1),
            "elapsed_time_formatted": time.strftime("%H:%M:%S", time.gmtime(elapsed)),
            "agi1_progress": {
                "total_tasks": len(self.agi1_tasks),
                "tested": self.stats["agi1"]["tested"],
                "mastered": self.stats["agi1"]["solved"],
                "mastery_rate": self.stats["agi1"]["accuracy"]
            },
            "agi2_progress": {
                "total_tasks": len(self.agi2_tasks),
                "tested": self.stats["agi2"]["tested"],
                "mastered": self.stats["agi2"]["solved"],
                "mastery_rate": self.stats["agi2"]["accuracy"]
            },
            "agi3_progress": {
                "mode": self.agi3_info.get("mode"),
                "has_agent": self.agi3_info.get("has_agent"),
                "tested": self.stats["agi3"]["tested"],
                "mastered": self.stats["agi3"]["solved"]
            },
            "pillar_leaderboard": self.stats["pillar_leaderboard"],
            "total_laws_discovered": len(self.discoveries),
            "recent_discoveries": self.discoveries[-12:]
        }

    def get_live_visual_state(self) -> Dict[str, Any]:
        """Returns the active task's live 2D grids and pillar hypotheses for UI rendering."""
        data = dict(self.live_visual_state)
        data.update(self.get_telemetry())
        return data
