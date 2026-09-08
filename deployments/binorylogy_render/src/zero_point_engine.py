"""
Zero-Point Entropy Engine

Part of Phase 27 Plug-and-Play Architecture.
Implements the "Architect's Hammer" hypothesis: 
Intelligence emerges from the pure will to exist (dH/dt ≥ 0).
"""

import numpy as np
from typing import Any, Dict, List, Tuple, Optional
from collections import deque
from entropy_engine import EntropyEngine, PrescriptiveAction

class ZeroPointEngine(EntropyEngine):
    """
    The Zero-Point Engine.
    
    Assumption: Zero knowledge.
    Mandate: Survive (maintain dH/dt ≥ 0).
    Result: Symbols emerge as 'Metabolic Anchors'.
    """
    
    def __init__(self):
        # Core State
        self.sigma = 1.0  # Starts pure
        self.omega = 0.0
        self.lambda_ = 0.1
        
        # Survival State
        self.energy = 100.0
        self.metabolic_anchors: Dict[int, Dict] = {} # Discovered symbols
        self.friction_map: Dict[int, Dict] = {}      # Discovered hazards
        
        # History
        self.metabolism_history = deque(maxlen=100)
        self.viability_history = deque(maxlen=100)
        
        # Phase 8: The Fever Protocol
        self.temperature = 0.0          # System Temperature (τ)
        self.divergence_history = deque(maxlen=10)  # Track recent divergence
        self.stagnation_count = 0       # Cycles of no improvement
        self.fever_threshold = 3        # Cycles before fever triggers
        self.max_temperature = 1.0      # Maximum fever intensity
        
        # Phase 9: Viscous Momentum
        self.momentum = 0.0             # Accumulated solving energy
        self.momentum_decay = 0.1       # Natural drain per cycle
        self.momentum_threshold = -0.5  # Exit when depleted below this
        self.last_divergence = None     # For calculating dΔ/dt
        
        # Phase 10: IRREVERSIBILITY PRIMITIVE (The 2nd Law)
        # This is THE causal ordering mechanism - no clocks, just entropy production
        self.entropy_produced = 0.0     # Total entropy produced (monotonically increases)
        self.entropy_budget = 10000.0   # Maximum allowed irreversibility
        self.entropy_history = deque(maxlen=100)  # Track entropy production rate
        self.causal_order = 0           # Current position in causal sequence
        
    def update(self, observation: Any, action: Any, reward: float) -> PrescriptiveAction:
        """
        Survival-based update cycle.
        """
        # 1. Sense Ω (Entropy)
        self.omega = self._measure_entropy(observation)
        
        # 2. Compute Metabolism (dH/dt)
        # We use action cost as friction proxy if reward is not explicit energy
        friction = 0.1 if reward == 0 else -reward
        self.lambda_ = max(0.01, friction)
        
        # Σ improves as we discover anchors
        self.sigma = 1.0 + (len(self.metabolic_anchors) * 0.1)
        
        # dH/dt = (Σ × Ω) - Λ
        dH_dt = (self.sigma * self.omega) - self.lambda_
        self.metabolism_history.append(dH_dt)
        self.energy += dH_dt
        
        # 3. Discover Anchors (Grounding)
        # If metabolism spikes, this pattern is a symbol of life
        if dH_dt > 1.0:
            obs_hash = self._hash_observation(observation)
            
            # Extract actual pattern data
            if hasattr(observation, 'context'):
                pattern_data = observation.context 
            else:
                pattern_data = observation
                
            if obs_hash not in self.metabolic_anchors:
                self.metabolic_anchors[obs_hash] = {
                    'pattern': pattern_data,
                    'boost': dH_dt,
                    'step': len(self.metabolism_history),
                    'hits': 1
                }
        
        # 4. Prescribe Action based on Survival
        return self._prescribe_survival_action(dH_dt)
        
    def register_anchor(self, pattern: np.ndarray, viability_boost: float):
        """
        Phase 4: Memetic Memory.
        Store a pattern if it provides high metabolic boost (Low Entropy/High Resonance).
        """
        if pattern.size == 0: return
        
        obs_hash = self._hash_observation(pattern)
        
        # Only store if new or better
        if obs_hash not in self.metabolic_anchors:
            self.metabolic_anchors[obs_hash] = {
                'pattern': pattern,
                'boost': viability_boost,
                'step': len(self.metabolism_history),
                'hits': 1
            }
        else:
            self.metabolic_anchors[obs_hash]['hits'] += 1
            self.metabolic_anchors[obs_hash]['boost'] = max(
                self.metabolic_anchors[obs_hash]['boost'], 
                viability_boost
            )

    def get_best_anchors(self, n: int = 5) -> List[np.ndarray]:
        """
        Retrieve top N anchors by metabolic boost.
        Used by Memetic Actuator for composition.
        """
        if not self.metabolic_anchors: return []
        
        # Sort by boost * hits (Reinforced Hebbian Survival)
        sorted_anchors = sorted(
            self.metabolic_anchors.values(), 
            key=lambda x: x['boost'] * (1 + np.log(x['hits'])), 
            reverse=True
        )
        
        return [item['pattern'] for item in sorted_anchors[:n]]

    def get_dashboard(self) -> Dict[str, Any]:
        """
        Return standard dashboard for agent visualization.
        """
        return {
            'sigma': round(self.sigma, 3),
            'omega': round(self.omega, 3),
            'lambda': round(self.lambda_, 3),
            'viability_ratio': round(self._compute_viability(), 3),
            'metabolism': round(self.metabolism_history[-1] if self.metabolism_history else 0, 3),
            'energy': round(self.energy, 3),
            'anchors_found': len(self.metabolic_anchors),
            'diagnostic': self._get_diagnostic(),
            'prescribed_action': self._get_last_prescription()
        }

    # ===========================================
    # SURVIVAL NAVIGATION
    # ===========================================
    
    def navigate_via_survival(self, 
                             current_pos: Tuple[int, int],
                             known_treasures: Dict[Tuple[int, int], float],
                             visit_history: Dict[Tuple[int, int], int],
                             valid_neighbors: List[Tuple[int, int, int]]) -> int:
        """
        Survival-driven navigation using metabolism and anchor memory.
        
        Strategy:
        1. When metabolism low: seek nearest known treasure (starvation avoidance)
        2. When safe: explore randomly, preferring unvisited cells
        3. Learn treasure locations as anchors
        """
        STARVATION_THRESHOLD = 30.0
        current_metabolism = self.metabolism_history[-1] if self.metabolism_history else 50.0
        
        # Critical: seek known food
        if current_metabolism < STARVATION_THRESHOLD and known_treasures:
            current_x, current_y = current_pos
            best_action = 4  # WAIT
            best_improvement = -float('inf')
            
            for action_idx, nx, ny in valid_neighbors:
                # Distance change to nearest treasure
                for treasure_pos in known_treasures.keys():
                    tx, ty = treasure_pos
                    next_dist = abs(nx - tx) + abs(ny - ty)
                    curr_dist = abs(current_x - tx) + abs(current_y - ty)
                    improvement = curr_dist - next_dist
                    if improvement > best_improvement:
                        best_improvement = improvement
                        best_action = action_idx
            
            return best_action if best_improvement > 0 else 4
        
        # Safe: explore with novelty
        else:
            weights = []
            actions = []
            
            for action_idx, nx, ny in valid_neighbors:
                visit_count = visit_history.get((nx, ny), 0)
                weight = 1.0 / (1.0 + visit_count)
                weights.append(weight)
                actions.append(action_idx)
            
            if not weights:
                return 4
            
            total = sum(weights)
            if total > 0:
                probs = [w / total for w in weights]
                return np.random.choice(actions, p=probs)
            else:
                return actions[0]

    # ============================================
    # Phase 7: Epistemic Executive Layer
    # ============================================
    
    def measure_divergence(self, prediction: np.ndarray, expected: np.ndarray) -> float:
        """
        Phase 7: Epistemic Friction.
        Measures how far the prediction is from truth.
        
        Returns:
            Pixel-level divergence (0 = perfect match, higher = more starvation)
        """
        if prediction.shape != expected.shape:
            # Shape mismatch: maximum starvation
            return float(prediction.size + expected.size)
        
        divergence = np.sum(prediction != expected)
        return float(divergence)
    
    def get_metabolic_pressure(self, divergence: float, max_pixels: int = 100) -> float:
        """
        Convert divergence to metabolic pressure (starvation level).
        
        Returns:
            Pressure in range [0, 1] where 1 = complete starvation
        """
        return min(1.0, divergence / max(1, max_pixels))

    # ============================================
    # Phase 8: The Fever Protocol
    # ============================================
    
    def update_fever(self, divergence: float) -> str:
        """
        Phase 8: Metabolic Annealing.
        Track divergence trends and adjust system Temperature.
        
        Returns:
            Current fever state: 'healthy', 'infected', 'critical'
        """
        self.divergence_history.append(divergence)
        
        if len(self.divergence_history) < 2:
            return 'healthy'
        
        # Check if divergence is decreasing
        recent = list(self.divergence_history)[-3:] if len(self.divergence_history) >= 3 else list(self.divergence_history)
        is_improving = recent[-1] < recent[0]
        
        if is_improving:
            # Cooling down - divergence is decreasing
            self.stagnation_count = 0
            self.temperature = max(0.0, self.temperature - 0.2)
            return 'healthy'
        else:
            # Stagnation or worsening
            self.stagnation_count += 1
            
            if self.stagnation_count >= self.fever_threshold:
                # CRITICAL: Force fever spike
                self.temperature = min(self.max_temperature, self.temperature + 0.3)
                if self.temperature >= 0.7:
                    return 'critical'
                else:
                    return 'infected'
            else:
                # Warming up
                self.temperature = min(self.max_temperature, self.temperature + 0.1)
                return 'infected'
    
    def get_fever_state(self) -> dict:
        """Get current fever diagnostics."""
        return {
            'temperature': round(self.temperature, 2),
            'stagnation_count': self.stagnation_count,
            'state': 'critical' if self.temperature >= 0.7 else ('infected' if self.temperature > 0.3 else 'healthy')
        }
    
    def should_abandon_motive(self) -> bool:
        """
        Phase 8: Fever-induced motive abandonment.
        When temperature is critical, the Agent must abandon its current beautiful lie.
        """
        return self.temperature >= 0.7
    
    def reset_fever(self):
        """Reset fever state after successful adaptation."""
        self.temperature = 0.0
        self.stagnation_count = 0
        self.divergence_history.clear()

    # ============================================
    # Phase 9: Viscous Momentum
    # ============================================
    
    def update_momentum(self, divergence: float) -> float:
        """
        Phase 9: Viscous Momentum.
        Momentum += (dΔ/dt) - Decay
        
        Returns:
            Current momentum value
        """
        if self.last_divergence is None:
            self.last_divergence = divergence
            return self.momentum
        
        # Calculate rate of error reduction (positive = improving)
        delta = self.last_divergence - divergence  # Positive when improving
        
        # Update momentum: gain from progress, lose from decay
        self.momentum += delta - self.momentum_decay
        
        # Clamp to prevent runaway
        self.momentum = max(-2.0, min(5.0, self.momentum))
        
        # Update history
        self.last_divergence = divergence
        
        return self.momentum
    
    def has_momentum(self) -> bool:
        """Check if Agent has enough momentum to continue."""
        return self.momentum > self.momentum_threshold
    
    def get_momentum_state(self) -> dict:
        """Get momentum diagnostics."""
        return {
            'momentum': round(self.momentum, 3),
            'threshold': self.momentum_threshold,
            'has_fuel': self.has_momentum(),
            'last_divergence': self.last_divergence
        }
    
    def reset_momentum(self):
        """Reset momentum for new task."""
        self.momentum = 0.0
        self.last_divergence = None

    # ============================================
    # Internal Logic
    # ============================================

    def _measure_entropy(self, observation: Any) -> float:
        """Measure Shannon entropy + Spatial Complexity (Connected Components)"""
        try:
            if isinstance(observation, np.ndarray):
                data = observation.flatten()
            else:
                return 1.0
                
            # 1. Shannon Entropy (Distribution)
            unique, counts = np.unique(data, return_counts=True)
            probs = counts / data.size
            shannon = -np.sum(probs * np.log2(probs + 1e-10))
            
            # 2. Spatial Entropy (Transitions / Edges)
            # A solid block has fewer edges than scattered noise.
            # We count horizontal and vertical transitions.
            h_edges = np.sum(observation[:, 1:] != observation[:, :-1])
            v_edges = np.sum(observation[1:, :] != observation[:-1, :])
            total_edges = h_edges + v_edges
            
            # Normalize: Max edges is approx 2 * size.
            # We want this to be additive to Shannon.
            # High edges = High entropy.
            # 10 scattered pixels -> ~40 edges.
            # 10 linear pixels -> ~22 edges.
            structural_entropy = np.log2(max(1, total_edges)) * 0.5
            
            # Debug
            # print(f"DEBUG: Shannon={shannon:.2f}, Struct={structural_entropy:.2f}")  
            return shannon + structural_entropy
        except Exception as e:
            # print(f"DEBUG: Entropy Error: {e}")
            return 1.0

    def _prescribe_survival_action(self, dH_dt: float) -> PrescriptiveAction:
        """
        Prescribe action based on immediate survival needs.
        """
        # If dying rapidly, BREACH (Panic/Escape)
        if dH_dt < -1.0:
            return PrescriptiveAction.BREACH
            
        # If thriving, REFINERY (optimize anchors)
        if dH_dt > 2.0:
            return PrescriptiveAction.REFINERY
            
        # If struggling but alive, INJECTION (seek new anchors)
        if 0 < dH_dt < 0.5:
            return PrescriptiveAction.INJECTION
            
        return PrescriptiveAction.CONTINUE

    def _compute_viability(self) -> float:
        """Rv = Average positive metabolism / Average negative metabolism"""
        if not self.metabolism_history:
            return 1.0
        
        recent = list(self.metabolism_history)[-10:]
        pos = sum(m for m in recent if m > 0)
        neg = abs(sum(m for m in recent if m < 0))
        
        return pos / max(neg, 0.01)

    def _hash_observation(self, obs: Any) -> int:
        if isinstance(obs, np.ndarray):
            return hash(obs.tobytes())
        return hash(str(obs))

    def _get_diagnostic(self) -> str:
        rv = self._compute_viability()
        if rv < 1.0: return "DYING (Dissipating)"
        if rv > 3.0: return "THRIVING (Accumulating)"
        return "SURVIVING (Homeostatic)"

    def _get_last_prescription(self) -> str:
        if not self.metabolism_history: return "NONE"
        last_metric = self.metabolism_history[-1]
        return self._prescribe_survival_action(last_metric).value
        
    def measure_viability(self, observation: Any, is_anchor_search: bool = False) -> float:
        """
        Phase 3.5: Structural Coupling (Resonance).
        
        Viability = Resonance (Link to World) - Dissipation (Cost of Complexity).
        
        Mandate: Reduce Entropy ONLY if you preserve Meaning (Anchors).
        params:
            is_anchor_search: If True, we look for simple, ordered blocks (Primitives). 
                              We do NOT penalize low complexity in this mode.
        """
        candidate_grid = observation if isinstance(observation, np.ndarray) else None
        if candidate_grid is None: return 0.0
        
        # 1. Measure Dissipation (Cost)
        # Raw Entropy of the grid (complexity)
        # We want to minimize this (maximize -entropy)
        omega = self._measure_entropy(candidate_grid)
        dissipation = omega * 0.5 # Weighting factor
        
        # 2. Measure Resonance (Life)
        # Check if known Anchors (from Input) exist in Candidate
        resonance = 0.0
        
        # 2a. Unique Color Count (Vocabulary Preservation)
        unique_colors = len(np.unique(candidate_grid))
        resonance += unique_colors * 0.5
        
        # 2b. Spatial Structure (Non-randomness)
        # If grid is too simple (1 color), low resonance.
        # BUT: If we are searching for anchors, 1 color is a valid primitive (Solid Block).
        if unique_colors < 2 and not is_anchor_search:
             resonance -= 5.0 # Penalty for "Melting" (Solution level)
        elif is_anchor_search:
             # Reward compactness/simplicity for anchors
             resonance += 1.0 
        
        # 3. Net Metabolism
        dH_dt = resonance - dissipation
        
        return dH_dt

    # ============================================
    # Phase 10: IRREVERSIBILITY (The 2nd Law)
    # ============================================
    
    def produce_entropy(self, delta_s: float) -> bool:
        """
        Record entropy production from an irreversible process.
        
        This is THE causal ordering mechanism:
        - Each action has a thermodynamic cost
        - Entropy monotonically increases (2nd Law)
        - When budget exhausted, system halts
        
        No clocks. No time variable. Just irreversibility.
        
        Args:
            delta_s: Entropy produced by this action (always >= 0)
            
        Returns:
            True if action allowed, False if budget exhausted
        """
        if delta_s < 0:
            delta_s = 0  # Entropy cannot decrease (enforce 2nd Law)
            
        # Check if we can afford this action
        if self.entropy_produced + delta_s > self.entropy_budget:
            return False  # Budget exhausted - system must halt
        
        # Record entropy production
        self.entropy_produced += delta_s
        self.entropy_history.append(delta_s)
        self.causal_order += 1  # This creates the ordering
        
        return True
    
    def is_budget_exhausted(self) -> bool:
        """Check if system has exhausted its irreversibility budget."""
        return self.entropy_produced >= self.entropy_budget
    
    def get_causal_state(self) -> Dict[str, Any]:
        """
        Get the current causal state of the system.
        
        This reveals the position in the causal sequence
        without needing a clock.
        """
        return {
            'causal_order': self.causal_order,
            'entropy_produced': self.entropy_produced,
            'entropy_remaining': self.entropy_budget - self.entropy_produced,
            'entropy_rate': np.mean(list(self.entropy_history)) if self.entropy_history else 0.0,
            'is_exhausted': self.is_budget_exhausted()
        }
    
    def calculate_action_entropy(self, old_state: np.ndarray, new_state: np.ndarray) -> float:
        """
        Calculate entropy produced by a state transition.
        
        This measures "how much changed" - the thermodynamic cost
        of moving from one state to another.
        
        Physics: ΔS ∝ |state_change|
        """
        if old_state is None or new_state is None:
            return 0.1  # Minimum entropy for any action
        
        # Compute state difference
        try:
            diff = np.abs(new_state.astype(float) - old_state.astype(float))
            delta_s = np.sum(diff) / max(1, old_state.size)
            return max(0.01, delta_s)  # Minimum entropy > 0
        except:
            return 0.1
    
    def reset_entropy_budget(self, new_budget: float = None):
        """Reset entropy tracking for new task."""
        self.entropy_produced = 0.0
        self.causal_order = 0
        self.entropy_history.clear()
        if new_budget is not None:
            self.entropy_budget = new_budget
