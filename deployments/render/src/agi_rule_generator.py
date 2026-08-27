"""
Universal Rule Generator for AGI Systems
Inspired by Theory of Everything approach - one unified framework
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Callable, Dict, Any, Tuple
from enum import Enum
import copy

# ============================================================================
# PART 1: CORE PRIMITIVES (The "Physics" of the System)
# ============================================================================

class Transform(Enum):
    """Basic transformation operations"""
    IDENTITY = "identity"
    FILL = "fill"
    ROTATE_90 = "rotate_90"
    REFLECT_H = "reflect_horizontal"
    REFLECT_V = "reflect_vertical"
    COUNT = "count"
    SCALE = "scale"
    TRANSLATE = "translate"
    COMPOSE = "compose"

@dataclass
class Rule:
    """
    A rule is a transformation with conditions
    Rule = (Precondition, Transform, Parameters)
    """
    name: str
    precondition: Callable[[np.ndarray], bool]
    transform: Callable[[np.ndarray, Dict], np.ndarray]
    parameters: Dict[str, Any]
    confidence: float = 1.0
    
    def __repr__(self):
        return f"Rule({self.name}, conf={self.confidence:.2f})"

# ============================================================================
# PART 2: ATOMIC TRANSFORMATIONS (Building Blocks)
# ============================================================================

class AtomicTransforms:
    """Library of atomic transformations"""
    
    @staticmethod
    def fill_enclosed(grid: np.ndarray, params: Dict) -> np.ndarray:
        """Fill enclosed regions with specified color"""
        result = grid.copy()
        border_color = params.get('border_color', 3)
        fill_color = params.get('fill_color', 4)
        
        # Find enclosed regions (simplified - flood fill from borders)
        visited = np.zeros_like(grid, dtype=bool)
        
        def is_enclosed(r, c):
            if visited[r, c] or grid[r, c] == border_color:
                return False
            # Check if reachable from border
            # (Simplified: just check if surrounded)
            neighbors = [
                (r-1, c), (r+1, c), (r, c-1), (r, c+1)
            ]
            border_found = False
            for nr, nc in neighbors:
                if 0 <= nr < grid.shape[0] and 0 <= nc < grid.shape[1]:
                    if grid[nr, nc] == border_color:
                        border_found = True
            return border_found
        
        for r in range(1, grid.shape[0]-1):
            for c in range(1, grid.shape[1]-1):
                if grid[r, c] == 0:  # Empty cell
                    # Check if it's inside a rectangle
                    if (grid[r-1, c] == border_color or grid[r+1, c] == border_color) and \
                       (grid[r, c-1] == border_color or grid[r, c+1] == border_color):
                        # Simple heuristic: if bordered, fill
                        result[r, c] = fill_color
        
        return result
    
    @staticmethod
    def rotate_90(grid: np.ndarray, params: Dict) -> np.ndarray:
        """Rotate grid 90 degrees clockwise"""
        return np.rot90(grid, k=-1)
    
    @staticmethod
    def reflect_horizontal(grid: np.ndarray, params: Dict) -> np.ndarray:
        """Reflect horizontally"""
        return np.fliplr(grid)
    
    @staticmethod
    def count_objects(grid: np.ndarray, params: Dict) -> int:
        """Count distinct objects of a color"""
        target_color = params.get('color', 3)
        # Simplified: count connected components
        visited = np.zeros_like(grid, dtype=bool)
        count = 0
        
        def flood_fill(r, c):
            if r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1]:
                return
            if visited[r, c] or grid[r, c] != target_color:
                return
            visited[r, c] = True
            flood_fill(r-1, c)
            flood_fill(r+1, c)
            flood_fill(r, c-1)
            flood_fill(r, c+1)
        
        for r in range(grid.shape[0]):
            for c in range(grid.shape[1]):
                if grid[r, c] == target_color and not visited[r, c]:
                    flood_fill(r, c)
                    count += 1
        
        return count
    
    @staticmethod
    def compose(transforms: List[Callable], grid: np.ndarray, params: Dict) -> np.ndarray:
        """Compose multiple transformations"""
        result = grid.copy()
        for t in transforms:
            result = t(result, params)
        return result

# ============================================================================
# PART 3: RULE DISCOVERY ENGINE
# ============================================================================

class RuleDiscoveryEngine:
    """
    Discovers rules from input/output examples using:
    1. Difference analysis (what changed?)
    2. Pattern matching (what patterns exist?)
    3. Hypothesis generation (what rule explains this?)
    4. Verification (does rule work on all examples?)
    """
    
    def __init__(self):
        self.atomic_transforms = AtomicTransforms()
        self.discovered_rules = []
        
    def discover_rules(self, examples: List[Tuple[np.ndarray, np.ndarray]]) -> List[Rule]:
        """
        Discover rules from input-output examples
        Returns ranked list of candidate rules
        """
        candidates = []
        
        # 1. Analyze differences
        diff_patterns = self._analyze_differences(examples)
        
        # 2. Generate hypotheses
        hypotheses = self._generate_hypotheses(diff_patterns)
        
        # 3. Test hypotheses on all examples
        for hyp in hypotheses:
            score = self._test_hypothesis(hyp, examples)
            if score > 0.5:  # Threshold
                candidates.append((hyp, score))
        
        # 4. Rank by score
        candidates.sort(key=lambda x: x[1], reverse=True)
        
        return [rule for rule, score in candidates]
    
    def _analyze_differences(self, examples: List[Tuple]) -> Dict:
        """Analyze what changed between input and output"""
        patterns = {
            'cells_changed': [],
            'colors_added': [],
            'colors_removed': [],
            'shape_changes': []
        }
        
        for inp, out in examples:
            diff = (out != inp)
            patterns['cells_changed'].append(np.sum(diff))
            
            inp_colors = set(inp.flatten())
            out_colors = set(out.flatten())
            patterns['colors_added'].append(out_colors - inp_colors)
            patterns['colors_removed'].append(inp_colors - out_colors)
        
        return patterns
    
    def _generate_hypotheses(self, patterns: Dict) -> List[Rule]:
        """Generate rule hypotheses based on patterns"""
        hypotheses = []
        
        # Hypothesis 1: Fill operation (if color 4 added consistently)
        if all(4 in colors for colors in patterns['colors_added']):
            hypotheses.append(Rule(
                name="fill_enclosed_with_4",
                precondition=lambda g: 3 in g,  # Border exists
                transform=self.atomic_transforms.fill_enclosed,
                parameters={'border_color': 3, 'fill_color': 4}
            ))
        
        # Hypothesis 2: Rotation
        hypotheses.append(Rule(
            name="rotate_90",
            precondition=lambda g: True,
            transform=self.atomic_transforms.rotate_90,
            parameters={}
        ))
        
        # Hypothesis 3: Reflection
        hypotheses.append(Rule(
            name="reflect_h",
            precondition=lambda g: True,
            transform=self.atomic_transforms.reflect_horizontal,
            parameters={}
        ))
        
        # TODO: Add more sophisticated hypothesis generation
        # - Symmetry detection
        # - Object counting
        # - Conditional fills
        # - Compositional rules
        
        return hypotheses
    
    def _test_hypothesis(self, rule: Rule, examples: List[Tuple]) -> float:
        """Test if rule works on all examples, return accuracy"""
        correct = 0
        total = len(examples)
        
        for inp, expected_out in examples:
            try:
                if rule.precondition(inp):
                    predicted_out = rule.transform(inp, rule.parameters)
                    if np.array_equal(predicted_out, expected_out):
                        correct += 1
            except:
                pass  # Rule failed, skip
        
        return correct / total if total > 0 else 0.0

# ============================================================================
# PART 4: META-RULE GENERATOR (Self-Modification)
# ============================================================================

class MetaRuleGenerator:
    """
    Generates rules that create/modify other rules
    This is the "God equation" - rules about rules
    """
    
    def __init__(self):
        self.rule_space = []  # All known rules
        self.meta_rules = []  # Rules for creating rules
        
    def evolve_rule(self, rule: Rule, feedback: float) -> Rule:
        """
        Evolve a rule based on feedback
        Uses gradient-free optimization (evolutionary approach)
        """
        new_rule = copy.deepcopy(rule)
        
        if feedback < 0.5:  # Rule performing poorly
            # Mutate parameters
            for key in new_rule.parameters:
                if isinstance(new_rule.parameters[key], (int, float)):
                    # Add noise
                    noise = np.random.randn() * 0.1
                    new_rule.parameters[key] += noise
        
        # Adjust confidence
        new_rule.confidence = feedback
        
        return new_rule
    
    def compose_rules(self, rule1: Rule, rule2: Rule) -> Rule:
        """Create composite rule from two rules"""
        def composite_transform(grid, params):
            temp = rule1.transform(grid, rule1.parameters)
            return rule2.transform(temp, rule2.parameters)
        
        return Rule(
            name=f"compose_{rule1.name}_{rule2.name}",
            precondition=lambda g: rule1.precondition(g) and rule2.precondition(g),
            transform=composite_transform,
            parameters={**rule1.parameters, **rule2.parameters},
            confidence=min(rule1.confidence, rule2.confidence)
        )
    
    def generate_meta_rule(self, successful_rules: List[Rule]) -> Callable:
        """
        Generate a meta-rule from patterns in successful rules
        Returns a function that creates new rules
        """
        # Analyze what makes rules successful
        # Extract common patterns in:
        # - Preconditions
        # - Transform types
        # - Parameter ranges
        
        def meta_rule_factory(context: Dict) -> Rule:
            """Factory function that creates rules based on context"""
            # Example: If context suggests geometric pattern,
            # create rotation/reflection rules
            if context.get('geometric', False):
                return Rule(
                    name="auto_generated_geometric",
                    precondition=lambda g: True,
                    transform=AtomicTransforms.rotate_90,
                    parameters={}
                )
            # Add more sophisticated rule generation logic
            return None
        
        return meta_rule_factory

# ============================================================================
# PART 5: UNIFIED AGI SYSTEM
# ============================================================================

class UnifiedAGI:
    """
    The complete system that ties everything together
    One update rule governs: Prediction, Perception, Action, Learning
    """
    
    def __init__(self):
        self.discovery_engine = RuleDiscoveryEngine()
        self.meta_generator = MetaRuleGenerator()
        self.world_model = {}  # Beliefs about world
        self.rule_library = []  # Known rules
        self.state = None
        
    def god_equation(self, state: np.ndarray, observations: List, actions: List) -> Dict:
        """
        Unified update rule that handles everything
        
        Args:
            state: Current world state
            observations: New observations
            actions: Possible actions
            
        Returns:
            Updated beliefs, predictions, selected action, learned rules
        """
        # PERCEPTION: Update beliefs based on observations
        beliefs = self._update_beliefs(state, observations)
        
        # PREDICTION: Predict future states
        predictions = self._predict_future(state, beliefs)
        
        # ACTION: Select best action
        action = self._select_action(state, predictions, actions)
        
        # LEARNING: Discover/update rules
        new_rules = self._learn_rules(observations)
        
        return {
            'beliefs': beliefs,
            'predictions': predictions,
            'action': action,
            'learned_rules': new_rules
        }
    
    def _update_beliefs(self, state, observations):
        """Bayesian belief update"""
        # Simplified: Just store observations
        return {'observed': observations, 'uncertainty': 0.5}
    
    def _predict_future(self, state, beliefs):
        """Use learned rules to predict"""
        predictions = []
        for rule in self.rule_library:
            if rule.precondition(state):
                pred = rule.transform(state, rule.parameters)
                predictions.append((pred, rule.confidence))
        return predictions
    
    def _select_action(self, state, predictions, actions):
        """Choose action that maximizes expected value"""
        # Simplified: Random for now
        if actions:
            return np.random.choice(actions)
        return None
    
    def _learn_rules(self, observations):
        """Discover new rules from observations"""
        if len(observations) > 1:
            examples = [(observations[i], observations[i+1]) 
                       for i in range(len(observations)-1)]
            new_rules = self.discovery_engine.discover_rules(examples)
            self.rule_library.extend(new_rules)
            return new_rules
        return []
    
    def solve_arc_task(self, training_examples: List[Tuple]) -> Callable:
        """
        Solve an ARC task by discovering the rule
        Returns a function that transforms input to output
        """
        # Discover rules from training examples
        rules = self.discovery_engine.discover_rules(training_examples)
        
        if rules:
            best_rule = rules[0]  # Highest confidence
            print(f"Discovered rule: {best_rule}")
            
            # Return transformation function
            def solution(test_input):
                return best_rule.transform(test_input, best_rule.parameters)
            
            return solution
        else:
            print("No rule discovered!")
            return lambda x: x  # Identity

# ============================================================================
# PART 6: DEMONSTRATION
# ============================================================================

if __name__ == "__main__":
    # Example: Solve the rectangle-fill ARC task
    
    # Training example (simplified)
    train_input = np.array([
        [0, 0, 0, 0, 0, 0],
        [0, 0, 3, 0, 0, 0],
        [0, 3, 0, 3, 0, 0],
        [0, 0, 3, 0, 3, 0],
        [0, 0, 0, 3, 0, 0],
        [0, 0, 0, 0, 0, 0]
    ])
    
    train_output = np.array([
        [0, 0, 0, 0, 0, 0],
        [0, 0, 3, 0, 0, 0],
        [0, 3, 4, 3, 0, 0],
        [0, 0, 3, 4, 3, 0],
        [0, 0, 0, 3, 0, 0],
        [0, 0, 0, 0, 0, 0]
    ])
    
    # Initialize AGI
    agi = UnifiedAGI()
    
    # Learn from examples
    training_data = [(train_input, train_output)]
    solution_func = agi.solve_arc_task(training_data)
    
    # Test on new input
    test_input = np.array([
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 3, 3, 3, 3, 0, 0],
        [0, 0, 3, 0, 0, 3, 0, 0],
        [0, 0, 3, 0, 0, 3, 0, 0],
        [0, 0, 3, 3, 3, 3, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ])
    
    predicted_output = solution_func(test_input)
    
    print("Test Input:")
    print(test_input)
    print("\nPredicted Output:")
    print(predicted_output)
    
    # Demonstrate meta-learning
    print("\n=== Meta-Learning Demo ===")
    print(f"Rule library size: {len(agi.rule_library)}")
    
    # Show God equation in action
    observations = [train_input, train_output]
    result = agi.god_equation(train_input, observations, actions=['fill', 'rotate'])
    
    print(f"\nGod Equation Output:")
    print(f"Beliefs: {result['beliefs']}")
    print(f"Action: {result['action']}")
    print(f"New rules learned: {len(result['learned_rules'])}")
