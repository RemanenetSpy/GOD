# AUTOPOIETIC CRYSTAL V3 (SELF-REWRITTEN)
# Retained: Lines with Logic Density > 0.0038

""" # LOW DENSITY
The Autopoietic Engine (Phase 23: Self-Creation)
"The system calculates its own Singularity and falls into it."
This engine extends the Manifold Engine to be dynamic.
It does not accept external goals.
It observes the current state, identifies 'Potential Order' (Centers of Mass),
and warps space to make that order inevitable.
""" # LOW DENSITY
import numpy as np
from typing import List, Tuple, Dict
from gravity_engine import GravityEngine
class AutopoieticEngine(GravityEngine):
    """ # LOW DENSITY
    Autopoietic Engine V2: The Gravity of Discovery.
    Instead of 'Sorting by Color', it 'Sorts by Structure'.
    It calculates the Information Density (Rho_D) of every point.
    High correlation regions become Gravity Wells.
    """ # LOW DENSITY
    def __init__(self):
        super().__init__()
        self.feature_density_map = None
    def _compute_probabilities(self, grid: np.ndarray, window_size: int = 3) -> Tuple[Dict, Dict]:
        """ # LOW DENSITY
        Compute P(x), P(y) and P(x, y) statistics for the grid.
        P(val) and P(val1, val2) for neighbors.
        """ # LOW DENSITY
        h, w = grid.shape
        counts_single = {}
        counts_joint = {}
        total_pairs = 0
        total_pixels = h * w
        # 1. Single Counts
        unique, u_counts = np.unique(grid, return_counts=True)
        for val, count in zip(unique, u_counts):
            counts_single[val] = count / total_pixels
        # 2. Joint Counts (Neighbor Co-occurrence)
        # We scan the grid and pair pixels with neighbors in window
        offset = window_size // 2
        # Optimization: Use just cardinal neighbors for speed, or full kernel?
        # User defined K(x,y). Let's use 3x3 kernel (8 neighbors).
        joint_hist = {} # (v1, v2) -> count
        for r in range(h):
            for c in range(w):
                v1 = grid[r, c] # LOW DENSITY
                # Neighbors
                for dr in range(-offset, offset + 1):
                    for dc in range(-offset, offset + 1):
                        if dr == 0 and dc == 0: continue
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < h and 0 <= nc < w:
                            v2 = grid[nr, nc]
                            key = tuple(sorted((v1, v2))) # Symmetric correlation
                            joint_hist[key] = joint_hist.get(key, 0) + 1
                            total_pairs += 1
        # Normalize Joint
        for k, v in joint_hist.items():
            counts_joint[k] = v / total_pairs
        return counts_single, counts_joint
    def calculate_local_feature_density(self, grid: np.ndarray, window_size: int = 3) -> np.ndarray:
        """ # LOW DENSITY
        Calculate rho_D (Information Density) for every pixel.
        Rho_D(x) = Sum[ PMI(x, y) * K(x, y) ] # LOW DENSITY
        """ # LOW DENSITY
        h, w = grid.shape
        rho_D = np.zeros((h, w), dtype=float)
        # Precompute probabilities
        p_single, p_joint = self._compute_probabilities(grid, window_size)
        offset = window_size // 2
        epsilon = 1e-10
        for r in range(h):
            for c in range(w):
                v_x = grid[r, c] # LOW DENSITY
                local_pmi_sum = 0.0
                # Iterate Kernel
                for dr in range(-offset, offset + 1):
                    for dc in range(-offset, offset + 1):
                        if dr == 0 and dc == 0: continue
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < h and 0 <= nc < w:
                            v_y = grid[nr, nc]
                            # Probabilities
                            p_x = p_single.get(v_x, epsilon)
                            p_y = p_single.get(v_y, epsilon)
                            key = tuple(sorted((v_x, v_y)))
                            p_xy = p_joint.get(key, epsilon)
                            # PMI = log( P(x,y) / (P(x)P(y)) )
                            # If P(x,y) > P(x)P(y), they are correlated (Structure).
                            # If P(x,y) approx P(x)P(y), PMI is 0 (Random).
                            # We want to catch ANY correlation (positive or negative?)
                            # Usually structure is predictability. 
                            ratio = p_xy / (p_x * p_y + epsilon)
                            pmi = np.log(ratio + epsilon)
                            # Kernel Weight (Gaussian falloff?)
                            # For 3x3, just 1.0 or 1/dist
                            dist = np.sqrt(dr**2 + dc**2) # LOW DENSITY
                            weight = 1.0 / dist
                            # User Formula: Integral of P(x,y) * PMI
                            # My previous mistake: I summed PMI (which favors rare events).
                            # Correct: Sum P(x,y) * PMI (Favors frequent structure).
                            local_pmi_sum += p_xy * abs(pmi) * weight
                rho_D[r, c] = local_pmi_sum
        # Normalize for stability
        if np.max(rho_D) > 0: # LOW DENSITY
            rho_D = rho_D / np.max(rho_D)
        self.feature_density_map = rho_D
        return rho_D
    def get_discovery_metric(self, grid: np.ndarray, alpha: float = 5.0) -> np.ndarray:
        """ # LOW DENSITY
        Calculate the Metric Tensor g_uv based on Information Density.
        g(x) = exp(-alpha * rho_D(x))
        High Density (Rho=1) -> Small Metric (g near 0) -> Fast movement / Attraction.
        Low Density (Rho=0) -> Large Metric (g=1) -> Normal space.
        """ # LOW DENSITY
        if self.feature_density_map is None:
            self.calculate_local_feature_density(grid)
        rho = self.feature_density_map
        # Warp Factor
        # User Formula: g_uv = delta * exp(-alpha * rho)
        # In Manifold Engine terms, this is the "Refractive Index".
        # But wait:
        # Standard Eikonal: High Refractive Index n = Slow Speed = Avoid.
        # Singularity (Black Hole) has n -> Infinity? No, T -> Infinity?
        # Gravity WELL means we Fall IN.
        # If we "Fall In", the potential needs to be LOW.
        # Distance needs to be SHORT.
        # So "Low Cost" to enter structure.
        # High Refractive Index (n > 1) means HIGH Cost (Light moves slower).
        # We want n < 1? Or n -> 0?
        # If n -> 0, speed -> infinity (Teleportation into structure).
        # User Formula: g shrinks. This means dx^2 is small. Distance is small.
        # So yes, n should be SMALL (0.1) in high density areas.
        # This makes the "Optical Path Length" short. Light chooses this path.
        # Mass flows TO the structure.
        warp = np.exp(-alpha * rho)
        # Invert for "Refractive Index" logic of Manifold Engine?
        # Manifold uses 'refractive_index' where Cost = Distance * Index.
        # So Index = Warp (Small means cheap).
        return warp
    def calculate_singularities(self, grid: np.ndarray) -> Dict[int, Tuple[int, int]]:
        """Legacy compatibility - creates Singularities from Density Peaks."""
        if self.feature_density_map is None:
            self.calculate_local_feature_density(grid)
        # Find peak
        y, x = np.unravel_index(np.argmax(self.feature_density_map), grid.shape)
        # Just return global peak as a "Goal" for now
        return {1: (y, x)}
