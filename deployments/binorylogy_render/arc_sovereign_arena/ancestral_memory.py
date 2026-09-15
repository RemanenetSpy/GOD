"""
Ancestral Causal Memory for ARC Sovereign Survival Ecology
Maintains durable, cross-generational causal knowledge:
1. Confirmed Nutrition: (task_id, r, c) -> correct color (permanent food source)
2. Toxic Ledger: (task_id, r, c, color) -> penalty count / failure weight
3. Lethal Traces: Records exact action sequences preceding starvation deaths
4. Veto Mechanism: Supplies Quantum Pillar with invalid/toxic color masks
"""

import json
from typing import Dict, Tuple, List, Any, Optional


class AncestralCausalMemory:
    """
    Episodic and semantic causal memory of past lives.
    Prevents the Sovereign Civilization from repeating fatal mistakes.
    """

    def __init__(self):
        # Key: f"{task_id}:{r}:{c}" -> int (confirmed correct color)
        self.confirmed_nutrition: Dict[str, int] = {}
        # Key: f"{task_id}:{r}:{c}:{color}" -> float (toxic penalty weight)
        self.toxic_ledger: Dict[str, float] = {}
        # Key: task_id -> int (starvation deaths count)
        self.task_deaths: Dict[str, int] = {}
        # List of recent lethal starvation traces
        self.lethal_traces: List[Dict[str, Any]] = []
        # Invariant Law Ledger: task_id -> {law_signature, pillar_id, description, complexity}
        self.discovered_invariants: Dict[str, Dict[str, Any]] = {}
        # Invariant Class Prior Statistics: law_signature -> success count
        self.invariant_class_counts: Dict[str, int] = {}

    def record_nutrition(self, task_id: str, r: int, c: int, color: int):
        """Records a verified food source."""
        key = f"{task_id}:{r}:{c}"
        self.confirmed_nutrition[key] = int(color)
        # Clear any old toxic marks for this correct color
        toxic_key = f"{task_id}:{r}:{c}:{color}"
        if toxic_key in self.toxic_ledger:
            del self.toxic_ledger[toxic_key]

    def record_toxic(self, task_id: str, r: int, c: int, color: int, penalty: float = 3.0):
        """Records a toxic pixel that wasted energy."""
        key = f"{task_id}:{r}:{c}:{color}"
        self.toxic_ledger[key] = self.toxic_ledger.get(key, 0.0) + float(penalty)

    def record_starvation_death(self, task_id: str, trace: List[Dict[str, Any]]):
        """
        Retrograde Causal Credit Assignment:
        Heavily penalizes the paint actions in the final moments before starvation.
        """
        self.task_deaths[task_id] = self.task_deaths.get(task_id, 0) + 1

        penalized_actions = 0
        for entry in trace:
            if entry.get("action") == "PAINT":
                r = int(entry.get("r", 0))
                c = int(entry.get("c", 0))
                color = int(entry.get("color", 0))
                # Heavy lethal punishment: marks this action as a contributor to starvation
                self.record_toxic(task_id, r, c, color, penalty=15.0)
                penalized_actions += 1

        self.lethal_traces.append({
            "task_id": task_id,
            "penalized_actions": penalized_actions,
            "trace_len": len(trace),
            "trace_sample": trace[-5:] if len(trace) > 5 else trace
        })
        if len(self.lethal_traces) > 50:
            self.lethal_traces.pop(0)

    def is_confirmed_nutrition(self, task_id: str, r: int, c: int) -> Optional[int]:
        """Returns confirmed color if known, else None."""
        return self.confirmed_nutrition.get(f"{task_id}:{r}:{c}")

    def get_toxic_weight(self, task_id: str, r: int, c: int, color: int) -> float:
        """Returns accumulated toxicity weight of a color choice at (r, c)."""
        return self.toxic_ledger.get(f"{task_id}:{r}:{c}:{color}", 0.0)

    def get_veto_mask(self, task_id: str, r: int, c: int) -> List[int]:
        """Returns list of colors proven to be toxic or lethal at this tile."""
        vetoed = []
        for color in range(10):
            if self.get_toxic_weight(task_id, r, c, color) > 0.0:
                vetoed.append(color)
        return vetoed

    def record_invariant_solution(self, task_id: str, law_signature: str, pillar_id: str,
                                   description: str, complexity: float = 1.0):
        """Records a verified invariant physical law that solved a task across all demonstration pairs."""
        self.discovered_invariants[task_id] = {
            "law_signature": law_signature,
            "pillar_id": pillar_id,
            "description": description,
            "complexity": float(complexity)
        }
        self.invariant_class_counts[law_signature] = self.invariant_class_counts.get(law_signature, 0) + 1

    def get_invariant_solution(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Returns the discovered invariant law for a given task, if already known."""
        return self.discovered_invariants.get(task_id)

    def get_invariant_priors(self) -> List[str]:
        """Returns invariant law signatures sorted by historical success frequency."""
        return sorted(self.invariant_class_counts.keys(), key=lambda k: self.invariant_class_counts[k], reverse=True)

    def to_dict(self) -> Dict[str, Any]:
        """Serializes ancestral memory for checkpoint storage and telemetry."""
        return {
            "confirmed_nutrition": self.confirmed_nutrition,
            "toxic_ledger": self.toxic_ledger,
            "task_deaths": self.task_deaths,
            "discovered_invariants": self.discovered_invariants,
            "invariant_class_counts": self.invariant_class_counts,
            "total_invariants_discovered": len(self.discovered_invariants),
            "total_nutrition_discovered": len(self.confirmed_nutrition),
            "total_toxic_vetoed": len(self.toxic_ledger),
            "total_deaths_recorded": sum(self.task_deaths.values()),
            "recent_lethal_traces": self.lethal_traces[-5:]
        }

    def load_dict(self, data: Dict[str, Any]):
        """Restores ancestral memory from vault checkpoint."""
        if not data:
            return
        self.confirmed_nutrition = data.get("confirmed_nutrition", {})
        self.toxic_ledger = data.get("toxic_ledger", {})
        self.task_deaths = data.get("task_deaths", {})
        self.lethal_traces = data.get("recent_lethal_traces", [])
        self.discovered_invariants = data.get("discovered_invariants", {})
        self.invariant_class_counts = data.get("invariant_class_counts", {})

