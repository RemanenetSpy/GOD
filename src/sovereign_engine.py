"""
Universal Sovereign Entropy Engine

Domain-independent implementation of the Sovereign Entropy Engine.
Measures Σ, Ω, Λ using universal information-theoretic principles.
"""

import numpy as np
from typing import Any, Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum
from collections import deque





@dataclass
class EngineState:
    """Complete state of Sovereign Entropy Engine"""
    # Core Variables (The Trinity)
    sigma: float = 1.0       # Σ - Filter Efficiency (signal/noise discrimination)
    omega: float = 0.0       # Ω - Entropy (available chaos in environment)
    lambda_: float = 0.1     # Λ - Friction (systemic resistance)
    
    # Learning Parameters
    eta: float = 0.05        # η - Learning rate
    kappa: float = 1.0       # κ - Pattern recognition capability
    alpha: float = 0.1       # α - Adaptation rate
    
    # State Tracking
    initial_entropy: float = 0.0
    current_entropy: float = 0.0
    
    # History (for universal measurement)
    extraction_history: List[float] = field(default_factory=list)
    observation_history: deque = field(default_factory=lambda: deque(maxlen=100))
    action_history: deque = field(default_factory=lambda: deque(maxlen=100))
    reward_history: deque = field(default_factory=lambda: deque(maxlen=100))


from entropy_engine import EntropyEngine, PrescriptiveAction

