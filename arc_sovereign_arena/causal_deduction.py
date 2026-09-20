"""
ARC Sovereign Inverse Causal Deduction Engine
Deduces physical and mathematical laws directly from observed differences (Deltas)
between Input and Output scenes without blind brute-force guessing.

The 4 Sovereign Pillars act as specialized analytical lenses:
1. Classical-Eikonal: Kinematics (gravity, translations, collision), Optics (Fermat rays, D4 symmetries, scaling).
2. String-10D-Topological: Invariants (Euler cavities, hole-filling, component filtering, boundaries).
3. Quantum-Superposed: Discrete state transitions (permutation ciphers, mass-to-state mappings, parity).
4. Modern-Thermodynamic: Information compression, intermediate state deduction (f ∘ g composition).
"""

import numpy as np
import scipy.ndimage
from typing import List, Dict, Tuple, Optional, Callable, Any
from arc_sovereign_arena.perception import PerceptualScene, GridObject


class DeducedHypothesis:
    """A mathematically deduced law with provenance and confidence."""
    __slots__ = ("pillar_id", "signature", "description", "func", "complexity")

    def __init__(self, pillar_id: str, signature: str, description: str,
                 func: Callable[[np.ndarray], Optional[np.ndarray]], complexity: float = 1.0):
        self.pillar_id = pillar_id
        self.signature = signature
        self.description = description
        self.func = func
        self.complexity = complexity

    def apply(self, grid: np.ndarray) -> Optional[np.ndarray]:
        try:
            return self.func(grid)
        except Exception:
            return None


class NoetherInvariantProfile:
    """
    Physical Invariant Audit across all demonstration pairs (Input -> Output).
    Quantifies conservation of mass, spatial geometry, topology, and momentum.
    """
    def __init__(self, train_pairs: List[Dict[str, np.ndarray]]):
        self.is_mass_conserved = True
        self.is_shape_conserved = True
        self.is_geometry_conserved = True
        self.dim_ratio: Tuple[float, float] = (1.0, 1.0)
        self.cm_shift: Optional[Tuple[float, float]] = None
        self.color_delta: Dict[int, int] = {}
        self.dominant_field: Optional[str] = None

        if not train_pairs:
            return

        p0_in = train_pairs[0]["input"]
        p0_out = train_pairs[0]["output"]
        h_in, w_in = p0_in.shape
        h_out, w_out = p0_out.shape
        self.dim_ratio = (h_out / max(1, h_in), w_out / max(1, w_in))
        self.is_shape_conserved = (h_in == h_out and w_in == w_out)

        # 1. Mass Conservation Audit: exact color multiset equality across all pairs
        for pair in train_pairs:
            hist_in = np.bincount(pair["input"].flat, minlength=10)
            hist_out = np.bincount(pair["output"].flat, minlength=10)
            if not np.array_equal(hist_in, hist_out):
                self.is_mass_conserved = False
                for c in range(10):
                    diff = int(hist_out[c] - hist_in[c])
                    if diff != 0:
                        self.color_delta[c] = diff
                break

        # 2. Geometry Conservation: spatial distribution of active foreground pixels
        if self.is_shape_conserved:
            for pair in train_pairs:
                mask_in = (pair["input"] != 0)
                mask_out = (pair["output"] != 0)
                if not np.array_equal(mask_in, mask_out):
                    self.is_geometry_conserved = False
                    break

        # 3. Center of Mass Shift (Momentum / Field Direction)
        if self.is_shape_conserved:
            in_fg = np.argwhere(p0_in != 0)
            out_fg = np.argwhere(p0_out != 0)
            if len(in_fg) > 0 and len(out_fg) > 0:
                cm_in = np.mean(in_fg, axis=0)
                cm_out = np.mean(out_fg, axis=0)
                dr, dc = float(cm_out[0] - cm_in[0]), float(cm_out[1] - cm_in[1])
                self.cm_shift = (dr, dc)
                if dr > 0.5 and abs(dc) <= abs(dr):
                    self.dominant_field = "gravity_down"
                elif dr < -0.5 and abs(dc) <= abs(dr):
                    self.dominant_field = "gravity_up"
                elif dc > 0.5 and abs(dr) <= abs(dc):
                    self.dominant_field = "gravity_right"
                elif dc < -0.5 and abs(dr) <= abs(dc):
                    self.dominant_field = "gravity_left"


