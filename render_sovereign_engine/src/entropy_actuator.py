import numpy as np
import copy

# Robust imports
from atomic_actions import AtomicPhysics
from entropy_engine import EntropyEngine

class EntropyActuator:
    """
    The 'Hands' of the Zero-Point Engine.
    Uses Evolutionary Search to find the output grid that maximizes Survival (Viability).
    """
    
    def __init__(self, engine: EntropyEngine):
        self.engine = engine
        
    def generate_solution(self, input_grid: np.ndarray, generations=100, population_size=10) -> np.ndarray:
        """
        Evolve the input grid into the solution using survival maximization.
        Phase 4: Uses MEMETIC ANCHORS (Smart Mutation).
        """
        # Start with the input (many ARC tasks preserve structure)
        current_grid = input_grid.copy()
        
        # Initial Baselines
        best_grid = current_grid.copy()
        best_viability = self._evaluate(best_grid)
        
        # Phase 4: Retrieve Discovered Anchors
        anchors = []
        if hasattr(self.engine, 'get_best_anchors'):
            anchors = self.engine.get_best_anchors(n=5)
            if anchors:
                print(f"🧬 Memetic Actuator: Using {len(anchors)} discovered anchors for mutation.")
        
        print(f"DEBUG: Initial Viability: {best_viability:.4f}")
        
        # Evolution Loop (Hill Climbing / Simulated Annealing lite)
        for gen in range(generations):
            candidates = []
            
            # 1. Generate Mutants
            for _ in range(population_size):
                # Apply mutation (Actuator now passes anchors to Physics)
                mutant = AtomicPhysics.mutate(best_grid, anchors=anchors)
                candidates.append(mutant)
                
            # 2. Evaluate Fitness (Metabolism)
            scores = []
            for mutant in candidates:
                score = self._evaluate(mutant)
                scores.append(score)
            
            # 3. Select Best
            max_score = max(scores)
            if max_score > best_viability:
                idx = scores.index(max_score)
                best_grid = candidates[idx]
                best_viability = max_score
                # print(f"DEBUG: Gen {gen} | Improvement! New Rv: {best_viability:.4f}")
            else:
                # print(f"DEBUG: Gen {gen} | Stagnation")
                pass
                
        return best_grid

    def _evaluate(self, grid: np.ndarray) -> float:
        """
        Ask the Engine: 'How does this grid make you feel?'
        Returns Viability Ratio (Rv).
        """
        # We need to feed this grid into the engine as an Observation
        # The engine measures the entropy of the *observation*.
        
        # Note: In the zero_point_engine.py, 'update' calculates metrics.
        # We need a 'measure_viability(grid)' method that doesn't necessarily update state history, 
        # or we use a temporary engine copy.
        # For efficiency, we'll ask the engine to just calculate metrics on a static grid.
        
        # HACK: Ideally we refactor engine to separate 'measure' from 'update'.
        # For now, we assume the engine has a `measure_viability(grid)` method.
        # If not, we will add it to ZeroPointEngine.
        
        if hasattr(self.engine, 'measure_viability'):
             return self.engine.measure_viability(grid)
             
        # Fallback if method not present yet (Part of refactor)
        return 0.0
    
    def generate_solution_epistemic(self, input_grid: np.ndarray, expected_output: np.ndarray, 
                                      generations=100, population_size=10) -> np.ndarray:
        """
        Phase 7: Epistemic Evolution.
        Evolve the input grid toward TRUTH (expected_output) using Divergence as fitness.
        
        The Agent is "starving" until Divergence -> 0.
        """
        current_grid = input_grid.copy()
        
        best_grid = current_grid.copy()
        best_divergence = self._measure_divergence(best_grid, expected_output)
        
        # Phase 4: Retrieve Discovered Anchors
        anchors = []
        if hasattr(self.engine, 'get_best_anchors'):
            anchors = self.engine.get_best_anchors(n=5)
        
        # Evolution Loop
        for gen in range(generations):
            candidates = []
            
            # 1. Generate Mutants
            for _ in range(population_size):
                mutant = AtomicPhysics.mutate(best_grid, anchors=anchors)
                candidates.append(mutant)
                
            # 2. Evaluate Fitness (EPISTEMIC: Lower Divergence = Better)
            scores = []
            for mutant in candidates:
                divergence = self._measure_divergence(mutant, expected_output)
                scores.append(divergence)
            
            # 3. Select Best (LOWEST divergence)
            min_score = min(scores)
            if min_score < best_divergence:
                idx = scores.index(min_score)
                best_grid = candidates[idx]
                best_divergence = min_score
                
                # Early exit if perfect match
                if best_divergence == 0:
                    break
                    
        return best_grid
    
    def _measure_divergence(self, prediction: np.ndarray, expected: np.ndarray) -> float:
        """Measure pixel-level divergence from truth."""
        if prediction.shape != expected.shape:
            return float(prediction.size + expected.size)
        return float(np.sum(prediction != expected))

