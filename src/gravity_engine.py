"""
Gravity Engine (The Mechanics)
Phase 10: Sovereign Gravity Protocol

Implements the physics of the agent.
Uses the Universal Metric to calculate gradients.
Applies "Forces" (Motives) to move down the gradient.
"""

import numpy as np
from typing import Any, List, Optional, Tuple
from universal_metric import UniversalMetric
from active_motives import MotiveType, MotivePhysics

class GravityEngine:
    """
    The Engine of Collapse.
    """
    def __init__(self):
        self.metric = UniversalMetric()
        self.history_potential: List[float] = []
        self.metabolic_anchors: Dict[int, Dict] = {} # Discovered symbols
        self.train_pairs: List[Tuple[np.ndarray, np.ndarray]] = []
        
    def register_anchor(self, patch: np.ndarray, viability: float):
        """Phase 4: Remember stable patterns (Mass Concentrations)."""
        patch_hash = hash(patch.tobytes())
        # Store if new or better
        if patch_hash not in self.metabolic_anchors or viability > self.metabolic_anchors[patch_hash]['viability']:
            self.metabolic_anchors[patch_hash] = {
                'patch': patch, 
                'viability': viability,
                'count': 1
            }
            
    def measure_viability(self, patch: np.ndarray, is_anchor_search: bool = False) -> float:
        """Measure intrinsic stability (Order/Density)."""
        # Compare to self to get internal metrics (Div=0)
        _, entropy, density = self.metric.measure_mass(patch, patch)
        
        if density < 0.1: return 0.0 # Too empty
        
        # Heuristic: Density is good (Existence), Entropy is cost (Complexity).
        # We want Dense but Simple patterns.
        score = density / (1.0 + entropy * 0.2)
        return min(1.0, score)
            
    def get_best_anchors(self, n: int = 5) -> List[np.ndarray]:
        """Retrieve highest-mass anchors to guide mutation."""
        if not self.metabolic_anchors:
            return []
        # Sort by viability
        sorted_anchors = sorted(self.metabolic_anchors.values(), key=lambda x: x['viability'], reverse=True)
        return [item['patch'] for item in sorted_anchors[:n]]

    def _liquefy(self, grid: np.ndarray, temperature: float = 1.0) -> np.ndarray:
        """Convert Solid Grid to Fluid Field (Probability Tensor)."""
        h, w = grid.shape
        fluid = np.zeros((h, w, 10))
        
        # Smooth initialization (Softmax-like with Temperature)
        # If temp is low, it's almost one-hot. If high, it's uniform.
        epsilon = 0.01 * temperature
        fluid.fill(epsilon / 10.0)
        
        rows, cols = np.indices((h, w))
        fluid[rows, cols, grid] = 1.0 - epsilon
        
        # Normalize
        fluid /= np.sum(fluid, axis=2, keepdims=True)
        return fluid

    def _crystallize(self, fluid: np.ndarray) -> np.ndarray:
        """Convert Fluid Field back to Solid Grid."""
        return np.argmax(fluid, axis=2)

    def topological_evolution(self, fluid: np.ndarray) -> np.ndarray:
        """
        Phase 13: ELASTIC SPACETIME.
        Evaporate empty dimensions (Vacuum Collapse).
        """
        # 1. measure pressure
        row_mass, col_mass = self.metric.measure_mass_profile(fluid)
        
        # Threshold: if mass < 0.01 (Vacuum), evaporate.
        vacuum_threshold = 0.01
        
        keep_rows = row_mass > vacuum_threshold
        keep_cols = col_mass > vacuum_threshold
        
        # Identify vacuum regions
        # If we have vacuum at edges, we crop.
        # If we have vacuum in middle, we split? (Not yet).
        
        # Simple bounding box implementation via evaporation
        # If EVERYTHING is vacuum, don't collapse to 0x0
        if not np.any(keep_rows) or not np.any(keep_cols):
             return fluid
             
        # Crop (Evaporate)
        # Slicing operates on the tensor
        new_fluid = fluid[keep_rows][:, keep_cols]
        
        # Report
        if new_fluid.shape != fluid.shape:
             print(f"📉 Spacetime Evaporation: {fluid.shape} -> {new_fluid.shape}")
             
        return new_fluid

    def _inflate(self, fluid: np.ndarray, target_shape: Tuple[int, int]) -> np.ndarray:
        """
        Phase 14: INFLATIONARY COSMOLOGY.
        Expand the universe to fit the Truth.
        """
        current_h, current_w, c = fluid.shape
        target_h, target_w = target_shape
        
        if current_h >= target_h and current_w >= target_w:
            return fluid
            
        # Calculate new shape (Growth)
        new_h = max(current_h, target_h)
        new_w = max(current_w, target_w)
        
        # Create new vacuum universe
        new_fluid = np.zeros((new_h, new_w, c))
        
        # Fill vacuum with low probability uniform dust
        epsilon = 0.001
        new_fluid.fill(epsilon / 10.0)
        new_fluid[:, :, 0] = 1.0 - epsilon # Mostly background 0
        
        # Embed current universe (Symmetry Expansion source)
        # For now, place at top-left (Anchor point).
        # Theoretically, we should find the "Center of Mass", but 0,0 is standard ARC anchor.
        new_fluid[:current_h, :current_w, :] = fluid
        
        print(f"📈 Spacetime Inflation: {fluid.shape} -> {new_fluid.shape}")
        return new_fluid

    def fluid_dynamics_elastic(self, initial_state: np.ndarray, target_state: Optional[np.ndarray], steps: int = 50) -> np.ndarray:
        """
        Phase 13/14: Fluid Dynamics + Elastic Spacetime (Evaporation & Inflation).
        Updated for Phase 15: Supports Blind Mode (target_state=None).
        """
        # 1. Liquefy
        fluid = self._liquefy(initial_state, temperature=1.0)
        learning_rate = 0.1
        
        # 2. Flow Loop with Topology Checks
        for i in range(steps):
             # A. Inflation Check (Start of flow)
             # If the Truth (Target) is bigger than the World, we must Inflate.
             # Phase 15: If Blind, we don't have target_state to check size.
             # We rely on 'Consensus' from Train Pairs?
             # For now, skip Inflation if Blind (Assume Output ~ Input size unless Metric drives it)
             
             if target_state is not None and i == 0:
                  fluid = self._inflate(fluid, target_state.shape)
                  
             # B. Topological Evolution (Evaporation)
             # Check if we should evaporate boundary vacuum (Shrink wrap)
             if i > 0 and i % 10 == 0:
                 fluid = self.topological_evolution(fluid)
             
             # Align shapes for Gradient Calculation
             current_h, current_w, _ = fluid.shape
             
             # Calculate Gradient
             if target_state is not None:
                 # SUPERVISED MODE (Training)
                 # Handle shape mismatch (Training wheels)
                 if current_h == target_state.shape[0] and current_w == target_state.shape[1]:
                     grad = self.metric.calculate_gradient_fluid(fluid, target_state)
                 else:
                     # Force match if simple logic failed
                     if i == 0:
                         fluid = self._inflate(fluid, target_state.shape)
                     continue
             else:
                 # HOLOGRAPHIC MODE (Blind)
                 # Gradient is d(GlobalResonance)/dFluid
                 # We assume Metric can calculate this. 
                 # Currently calculate_gradient_fluid requires 'target'.
                 # We need a new metric Gradient for Resonance or approximate it via Sampling.
                 
                 # Approximating Gradient for Resonance is expensive (requires perturbing fluid).
                 # For Phase 15 PoC, we skip Fluid Flow in Blind Mode and rely on Discrete Search for now?
                 # Or we treat 'train_pairs' average output as a 'Ghost Target'?
                 
                 # Simple Heuristic: The Ghost Target is the Input transformed by the Average Delta of Train Pairs.
                 # This is "Induction" (Trap).
                 # For now, Fluid Mode halts in Blind Mode (Physics freeze).
                 continue

             fluid_unconstrained = fluid - learning_rate * grad
             fluid_clipped = np.clip(fluid_unconstrained, 1e-9, 1.0)
             fluid = fluid_clipped / np.sum(fluid_clipped, axis=2, keepdims=True)

        # 3. Crystallize
        return self._crystallize(fluid)
        
    def update(self, observation: Any, action: Any, reward: float) -> Any:
        # Phase 15: Memory
        if hasattr(observation, 'train_examples') and observation.train_examples:
            # Only store if unique? Or just overwrite?
            # Benchmark passes all examples every time.
            self.train_pairs = observation.train_examples
        return None
        
    def get_dashboard(self) -> dict:
        return {
            "potential": self.history_potential[-1] if self.history_potential else 0.0,
            "anchors_discovered": len(self.metabolic_anchors)
        }

    # ===========================================
    # PHASE 10.5: GENERAL RELATIVITY NAVIGATION
    # ===========================================
    
    # ===========================================
    # PHASE 10.5: GENERAL RELATIVITY NAVIGATION
    # (UPGRADED via MANIFOLD INJECTION - PHASE 25)
    # ===========================================
    
    def calculate_potential_field(self, 
                                  maze_state: np.ndarray,
                                  goal_pos: Tuple[int, int] = None,
                                  wall_value: int = 1,
                                  max_iterations: int = 1000,
                                  tolerance: float = 0.001,
                                  goals: List[Tuple[int, int]] = None) -> np.ndarray:
        """
        Solve Eikonal Equation for GR potential field (True Gravity).
        Supports Multi-Source Gravity (Frontier Exploration).
        """
        # 1. Define Metric (Refractive Index)
        h, w = maze_state.shape
        refractive_index = np.ones((h, w), dtype=float)
        
        # Walls = Infinite Time Dilation
        WALL_COST = 1e9
        refractive_index[maze_state == wall_value] = WALL_COST
        
        # 2. Solve Eikonal (Fast Marching)
        import heapq
        arrival_time = np.full((h, w), np.inf)
        pq = []
        
        # Setup Goals (Event Horizons)
        targets = []
        if goals is not None:
            targets.extend(goals)
        if goal_pos is not None:
            targets.append(goal_pos)
            
        for gx, gy in targets:
            if 0 <= gx < h and 0 <= gy < w:
                arrival_time[gx, gy] = 0.0
                heapq.heappush(pq, (0.0, gx, gy))
            
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        while pq:
            current_t, x, y = heapq.heappop(pq)
            
            if current_t > arrival_time[x, y]:
                continue
                
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                
                if 0 <= nx < h and 0 <= ny < w:
                    # Metric cost
                    cost = refractive_index[nx, ny]
                    new_time = current_t + cost
                    
                    if new_time < arrival_time[nx, ny]:
                        arrival_time[nx, ny] = new_time
                        heapq.heappush(pq, (new_time, nx, ny))
                        
        return arrival_time
    
    def navigate_via_gradient(self,
                             field: np.ndarray,
                             pos: Tuple[int, int]) -> int:
        """
        Pure physics: follow steepest descent.
        
        In GR, objects follow geodesics (curved paths).
        This is equivalent to following ∇φ downhill.
        
        Args:
            field: Potential field from calculate_potential_field
            pos: Current (x, y) position
            
        Returns:
            Action index: 0=UP, 1=DOWN, 2=LEFT, 3=RIGHT, 4=WAIT
        """
        x, y = pos
        best_action = 4  # WAIT
        best_gradient = -float('inf')
        
        # Check all 4 directions
        actions = [
            (0, (-1, 0)),  # UP
            (1, (1, 0)),   # DOWN
            (2, (0, -1)),  # LEFT
            (3, (0, 1))    # RIGHT
        ]
        
        for action_idx, (dx, dy) in actions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < field.shape[0] and 0 <= ny < field.shape[1]:
                if np.isfinite(field[nx, ny]):
                    # Gradient = decrease in potential
                    gradient = field[x, y] - field[nx, ny]
                    if gradient > best_gradient:
                        best_gradient = gradient
                        best_action = action_idx
        
        return best_action

    def gravitational_collapse(self, 
                             initial_state: np.ndarray, 
                             target_state: Optional[np.ndarray], 
                             actuator: Any, 
                             max_energy_cycles: int = 100) -> np.ndarray:
        """
        The Main Physics Loop (Continuous Descent).
        Supports Blind Solving (Holographic Mode).
        """
        current_state = initial_state.copy()
        
        is_blind = (target_state is None)
        
        if is_blind:
             print("🌌 Gravity Well: HOLOGRAPHIC MODE (Blind). Searching for Resonance...")
             if not self.train_pairs:
                 print("⚠️ No Training Pairs in Memory. Cannot resonate. Returning Input.")
                 return current_state
             
             # Initial Potential (Global Dissonance)
             current_potential = self.metric.measure_global_resonance(
                 self.train_pairs, initial_state, current_state
             )
             print(f"🌌 Holographic Potential: {current_potential:.4f}")
        else:
             current_potential = self.metric.calculate_potential(current_state, target_state)
             print(f"🌌 Gravity Well Initialized. Potential: {current_potential:.4f}")
        
        cycle = 0
        while cycle < max_energy_cycles:
            cycle += 1
            
            # 1. Equilibrium Check
            if not is_blind:
                div, _, _ = self.metric.measure_mass(current_state, target_state)
                if div == 0:
                    print("✨ Singularity Reached (Divergence 0). Collapse Complete.")
                    return current_state
            else:
                 # In Blind Mode, we stop if Potential is low enough or gradients vanish
                 if current_potential < 0.1:
                      print("✨ Holographic Alignment Reached. Collapse Complete.")
                      return current_state
            
            # 2. Gradient Sensing (Search)
            best_gradient = 0.0
            best_motive = None
            best_next_state = None
            best_potential = current_potential
            
            possible_forces = [m for m in MotiveType] 
            
            for motive in possible_forces:
                try:
                    next_state = MotivePhysics.apply_motive(current_state, motive)
                    
                    if is_blind:
                         next_potential = self.metric.measure_global_resonance(
                             self.train_pairs, initial_state, next_state
                         )
                    else:
                         next_potential = self.metric.calculate_potential(next_state, target_state)
                    
                    gradient = current_potential - next_potential # Positive = Descent
                    
                    if gradient > 0.001 and gradient > best_gradient:
                         best_gradient = gradient
                         best_motive = motive
                         best_next_state = next_state
                         best_potential = next_potential
                except:
                    continue
            
            # 3. Apply Force
            if best_motive:
                print(f"📉 Descent: ΔΦ={best_gradient:.4f} via {best_motive.name} | Φ={best_potential:.4f}")
                current_state = best_next_state
                current_potential = best_potential
                
                # Kinetic Energy / Tunneling
                if abs(best_gradient) > 5.0 and not is_blind:
                     # Only refine if we know target? Or use Actuator blindly?
                     pass
            else:
                # 4. Local Minimum
                # Blind Mode doesn't support Fluid Dynamics yet (Gradient undefined).
                if is_blind:
                     print(f"🛑 Local Minimum at Φ={current_potential:.4f}. Stabilizing.")
                     return current_state
                
                print(f"🛑 Local Minimum at Φ={current_potential:.4f}. Liquefying...")
                
                try:
                    fluid_state = self.fluid_dynamics_elastic(current_state, target_state, steps=50)
                    fluid_pot = self.metric.calculate_potential(fluid_state, target_state)
                    
                    if fluid_pot < current_potential:
                        print(f"💧 Fluid Flow Successful! Φ {current_potential:.4f} -> {fluid_pot:.4f}")
                        current_state = fluid_state
                        current_potential = fluid_pot
                    else:
                        print("❄️ Fluid Froze. System halted.")
                        return current_state
                except Exception as e:
                     print(f"⚠️ Fluid Engine Error: {e}")
                     return current_state

        return current_state

    # ============================================
    # Phase 10: RELAXATION DYNAMICS (Irreversibility)
    # ============================================
    
    def relaxation_step(self, current_state: np.ndarray, target_state: np.ndarray, 
                        zero_point: Optional['ZeroPointEngine'] = None) -> Tuple[np.ndarray, float]:
        """
        Single relaxation step with entropy production.
        
        This creates CAUSAL ORDERING without time:
        - Each step produces entropy (thermodynamic cost)
        - Entropy production creates irreversibility
        - Irreversibility creates sequence (what happened "before" vs "after")
        
        Args:
            current_state: Current configuration
            target_state: Goal configuration
            zero_point: Optional Zero-Point engine to track global entropy
            
        Returns:
            (next_state, delta_entropy)
        """
        # Calculate potential gradient
        current_potential = self.metric.calculate_potential(current_state, target_state)
        
        # Find best local move (down gradient)
        best_next_state = current_state.copy()
        best_gradient = 0.0
        
        forces = MotivePhysics.get_forces_for_motive(MotiveType.DESCEND)
        
        for motive in forces:
            try:
                next_state = MotivePhysics.apply_force(current_state, motive)
                next_potential = self.metric.calculate_potential(next_state, target_state)
                gradient = current_potential - next_potential
                
                if gradient > best_gradient:
                    best_gradient = gradient
                    best_next_state = next_state
            except:
                continue
        
        # Calculate entropy production (thermodynamic cost of this step)
        delta_entropy = self._calculate_relaxation_entropy(current_state, best_next_state, best_gradient)
        
        # If Zero-Point provided, record entropy globally
        if zero_point is not None:
            if not zero_point.produce_entropy(delta_entropy):
                # Budget exhausted - cannot take this step
                return current_state, 0.0
        
        return best_next_state, delta_entropy
    
    def _calculate_relaxation_entropy(self, old_state: np.ndarray, new_state: np.ndarray, 
                                       gradient: float) -> float:
        """
        Calculate entropy produced by a relaxation step.
        
        Physics: ΔS = work / temperature
        
        In our system:
        - Work = gradient magnitude (how much potential changed)
        - Temperature = system "stiffness" (how hard it is to change)
        """
        # Base entropy from state change
        try:
            diff = np.abs(new_state.astype(float) - old_state.astype(float))
            state_entropy = np.sum(diff) / max(1, old_state.size)
        except:
            state_entropy = 0.1
        
        # Add entropy from gradient descent (work done)
        work_entropy = abs(gradient) * 0.1
        
        # Total entropy (always positive - 2nd Law)
        total_entropy = max(0.01, state_entropy + work_entropy)
        
        return total_entropy
    
    def relaxation_solve(self, initial_state: np.ndarray, target_state: np.ndarray,
                         zero_point: Optional['ZeroPointEngine'] = None,
                         max_steps: int = 1000) -> Tuple[np.ndarray, List[float]]:
        """
        Solve via relaxation dynamics with entropy tracking.
        
        Unlike collapse(), this explicitly tracks entropy production
        to create causal ordering.
        
        Terminates when:
        1. Reached target (potential = 0)
        2. Local minimum (no gradient)
        3. Entropy budget exhausted (if zero_point provided)
        """
        current_state = initial_state.copy()
        entropy_trace = []
        
        for step in range(max_steps):
            # Check entropy budget
            if zero_point is not None and zero_point.is_budget_exhausted():
                print(f"🔋 Entropy budget exhausted at step {step}")
                break
            
            # Take relaxation step
            next_state, delta_entropy = self.relaxation_step(current_state, target_state, zero_point)
            entropy_trace.append(delta_entropy)
            
            # Check for convergence
            if delta_entropy < 0.001:
                print(f"✅ Converged at step {step} (no more entropy production)")
                break
            
            # Check if reached target
            if np.array_equal(next_state, target_state):
                print(f"🎯 Reached target at step {step}")
                break
            
            current_state = next_state
        
        return current_state, entropy_trace
