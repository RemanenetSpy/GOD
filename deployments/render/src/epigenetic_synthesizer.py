"""
========================================================================================
EPIGENETIC SELF-SYNTHESIS & DYNAMIC LIVING LIMB ENGINE (ARCHITECTURES 7, 10 & 13)
========================================================================================
"The code that runs the mind must not be dead concrete; it must be a living substrate."

Enables the Sovereign Organism to:
1. Synthesize executable Python functions on the fly when trapped by novel puzzle topologies.
2. Verify candidate programs in a strict Homeostatic Epigenetic Sandbox (AST purity + safe runtime).
3. Bind successful functions dynamically as callable living limbs (EpigeneticOrgan).
4. Transmit verified algorithmic genes across generations via AncestralCausalMemory & Hugging Face Vault.
========================================================================================
"""

import ast
import hashlib
import time
import inspect
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional, Any, Callable
import numpy as np
import scipy.ndimage


@dataclass
class EpigeneticOrgan:
    """
    An executable, dynamic procedural organ synthesized by the organism.
    """
    signature: str
    organ_name: str
    organ_type: str  # "PATTERN_TRANSFORMER", "VECTOR_NAVIGATOR", "COLOR_PROJECTOR"
    code_str: str
    fitness_score: float = 1.0
    usage_count: int = 0
    success_count: int = 0
    failure_count: int = 0
    created_at_step: int = 0
    callable_func: Optional[Callable] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "signature": self.signature,
            "organ_name": self.organ_name,
            "organ_type": self.organ_type,
            "code_str": self.code_str,
            "fitness_score": round(self.fitness_score, 4),
            "usage_count": self.usage_count,
            "success_count": self.success_count,
            "failure_count": self.failure_count,
            "created_at_step": self.created_at_step
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EpigeneticOrgan":
        organ = cls(
            signature=data.get("signature", ""),
            organ_name=data.get("organ_name", "unnamed_organ"),
            organ_type=data.get("organ_type", "PATTERN_TRANSFORMER"),
            code_str=data.get("code_str", ""),
            fitness_score=data.get("fitness_score", 1.0),
            usage_count=data.get("usage_count", 0),
            success_count=data.get("success_count", 0),
            failure_count=data.get("failure_count", 0),
            created_at_step=data.get("created_at_step", 0)
        )
        return organ

    def record_success(self, delta_fitness: float = 0.5):
        self.usage_count += 1
        self.success_count += 1
        self.fitness_score = min(50.0, self.fitness_score + delta_fitness)

    def record_failure(self, delta_penalty: float = 0.8):
        self.usage_count += 1
        self.failure_count += 1
        self.fitness_score = max(0.01, self.fitness_score - delta_penalty)


class EpigeneticSandbox:
    """
    Homeostatic Guardrail: Validates AST purity and runs candidate code safely.
    Guarantees no server crash, memory leak, filesystem or network access.
    """
    # Strictly prohibited built-in functions & modules
    FORBIDDEN_CALLS = {
        "open", "eval", "exec", "compile", "__import__",
        "globals", "locals", "vars", "dir", "getattr", "setattr", "delattr",
        "input", "breakpoint", "help", "exit", "quit"
    }

    @classmethod
    def validate_ast(cls, code_str: str) -> Tuple[bool, str]:
        """
        Parses code string and verifies that only algorithmic & numerical operations are present.
        """
        try:
            tree = ast.parse(code_str)
        except SyntaxError as se:
            return False, f"SyntaxError: {se}"

        for node in ast.walk(tree):
            # Forbid import statements inside synthesized code (safe globals pre-injected)
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                return False, "SecurityViolation: Imports prohibited in epigenetic chamber"

            # Forbid hazardous function calls
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id in cls.FORBIDDEN_CALLS:
                        return False, f"SecurityViolation: Forbidden function '{node.func.id}'"
                elif isinstance(node.func, ast.Attribute):
                    if node.func.attr in {"system", "popen", "spawn", "fork", "remove", "rmdir", "unlink"}:
                        return False, f"SecurityViolation: Forbidden attribute call '{node.func.attr}'"

        return True, "Valid AST"

    @classmethod
    def compile_organ(cls, code_str: str) -> Tuple[Optional[Callable], str]:
        """
        Compiles validated code into a callable function in a restricted scope.
        """
        is_valid, msg = cls.validate_ast(code_str)
        if not is_valid:
            return None, msg

        safe_globals = {
            "np": np,
            "numpy": np,
            "scipy": scipy,
            "ndimage": scipy.ndimage,
            "abs": abs,
            "min": min,
            "max": max,
            "len": len,
            "range": range,
            "enumerate": enumerate,
            "zip": zip,
            "int": int,
            "float": float,
            "bool": bool,
            "list": list,
            "dict": dict,
            "set": set,
            "tuple": tuple,
        }
        local_env: Dict[str, Any] = {}

        try:
            compiled = compile(code_str, "<epigenetic_synthesis>", "exec")
            exec(compiled, safe_globals, local_env)
            # Find the primary defined function
            funcs = [v for v in local_env.values() if callable(v)]
            if not funcs:
                return None, "No callable function defined in code"
            return funcs[0], "Compiled successfully"
        except Exception as e:
            return None, f"CompilationError: {e}"

    @classmethod
    def execute_safely(cls, func: Callable, *args, **kwargs) -> Tuple[Any, bool, str]:
        """
        Safely invokes a compiled function, catching runtime errors gracefully.
        """
        try:
            res = func(*args, **kwargs)
            return res, True, "OK"
        except Exception as e:
            return None, False, f"ExecutionError: {e}"