class InverseCausalDeducer:
    """
    Analyzes training examples (Input_k -> Output_k) and directly deduces candidate laws
    via Noether Invariant Analysis, Potential Field Gradients, and Minimal Description Length.
    """

    @classmethod
    def deduce_all(cls, train_pairs: List[Dict[str, np.ndarray]]) -> List[DeducedHypothesis]:
        if not train_pairs:
            return []

        hyps: List[DeducedHypothesis] = []
        p0_in = train_pairs[0]["input"]
        p0_out = train_pairs[0]["output"]

        # First-Principles Noether Invariant Audit
        profile = NoetherInvariantProfile(train_pairs)

        # 0. Primary Noether & Field Invariant Deductions (Gravity, Momentum, Diffusion)
        hyps.extend(cls._deduce_noether_and_field_laws(train_pairs, profile))

        # Parse initial perceptual scenes
        in_scenes = [PerceptualScene(p["input"]) for p in train_pairs]
        out_scenes = [PerceptualScene(p["output"]) for p in train_pairs]

        # 1. Classical-Eikonal Deductions (Optics, Affine Symmetries, Kinematics)
        hyps.extend(cls._deduce_classical(train_pairs, in_scenes, out_scenes))

        # 2. String-10D-Topological Deductions (Cavities, Invariants, Filtering)
        hyps.extend(cls._deduce_topological(train_pairs, in_scenes, out_scenes))

        # 3. Quantum-Superposed Deductions (Ciphers, Mass-to-State, Parity)
        hyps.extend(cls._deduce_quantum(train_pairs, in_scenes, out_scenes))

        # 4. Modern-Thermodynamic Deductions (2-Step Intermediate Compositions)
        hyps.extend(cls._deduce_thermodynamic_compositions(train_pairs, hyps))

        return hyps

    # ═════════════════════════════════════════════════════════════════════════
    # 0. NOETHER & CONTINUOUS FIELD INVARIANT DEDUCTIONS
    # ═════════════════════════════════════════════════════════════════════════
    @classmethod
    def _deduce_noether_and_field_laws(cls, train_pairs: List[Dict[str, np.ndarray]],
                                       profile: NoetherInvariantProfile) -> List[DeducedHypothesis]:
        deduced = []
        p0_in = train_pairs[0]["input"]
        p0_out = train_pairs[0]["output"]

        # A. Conservative Gravitational & Kinematic Advection (Least Action Potential Gradient)
        if profile.is_shape_conserved:
            def make_gravity_down():
                def g_down(grid):
                    res = np.zeros_like(grid)
                    h, w = grid.shape
                    for c in range(w):
                        col = grid[:, c]
                        nz = col[col != 0]
                        if len(nz) > 0:
                            res[h - len(nz):, c] = nz
                    return res
                return g_down

            def make_gravity_up():
                def g_up(grid):
                    res = np.zeros_like(grid)
                    for c in range(grid.shape[1]):
                        col = grid[:, c]
                        nz = col[col != 0]
                        if len(nz) > 0:
                            res[:len(nz), c] = nz
                    return res
                return g_up

            def make_gravity_left():
                def g_left(grid):
                    res = np.zeros_like(grid)
                    for r in range(grid.shape[0]):
                        row = grid[r, :]
                        nz = row[row != 0]
                        if len(nz) > 0:
                            res[r, :len(nz)] = nz
                    return res
                return g_left

            def make_gravity_right():
                def g_right(grid):
                    res = np.zeros_like(grid)
                    w = grid.shape[1]
                    for r in range(grid.shape[0]):
                        row = grid[r, :]
                        nz = row[row != 0]
                        if len(nz) > 0:
                            res[r, w - len(nz):] = nz
                    return res
                return g_right

            # Prioritize matching gravitational field direction based on Center-of-Mass gradient
            gravity_candidates = [
                ("gravity_down", "Classical Kinematics: Gravitational Advection Downward (-grad_Phi = -g j)", make_gravity_down()),
                ("gravity_up", "Classical Kinematics: Gravitational Inversion Upward (-grad_Phi = +g j)", make_gravity_up()),
                ("gravity_left", "Classical Kinematics: Horizontal Drift Leftward (-grad_Phi = -g i)", make_gravity_left()),
                ("gravity_right", "Classical Kinematics: Horizontal Drift Rightward (-grad_Phi = +g i)", make_gravity_right()),
            ]

            # Obstacle-supported gravity (particles fall until hitting an obstacle or floor)
            def make_supported_gravity_down():
                def sg_down(grid):
                    res = grid.copy()
                    h, w = res.shape
                    moved = True
                    # Simulate falling steps until rest
                    for _ in range(h):
                        if not moved:
                            break
                        moved = False
                        for r in range(h - 2, -1, -1):
                            for c in range(w):
                                if res[r, c] != 0 and res[r + 1, c] == 0:
                                    res[r + 1, c] = res[r, c]
                                    res[r, c] = 0
                                    moved = True
                    return res
                return sg_down

            gravity_candidates.append((
                "gravity_supported_down",
                "Classical Kinematics: Obstacle-Supported Gravity Downward",
                make_supported_gravity_down()
            ))

            for sig, desc, op in gravity_candidates:
                # If mass is conserved or field direction matches, test candidate
                sample_t = op(p0_in)
                if sample_t is not None and sample_t.shape == p0_out.shape:
                    deduced.append(DeducedHypothesis(
                        "classical_prime", f"noether_{sig}", desc, op, complexity=1.1
                    ))

            # B. Center of Mass Momentum Translation
            if profile.cm_shift is not None:
                dr = int(round(profile.cm_shift[0]))
                dc = int(round(profile.cm_shift[1]))
                if dr != 0 or dc != 0:
                    def make_cm_shift(r_s, c_s):
                        return lambda x: np.roll(np.roll(x, r_s, axis=0), c_s, axis=1)
                    deduced.append(DeducedHypothesis(
                        "classical_prime",
                        f"noether_momentum_shift_{dr}_{dc}",
                        f"Noether Momentum Shift: Center-of-Mass Vector ({dr}, {dc})",
                        make_cm_shift(dr, dc),
                        complexity=1.2
                    ))

        # C. Fluid Diffusion Wavefront (Laplacian Propagation)
        # Check if new colored mass appeared that diffuses from existing seed pixels
        if profile.is_shape_conserved and profile.color_delta:
            for seed_color, delta in profile.color_delta.items():
                if delta > 0 and seed_color != 0:
                    # Color increased: test Laplacian flood-fill into adjacent background 0s
                    def make_laplacian_diffusion(col=seed_color):
                        def diffuse_fn(grid):
                            res = grid.copy()
                            seed_mask = (grid == col)
                            # Diffuse into connected background zeros
                            struct = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], dtype=bool)
                            dilated = scipy.ndimage.binary_dilation(seed_mask, structure=struct)
                            # Only fill where currently empty (0)
                            res[dilated & (grid == 0)] = col
                            return res
                        return diffuse_fn

                    deduced.append(DeducedHypothesis(
                        "modern_prime",
                        f"noether_laplacian_diffusion_c{seed_color}",
                        f"Modern Thermodynamics: Laplacian Fluid Diffusion (Color {seed_color})",
                        make_laplacian_diffusion(seed_color),
                        complexity=1.3
                    ))

        return deduced

    # ═════════════════════════════════════════════════════════════════════════
    # 1. CLASSICAL-EIKONAL DEDUCTIONS
    # ═════════════════════════════════════════════════════════════════════════
    @classmethod
    def _deduce_classical(cls, train_pairs, in_scenes, out_scenes) -> List[DeducedHypothesis]:
        deduced = []
        p0_in = train_pairs[0]["input"]
        p0_out = train_pairs[0]["output"]
        h_in, w_in = p0_in.shape
        h_out, w_out = p0_out.shape

        # A. D4 Symmetries (Direct Analytical Matching)
        d4_transforms = [
            ("ident", "Identity", lambda x: x.copy()),
            ("rot90", "90-degree Spatial Rotation", lambda x: np.rot90(x, 1)),
            ("rot180", "180-degree Spatial Rotation", lambda x: np.rot90(x, 2)),
            ("rot270", "270-degree Spatial Rotation", lambda x: np.rot90(x, 3)),
            ("fliph", "Horizontal Parity Reflection P_x", lambda x: np.fliplr(x)),
            ("flipv", "Vertical Parity Reflection P_y", lambda x: np.flipud(x)),
            ("diag", "Main Diagonal Transpose P_xy", lambda x: x.T),
            ("antidiag", "Anti-Diagonal Reflection", lambda x: np.flip(x.T)),
        ]
        for name, desc, op in d4_transforms:
            # Check if this transform matches dimensions
            sample_t = op(p0_in)
            if sample_t.shape == p0_out.shape:
                deduced.append(DeducedHypothesis(
                    "classical_prime", f"affine_{name}", f"Classical D4: {desc}", op, complexity=1.0
                ))

        # B. Bounding Box Crop Deduction
        # Check if output matches bounding box of non-background objects
        bbox0 = in_scenes[0].get_full_bbox()
        if bbox0 is not None:
            bh = bbox0[2] - bbox0[0] + 1
            bw = bbox0[3] - bbox0[1] + 1
            if (bh, bw) == (h_out, w_out):
                def make_bbox_crop():
                    def crop_fn(grid):
                        scene = PerceptualScene(grid)
                        b = scene.get_full_bbox()
                        if b is None:
                            return grid
                        return grid[b[0]:b[2]+1, b[1]:b[3]+1]
                    return crop_fn
                deduced.append(DeducedHypothesis(
                    "classical_prime", "deduced_bbox_crop",
                    "Classical Optics: Foreground Bounding Box Crop",
                    make_bbox_crop(), complexity=1.2
                ))

        # C. Homothetic Scaling Deduction (Integer Multipliers)
        if h_out > h_in and w_out > w_in and h_out % h_in == 0 and w_out % w_in == 0:
            scale_r = h_out // h_in
            scale_c = w_out // w_in
            if scale_r == scale_c:
                s = scale_r
                deduced.append(DeducedHypothesis(
                    "classical_prime", f"homothety_{s}x",
                    f"Classical Scale: Homothetic Expansion {s}x",
                    lambda x, factor=s: np.repeat(np.repeat(x, factor, axis=0), factor, axis=1),
                    complexity=1.3
                ))

        # D. Optical Ray Geodesics (Fermat Connections)
        # Check if output contains lines of a beam color connecting particles of a source color
        colors_in = set(np.unique(p0_in))
        colors_out = set(np.unique(p0_out))
        new_colors = colors_out - colors_in
        candidate_beams = list(new_colors) if new_colors else [c for c in colors_out if c != 0]

        for beam_c in candidate_beams:
            for src_c in [c for c in colors_in if c != 0]:
                def make_ray_geodesic(source_col, beam_col):
                    def ray_fn(grid):
                        res = grid.copy()
                        coords = np.argwhere(grid == source_col)
                        if len(coords) < 2:
                            return res
                        for i in range(len(coords)):
                            for j in range(i + 1, len(coords)):
                                r1, c1 = coords[i]
                                r2, c2 = coords[j]
                                if r1 == r2:  # Horizontal ray
                                    c_min, c_max = min(c1, c2), max(c1, c2)
                                    path = res[r1, c_min+1:c_max]
                                    if np.all((path == 0) | (path == beam_col)):
                                        res[r1, c_min+1:c_max] = beam_col
                                elif c1 == c2:  # Vertical ray
                                    r_min, r_max = min(r1, r2), max(r1, r2)
                                    path = res[r_min+1:r_max, c1]
                                    if np.all((path == 0) | (path == beam_col)):
                                        res[r_min+1:r_max, c1] = beam_col
                                elif abs(r1 - r2) == abs(c1 - c2):  # Diagonal ray
                                    dr = 1 if r2 > r1 else -1
                                    dc = 1 if c2 > c1 else -1
                                    steps = abs(r1 - r2)
                                    can_draw = True
                                    for s in range(1, steps):
                                        curr = res[r1 + s*dr, c1 + s*dc]
                                        if curr != 0 and curr != beam_col:
                                            can_draw = False
                                            break
                                    if can_draw:
                                        for s in range(1, steps):
                                            res[r1 + s*dr, c1 + s*dc] = beam_col
                        return res
                    return ray_fn

                deduced.append(DeducedHypothesis(
                    "classical_prime", f"ray_geodesic_{src_c}_{beam_c}",
                    f"Classical Fermat Ray: Source {src_c} -> Beam {beam_c}",
                    make_ray_geodesic(src_c, beam_c), complexity=2.0
                ))

        # E. Kinematic Gravitational Advection (Downward, Upward, Lateral)
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

        if h_in == h_out and w_in == w_out:
            deduced.append(DeducedHypothesis(
                "classical_prime", "gravity_advection_down",
                "Classical Kinematics: Gravitational Mass Advection Downward",
                gravity_down, complexity=1.5
            ))
            deduced.append(DeducedHypothesis(
                "classical_prime", "gravity_advection_up",
                "Classical Kinematics: Gravitational Mass Advection Upward",
                gravity_up, complexity=1.5
            ))

            # F. Boundary-Anchored Relative Kinematics & Shear Advection (No-Slip Boundary + Differential Drift)
            shear_configs = [
                ("bottom_base", "right", "Fixed Bottom Base + Rightward Shear Drift", "bottom", 0, 1),
                ("bottom_base", "left", "Fixed Bottom Base + Leftward Shear Drift", "bottom", 0, -1),
                ("top_base", "right", "Fixed Top Base + Rightward Shear Drift", "top", 0, 1),
                ("top_base", "left", "Fixed Top Base + Leftward Shear Drift", "top", 0, -1),
                ("left_base", "down", "Fixed Left Base + Downward Shear Drift", "left", 1, 0),
                ("left_base", "up", "Fixed Left Base + Upward Shear Drift", "left", -1, 0),
                ("right_base", "down", "Fixed Right Base + Downward Shear Drift", "right", 1, 0),
                ("right_base", "up", "Fixed Right Base + Upward Shear Drift", "right", -1, 0),
            ]
            for tag, sdir, desc, anchor_type, dr, dc in shear_configs:
                def make_anchored_shear_op(atype=anchor_type, shift_r=dr, shift_c=dc):
                    def shear_fn(grid):
                        res = np.zeros_like(grid)
                        h, w = grid.shape
                        colors = [c for c in np.unique(grid) if c != 0]
                        for col in colors:
                            coords = np.argwhere(grid == col)
                            if len(coords) == 0:
                                continue
                            r_min, c_min = np.min(coords, axis=0)
                            r_max, c_max = np.max(coords, axis=0)
                            for r, c in coords:
                                is_anchored = False
                                if atype == "bottom":
                                    # Fixed base: bottom row or corner cell above bottom
                                    if r == r_max or (r == r_max - 1 and c == c_max):
                                        is_anchored = True
                                elif atype == "top":
                                    if r == r_min or (r == r_min + 1 and c == c_min):
                                        is_anchored = True
                                elif atype == "left":
                                    if c == c_min or (c == c_min + 1 and r == r_max):
                                        is_anchored = True
                                elif atype == "right":
                                    if c == c_max or (c == c_max - 1 and r == r_min):
                                        is_anchored = True

                                if is_anchored:
                                    res[r, c] = col
                                else:
                                    nr, nc = r + shift_r, c + shift_c
                                    if 0 <= nr < h and 0 <= nc < w:
                                        res[nr, nc] = col
                        return res
                    return shear_fn

                deduced.append(DeducedHypothesis(
                    "classical_prime", f"anchored_shear_{tag}_{sdir}",
                    f"Classical Kinematics: {desc}",
                    make_anchored_shear_op(anchor_type, dr, dc),
                    complexity=1.8
                ))

        return deduced

    # ═════════════════════════════════════════════════════════════════════════
    # 2. STRING-10D-TOPOLOGICAL DEDUCTIONS
    # ═════════════════════════════════════════════════════════════════════════
    @classmethod
    def _deduce_topological(cls, train_pairs, in_scenes, out_scenes) -> List[DeducedHypothesis]:
        deduced = []
        p0_in = train_pairs[0]["input"]
        p0_out = train_pairs[0]["output"]

        # A. Cavity / Internal Enclosure Hole-Filling
        # Check if objects have holes that are filled in output
        has_holes_in = any(len(o.holes) > 0 for s in in_scenes for o in s.objects)
        colors_out = set(np.unique(p0_out))

        if has_holes_in:
            for fill_c in [c for c in colors_out if c != 0]:
                def make_cavity_fill(target_color):
                    def fill_fn(grid):
                        res = grid.copy()
                        scene = PerceptualScene(grid)
                        for obj in scene.objects:
                            if obj.holes:
                                for hr, hc in obj.holes:
                                    res[hr, hc] = target_color
                        return res
                    return fill_fn

                deduced.append(DeducedHypothesis(
                    "string_meta", f"topological_cavity_fill_{fill_c}",
                    f"Topological Euler Invariant: Fill Internal Cavities with {fill_c}",
                    make_cavity_fill(fill_c), complexity=1.8
                ))

        # B. Invariant Component Filtering (Keep Largest / Smallest / Unique Color)
        def keep_largest_cc_bbox(grid):
            scene = PerceptualScene(grid)
            largest = scene.get_largest_object()
            if largest is None:
                return grid
            return largest.isolate()

        def keep_smallest_cc_bbox(grid):
            scene = PerceptualScene(grid)
            smallest = scene.get_smallest_object()
            if smallest is None:
                return grid
            return smallest.isolate()

        def keep_unique_color_bbox(grid):
            scene = PerceptualScene(grid)
            uniques = scene.get_unique_color_objects()
            if not uniques:
                return grid
            return uniques[0].isolate()

        deduced.append(DeducedHypothesis(
            "string_meta", "filter_largest_cc_bbox",
            "Topological Filter: Extract Largest Connected Component BBox",
            keep_largest_cc_bbox, complexity=1.6
        ))
        deduced.append(DeducedHypothesis(
            "string_meta", "filter_smallest_cc_bbox",
            "Topological Filter: Extract Smallest Connected Component BBox",
            keep_smallest_cc_bbox, complexity=1.6
        ))
        deduced.append(DeducedHypothesis(
            "string_meta", "filter_unique_color_bbox",
            "Topological Filter: Extract Unique Color Component BBox",
            keep_unique_color_bbox, complexity=1.6
        ))

        # C. Perimeter / Outer Boundary Extraction
        def extract_perimeter(grid):
            scene = PerceptualScene(grid)
            res = np.zeros_like(grid)
            for obj in scene.objects:
                for pr, pc in obj.perimeter:
                    res[pr, pc] = obj.color
            return res

        deduced.append(DeducedHypothesis(
            "string_meta", "topological_perimeter",
            "Topological Boundary: Isolate Outer Perimeters",
            extract_perimeter, complexity=1.7
        ))

        # D. Kronecker Self-Similar Fractal Expansion
        def kronecker_fractal(grid):
            mask = (grid != 0).astype(int)
            return np.kron(mask, grid)

        # E. Invariant 1x1 Decision: Color with Maximum Disconnected Components (Entropy / Dust Cloud)
        def max_components_dust(grid):
            scene = PerceptualScene(grid)
            counts = {}
            for o in scene.objects:
                counts[o.color] = counts.get(o.color, 0) + 1
            if not counts:
                return np.array([[0]], dtype=int)
            max_c = max(counts.keys(), key=lambda c: counts[c])
            return np.array([[max_c]], dtype=int)

        deduced.append(DeducedHypothesis(
            "string_meta", "topological_max_components_dust",
            "Topological Entropy: Color with Maximum Disconnected Components (Dust Cloud)",
            max_components_dust, complexity=1.4
        ))

        # F. Invariant 1x1 Decision: Color with Maximum Internal Cavities (Euler Genus / Holes)
        def max_cavities_genus(grid):
            scene = PerceptualScene(grid)
            cavities = {}
            for o in scene.objects:
                cavities[o.color] = cavities.get(o.color, 0) + len(o.holes)
            if not cavities or max(cavities.values()) == 0:
                return np.array([[0]], dtype=int)
            max_c = max(cavities.keys(), key=lambda c: cavities[c])
            return np.array([[max_c]], dtype=int)

        deduced.append(DeducedHypothesis(
            "string_meta", "topological_max_cavities_genus",
            "Topological Euler Invariant: Color with Maximum Internal Cavities (Holes)",
            max_cavities_genus, complexity=1.5
        ))

        # G. Solitary Unpaired Object Extraction (Particle-Antiparticle Annihilation)
        def solitary_unpaired_crop(grid):
            scene = PerceptualScene(grid)
            shape_groups = {}
            for o in scene.objects:
                key = (o.color, o.size, o.height, o.width, o.shape_signature)
                shape_groups.setdefault(key, []).append(o)
            unpaired = []
            for key, objs in shape_groups.items():
                if len(objs) % 2 == 1:
                    unpaired.extend(objs)
            if not unpaired:
                shape_only = {}
                for o in scene.objects:
                    key = (o.size, o.height, o.width, o.shape_signature)
                    shape_only.setdefault(key, []).append(o)
                for key, objs in shape_only.items():
                    if len(objs) % 2 == 1:
                        unpaired.extend(objs)
            if not unpaired:
                return grid
            min_r = min(o.bbox[0] for o in unpaired)
            min_c = min(o.bbox[1] for o in unpaired)
            max_r = max(o.bbox[2] for o in unpaired)
            max_c = max(o.bbox[3] for o in unpaired)
            return grid[min_r:max_r+1, min_c:max_c+1]

        deduced.append(DeducedHypothesis(
            "string_meta", "topological_solitary_unpaired_crop",
            "Topological Parity: Solitary Unpaired Object Isolation (Annihilation Invariant)",
            solitary_unpaired_crop, complexity=1.6
        ))

        return deduced

    # ═════════════════════════════════════════════════════════════════════════
    # 3. QUANTUM-SUPERPOSED DEDUCTIONS
    # ═════════════════════════════════════════════════════════════════════════
    @classmethod
    def _deduce_quantum(cls, train_pairs, in_scenes, out_scenes) -> List[DeducedHypothesis]:
        deduced = []

        # A. Direct Discrete State Permutation Cipher {c_in -> c_out}
        # Deduce consistent color mapping across all train pairs
        state_map: Dict[int, int] = {}
        is_consistent_cipher = True

        for pair in train_pairs:
            inp, out = pair["input"], pair["output"]
            if inp.shape != out.shape:
                is_consistent_cipher = False
                break
            for c_in, c_out in zip(inp.flat, out.flat):
                if c_in in state_map:
                    if state_map[c_in] != c_out:
                        is_consistent_cipher = False
                        break
                else:
                    state_map[c_in] = int(c_out)
            if not is_consistent_cipher:
                break

        if is_consistent_cipher and state_map:
            def make_cipher_op(mapping):
                def cipher_fn(grid):
                    res = grid.copy()
                    for k, v in mapping.items():
                        res[grid == k] = v
                    return res
                return cipher_fn

            deduced.append(DeducedHypothesis(
                "quantum_prime", f"quantum_cipher_{len(state_map)}states",
                f"Quantum Discrete State Permutation: {state_map}",
                make_cipher_op(state_map), complexity=1.1
            ))

        # B. Cluster Mass to State Mapping {Area -> Color}
        mass_map: Dict[int, int] = {}
        is_consistent_mass = True

        for pair in train_pairs:
            inp, out = pair["input"], pair["output"]
            if inp.shape != out.shape:
                is_consistent_mass = False
                break
            labeled, num_features = scipy.ndimage.label(inp != 0)
            for feat_idx in range(1, num_features + 1):
                mask = (labeled == feat_idx)
                area = int(np.sum(mask))
                out_colors = np.unique(out[mask])
                if len(out_colors) == 1:
                    c_out = int(out_colors[0])
                    if area in mass_map:
                        if mass_map[area] != c_out:
                            is_consistent_mass = False
                            break
                    else:
                        mass_map[area] = c_out
                else:
                    is_consistent_mass = False
                    break
            if not is_consistent_mass:
                break

        if is_consistent_mass and len(mass_map) >= 2:
            def make_mass_op(mapping):
                def mass_fn(grid):
                    res = grid.copy()
                    labeled, num_features = scipy.ndimage.label(grid != 0)
                    for feat_idx in range(1, num_features + 1):
                        mask = (labeled == feat_idx)
                        area = int(np.sum(mask))
                        if area in mapping:
                            res[mask] = mapping[area]
                    return res
                return mass_fn

            deduced.append(DeducedHypothesis(
                "quantum_prime", f"cluster_mass_mapping_{len(mass_map)}keys",
                f"Quantum Cluster Mass to State Mapping: {mass_map}",
                make_mass_op(mass_map), complexity=1.4
            ))

        return deduced

    # ═════════════════════════════════════════════════════════════════════════
    # 4. MODERN-THERMODYNAMIC INTERMEDIATE COMPOSITION (f ∘ g)
    # ═════════════════════════════════════════════════════════════════════════
    @classmethod
    def _deduce_thermodynamic_compositions(
        cls,
        train_pairs: List[Dict[str, np.ndarray]],
        single_hyps: List[DeducedHypothesis]
    ) -> List[DeducedHypothesis]:
        """
        Synthesizes 2-step compound laws:
        Applies T_1 to obtain intermediate state I', then dynamically deduces T_2 from (I', O).
        """
        composed: List[DeducedHypothesis] = []
        p0_in = train_pairs[0]["input"]
        p0_out = train_pairs[0]["output"]

        # Filter candidate T_1: spatial transformations (crop, scale, rotation, filter)
        # Exclude identity to prevent trivial self-compositions
        t1_candidates = [
            h for h in single_hyps
            if h.signature != "affine_ident" and (
                h.signature.startswith("affine_") or
                h.signature.startswith("deduced_bbox_") or
                h.signature.startswith("filter_") or
                h.signature.startswith("homothety_")
            )
        ]

        for t1 in t1_candidates:
            # Check if T_1 alone already matches (if so, no composition needed)
            matches_alone = True
            valid_intermediate = True
            intermediate_pairs = []

            for pair in train_pairs:
                inter = t1.apply(pair["input"])
                if inter is None or inter.shape != pair["output"].shape:
                    valid_intermediate = False
                    matches_alone = False
                    break
                intermediate_pairs.append({"input": inter, "output": pair["output"]})
                if not np.array_equal(inter, pair["output"]):
                    matches_alone = False

            if matches_alone or not valid_intermediate:
                continue

            # Intermediate state I' matches output dimensions!
            # Dynamically deduce T_2 directly from (I', O)
            t2_candidates = []

            # 1. Check if T_2 is a D4 symmetry of the intermediate state
            inter0 = intermediate_pairs[0]["input"]
            out0 = intermediate_pairs[0]["output"]
            for d_name, d_desc, d_op in [
                ("rot90", "90-degree Rotation", lambda x: np.rot90(x, 1)),
                ("rot180", "180-degree Rotation", lambda x: np.rot90(x, 2)),
                ("rot270", "270-degree Rotation", lambda x: np.rot90(x, 3)),
                ("fliph", "Horizontal Reflection", lambda x: np.fliplr(x)),
                ("flipv", "Vertical Reflection", lambda x: np.flipud(x)),
            ]:
                if np.array_equal(d_op(inter0), out0):
                    t2_candidates.append(DeducedHypothesis(
                        "classical_prime", f"d4_{d_name}", d_desc, d_op
                    ))

            # 2. Check if T_2 is a color permutation cipher of intermediate state
            cipher_map = {}
            valid_cipher = True
            for ip in intermediate_pairs:
                for c_in, c_out in zip(ip["input"].flat, ip["output"].flat):
                    if c_in in cipher_map:
                        if cipher_map[c_in] != c_out:
                            valid_cipher = False
                            break
                    else:
                        cipher_map[c_in] = int(c_out)
                if not valid_cipher:
                    break

            if valid_cipher and cipher_map and any(k != v for k, v in cipher_map.items()):
                def make_cipher_fn(mapping):
                    def c_fn(grid):
                        res = grid.copy()
                        for k, v in mapping.items():
                            res[grid == k] = v
                        return res
                    return c_fn

                t2_candidates.append(DeducedHypothesis(
                    "quantum_prime", f"cipher_{len(cipher_map)}c",
                    f"Color Cipher {cipher_map}", make_cipher_fn(cipher_map)
                ))

            # Assemble compound hypotheses (T_2 ∘ T_1)
            for t2 in t2_candidates:
                def make_comp(op1, op2):
                    def comp_fn(grid):
                        i1 = op1.apply(grid)
                        if i1 is None:
                            return None
                        return op2.apply(i1)
                    return comp_fn

                composed.append(DeducedHypothesis(
                    "modern_prime",
                    f"composite_{t1.signature}_THEN_{t2.signature}",
                    f"Modern Thermodynamic 2-Step Law: [{t1.description}] -> [{t2.description}]",
                    make_comp(t1, t2),
                    complexity=t1.complexity + t2.complexity
                ))

        return composed
