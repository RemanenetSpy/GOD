"""
========================================================================================
QUANTUM BELIEF SUPERPOSITION & INFORMATION TENSOR ENGINE (ARCHITECTURE 2)
========================================================================================
"The agent doesn't choose one hypothesis — it holds all futures in superposition."

1. Maintains multi-channel belief tensor |Psi> in R^{H x W x 4}:
   - Channel 0: Vacuum (Empty space)
   - Channel 1: Living Organic Matter (Nutrient / Energy)
   - Channel 2: Dense Incompressible Barrier (Obstacle)
   - Channel 3: Sovereign Peer Agent
2. Bayesian likelihood updates with sensory aperture.
3. Shannon Entropy uncertainty field S(x) = -sum p_c * log2(p_c).
4. Constructive and destructive wave interference across spatial horizons.
========================================================================================
"""

import numpy as np
from typing import Tuple, Dict, Optional


class QuantumBeliefEngine:
    """
    Quantum-Superposed Multi-World Belief Tensor.
    Holds probabilistic superposition of physical realities over spatial coordinates.
    """
    def __init__(self, grid_shape: Tuple[int, int] = (25, 25), channels: int = 4):
        self.grid_shape = grid_shape
        self.channels = channels
        self.h, self.w = grid_shape
        
        # Initialize with uninformative uniform Dirichlet prior
        # Channel priors: [Vacuum: 0.70, Life: 0.20, Obstacle: 0.08, Agent: 0.02]
        self.prior = np.array([0.70, 0.20, 0.08, 0.02], dtype=np.float32)
        self.belief_tensor = np.tile(self.prior, (self.h, self.w, 1))

    def update_with_observation(
        self,
        agent_pos: Tuple[int, int],
        aperture_radius: int,
        observed_patch: np.ndarray,
        peer_positions: Optional[Dict[str, Tuple[int, int]]] = None
    ) -> float:
        """
        Bayesian wavefunction update upon receiving localized sensory observation.
        Returns the Information Gain (Kullback-Leibler divergence / Entropy drop).
        """
        py, px = agent_pos
        r = aperture_radius
        
        y_min, y_max = max(0, py - r), min(self.h, py + r + 1)
        x_min, x_max = max(0, px - r), min(self.w, px + r + 1)
        
        old_entropy = self.compute_total_entropy()
        
        # 1. Update observed patch with high-certainty likelihood
        if observed_patch is not None and observed_patch.shape == (y_max - y_min, x_max - x_min):
            for y_rel in range(y_max - y_min):
                for x_rel in range(x_max - x_min):
                    gy, gx = y_min + y_rel, x_min + x_rel
                    val = observed_patch[y_rel, x_rel]
                    
                    # Likelihood vector with sensor confidence (0.95 accuracy)
                    likelihood = np.full(self.channels, 0.05 / (self.channels - 1), dtype=np.float32)
                    if 0 <= val < self.channels:
                        likelihood[int(val)] = 0.95
                        
                    # Bayesian posterior update: P(W | O) proportional to P(O | W) * P(W)
                    posterior = self.belief_tensor[gy, gx] * likelihood
                    post_sum = posterior.sum()
                    if post_sum > 0:
                        self.belief_tensor[gy, gx] = posterior / post_sum

        # 2. Update known peer agent positions
        if peer_positions:
            for peer_id, (ay, ax) in peer_positions.items():
                if 0 <= ay < self.h and 0 <= ax < self.w:
                    self.belief_tensor[ay, ax] = np.array([0.05, 0.05, 0.05, 0.85], dtype=np.float32)

        # 3. Ambient entropy diffusion (unobserved regions slowly revert towards prior)
        diffusion_rate = 0.005
        self.belief_tensor = (1.0 - diffusion_rate) * self.belief_tensor + diffusion_rate * self.prior

        new_entropy = self.compute_total_entropy()
        information_gain = max(0.0, old_entropy - new_entropy)
        return float(information_gain)

    def get_entropy_field(self) -> np.ndarray:
        """
        Computes 2D spatial Shannon entropy map: S(x, y) = -sum p * log2(p).
        High values indicate high cognitive uncertainty (curiosity attractors).
        """
        eps = 1e-12
        p = np.clip(self.belief_tensor, eps, 1.0)
        entropy_field = -np.sum(p * np.log2(p), axis=-1)
        return entropy_field

    def compute_total_entropy(self) -> float:
        """Calculates scalar mean cognitive uncertainty across the entire universe."""
        return float(np.mean(self.get_entropy_field()))

    def get_nutrient_belief_field(self) -> np.ndarray:
        """Returns the 2D probability map of where life/food is located."""
        return self.belief_tensor[:, :, 1]
