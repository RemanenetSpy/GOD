"""
ARC Task Loader (AGI-1, AGI-2, AGI-3)
Zero hardcoding: reads tasks dynamically from disk as raw numeric matrices.
Robust multi-root path detection for local & Render container layouts.
"""

import os
import glob
import json
import numpy as np
from typing import List, Dict, Any, Optional


class ARCTaskLoader:
    def __init__(self, base_dir: Optional[str] = None):
        if base_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        self.agi1_dir = ""
        self.agi2_dir = ""
        self.agi3_dir = ""

        # Check candidate root paths
        candidates = [
            base_dir,
            os.path.join(base_dir, ".."),
            os.path.abspath("."),
            os.path.abspath(".."),
            os.path.dirname(os.path.abspath("."))
        ]
        for c in candidates:
            p1 = os.path.join(c, "research_archive", "arc_agi", "ARC-AGI-master", "data", "training")
            if os.path.exists(p1):
                self.agi1_dir = os.path.abspath(p1)
                self.agi2_dir = os.path.abspath(os.path.join(c, "research_archive", "arc_agi", "ARC-AGI-master", "data", "evaluation"))
                self.agi3_dir = os.path.abspath(os.path.join(c, "research_archive", "arc_agi", "arc_agi_3_submission"))
                break

    def get_agi1_tasks(self) -> List[str]:
        """Returns all 400 ARC-AGI-1 training task file paths."""
        if not self.agi1_dir or not os.path.exists(self.agi1_dir):
            return []
        return sorted(glob.glob(os.path.join(self.agi1_dir, "*.json")))

    def get_agi2_tasks(self) -> List[str]:
        """Returns all 400 ARC-AGI-2 evaluation task file paths."""
        if not self.agi2_dir or not os.path.exists(self.agi2_dir):
            return []
        return sorted(glob.glob(os.path.join(self.agi2_dir, "*.json")))

    def get_agi3_info(self) -> Dict[str, Any]:
        """Returns AGI-3 interactive game configuration."""
        agent_path = os.path.join(self.agi3_dir, "agent", "my_agent.py") if self.agi3_dir else ""
        return {
            "path": self.agi3_dir,
            "has_agent": bool(agent_path and os.path.exists(agent_path)),
            "mode": "interactive_frame_exploration"
        }

    @staticmethod
    def parse_task(file_path: str) -> Optional[Dict[str, Any]]:
        """Parses a JSON task into numpy array pairs."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                raw = json.load(f)

            task_id = os.path.basename(file_path).replace(".json", "")
            train_pairs = []
            for p in raw.get("train", []):
                train_pairs.append({
                    "input": np.array(p["input"], dtype=np.int32),
                    "output": np.array(p["output"], dtype=np.int32)
                })

            test_pairs = []
            for p in raw.get("test", []):
                t_dict = {"input": np.array(p["input"], dtype=np.int32)}
                if "output" in p:
                    t_dict["output"] = np.array(p["output"], dtype=np.int32)
                test_pairs.append(t_dict)

            return {
                "task_id": task_id,
                "train": train_pairs,
                "test": test_pairs,
                "path": file_path
            }
        except Exception:
            return None
