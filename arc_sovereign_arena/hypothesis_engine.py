"""
ARC Sovereign Hypothesis Engine
Maps mathematical and physical operators directly to the 4 Sovereign Pillars:
- Classical-Eikonal: Affine symmetries (D4), spatial shifts, gravity advection, bounding crops, compound D4, homothety, kaleidoscope expansions.
- Quantum-Superposed: State permutation ciphers, crop-permutation compositions, multi-operator superposition.
- Modern-Thermodynamic: Cellular diffusion, vacuum entropy background crops, minimum thermal energy clusters.
- String-10D-Topological: Enclosure hole-filling, largest connected component extractions, Kronecker fractals, boundary perimeters.
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

        # 4. Bounding Box Isolation & Compound Symmetries
        def bbox_crop(grid):
            nz = np.argwhere(grid != 0)
            if len(nz) == 0:
                return grid
            min_r, min_c = nz.min(axis=0)
            max_r, max_c = nz.max(axis=0)
            return grid[min_r:max_r+1, min_c:max_c+1]

        hyps.append(Hypothesis("classical_prime", "bounding_box_crop", "Minimal non-zero bounding box crop", bbox_crop))

        for d_name, d_desc, d_op in d4_ops[1:]:
            hyps.append(Hypothesis(
                "classical_prime",
                f"bbox_crop_{d_name}",
                f"Bounding Box Crop + {d_desc}",
                lambda x, op=d_op: op(bbox_crop(x))
            ))

        # 5. Integer Homothetic Scaling
        for scale in [2, 3, 4]:
            hyps.append(Hypothesis(
                "classical_prime",
                f"scale_homothety_{scale}x",
                f"Integer Homothetic Scale {scale}x",
                lambda x, s=scale: np.repeat(np.repeat(x, s, axis=0), s, axis=1)
            ))

        # 6. Concatenation & Symmetry Overlays
        hyps.append(Hypothesis("classical_prime", "concat_h_flip", "Horizontal Concatenation with Parity Flip", lambda x: np.concatenate([x, np.fliplr(x)], axis=1)))
        hyps.append(Hypothesis("classical_prime", "concat_v_flip", "Vertical Concatenation with Parity Flip", lambda x: np.concatenate([x, np.flipud(x)], axis=0)))
        hyps.append(Hypothesis("classical_prime", "concat_h_ident", "Horizontal Concatenation Identity", lambda x: np.concatenate([x, x], axis=1)))
        hyps.append(Hypothesis("classical_prime", "mirror_v_overlay", "Vertical Reflection Parity Overlay", lambda x: np.where(x != 0, x, np.flipud(x))))
        hyps.append(Hypothesis("classical_prime", "mirror_h_overlay", "Horizontal Reflection Parity Overlay", lambda x: np.where(x != 0, x, np.fliplr(x))))

        # 7. 4-Fold D4 Kaleidoscope Expansion
        def quad_mirror(x):
            top = np.concatenate([x, np.fliplr(x)], axis=1)
            bottom = np.concatenate([np.flipud(x), np.rot90(x, 2)], axis=1)
            return np.concatenate([top, bottom], axis=0)

        hyps.append(Hypothesis("classical_prime", "quad_mirror_expansion", "4-Fold D4 Kaleidoscope Expansion", quad_mirror))

        # 8. Optical Ray Geodesics (Fermat's Principle / Wavefront propagation)
        if sample_in.shape == sample_out.shape:
            unique_in = [c for c in np.unique(sample_in) if c != 0]
            unique_out = [c for c in np.unique(sample_out) if c != 0]
            beam_targets = list(set(unique_out + [c for c in unique_out if c not in unique_in]))
            for sc in unique_in:
                for bc in beam_targets:
                    def make_ray_conn(src_c, beam_c):
                        def _conn(grid):
                            coords = np.argwhere(grid == src_c)
                            if len(coords) < 2:
                                return grid
                            res = grid.copy()
                            for i in range(len(coords)):
                                for j in range(i + 1, len(coords)):
                                    r1, c1 = coords[i]
                                    r2, c2 = coords[j]
                                    if r1 == r2:
                                        c_min, c_max = min(c1, c2), max(c1, c2)
                                        for col in range(c_min + 1, c_max):
                                            if res[r1, col] == 0:
                                                res[r1, col] = beam_c
                                    elif c1 == c2:
                                        r_min, r_max = min(r1, r2), max(r1, r2)
                                        for row in range(r_min + 1, r_max):
                                            if res[row, c1] == 0:
                                                res[row, c1] = beam_c
                            return res
                        return _conn
                    hyps.append(Hypothesis(
                        "classical_prime",
                        f"eikonal_ray_connect_{sc}_{bc}",
                        f"Eikonal Ray Connect source {sc} with beam {bc}",
                        make_ray_conn(sc, bc)
                    ))

            # 9. Gravitational Vector Attraction Between Physical Bodies
            if len(unique_in) >= 2:
                for mc in unique_in:
                    for ac in unique_in:
                        if mc == ac:
                            continue
                        def make_attract(mover_c, attr_c):
                            def _attr(grid):
                                m_coords = np.argwhere(grid == mover_c)
                                a_coords = np.argwhere(grid == attr_c)
                                if len(m_coords) == 0 or len(a_coords) == 0:
                                    return grid
                                m_cm = m_coords.mean(axis=0)
                                a_cm = a_coords.mean(axis=0)
                                dr_total = a_cm[0] - m_cm[0]
                                dc_total = a_cm[1] - m_cm[1]
                                if abs(dr_total) >= abs(dc_total):
                                    step_r = 1 if dr_total > 0 else -1
                                    step_c = 0
                                else:
                                    step_r = 0
                                    step_c = 1 if dc_total > 0 else -1
                                h, w = grid.shape
                                other_mask = (grid != 0) & (grid != mover_c)
                                curr_m = m_coords.copy()
                                max_steps = max(h, w)
                                best_m = curr_m.copy()
                                for _ in range(max_steps):
                                    next_m = best_m + np.array([step_r, step_c])
                                    collision = False
                                    for r, c in next_m:
                                        if not (0 <= r < h and 0 <= c < w) or other_mask[r, c]:
                                            collision = True
                                            break
                                    if collision:
                                        break
                                    best_m = next_m
                                res = grid.copy()
                                res[grid == mover_c] = 0
                                for r, c in best_m:
                                    res[r, c] = mover_c
                                return res
                            return _attr
                        hyps.append(Hypothesis(
                            "classical_prime",
                            f"gravitational_attraction_{mc}_{ac}",
                            f"Gravitational Attraction: Color {mc} attracted to {ac}",
                            make_attract(mc, ac)
                        ))

            # 10. Non-Wrapping Selective Cardinal Translations
            for mc in unique_in:
                for dr in [-3, -2, -1, 0, 1, 2, 3]:
                    for dc in [-3, -2, -1, 0, 1, 2, 3]:
                        if dr == 0 and dc == 0:
                            continue
                        def make_selective_shift(col, r, c):
                            def _cs(grid):
                                h, w = grid.shape
                                res = grid.copy()
                                res[res == col] = 0
                                coords = np.argwhere(grid == col)
                                for cr, cc in coords:
                                    nr, nc = cr + r, cc + c
                                    if 0 <= nr < h and 0 <= nc < w:
                                        res[nr, nc] = col
                                return res
                            return _cs
                        hyps.append(Hypothesis(
                            "classical_prime",
                            f"selective_shift_{mc}_{dr}_{dc}",
                            f"Selective shift color {mc} by ({dr}, {dc})",
                            make_selective_shift(mc, dr, dc)
                        ))

        return hyps

    @staticmethod
    def generate_quantum_hypotheses(train_pairs: List[Dict[str, np.ndarray]]) -> List[Hypothesis]:
        """Quantum-Superposed: multi-state superposition, permutation ciphers & color remapping."""
        hyps = []
        if not train_pairs:
            return hyps

        p0_in, p0_out = train_pairs[0]["input"], train_pairs[0]["output"]

        # Helper bbox
        def bbox_crop(grid):
            nz = np.argwhere(grid != 0)
            if len(nz) == 0:
                return grid
            min_r, min_c = nz.min(axis=0)
            max_r, max_c = nz.max(axis=0)
            return grid[min_r:max_r+1, min_c:max_c+1]

        # 1. Direct color permutation cipher
        if p0_in.shape == p0_out.shape:
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

        # 2. BBox Crop + Quantum Permutation Cipher
        cropped_pairs = [(bbox_crop(pr["input"]), pr["output"]) for pr in train_pairs]
        if not any(c_in.shape != c_out.shape for c_in, c_out in cropped_pairs):
            cmap_crop = {}
            consistent_crop = True
            for c_in, c_out in cropped_pairs:
                for u in np.unique(c_in):
                    targets = np.unique(c_out[c_in == u])
                    if len(targets) == 1:
                        if u in cmap_crop and cmap_crop[u] != targets[0]:
                            consistent_crop = False
                            break
                        cmap_crop[u] = targets[0]
                    else:
                        consistent_crop = False
                        break
                if not consistent_crop:
                    break

            if consistent_crop and cmap_crop:
                def make_crop_map(mapping):
                    return lambda g: np.vectorize(lambda c: mapping.get(c, c))(bbox_crop(g))
                hyps.append(Hypothesis(
                    "quantum_prime",
                    f"bbox_crop_color_permutation_{len(cmap_crop)}states",
                    f"BBox Crop + Quantum Color Permutation {dict(cmap_crop)}",
                    make_crop_map(dict(cmap_crop))
                ))

        # 3. Color-conditional filters (project onto state c)
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

        # 4. Cluster Mass to Energy State Mapping
        if p0_in.shape == p0_out.shape:
            sz_map = {}
            consistent = True
            for pr in train_pairs:
                labeled, num = scipy.ndimage.label(pr["input"] != 0)
                for i in range(1, num + 1):
                    sz = int(np.sum(labeled == i))
                    out_colors = np.unique(pr["output"][labeled == i])
                    if len(out_colors) == 1 and out_colors[0] != 0:
                        c = out_colors[0]
                        if sz in sz_map and sz_map[sz] != c:
                            consistent = False
                            break
                        sz_map[sz] = c
                    else:
                        consistent = False
                        break
                if not consistent:
                    break
            if consistent and sz_map:
                def make_sz_recolor(mapping):
                    def _rc(grid):
                        labeled, num = scipy.ndimage.label(grid != 0)
                        if num == 0:
                            return grid
                        res = grid.copy()
                        for i in range(1, num + 1):
                            sz = int(np.sum(labeled == i))
                            if sz in mapping:
                                res[labeled == i] = mapping[sz]
                        return res
                    return _rc
                hyps.append(Hypothesis(
                    "quantum_prime",
                    f"cluster_mass_recolor_{len(sz_map)}",
                    f"Cluster Mass to State Mapping {dict(sz_map)}",
                    make_sz_recolor(dict(sz_map))
                ))

        return hyps

    @staticmethod
    def generate_thermodynamic_hypotheses(sample_in: np.ndarray, sample_out: np.ndarray) -> List[Hypothesis]:
        """Modern-Thermodynamic: cellular diffusion, vacuum entropy crops, minimum thermal energy clusters."""
        hyps = []

        # 1. 4-Neighbor Cellular Dilation / Diffusion
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

        # Helper bbox
        def bbox_crop(grid):
            nz = np.argwhere(grid != 0)
            if len(nz) == 0:
                return grid
            min_r, min_c = nz.min(axis=0)
            max_r, max_c = nz.max(axis=0)
            return grid[min_r:max_r+1, min_c:max_c+1]

        # 2. Vacuum-Invariant Background Entropy Crop
        def bg_crop(grid):
            counts = np.bincount(grid.ravel(), minlength=10)
            bg = counts.argmax()
            nz = np.argwhere(grid != bg)
            if len(nz) == 0:
                return grid
            min_r, min_c = nz.min(axis=0)
            max_r, max_c = nz.max(axis=0)
            return grid[min_r:max_r+1, min_c:max_c+1]

        hyps.append(Hypothesis("modern_prime", "bg_invariant_bbox_crop", "Vacuum-Invariant BBox Crop", bg_crop))

        # 3. Minimum Thermal Energy Cluster Extraction (Lowest entropy/area localized component)
        def smallest_cc_crop(grid):
            nz_mask = (grid != 0)
            if not np.any(nz_mask):
                return grid
            labeled, num = scipy.ndimage.label(nz_mask)
            if num == 0:
                return grid
            counts = [np.sum(labeled == i) for i in range(1, num + 1)]
            min_idx = np.argmin(counts) + 1
            isolated = np.where(labeled == min_idx, grid, 0)
            return bbox_crop(isolated)

        hyps.append(Hypothesis("modern_prime", "smallest_cc_crop", "Minimum Thermal Energy Cluster Crop", smallest_cc_crop))

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

        # Helper bbox
        def bbox_crop(grid):
            nz = np.argwhere(grid != 0)
            if len(nz) == 0:
                return grid
            min_r, min_c = nz.min(axis=0)
            max_r, max_c = nz.max(axis=0)
            return grid[min_r:max_r+1, min_c:max_c+1]

        # 2. Largest Connected Component Extraction & BBox Crop
        def largest_cc_crop(grid):
            nz_mask = (grid != 0)
            if not np.any(nz_mask):
                return grid
            labeled, num = scipy.ndimage.label(nz_mask)
            if num == 0:
                return grid
            counts = [np.sum(labeled == i) for i in range(1, num + 1)]
            max_idx = np.argmax(counts) + 1
            isolated = np.where(labeled == max_idx, grid, 0)
            return bbox_crop(isolated)

        hyps.append(Hypothesis("string_meta", "largest_cc_bbox_crop", "Topological Largest Component BBox Crop", largest_cc_crop))

        # 3. Kronecker Self-Similar Fractal Expansion
        def kronecker_fractal(grid):
            mask = (grid != 0).astype(int)
            return np.kron(mask, grid)

        hyps.append(Hypothesis("string_meta", "kronecker_fractal_expansion", "Self-similar Kronecker fractal expansion", kronecker_fractal))

        # 4. Perimeter / Boundary Extraction
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

        # 1. Analytical Inverse Causal Deduction (Deducing rules from Delta & Perception)
        try:
            from arc_sovereign_arena.causal_deduction import InverseCausalDeducer
            deduced_hyps = InverseCausalDeducer.deduce_all(train_pairs)
            for dh in deduced_hyps:
                hyps.append(Hypothesis(dh.pillar_id, dh.signature, dh.description, dh.func))
        except Exception:
            pass

        # 2. Foundational Physical & Topological Operator Generators
        hyps.extend(cls.generate_classical_hypotheses(p0_in, p0_out))
        hyps.extend(cls.generate_quantum_hypotheses(train_pairs))
        hyps.extend(cls.generate_thermodynamic_hypotheses(p0_in, p0_out))
        hyps.extend(cls.generate_string_hypotheses(p0_in, p0_out))

        # 3. Council Composition: D4 Symmetries combined with Color Permutation
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
