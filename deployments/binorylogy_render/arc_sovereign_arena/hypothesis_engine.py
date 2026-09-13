"""
ARC Sovereign Hypothesis Engine
Maps mathematical and physical operators directly to the 4 Sovereign Pillars:
- Classical-Eikonal: Affine symmetries (D4), spatial shifts, gravity advection, bounding crops.
- Quantum-Superposed: State permutation ciphers, multi-operator superposition.
- Modern-Thermodynamic: Cellular diffusion, neighbor dilation, MDL entropy reduction.
- String-10D-Topological: Enclosure hole-filling, connected components, Kronecker fractals.
"""

import numpy as np
import scipy.ndimage
from typing import List, Tuple, Dict, Any, Callable, Optional


class Hypothesis:
    def __init__(self, pillar_id: str, signature: str, description: str, func: Callable[[np.ndarray], np.ndarray]):
        self.pillar_id = pillar_id
        self.signature = signature
        self.description = description
        self.func = func

    def apply(self, grid: np.ndarray) -> Optional[np.ndarray]:
        try:
            return self.func(grid)
        except Exception:
            return None


class SovereignHypothesisGenerator:
    """Generates candidate transformation hypotheses from the 4 Pillars without hardcoding."""

    @staticmethod
    def generate_classical_hypotheses(sample_in: np.ndarray, sample_out: np.ndarray) -> List[Hypothesis]:
        """Classical-Eikonal: deterministic geometric optics, ray-tracing, affine symmetries & gravity."""
        hyps = []

        # 1. D4 Dihedral Symmetries (Rotations & Parity Inversions)
        d4_ops = [
            ("ident", "Identity Invariant", lambda x: x.copy()),
            ("rot90", "90-degree Spatial Rotation", lambda x: np.rot90(x, 1)),
            ("rot180", "180-degree Spatial Rotation", lambda x: np.rot90(x, 2)),
            ("rot270", "270-degree Spatial Rotation", lambda x: np.rot90(x, 3)),
            ("fliph", "Horizontal Parity Reflection P_x", lambda x: np.fliplr(x)),
            ("flipv", "Vertical Parity Reflection P_y", lambda x: np.flipud(x)),
            ("diag", "Main Diagonal Transpose P_xy", lambda x: x.T),
            ("antidiag", "Anti-Diagonal Reflection", lambda x: np.flip(x.T)),
        ]
        for name, desc, op in d4_ops:
            hyps.append(Hypothesis("classical_prime", f"affine_{name}", desc, op))

        # 2. Spatial Translation Vectors (dr, dc)
        if sample_in.shape == sample_out.shape:
            for dr in [-3, -2, -1, 1, 2, 3]:
                for dc in [-3, -2, -1, 1, 2, 3]:
                    def make_shift(r, c):
                        return lambda x: np.roll(np.roll(x, r, axis=0), c, axis=1)
                    hyps.append(Hypothesis(
                        "classical_prime",
                        f"translation_{dr}_{dc}",
                        f"Spatial translation vector ({dr}, {dc})",
                        make_shift(dr, dc)
                    ))

        # 3. Kinematic Gravitational Advection (Down, Up, Left, Right)
        def gravity_down(grid):
            res = np.zeros_like(grid)
            h, w = grid.shape
            for c in range(w):
                col = grid[:, c]
                nz = col[col != 0]
                if len(nz) > 0:
                    res[h - len(nz):, c] = nz
            return res

        def gravity_up(grid):
            res = np.zeros_like(grid)
            h, w = grid.shape
            for c in range(w):
                col = grid[:, c]
                nz = col[col != 0]
                if len(nz) > 0:
                    res[:len(nz), c] = nz
            return res

        def gravity_right(grid):
            res = np.zeros_like(grid)
            h, w = grid.shape
            for r in range(h):
                row = grid[r, :]
                nz = row[row != 0]
                if len(nz) > 0:
                    res[r, w - len(nz):] = nz
            return res

        def gravity_left(grid):
            res = np.zeros_like(grid)
            h, w = grid.shape
            for r in range(h):
                row = grid[r, :]
                nz = row[row != 0]
                if len(nz) > 0:
                    res[r, :len(nz)] = nz
            return res

        hyps.append(Hypothesis("classical_prime", "gravity_advection_down", "Gravitational mass advection downward", gravity_down))
        hyps.append(Hypothesis("classical_prime", "gravity_advection_up", "Gravitational mass advection upward", gravity_up))
        hyps.append(Hypothesis("classical_prime", "gravity_advection_right", "Gravitational mass advection rightward", gravity_right))
        hyps.append(Hypothesis("classical_prime", "gravity_advection_left", "Gravitational mass advection leftward", gravity_left))

        # 4. Bounding Box Isolation / Crop
        def bbox_crop(grid):
            nz = np.argwhere(grid != 0)
            if len(nz) == 0:
                return grid
            min_r, min_c = nz.min(axis=0)
            max_r, max_c = nz.max(axis=0)
            return grid[min_r:max_r+1, min_c:max_c+1]

        hyps.append(Hypothesis("classical_prime", "bounding_box_crop", "Minimal non-zero bounding box crop", bbox_crop))

        return hyps

    @staticmethod
    def generate_quantum_hypotheses(train_pairs: List[Dict[str, np.ndarray]]) -> List[Hypothesis]:
        """Quantum-Superposed: multi-state superposition, permutation ciphers & color remapping."""
        hyps = []
        if not train_pairs:
            return hyps

        p0_in, p0_out = train_pairs[0]["input"], train_pairs[0]["output"]
        if p0_in.shape != p0_out.shape:
            return hyps

        # Induce color mapping from demonstration pairs
        cmap = {}
        consistent = True
        for p in train_pairs:
            inp, out = p["input"], p["output"]
            if inp.shape != out.shape:
                consistent = False
                break
            for u in np.unique(inp):
                targets = np.unique(out[inp == u])
                if len(targets) == 1:
                    if u in cmap and cmap[u] != targets[0]:
                        consistent = False
                        break
                    cmap[u] = targets[0]
                else:
                    consistent = False
                    break
            if not consistent:
                break

        if consistent and cmap and any(k != v for k, v in cmap.items()):
            def make_palette_map(mapping):
                return lambda x: np.vectorize(lambda c: mapping.get(c, c))(x)
            hyps.append(Hypothesis(
                "quantum_prime",
                f"color_permutation_{len(cmap)}states",
                f"Quantum discrete state permutation cipher {dict(cmap)}",
                make_palette_map(dict(cmap))
            ))

        # Color-conditional filters (project onto state c)
        for c in np.unique(p0_in):
            if c == 0:
                continue
            def make_filter(color):
                return lambda x: np.where(x == color, x, 0)
            hyps.append(Hypothesis(
                "quantum_prime",
                f"state_projection_color_{c}",
                f"Quantum state projection onto eigenstate color {c}",
                make_filter(c)
            ))

        return hyps

    @staticmethod
    def generate_thermodynamic_hypotheses(sample_in: np.ndarray, sample_out: np.ndarray) -> List[Hypothesis]:
        """Modern-Thermodynamic: cellular diffusion, dilation & entropy reduction."""
        hyps = []

        # 4-Neighbor Cellular Dilation / Diffusion
        def cellular_diffuse_1step(grid):
            res = grid.copy()
            h, w = grid.shape
            for r in range(h):
                for c in range(w):
                    if grid[r, c] != 0:
                        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < h and 0 <= nc < w and grid[nr, nc] == 0:
                                res[nr, nc] = grid[r, c]
            return res

        def cellular_diffuse_diagonal(grid):
            res = grid.copy()
            h, w = grid.shape
            for r in range(h):
                for c in range(w):
                    if grid[r, c] != 0:
                        for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < h and 0 <= nc < w and grid[nr, nc] == 0:
                                res[nr, nc] = grid[r, c]
            return res

        hyps.append(Hypothesis("modern_prime", "cellular_diffusion_4neighbor", "Orthogonal 4-neighbor cellular diffusion", cellular_diffuse_1step))
        hyps.append(Hypothesis("modern_prime", "cellular_diffusion_diagonal", "Diagonal cellular diffusion", cellular_diffuse_diagonal))

        return hyps

    @staticmethod
    def generate_string_hypotheses(sample_in: np.ndarray, sample_out: np.ndarray) -> List[Hypothesis]:
        """String-10D-Topological: topological invariants, hole-filling, connected components, Kronecker fractals."""
        hyps = []

        # 1. Topological Enclosure / Hole Filling
        unique_colors = np.unique(sample_in)
        for bound_c in unique_colors:
            if bound_c == 0:
                continue
            for fill_c in range(1, 10):
                if fill_c == bound_c:
                    continue
                def make_hole_fill(b_col, f_col):
                    def _fill(x):
                        if not np.any(x == b_col):
                            return x.copy()
                        bmask = (x == b_col)
                        fmask = scipy.ndimage.binary_fill_holes(bmask) & (~bmask)
                        out = x.copy()
                        out[fmask] = f_col
                        return out
                    return _fill
                hyps.append(Hypothesis(
                    "string_meta",
                    f"topological_enclosure_b{bound_c}_f{fill_c}",
                    f"Topological enclosure hole-filling (boundary={bound_c}, fill={fill_c})",
                    make_hole_fill(bound_c, fill_c)
                ))

        # 2. Kronecker Self-Similar Fractal Expansion
        def kronecker_fractal(grid):
            mask = (grid != 0).astype(int)
            return np.kron(mask, grid)

        hyps.append(Hypothesis("string_meta", "kronecker_fractal_expansion", "Self-similar Kronecker fractal expansion", kronecker_fractal))

        # 3. Perimeter / Boundary Extraction
        def extract_perimeter(grid):
            res = np.zeros_like(grid)
            h, w = grid.shape
            for r in range(h):
                for c in range(w):
                    if grid[r, c] != 0:
                        is_edge = (r == 0 or r == h-1 or c == 0 or c == w-1)
                        if not is_edge:
                            has_zero_neighbor = any(grid[r+dr, c+dc] == 0 for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)])
                            is_edge = has_zero_neighbor
                        if is_edge:
                            res[r, c] = grid[r, c]
            return res

        hyps.append(Hypothesis("string_meta", "topological_boundary_extraction", "Topological outer perimeter boundary extraction", extract_perimeter))

        return hyps

    @classmethod
    def generate_all(cls, train_pairs: List[Dict[str, np.ndarray]]) -> List[Hypothesis]:
        if not train_pairs:
            return []
        p0_in = train_pairs[0]["input"]
        p0_out = train_pairs[0]["output"]

        hyps: List[Hypothesis] = []
        hyps.extend(cls.generate_classical_hypotheses(p0_in, p0_out))
        hyps.extend(cls.generate_quantum_hypotheses(train_pairs))
        hyps.extend(cls.generate_thermodynamic_hypotheses(p0_in, p0_out))
        hyps.extend(cls.generate_string_hypotheses(p0_in, p0_out))

        # Council Composition: D4 Symmetries combined with Color Permutation
        quantum_maps = [h for h in hyps if h.signature.startswith("color_permutation_")]
        if quantum_maps:
            q_map = quantum_maps[0]
            d4_hyps = [h for h in hyps if h.signature.startswith("affine_rot") or h.signature.startswith("affine_flip")]
            for d in d4_hyps:
                def make_comp(op1, op2):
                    return lambda x: op2.func(op1.func(x)) if op1.apply(x) is not None else None
                hyps.append(Hypothesis(
                    "classical_prime",
                    f"composed_{d.signature}_{q_map.signature}",
                    f"Council Composition: {d.description} + {q_map.description}",
                    make_comp(d, q_map)
                ))

        return hyps
