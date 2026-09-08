"""
Universal Metric (The Law)
Phase 10: Sovereign Gravity Protocol

Property of the Universe, not the Agent.
Defines how "Information Mass" creates "Curvature" (Potential).
"""

import numpy as np
from typing import Any, Tuple, List

class UniversalMetric:
    """
    The Metric Tensor (G) and Field Solver.
    """
    
    def __init__(self):
        self.planck_constant = 1e-6 # Minimum limit for physics
        
    def measure_mass(self, state: np.ndarray, target: np.ndarray) -> Tuple[float, float, float]:
        """
        Calculate the Information Mass components.
        
        Args:
            state: Current state (Grid)
            target: Target state (Expected Output)
            
        Returns:
            (Divergence, Entropy, Density)
        """
        # 1. Divergence (External Error mass)
        # In ARC, this is pixel difference. In Robot, Euclidean distance.
        if state.shape != target.shape:
             # Shape mismatch is massive error (infinite mass)
             divergence = float(state.size + target.size)
        else:
             divergence = float(np.sum(state != target))
             
        # 2. Entropy (Internal Complexity mass)
        # Shannon entropy of the grid
        _, counts = np.unique(state, return_counts=True)
        probs = counts / state.size
        entropy = -np.sum(probs * np.log2(probs + self.planck_constant))
        
        # 3. Density (Information Density)
        # Ratio of non-background pixels to total area
        # Assuming 0 is background (Void)
        mass_pixels = np.sum(state != 0)
        density = mass_pixels / max(1, state.size)
        
        return divergence, entropy, density
    
    def calculate_coupling_constant(self, density: float) -> float:
        """
        Calculate Dynamic Lambda (λ).
        
        High Density (Complex/Chaos) -> Low λ (Trust Data / Accuracy)
        Low Density (Sparse/Order) -> High λ (Trust Law / Simplicity)
        """
        # Linear approximation: λ = 1 - Density
        # If density is 0 (Empty), λ is 1 (Maximize Simplicity)
        # If density is 1 (Full), λ is 0 (Maximize Accuracy)
        return max(0.1, 1.0 - density)
        
    def calculate_potential(self, state: np.ndarray, target: np.ndarray) -> float:
        """
        The Scalar Potential Field (Φ).
        Φ = Divergence + λ * Entropy
        """
        div, ent, density = self.measure_mass(state, target)
        lambda_val = self.calculate_coupling_constant(density)
        
        # The equation: Potential Energy of the system
        potential = div + (lambda_val * ent)
        
        return potential

    def calculate_gradient(self, current_potential: float, next_potential: float) -> float:
        """
        Calculate the gradient (Slope) between two states.
        ∇ = ΔΦ / Δx (where Δx is 1 'step' or transformation unit)
        """
        return next_potential - current_potential

    # Phase 11: FLUID DYNAMICS (Variational Inference)
    
    def measure_mass_fluid(self, soft_state: np.ndarray, target: np.ndarray) -> float:
        """
        Calculate Potential Φ for a Fluid Field (Probability Distribution).
        
        Args:
            soft_state: [H, W, 10] array of probabilities (sum=1 per pixel)
            target: [H, W] discrete grid of integers (The Truth)
            
        Returns:
            Scalar Potential (Cross-Entropy Loss)
        """
        # 1. Divergence (Cross-Entropy)
        # We want the probability of the True Class to be 1.0.
        # Loss = -log(p_target)
        
        # Safe log
        epsilon = 1e-9
        clipped_probs = np.clip(soft_state, epsilon, 1.0)
        
        # Create one-hot target
        h, w = target.shape
        target_one_hot = np.zeros((h, w, 10))
        # Use fancy indexing
        rows, cols = np.indices((h, w))
        target_one_hot[rows, cols, target] = 1.0
        
        # Calculate Cross Entropy: -Sum(target * log(prob))
        # Since target is one-hot, this picks the log-prob of the correct color.
        cross_entropy = -np.sum(target_one_hot * np.log(clipped_probs))
        
        # 2. Entropy (Uncertainty) - Optional Regularizer
        # We want the fluid to crystallize (Low Entropy).
        # But during flow, High Entropy might help tunnel. 
        # For now, Cross-Entropy drives prediction enough.
        
        return cross_entropy

    def calculate_gradient_fluid(self, soft_state: np.ndarray, target: np.ndarray) -> np.ndarray:
        """
        Analytical Gradient of the Potential field w.r.t the Fluid State.
        ∇Φ = d(CrossEntropy)/dP = -Target / P
        
        Returns:
             Gradient Tensor [H, W, 10] pointing towards higher Potential 
             (We descend, so we assume step = -learning_rate * grad)
        """
        epsilon = 1e-9
        clipped_probs = np.clip(soft_state, epsilon, 1.0)
        
        h, w = target.shape
        target_one_hot = np.zeros((h, w, 10))
        rows, cols = np.indices((h, w))
        target_one_hot[rows, cols, target] = 1.0
        
        # d(-log P) = -1/P. 
        # So Gradient = -Target / P
        # If Target is 0, grad is 0 (doesn't pull).
        # If Target is 1, grad is -1/P (Large negative pull if P is small -> Descent!)
        
        gradient = -target_one_hot / clipped_probs
        return gradient

    # Phase 13: ELASTIC SPACETIME (Dimensional Evaporation)
    
    def measure_mass_profile(self, state: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Analyze the distribution of Information Mass across dimensions.
        Used to detect Vacuum (Evaporation) or Pressure (Inflation).
        
        Args:
            state: [H, W] discrete grid OR [H, W, C] fluid tensor.
            
        Returns:
            (row_mass: [H], col_mass: [W]) - Normalized Mass per slice.
        """
        # Handle Fluid vs Solid
        if state.ndim == 3:
            # Fluid: Mass is Entropy/Density profile
            # High Entropy = High Activity (Mass)
            # Low Entropy (near 0 or 1) = Crystallized Mass?
            # Actually, "Vacuum" is state 0 (Background).
            # So Mass = sum(P_non_zero).
            
            # Sum prob of all non-zero classes
            # state is [H, W, 10]
            mass_map = np.sum(state[:, :, 1:], axis=2) # 1..9
        else:
            # Solid: Mass = non-zero pixels
            mass_map = (state != 0).astype(float)
            
        row_mass = np.sum(mass_map, axis=1)
        col_mass = np.sum(mass_map, axis=0)
        
        return row_mass, col_mass

    # Phase 15: THE HOLOGRAPHIC PRINCIPLE (Blind Solving)
    
    def measure_global_resonance(self, train_pairs: List[Tuple[np.ndarray, np.ndarray]], 
                               test_input: np.ndarray, 
                               test_guess: np.ndarray) -> float:
        """
        Measure the Global Entropy of the Task.
        How strictly does (test_input -> test_guess) follow the laws of (train_input -> train_output)?
        For Blind Solving (Evaluation Set).
        """
        # 1. Mass Conservation Ratio (R = Out/In)
        train_ratios = []
        for inp, out in train_pairs:
             m_in = np.sum(inp != 0) + 1e-9
             m_out = np.sum(out != 0) + 1e-9
             train_ratios.append(m_out / m_in)
             
        avg_train_ratio = np.mean(train_ratios)
        
        # Test Ratio
        m_test_in = np.sum(test_input != 0) + 1e-9
        
        if test_guess.ndim == 3:
             # Fluid
             guess_solid = np.argmax(test_guess, axis=2)
             m_test_out = np.sum(guess_solid != 0) + 1e-9
        else:
             m_test_out = np.sum(test_guess != 0) + 1e-9
             
        test_ratio = m_test_out / m_test_in
        
        # Penalize Deviation (Mass Potential)
        dissonance = abs(test_ratio - avg_train_ratio) * 10.0
        
        # 2. Color Palette Consistency
        train_out_palettes = [set(np.unique(out)) for _, out in train_pairs]
        super_palette = set()
        for p in train_out_palettes: super_palette.update(p)
        
        if test_guess.ndim != 3:
            test_colors = set(np.unique(test_guess))
            # Allowed: Super Palette OR Input Colors
            input_colors = set(np.unique(test_input))
            allowed = super_palette.union(input_colors)
            
            diff = test_colors - allowed
            if diff:
                 dissonance += len(diff) * 50.0

        return dissonance
