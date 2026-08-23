"""
========================================================================================
SOVEREIGN CIVILIZATION 24/7 CLOUD SERVER (RENDER.COM COMPATIBLE)
========================================================================================
1. Runs the FULL Python Sovereign Civilization Engine (4 Pillars + All Physics).
2. Runs a continuous background simulation loop evolving 24/7.
3. Automatically pushes checkpoints & subroutines to Hugging Face Dataset Vault.
4. Exposes a live HTTP `/ping` endpoint for Keep-Alive bots (UptimeRobot).
========================================================================================
"""

import os
import sys
import time
import json
import threading
from typing import Dict, Any
from fastapi import FastAPI
from fastapi.responses import JSONResponse

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from civilization import (
    SovereignCivilization,
    Observation,
    Action,
    PillarArchetype
)
from hf_dataset_memory import HFDatasetMemoryVault

# Hugging Face Dataset Cloud Vault configuration
HF_TOKEN = os.environ.get("HF_TOKEN", "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")
HF_REPO = os.environ.get("HF_DATASET_REPO", "Explorerp/sovereign-civilization-memory")

vault = HFDatasetMemoryVault(repo_id=HF_REPO, token=HF_TOKEN)

# 24/7 Background Evolution Engine
class ContinuousEvolutionRunner:
    def __init__(self, grid_size: int = 30):
        self.grid_size = grid_size
        self.civ = SovereignCivilization(grid_shape=(grid_size, grid_size))
        self.step_count = 0
        self.running = True
        self.last_saved_step = 0
        self.lock = threading.Lock()
        
        # Recover latest state from cloud
        self.load_from_cloud()
        
        # Start continuous evolution background worker thread
        self.thread = threading.Thread(target=self._evolution_loop, daemon=True)
        self.thread.start()

    def load_from_cloud(self):
        try:
            cloud_data = vault.load_checkpoint()
            if cloud_data:
                self.step_count = cloud_data.get("step_num", cloud_data.get("stepCount", 0))
                if "subroutines" in cloud_data:
                    self.civ.global_subroutine_archive.update(cloud_data["subroutines"])
                print(f"[Render Engine] Recovered from Cloud Vault at Step {self.step_count} with {len(self.civ.global_subroutine_archive)} subroutines!")
        except Exception as e:
            print(f"[Render Engine Warning] Initial recovery error: {e}")

    def _evolution_loop(self):
        print("[Render Engine] 24/7 Sovereign Evolution Loop STARTED in background!")
        while self.running:
            try:
                with self.lock:
                    self.step_count += 1
                    # Execute 1 step of true Python physics & multi-agent message routing
                    self.civ.step()
                    
                    # Auto-commit to Hugging Face Cloud Vault every 25 steps
                    if self.step_count - self.last_saved_step >= 25:
                        self.last_saved_step = self.step_count
                        state_dict = {
                            "step_num": self.step_count,
                            "subroutines": self.civ.global_subroutine_archive,
                            "agent_energies": {k: float(n.state.energy) for k, n in self.civ.nodes.items()},
                            "agent_temperatures": {k: float(n.state.temperature) for k, n in self.civ.nodes.items()},
                            "agent_fever": {k: bool(n.state.fever_active) for k, n in self.civ.nodes.items()},
                            "total_subroutines": len(self.civ.global_subroutine_archive)
                        }
                        vault.save_checkpoint(
                            state_dict,
                            commit_msg=f"Continuous 24/7 evolution step {self.step_count}",
                            async_upload=True
                        )
                        print(f"[Render Engine Sync] Step {self.step_count} | Minted Subroutines: {len(self.civ.global_subroutine_archive)}")

                # Delay per tick (100ms per step = ~36,000 steps per hour!)
                time.sleep(0.1)
            except Exception as e:
                print(f"[Render Evolution Error]: {e}")
                time.sleep(1.0)

    def get_status(self) -> Dict[str, Any]:
        with self.lock:
            return {
                "status": "RUNNING_24_7",
                "current_step": self.step_count,
                "total_subroutines_minted": len(self.civ.global_subroutine_archive),
                "active_pillars": list(self.civ.nodes.keys()),
                "energies": {k: float(n.state.energy) for k, n in self.civ.nodes.items()},
                "temperatures": {k: float(n.state.temperature) for k, n in self.civ.nodes.items()},
                "cloud_vault": HF_REPO
            }


# Initialize Runner & FastAPI App
runner = ContinuousEvolutionRunner()
app = FastAPI(title="Sovereign Civilization 24/7 Cloud Engine")

@app.get("/")
def home():
    return runner.get_status()

@app.get("/ping")
def ping():
    """Keep-Alive endpoint for UptimeRobot (pings every 5 mins)."""
    return JSONResponse(content={"status": "OK", "step": runner.step_count})
