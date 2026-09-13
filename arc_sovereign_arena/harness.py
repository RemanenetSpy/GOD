"""
ARC Sovereign Harness (Plug-in / Plug-out)
Directly bridges the LIVING SovereignCivilization into ARC tasks without modifying core files.
Returns visual grid data for the live real-time UI canvas.
"""

import sys
import os
import time
import numpy as np
from typing import Dict, Any, Optional, Tuple, List

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for p in [root_dir, os.path.join(root_dir, "src"), os.path.join(root_dir, "render_sovereign_engine", "src")]:
    if p not in sys.path:
        sys.path.insert(0, p)

try:
    from binory_agents import SovereignCivilization
except ImportError:
    try:
        from src.binory_agents import SovereignCivilization
    except ImportError:
        SovereignCivilization = None

from arc_sovereign_arena.hypothesis_engine import SovereignHypothesisGenerator, Hypothesis


class SovereignArcHarness:
    def __init__(self, civilization: Optional[Any] = None):
        if civilization is not None:
            self.civilization = civilization
        elif SovereignCivilization is not None:
            self.civilization = SovereignCivilization()
        else:
            self.civilization = None

    def solve_task(self, task: Dict[str, Any], pass_number: int = 1) -> Dict[str, Any]:
        t0 = time.time()
        task_id = task["task_id"]
        train_pairs = task["train"]
        test_pairs = task["test"]

        if not train_pairs:
            return {
                "task_id": task_id, "solved": False, "reason": "No training pairs",
                "input_grid": [], "output_grid": [], "prediction_grid": [], "active_hyps": []
            }

        p0_in = train_pairs[0]["input"]
        p0_out = train_pairs[0]["output"]

        # 1. Generate candidate hypotheses across the 4 Pillars
        candidates = SovereignHypothesisGenerator.generate_all(train_pairs)

        winning_hyp: Optional[Hypothesis] = None
        best_pred: Optional[np.ndarray] = None

        for hyp in candidates:
            all_match = True
            for pair in train_pairs:
                pred = hyp.apply(pair["input"])
                if pred is None or pred.shape != pair["output"].shape or not np.array_equal(pred, pair["output"]):
                    all_match = False
                    break
            if all_match:
                winning_hyp = hyp
                best_pred = hyp.apply(p0_in)
                break

        elapsed = time.time() - t0

        # If not solved, generate a sample prediction from the first candidate for visual display
        if best_pred is None and candidates:
            sample_pred = candidates[0].apply(p0_in)
            best_pred = sample_pred if sample_pred is not None else np.zeros_like(p0_out)

        active_hyps_summary = [f"[{h.pillar_id.replace('_prime', '').replace('_meta', '')}] {h.description}" for h in candidates[:8]]

        if winning_hyp is None:
            return {
                "task_id": task_id,
                "solved": False,
                "pillar": None,
                "law": None,
                "time_sec": round(elapsed, 4),
                "hypotheses_tested": len(candidates),
                "train_accuracy": 0.0,
                "test_accuracy": 0.0,
                "input_grid": p0_in.tolist(),
                "output_grid": p0_out.tolist(),
                "prediction_grid": best_pred.tolist() if best_pred is not None else [],
                "active_hyps": active_hyps_summary
            }

        # 2. Blind Test Verification
        test_acc = 0.0
        if test_pairs and "output" in test_pairs[0]:
            test_pred = winning_hyp.apply(test_pairs[0]["input"])
            if test_pred is not None and test_pred.shape == test_pairs[0]["output"].shape and np.array_equal(test_pred, test_pairs[0]["output"]):
                test_acc = 1.0

        # 3. Credit winning Pillar in living SovereignCivilization
        pillar_name = winning_hyp.pillar_id
        if self.civilization and hasattr(self.civilization, "nodes") and pillar_name in self.civilization.nodes:
            node = self.civilization.nodes[pillar_name]
            if hasattr(node, "kolmogorov_engine") and hasattr(node.kolmogorov_engine, "program_library"):
                sig = f"arc_pass{pass_number}_{task_id}_{winning_hyp.signature}"
                node.kolmogorov_engine.program_library[sig] = winning_hyp.description
            if hasattr(node, "state") and hasattr(node.state, "energy"):
                node.state.energy = min(300.0, node.state.energy + 5.0)
            if hasattr(self.civilization, "fabric") and self.civilization.fabric:
                self.civilization.fabric.reinforce_synapse(pillar_name, pillar_name, amount=2.5)

        pillar_readable = {
            "classical_prime": "Classical-Eikonal",
            "quantum_prime": "Quantum-Superposed",
            "modern_prime": "Modern-Thermodynamic",
            "string_meta": "String-10D-Topological"
        }.get(pillar_name, pillar_name)

        return {
            "task_id": task_id,
            "solved": True,
            "pillar": pillar_readable,
            "signature": winning_hyp.signature,
            "description": winning_hyp.description,
            "train_accuracy": 1.0,
            "test_accuracy": test_acc,
            "hypotheses_tested": len(candidates),
            "time_sec": round(elapsed, 4),
            "input_grid": p0_in.tolist(),
            "output_grid": p0_out.tolist(),
            "prediction_grid": best_pred.tolist() if best_pred is not None else [],
            "active_hyps": active_hyps_summary
        }
