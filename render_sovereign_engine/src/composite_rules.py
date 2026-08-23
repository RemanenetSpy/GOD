"""
Phase 16.2: Compositional Rule Engine

Enables multi-rule execution for complex transformations.
Based on cognitive neuroscience: Working memory maintains intermediate states
allowing rule chaining (Rule A → enables → Rule B).

Key Innovation: Rules can ENABLE other rules through state changes.
"""

import numpy as np
from typing import List, Tuple, Optional, Set
from dataclasses import dataclass
from core import TransformationRule

@dataclass
class RuleApplication:
    """Record of a rule being applied"""
    rule: TransformationRule
    position: Tuple[int, int]
    previous_state: np.ndarray
    new_state: np.ndarray
    timestamp: int

class CompositeRuleEngine:
    """
    Compositional rule execution engine.
    
    Cognitive Model:
    - Working memory: Maintains intermediate transformation states
    - Rule chaining: Each rule application may enable new rules
    - Depth limiting: Prevents infinite loops (max_depth = 5)
    
    Example:
        Task: "Fill rectangles with blue AND rotate 90°"
        Step 1: Fill creates blue objects (rule 1)
        Step 2: Now blue objects exist → rotate them (rule 2)
    """
    
    def __init__(self, max_depth: int = 5):
        self.max_depth = max_depth
        self.execution_history: List[RuleApplication] = []
        self.applied_rule_types: Set[str] = set()
        
    def can_apply_rule(self, rule: TransformationRule, grid: np.ndarray, 
                       position: Tuple[int, int]) -> bool:
        """
        Check if rule is applicable at given position in current grid state.
        
        Args:
            rule: Rule to check
            grid: Current grid state
            position: Position to apply rule
            
        Returns:
            True if rule can be applied
        """
        ax, ay = position
        
        # Bounds check
        if not (0 <= ax < grid.shape[0] and 0 <= ay < grid.shape[1]):
            return False
        
        # Get cell color
        cell_color = grid[ax, ay]
        
        # Check input color match
        if rule.input_color != -1 and rule.input_color != cell_color:
            return False
        
        # Type-specific checks
        if rule.condition_type == "EXTEND_COL":
            # Check if column has consistent color
            col_vals = grid[:, ay]
            unique = np.unique(col_vals)
            unique = unique[unique != 0]
            return len(unique) == 1
            
        elif rule.condition_type == "EXTEND_ROW":
            # Check if row has consistent color
            row_vals = grid[ax, :]
            unique = np.unique(row_vals)
            unique = unique[unique != 0]
            return len(unique) == 1
        
        return True
    
    def apply_single_rule(self, rule: TransformationRule, grid: np.ndarray,
                         position: Tuple[int, int]) -> Optional[np.ndarray]:
        """
        Apply a single rule and return new grid state.
        
        Args:
            rule: Rule to apply
            grid: Current grid
            position: Where to apply
            
        Returns:
            New grid state or None if rule doesn't apply
        """
        if not self.can_apply_rule(rule, grid, position):
            return None
        
        # Make a copy
        new_grid = grid.copy()
        ax, ay = position
        
        # Apply based on rule type
        if rule.condition_type in ["COLOR_SWAP", "GLOBAL_COLOR"]:
            # Simple color change
            new_grid[ax, ay] = rule.output_color
            
        elif rule.condition_type == "EXTEND_COL":
            # Extend entire column
            col_color = new_grid[:, ay]
            unique = np.unique(col_color)
            unique = unique[unique != 0]
            if len(unique) == 1:
                target_color = rule.output_color if rule.output_color != -1 else int(unique[0])
                new_grid[:, ay] = target_color
                
        elif rule.condition_type == "EXTEND_ROW":
            # Extend entire row
            row_color = new_grid[ax, :]
            unique = np.unique(row_color)
            unique = unique[unique != 0]
            if len(unique) == 1:
                target_color = rule.output_color if rule.output_color != -1 else int(unique[0])
                new_grid[ax, :] = target_color
        
        # Check if state actually changed
        if np.array_equal(new_grid, grid):
            return None
            
        return new_grid
    
    def find_enabled_rules(self, rules: List[TransformationRule], 
                          current_grid: np.ndarray,
                          previous_grid: np.ndarray,
                          position: Tuple[int, int]) -> List[TransformationRule]:
        """
        Find rules that are NOW applicable but weren't before.
        
        This is the key insight: Rule A changes the grid,
        which may ENABLE Rule B to apply.
        
        Args:
            rules: All available rules
            current_grid: Grid after last rule
            previous_grid: Grid before last rule
            position: Current position
            
        Returns:
            List of newly enabled rules
        """
        enabled = []
        
        for rule in rules:
            # Skip if we've already applied this rule type
            # (prevents immediate loops)
            if rule.condition_type in self.applied_rule_types:
                continue
            
            # Was it applicable before?
            was_applicable = self.can_apply_rule(rule, previous_grid, position)
            
            # Is it applicable now?
            is_applicable = self.can_apply_rule(rule, current_grid, position)
            
            # Newly enabled?
            if is_applicable and not was_applicable:
                enabled.append(rule)
        
        return enabled
    
    def apply_rules_compositionally(self, rules: List[TransformationRule],
                                   grid: np.ndarray,
                                   position: Tuple[int, int],
                                   depth: int = 0) -> Tuple[np.ndarray, List[RuleApplication]]:
        """
        Apply rules compositionally with recursive chaining.
        
        Algorithm:
        1. Try each rule at current position
        2. If rule applies and changes state:
           a. Record application
           b. Check for newly enabled rules
           c. Recursively apply enabled rules
        3. Return final state + application trace
        
        Args:
            rules: Available rules
            grid: Current grid state
            position: Position to apply rules
            depth: Current recursion depth
            
        Returns:
            (final_grid, application_history)
        """
        if depth >= self.max_depth:
            # Hit depth limit
            return grid, []
        
        current_state = grid.copy()
        applications = []
        
        for rule in rules:
            # Try to apply this rule
            new_state = self.apply_single_rule(rule, current_state, position)
            
            if new_state is not None:
                # Rule applied successfully!
                
                # Record application
                app = RuleApplication(
                    rule=rule,
                    position=position,
                    previous_state=current_state.copy(),
                    new_state=new_state.copy(),
                    timestamp=depth
                )
                applications.append(app)
                
                # Mark this rule type as used
                self.applied_rule_types.add(rule.condition_type)
                
                # Find rules that are NOW enabled
                enabled_rules = self.find_enabled_rules(
                    rules, new_state, current_state, position
                )
                
                if enabled_rules:
                    # Chain! Apply newly enabled rules
                    final_state, chained_apps = self.apply_rules_compositionally(
                        enabled_rules, new_state, position, depth + 1
                    )
                    current_state = final_state
                    applications.extend(chained_apps)
                else:
                    # No chaining, just update state
                    current_state = new_state
        
        return current_state, applications
    
    def reset(self):
        """Reset for new position"""
        self.execution_history = []
        self.applied_rule_types = set()
