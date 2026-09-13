"""
ARC Sovereign Harness (Plug-in / Plug-out)
Directly bridges the LIVING SovereignCivilization into ARC tasks without modifying core files.
"""

import sys
import os
import time
import numpy as np
from typing import Dict, Any, Optional, Tuple, List

# Ensure src / render_sovereign_engine/src is importable
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for p in [root_dir, os.path.join(root_dir, "src"), os.path.join(root_dir, "render_sovereign_engine", "src")]:
    if p not in sys.path:
        sys.path.insert(0, p)

# Import the REAL living SovereignCivilization
try:
    from binory_agents import SovereignCivilization
except ImportError:
    try:
        from src.binory_agents import SovereignCivilization
    except ImportError:
        SovereignCivilization = None

from arc_sovereign_arena.hypothesis_engine import SovereignHypothesisGenerator, Hypothesis


class SovereignArcHarness:
    """
    Plug-in harness that feeds ARC tasks into the living SovereignCivilization.
    Zero rewriting: uses the real nodes and Hebbian fabric.
    """
    def __init__(self, civilization: Optional[Any] = None):
        if civilization is not None:
            self.civilization = civilization
        elif SovereignCivilization is not None:
            self.civilization = SovereignCivilization()
        else:
            self.civilization = None

    def solve_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Attempts to solve an ARC task through the 4 living Pillars.
        Strict zero-hardcoding: tests hypotheses against all training examples.
        """
        t0 = time.time()
        task_id = task["task_id"]
        train_pairs = task["train"]
        test_pairs = task["test"]

        if not train_pairs:
            return {"task_id": task_id, "solved": False, "reason": "No training pairs"}

        # 1. Generate hypotheses from the 4 Pillars
        candidates = SovereignHypothesisGenerator.generate_all(train_pairs)

        winning_hyp: Optional[Hypothesis] = None
        for hyp in candidates:
            # Check if hypothesis satisfies 100% of demonstration pairs
            all_match = True
            for pair in train_pairs:
                pred = hyp.apply(pair["input"])
                if pred is None or pred.shape != pair["output"].shape or not np.array_equal(pred, pair["output"]):
                    all_match = False
                    break
            if all_match:
                winning_hyp = hyp
                break

        elapsed = time.time() - t0

        if winning_hyp is None:
            return {
                "task_id": task_id,
                "solved": False,
                "pillar": None,
                "law": None,
                "time_sec": round(elapsed, 4),
                "hypotheses_tested": len(candidates),
                "train_accuracy": 0.0,
                "test_accuracy": 0.0
            }

        # 2. Blind Test Verification
        test_acc = 0.0
        if test_pairs and "output" in test_pairs[0]:
            test_pred = winning_hyp.apply(test_pairs[0]["input"])
            if test_pred is not None and test_pred.shape == test_pairs[0]["output"].shape and np.array_equal(test_pred, test_pairs[0]["output"]):
                test_acc = 1.0

        # 3. Credit the winning Pillar in the living SovereignCivilization
        pillar_name = winning_hyp.pillar_id
        if self.civilization and hasattr(self.civilization, "nodes") and pillar_name in self.civilization.nodes:
            node = self.civilization.nodes[pillar_name]
            # Record law into Kolmogorov engine
            if hasattr(node, "kolmogorov_engine") and hasattr(node.kolmogorov_engine, "program_library"):
                sig = f"arc_{task_id}_{winning_hyp.signature}"
                node.kolmogorov_engine.program_library[sig] = winning_hyp.description
            # Boost pillar energy
            if hasattr(node, "state") and hasattr(node.state, "energy"):
                node.state.energy = min(300.0, node.state.energy + 5.0)
            # Strengthen Hebbian synapse
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
            "time_sec": round(elapsed, 4)
        }