class UniversalSovereignEngine(EntropyEngine):
    """
    Universal Sovereign Entropy Engine.
    
    Measures Σ, Ω, Λ using domain-independent information theory:
    - Ω: Shannon entropy of observation stream
    - Σ: Mutual information between actions and rewards
    - Λ: Inverse of reward rate (resistance to progress)
    """
    
    def __init__(self):
        self.state = EngineState()
        self.prescriptive_history: List[Tuple[float, PrescriptiveAction]] = []
        
    def update(self, observation: Any, action: Any, reward: float) -> PrescriptiveAction:
        """
        Complete autonomous update cycle.
        """
        # Measure environment
        self.measure_omega_universal(observation)
        self.measure_sigma_universal(action, reward)
        self.measure_lambda_universal()
        
        # Evolve
        gradient = self.compute_efficiency_gradient_universal()
        self.evolve_filter(gradient)
        
        # Prescribe
        return self.prescribe_action()
        
    # ============================================
    # I. DESCRIPTIVE PHYSICS (4 Equations)
    # ============================================
    
    def compute_metabolism(self) -> float:
        """
        Equation 1: dH/dt = (Σ × Ω) - Λ
        
        Returns: Rate of extraction (Salt per moment)
        Law: If negative, system is dying
        """
        dH_dt = (self.state.sigma * self.state.omega) - self.state.lambda_
        self.state.extraction_history.append(dH_dt)
        return dH_dt
    
    def compute_success_limit(self) -> float:
        """
        Equation 2: Success = lim[t→∞] [η × Σ(Waste_i × κ)] - Λ
        
        Returns: Long-term success accumulation
        Uses recent extraction history as waste streams
        """
        if not self.state.extraction_history:
            return -self.state.lambda_
        
        # Use recent extractions as "waste streams"
        recent_waste = self.state.extraction_history[-20:]
        pattern_sum = sum(abs(w) * self.state.kappa for w in recent_waste)
        
        success = (self.state.eta * pattern_sum) - self.state.lambda_
        return success
    
    def evolve_filter(self, efficiency_gradient: float):
        """
        Equation 3: Σ(t+1) = Σ(t) + α × ∇(Efficiency)
        
        Modifies: self.state.sigma
        Law: Filter rewrites itself based on efficiency
        """
        delta_sigma = self.state.alpha * efficiency_gradient
        self.state.sigma += delta_sigma
        
        # Bounds: Σ must be positive
        self.state.sigma = max(0.01, min(100.0, self.state.sigma))
        
        return delta_sigma
    
    def compute_extinction(self) -> float:
        """
        Equation 4: Ex = Initial_Entropy - Final_State
        
        Returns: Extinction metric (0 = problem solved)
        Law: True success is extinction of problem
        """
        ex = self.state.initial_entropy - self.state.current_entropy
        return ex
    
    # ============================================
    # II. UNIVERSAL MEASUREMENT (Domain-Independent)
    # ============================================
    
    def measure_omega_universal(self, observation: Any) -> float:
        """
        Universal Ω measurement using Shannon Entropy.
        
        Ω = Entropy of observation stream
        - High Ω: Many unique/unpredictable observations
        - Low Ω: Repetitive/predictable observations
        """
        # Convert observation to hashable representation
        obs_hash = self._hash_observation(observation)
        self.state.observation_history.append(obs_hash)
        
        if len(self.state.observation_history) < 2:
            self.state.omega = 1.0
            return 1.0
        
        # Compute Shannon entropy of observation distribution
        unique, counts = np.unique(list(self.state.observation_history), return_counts=True)
        probabilities = counts / len(self.state.observation_history)
        
        # Shannon entropy: -Σ(p * log(p))
        omega = -np.sum(probabilities * np.log2(probabilities + 1e-10))
        
        # Normalize to reasonable range
        omega = max(0.1, min(10.0, omega))
        
        self.state.omega = omega
        
        # Track initial entropy for extinction
        if self.state.initial_entropy == 0.0:
            self.state.initial_entropy = omega
        self.state.current_entropy = omega
        
        return omega
    
    def measure_sigma_universal(self, action: Any, reward: float) -> float:
        """
        Universal Σ measurement using Mutual Information.
        
        Σ = I(Actions; Rewards) = How well actions predict rewards
        - High Σ: Actions reliably produce expected rewards (good filter)
        - Low Σ: Actions don't predict rewards (poor filter)
        """
        # Store action and reward
        action_hash = self._hash_observation(action)
        self.state.action_history.append(action_hash)
        self.state.reward_history.append(reward)
        
        if len(self.state.action_history) < 10:
            # Not enough data yet
            return self.state.sigma
        
        # Compute mutual information between actions and rewards
        # Discretize rewards into bins
        rewards = np.array(list(self.state.reward_history))
        reward_bins = np.percentile(rewards, [0, 33, 67, 100])
        reward_discrete = np.digitize(rewards, reward_bins)
        
        # Count joint occurrences
        actions = list(self.state.action_history)
        unique_actions = list(set(actions))
        
        # Compute I(A;R) = H(R) - H(R|A)
        h_r = self._entropy(reward_discrete)
        
        h_r_given_a = 0.0
        for action in unique_actions:
            # Get rewards for this action
            action_indices = [i for i, a in enumerate(actions) if a == action]
            if not action_indices:
                continue
            
            action_rewards = reward_discrete[action_indices]
            p_action = len(action_indices) / len(actions)
            h_r_given_a += p_action * self._entropy(action_rewards)
        
        mutual_info = h_r - h_r_given_a
        
        # Map to Σ range (0.1 to 10)
        sigma = 0.1 + (mutual_info * 2.0)
        sigma = max(0.1, min(10.0, sigma))
        
        self.state.sigma = sigma
        return sigma
    
    def measure_lambda_universal(self) -> float:
        """
        Universal Λ measurement using Reward Rate.
        
        Λ = Inverse of reward accumulation rate
        - High Λ: Low/negative rewards (high friction)
        - Low Λ: High positive rewards (low friction)
        """
        if len(self.state.reward_history) < 2:
            return self.state.lambda_
        
        # Compute recent reward rate
        recent_rewards = list(self.state.reward_history)[-20:]
        avg_reward = np.mean(recent_rewards)
        
        # Map reward to friction (inverse relationship)
        # Positive rewards → low friction
        # Negative rewards → high friction
        if avg_reward > 0:
            lambda_ = 1.0 / (avg_reward + 1.0)
        else:
            lambda_ = abs(avg_reward) + 1.0
        
        # Bounds
        lambda_ = max(0.01, min(10.0, lambda_))
        
        self.state.lambda_ = lambda_
        return lambda_
    
    def compute_efficiency_gradient_universal(self) -> float:
        """
        Universal ∇(Efficiency) using recent metabolism trend.
        
        ∇(Efficiency) = Change in dH/dt over time
        """
        if len(self.state.extraction_history) < 10:
            return 0.0
        
        # Compare recent vs older metabolism
        recent = np.mean(self.state.extraction_history[-5:])
        older = np.mean(self.state.extraction_history[-10:-5])
        
        gradient = recent - older
        return gradient
    
    # ============================================
    # III. PRESCRIPTIVE LOGIC (Decision Table)
    # ============================================
    
    def diagnose_state(self) -> Tuple[str, PrescriptiveAction]:
        """
        Implements complete prescriptive table.
        
        Returns: (diagnostic_label, prescribed_action)
        """
        sigma = self.state.sigma
        omega = self.state.omega
        lambda_ = self.state.lambda_
        
        # Condition 1: Λ > (Σ × Ω) - System Choked
        if lambda_ > (sigma * omega):
            return ("System Choked", PrescriptiveAction.BREACH)
        
        # Condition 2: Ω >> Σ - System Flooded
        if omega > 3 * sigma:  # Using 3x as threshold
            return ("System Flooded", PrescriptiveAction.REFINERY)
        
        # Condition 3: Σ >> Ω - System Starved
        if sigma > 3 * omega:
            return ("System Starved", PrescriptiveAction.INJECTION)
        
        # Condition 4: Ex ≈ 0 - System Solved
        ex = self.compute_extinction()
        if abs(ex) < 0.1:
            return ("System Solved", PrescriptiveAction.DISSOLVE)
        
        # Default: Normal operation
        return ("System Viable", PrescriptiveAction.CONTINUE)
    
    def prescribe_action(self) -> PrescriptiveAction:
        """
        Returns the optimal prescriptive action based on current state.
        """
        diagnostic, action = self.diagnose_state()
        
        # Log action
        metabolism = self.compute_metabolism()
        self.prescriptive_history.append((metabolism, action))
        
        return action
    
    # ============================================
    # IV. SYSTEM METRICS
    # ============================================
    
    def compute_viability_ratio(self) -> float:
        """
        Rv = (Σ × Ω) / Λ
        
        Returns: System health metric
        - Rv > 1: System is viable (extracting more than friction)
        - Rv < 1: System is dying
        """
        if self.state.lambda_ < 0.001:
            return float('inf')
        
        rv = (self.state.sigma * self.state.omega) / self.state.lambda_
        return rv
    
    def get_dashboard(self) -> dict:
        """
        Returns complete dashboard state for visualization.
        """
        metabolism = self.compute_metabolism()
        viability_ratio = self.compute_viability_ratio()
        success_limit = self.compute_success_limit()
        diagnostic, prescription = self.diagnose_state()
        
        return {
            'Σ (Sigma)': f'{self.state.sigma:.3f}',
            'Ω (Omega)': f'{self.state.omega:.3f}',
            'Λ (Lambda)': f'{self.state.lambda_:.3f}',
            'dH/dt': f'{metabolism:.3f}',
            'Rv': f'{viability_ratio:.3f}',
            'Success Limit': f'{success_limit:.3f}',
            'η': f'{self.state.eta:.3f}',
            'κ': f'{self.state.kappa:.3f}',
            'α': f'{self.state.alpha:.3f}',
            'Diagnosis': diagnostic,
            'Prescription': prescription.name,
            'Steps': len(self.state.observation_history)
        }

    # ===========================================
    # INFORMATION-THEORETIC NAVIGATION
    # ===========================================
    
    def navigate_via_information(self,
                                current_pos: Tuple[int, int],
                                uncertainty_map: np.ndarray,
                                visit_history: Dict[Tuple[int, int], int],
                                valid_neighbors: List[Tuple[int, int, int]]) -> int:
        """
        Information-theoretic navigation using Σ, Ω, Λ.
        
        Strategy:
        1. Maximize Λ (novelty): Seek unexplored regions
        2. Maximize Ω (coherence): Build consistent world model
        3. Maximize Σ (synthesis): Integrate observations efficiently
        """
        x, y = current_pos
        best_action = 4  # WAIT
        best_info_gain = -float('inf')
        
        h, w = uncertainty_map.shape
        
        for action_idx, nx, ny in valid_neighbors:
            # 1. Uncertainty reduction (Ω component)
            current_uncertainty = uncertainty_map[x, y] if 0 <= x < h and 0 <= y < w else 1.0
            next_uncertainty = uncertainty_map[nx, ny] if 0 <= nx < h and 0 <= ny < w else 1.0
            uncertainty_gain = next_uncertainty - current_uncertainty
            
            # 2. Novelty (Λ component)
            visit_count = visit_history.get((nx, ny), 0)
            novelty = 1.0 / (1.0 + visit_count)
            
            # 3. Combined metric (information gain)
            # Weight novelty higher (exploration-driven)
            info_gain = 0.3 * uncertainty_gain + 0.7 * novelty
            
            if info_gain > best_info_gain:
                best_info_gain = info_gain
                best_action = action_idx
        
        return best_action
    
    # ============================================
    # V. AUTONOMOUS UPDATE CYCLE
    # ============================================
    

    
    # ============================================
    # VI. UTILITY FUNCTIONS
    # ============================================
    
    def _hash_observation(self, obs: Any) -> int:
        """Convert any observation to hashable representation"""
        if isinstance(obs, np.ndarray):
            return hash(obs.tobytes())
        elif isinstance(obs, (list, tuple)):
            return hash(str(obs))
        else:
            return hash(str(obs))
    
    def _entropy(self, data: np.ndarray) -> float:
        """Compute Shannon entropy of discrete data"""
        unique, counts = np.unique(data, return_counts=True)
        probabilities = counts / len(data)
        return -np.sum(probabilities * np.log2(probabilities + 1e-10))
    
    def reset(self):
        """Reset engine state"""
        self.state = EngineState()
        self.prescriptive_history = []


# ============================================
# VII. EXAMPLE USAGE
# ============================================

if __name__ == "__main__":
    # Universal engine works with ANY domain
    engine = UniversalSovereignEngine()
    
    # Simulate arbitrary observation-action-reward stream
    for step in range(100):
        # Arbitrary observation (could be ARC grid, maze view, anything)
        observation = np.random.randint(0, 10, (5, 5))
        
        # Arbitrary action
        action = np.random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
        
        # Arbitrary reward
        reward = np.random.randn()
        
        # Update engine
        prescribed = engine.update(observation, action, reward)
        
        # Get dashboard
        if step % 10 == 0:
            dashboard = engine.get_dashboard()
            print(f"\nStep {step}:")
            print(f"  Σ={dashboard['sigma']:.2f}, Ω={dashboard['omega']:.2f}, Λ={dashboard['lambda']:.2f}")
            print(f"  Rv={dashboard['viability_ratio']:.2f}, dH/dt={dashboard['metabolism']:.2f}")
            print(f"  Diagnostic: {dashboard['diagnostic']}")
            print(f"  Prescribed: {dashboard['prescribed_action']}")
