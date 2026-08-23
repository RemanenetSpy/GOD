import numpy as np
from enum import Enum, auto
from typing import List, Tuple, Any, Optional
from active_motives import MotiveType, MotivePhysics

class ConditionType(Enum):
    ALWAYS = auto()
    IS_COLOR = auto()
    IS_NOT_COLOR = auto()
    # Future: IS_ISOLATED, IS_SHAPE, etc.

class CausalRule:
    """
    A Logic Rule: IF Condition(pixel) THEN Apply Motive(pixel)
    Currently operates at pixel level or component level.
    """
    def __init__(self, condition_type: ConditionType, condition_value: Any, motive: MotiveType):
        self.condition_type = condition_type
        self.condition_value = condition_value
        self.motive = motive
        
    def __repr__(self):
        return f"IF {self.condition_type.name}({self.condition_value}) THEN {self.motive.name}"

    def apply(self, grid: np.ndarray) -> np.ndarray:
        """Apply rule to grid."""
        # This is tricky specifically for GRAVITY which acts on the whole grid/column.
        # But we can simulate "Selective Gravity" by separating the grid into "Active" and "Passive" layers.
        # Active Layer = Pixels matching condition.
        # Passive Layer = Pixels NOT matching.
        # Apply Motive to Active Layer.
        # Recombine.
        
        h, w = grid.shape
        active_mask = np.zeros((h, w), dtype=bool)
        
        if self.condition_type == ConditionType.ALWAYS:
            active_mask[:] = True
        elif self.condition_type == ConditionType.IS_COLOR:
            active_mask = (grid == self.condition_value)
        elif self.condition_type == ConditionType.IS_NOT_COLOR:
            active_mask = (grid != self.condition_value) & (grid != 0) # Ignore background?
            
        # Split
        active_layer = np.zeros_like(grid)
        active_layer[active_mask] = grid[active_mask]
        
        passive_layer = grid.copy()
        passive_layer[active_mask] = 0
        
        # Apply Motive to Active Layer
        try:
            transformed_active = MotivePhysics.apply_motive(active_layer, self.motive)
            
            # Recombine
            output = passive_layer.copy()
            
            # Robust broadcasting: Handle shape mismatch (e.g., Rotation 90 changes dimensions)
            if transformed_active.shape != output.shape:
                # If shapes differ, we cannot simple overlay.
                # Prioritize the transformed active layer if it contains information
                return transformed_active
            
            mask_trans = (transformed_active != 0)
            output[mask_trans] = transformed_active[mask_trans]
            return output
            
        except Exception as e:
            # Fallback for physics failures
            # print(f"Physics error in CausalRule: {e}")
            return grid

class HypothesisEngine:
    """
    The Causal Leap: Reasons about WHY a motive works or fails.
    """
    
    @staticmethod
    def reason(motive: MotiveType, train_examples: list) -> 'CausalRule':
        """
        Generate a Causal Rule (Hypothesis) that best explains the data.
        """
        print(f"🤔 Reasoning about Motive: {motive.name}...")
        
        # 1. Establish Baseline (Global Application)
        base_rule = CausalRule(ConditionType.ALWAYS, None, motive)
        base_error = HypothesisEngine._evaluate_rule(base_rule, train_examples)
        
        if base_error == 0:
            print("   Global application works perfectly.")
            return base_rule
            
        print(f"   Global Error: {base_error} pixels. Searching for Constraints...")
        
        best_rule = base_rule
        best_error = base_error
        
        # 2. Search for Conditional Improvements
        # Hypothesis: "Only objects of Color X obey this motive"
        # Extract all colors present in inputs
        all_colors = set()
        for ex in train_examples:
            all_colors.update(np.unique(ex['input']))
        if 0 in all_colors: all_colors.remove(0) # Ignore black
            
        for color in all_colors:
            # Try IS_COLOR
            rule = CausalRule(ConditionType.IS_COLOR, color, motive)
            error = HypothesisEngine._evaluate_rule(rule, train_examples)
            
            if error < best_error:
                best_error = error
                best_rule = rule
                
            # Try IS_NOT_COLOR (Everything except X moves)
            rule_not = CausalRule(ConditionType.IS_NOT_COLOR, color, motive)
            error_not = HypothesisEngine._evaluate_rule(rule_not, train_examples)
            
            if error_not < best_error:
                best_error = error_not
                best_rule = rule_not
        
        print(f"💡 Epiphany: {best_rule} (Error: {best_error})")
        return best_rule
        
    @staticmethod
    def _evaluate_rule(rule: CausalRule, examples: List[dict]) -> int:
        """Count mismatch pixels across all examples."""
        total_error = 0
        for ex in examples:
            inp, out = ex['input'], ex['output']
            pred = rule.apply(inp)
            
            if pred.shape != out.shape:
                # Resize penalty? Or valid resize?
                # For now assume same size or max error
                total_error += pred.size 
                continue
                
            diff = (pred != out)
            total_error += np.sum(diff)
            
        return total_error