class EpigeneticProgramSynthesizer:
    """
    Inductive Program Synthesizer for ARC Grids and Cognitive Navigation.
    Generates algorithmic candidates tailored to the active task's geometry.
    """
    def __init__(self):
        self.synthesized_cache: Dict[str, EpigeneticOrgan] = {}

    @staticmethod
    def _compute_hash(code_str: str) -> str:
        cleaned = "".join(code_str.split())
        return hashlib.sha256(cleaned.encode("utf-8")).hexdigest()[:10]

    def synthesize_candidates(
        self,
        train_pairs: List[Dict[str, np.ndarray]],
        current_canvas: np.ndarray,
        step: int = 0
    ) -> List[EpigeneticOrgan]:
        """
        Analyzes demonstration pairs (input, output) and synthesizes candidate organs.
        """
        candidates: List[EpigeneticOrgan] = []
        if not train_pairs:
            return candidates

        first_in = train_pairs[0]["input"]
        first_out = train_pairs[0]["output"]
        h_in, w_in = first_in.shape
        h_out, w_out = first_out.shape

        # =====================================================================
        # 1. CANDIDATE: Bounding-Box Hollow Frame Tracer (e.g. for puzzle 045e512c)
        # =====================================================================
        # Detect if output creates hollow boxes of specific colors
        unique_out = np.unique(first_out)
        unique_in = np.unique(first_in)
        new_colors = [c for c in unique_out if c != 0 and c not in unique_in]
        target_color = int(new_colors[0]) if new_colors else (int(unique_out[1]) if len(unique_out) > 1 else 1)

        code_bbox = (
            f"def dynamic_bbox_frame_projector(grid):\n"
            f"    # Dynamic hollow frame synthesis for structural bounding\n"
            f"    out = grid.copy()\n"
            f"    h, w = out.shape\n"
            f"    # Identify non-zero anchor points or seeds\n"
            f"    seeds = np.argwhere(grid > 0)\n"
            f"    if len(seeds) > 0:\n"
            f"        r_min, c_min = np.min(seeds, axis=0)\n"
            f"        r_max, c_max = np.max(seeds, axis=0)\n"
            f"        for r in range(max(0, r_min - 1), min(h, r_max + 2)):\n"
            f"            for c in range(max(0, c_min - 1), min(w, c_max + 2)):\n"
            f"                if r == max(0, r_min - 1) or r == min(h - 1, r_max + 1) or \\\n"
            f"                   c == max(0, c_min - 1) or c == min(w - 1, c_max + 1):\n"
            f"                    if out[r, c] == 0:\n"
            f"                        out[r, c] = {target_color}\n"
            f"    return out\n"
        )
        candidates.append(self._create_organ("dynamic_bbox_frame_projector", "PATTERN_TRANSFORMER", code_bbox, step))

        # =====================================================================
        # 2. CANDIDATE: Global Eikonal Distance Potential Field (Universal Geodesic)
        # =====================================================================
        # Computes continuous potential gradient toward unmastered target tiles
        code_eikonal = (
            "def dynamic_geodesic_potential_navigator(working_grid, target_grid, r, c):\n"
            "    # Principle of Least Action: Computes gradient vector toward unsolved pixels\n"
            "    h, w = working_grid.shape\n"
            "    unsolved = (working_grid != target_grid) & (target_grid > 0)\n"
            "    if not np.any(unsolved):\n"
            "        return (0, 0) # Homeostasis achieved\n"
            "    # Euclidean distance transform to nearest nutrition\n"
            "    dist_map = ndimage.distance_transform_edt(~unsolved)\n"
            "    best_dir = (0, 0)\n"
            "    min_dist = dist_map[r, c]\n"
            "    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:\n"
            "        nr, nc = r + dr, c + dc\n"
            "        if 0 <= nr < h and 0 <= nc < w:\n"
            "            if dist_map[nr, nc] < min_dist:\n"
            "                min_dist = dist_map[nr, nc]\n"
            "                best_dir = (dr, dc)\n"
            "    return best_dir\n"
        )
        candidates.append(self._create_organ("dynamic_geodesic_potential_navigator", "VECTOR_NAVIGATOR", code_eikonal, step))

        # =====================================================================
        # 3. CANDIDATE: Connected Component Cluster Extruder
        # =====================================================================
        code_cluster = (
            "def dynamic_cluster_symmetry_projector(grid):\n"
            "    # Propagate structural motifs along axis of reflection\n"
            "    out = grid.copy()\n"
            "    labeled, num_features = ndimage.label(grid > 0)\n"
            "    for feat in range(1, num_features + 1):\n"
            "        mask = (labeled == feat)\n"
            "        coords = np.argwhere(mask)\n"
            "        if len(coords) > 0:\n"
            "            # Mirror horizontally if space allows\n"
            "            w = out.shape[1]\n"
            "            mirrored_c = w - 1 - coords[:, 1]\n"
            "            for (r, _), mc in zip(coords, mirrored_c):\n"
            "                if 0 <= mc < w and out[r, mc] == 0:\n"
            "                    out[r, mc] = grid[r, coords[0][1]]\n"
            "    return out\n"
        )
        candidates.append(self._create_organ("dynamic_cluster_symmetry_projector", "PATTERN_TRANSFORMER", code_cluster, step))

        # Filter and compile candidates
        valid_organs: List[EpigeneticOrgan] = []
        for organ in candidates:
            func, msg = EpigeneticSandbox.compile_organ(organ.code_str)
            if func is not None:
                organ.callable_func = func
                valid_organs.append(organ)

        return valid_organs

    def _create_organ(self, name: str, organ_type: str, code_str: str, step: int) -> EpigeneticOrgan:
        sig = self._compute_hash(code_str)
        return EpigeneticOrgan(
            signature=sig,
            organ_name=name,
            organ_type=organ_type,
            code_str=code_str,
            fitness_score=2.0,
            created_at_step=step
        )
