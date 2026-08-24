"""
========================================================================================
KAGGLE GPU ULTRA-FAST CONTINUOUS EVOLUTION RUNNER
========================================================================================
Runs 1,000,000+ steps of Continuous Lenia Multi-Agent Simulation on NVIDIA T4/P100 GPUs.
- Saves state 100% LOCALLY to /kaggle/working/ (Zero Hugging Face dependencies).
- Direct inside-notebook interactive HTML/Canvas visualizer.
- High-speed PyTorch / FFT-accelerated continuous wave physics.
========================================================================================
"""

import os
import sys
import time
import json
import numpy as np
from typing import Dict, Any, List, Tuple
from scipy.signal import convolve2d

# Ensure local source imports
sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('src'))
sys.path.insert(0, os.path.abspath('src/environments'))

from environments.registry import SubstrateRegistry
from civilization import SovereignCivilization, Observation, Action


class KaggleGPURunner:
    def __init__(
        self,
        grid_size: int = 25,
        max_population: int = 35,
        target_steps: int = 1_000_000,
        checkpoint_interval: int = 25_000,
        output_dir: str = "/kaggle/working" if os.path.exists("/kaggle") else "./kaggle_output",
        vault_name: str = "civilization_kaggle_vault.json"
    ):
        self.grid_size = grid_size
        self.grid_shape = (grid_size, grid_size)
        self.max_pop = max_population
        self.target_steps = target_steps
        self.checkpoint_interval = checkpoint_interval
        self.output_dir = output_dir
        self.vault_file = os.path.join(output_dir, vault_name)
        
        os.makedirs(output_dir, exist_ok=True)

        # 1. Instantiate Continuous Lenia Substrate
        print(f"[Kaggle GPU Engine] Initializing Continuous Lenia ({grid_size}x{grid_size})...")
        self.universe = SubstrateRegistry.get_substrate("lenia", grid_shape=self.grid_shape)

        # 2. Instantiate Sovereign Civilization
        self.civ = SovereignCivilization(
            grid_shape=self.grid_shape,
            max_population=max_population,
            enable_cyclic_pruning=True
        )

        # 3. Agent Initial Coordinates
        self.positions: Dict[str, Tuple[int, int]] = {
            "classical_prime": (2, 2),
            "quantum_prime": (grid_size - 3, 2),
            "modern_prime": (2, grid_size - 3),
            "string_meta": (grid_size - 3, grid_size - 3),
        }
        self.step_count = 0
        self.start_time = time.time()
        
        # Load local Kaggle checkpoint if resuming
        self.load_local_vault()

    def load_local_vault(self):
        if os.path.exists(self.vault_file):
            try:
                with open(self.vault_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.step_count = data.get("step_num", 0)
                if "subroutines" in data:
                    self.civ.global_subroutine_archive.update(data["subroutines"])
                print(f"[Kaggle Vault] Successfully loaded local checkpoint at Step {self.step_count:,} with {len(self.civ.global_subroutine_archive)} rules!")
            except Exception as e:
                print(f"[Kaggle Vault Warning] Could not load checkpoint: {e}")

    def save_local_vault(self):
        state_dict = {
            "mode_name": f"Kaggle GPU Sovereign Colony ({self.max_pop} max pop)",
            "substrate_name": "lenia",
            "step_num": self.step_count,
            "population": len(self.civ.nodes),
            "total_subroutines": len(self.civ.global_subroutine_archive),
            "subroutines": self.civ.global_subroutine_archive,
            "climate": self.universe.get_climate_telemetry(),
            "saved_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        with open(self.vault_file, 'w', encoding='utf-8') as f:
            json.dump(state_dict, f, indent=2)
        print(f"  💾 [Kaggle Local Vault Saved] Step {self.step_count:,} | Pop: {len(self.civ.nodes)} | Rules: {len(self.civ.global_subroutine_archive)} -> {self.vault_file}")

    def run(self):
        print("================================================================================")
        print(f"🚀 STARTING GPU HYPER-EVOLUTION RUN: {self.target_steps:,} STEPS")
        print(f"📁 Local Kaggle Output Vault: {self.vault_file}")
        print("================================================================================")

        h, w = self.grid_shape
        last_log_time = time.time()
        last_log_step = self.step_count

        while self.step_count < self.target_steps:
            self.step_count += 1
            
            # Position management
            for aid in list(self.civ.nodes.keys()):
                if aid not in self.positions:
                    self.positions[aid] = (
                        np.random.randint(2, self.grid_size - 2),
                        np.random.randint(2, self.grid_size - 2)
                    )
            for pos_id in list(self.positions.keys()):
                if pos_id not in self.civ.nodes:
                    del self.positions[pos_id]

            # 1. Physics step
            climate = self.universe.get_climate_telemetry()
            rewards = self.universe.step(self.positions)

            # 2. Build local sensory observations
            observations = {}
            for aid, node in self.civ.nodes.items():
                py, px = self.positions.get(aid, (0, 0))
                vis = self.universe.get_observation(py, px, node.aperture)
                observations[aid] = Observation(
                    visible_cells=vis,
                    position=(py, px),
                    reward=rewards.get(aid, 0.0)
                )

            # 3. Step civilization cognition
            actions = self.civ.step(observations, climate_telemetry=climate)

            # 4. Move agents
            for aid, act in actions.items():
                if aid not in self.positions:
                    continue
                py, px = self.positions[aid]
                if act == Action.MOVE_UP: py = max(0, py - 1)
                elif act == Action.MOVE_DOWN: py = min(h - 1, py + 1)
                elif act == Action.MOVE_LEFT: px = max(0, px - 1)
                elif act == Action.MOVE_RIGHT: px = min(w - 1, px + 1)
                self.positions[aid] = (py, px)

            # Checkpoint saving & Progress logging
            if self.step_count % self.checkpoint_interval == 0:
                self.save_local_vault()
                now = time.time()
                elapsed = now - last_log_time
                steps_done = self.step_count - last_log_step
                speed = steps_done / max(0.001, elapsed)
                pct = (self.step_count / self.target_steps) * 100
                tot_energy = sum(n.state.energy for n in self.civ.nodes.values())
                print(f"[{pct:5.1f}%] Step: {self.step_count:8,d} | Speed: {speed:6.1f} steps/s | Pop: {len(self.civ.nodes):2d} | Tot Energy: {tot_energy:6.1f} | Rules: {len(self.civ.global_subroutine_archive):2d}")
                last_log_time = now
                last_log_step = self.step_count

        self.save_local_vault()
        total_time = time.time() - self.start_time
        print("================================================================================")
        print(f"🎉 1 MILLION STEPS COMPLETE in {total_time/60.0:.2f} MINUTES!")
        print(f"Total Rules Discovered: {len(self.civ.global_subroutine_archive)}")
        print(f"Saved locally at: {self.vault_file}")
        print("================================================================================")


if __name__ == "__main__":
    runner = KaggleGPURunner(target_steps=1_000_000, checkpoint_interval=25_000)
    runner.run()
