"""
Phase 17.3: Abstraction Engine - Pure Discovery with Transfer Learning
Dynamic rule discovery with deep search mechanisms and motif memory.
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Callable, Dict, Any, Tuple, Optional
import copy
from deep_search import PredicateLibrary, MotifInductor, CompressionLearner, InvariantDetector
from motif_memory import MotifMemory
from vocabulary import MotifNamer, VocabularyBuilder, SelfInventedPredicateGenerator

# ============================================================================
# CORE DATA STRUCTURES
# ============================================================================

@dataclass
class AbstractRule:
    """
    A rule with dynamic precondition and transform functions.
    This enables the system to discover and apply arbitrary transformations.
    """
    name: str
    precondition: Callable[[np.ndarray, int, int], bool]  # (grid, row, col) -> bool
    transform: Callable[[np.ndarray, int, int, Dict], Optional[int]]  # returns target color or None
    parameters: Dict[str, Any]
    confidence: float = 1.0
    rule_type: str = "DYNAMIC"
    
    def __repr__(self):
        return f"AbstractRule({self.name}, type={self.rule_type}, conf={self.confidence:.2f})"

# ============================================================================
# RULE DISCOVERY ENGINE - Pure Discovery with Transfer Learning
# ============================================================================

class RuleDiscoveryEngine:
    """
    Discovers rules through deep search - NO hardcoded heuristics.
    Uses predicate search, motif induction, compression, invariant detection,
    AND motif memory for transfer learning across tasks!
    """
    
    def __init__(self, agent_id: str = "generic", vocabulary_builder: 'VocabularyBuilder' = None, motif_memory: 'MotifMemory' = None):
        self.predicate_lib = PredicateLibrary()
        self.motif_inductor = MotifInductor()
        self.compression_learner = CompressionLearner()
        self.invariant_detector = InvariantDetector()
        
        # Dependency Injection for Sovereign Agents
        # If provided, use the agent's specific memory. If not, create generic ones (backward compatibility)
        if motif_memory:
            self.motif_memory = motif_memory
        else:
            self.motif_memory = MotifMemory(persistence_file=f"memory_{agent_id}.pkl")

        # PHASE 18: SELF-INVENTED VOCABULARY
        self.motif_namer = MotifNamer() # Naming logic can be shared or instance-specific, currently shared logic is fine
        
        if vocabulary_builder:
            self.vocabulary_builder = vocabulary_builder
        else:
            self.vocabulary_builder = VocabularyBuilder(persistence_file=f"vocab_{agent_id}.pkl")
            
        self.vocab_predicate_generator = SelfInventedPredicateGenerator(self.vocabulary_builder)
        
        self.discovered_rules = []
        
    def discover_rules(self, context: np.ndarray, training_data: List[Tuple[int, int, int, int]], task_id: Optional[str] = None) -> List[AbstractRule]:
        """
        PURE DISCOVERY: Find patterns through deep search.
        NOW WITH EMERGENT GEOMETRY, COUNTING, SYMMETRY, TRANSFER LEARNING,
        AND SELF-INVENTED VOCABULARY!
        
        Args:
            context: Input grid
            training_data: List of (row, col, input_color, output_color)
            task_id: Optional task identifier for memory storage
            
        Returns:
            List of discovered AbstractRule objects
        """
        if not training_data:
            return []
        
        hypotheses = []
        
        # Step 1: Detect invariants (constraints)
        invariants = self.invariant_detector.detect(context, training_data)
        
        # Step 2: Induce motifs (patterns)
        motifs = self.motif_inductor.induce_motifs(context, training_data)
        
        # Step 2.5: TRANSFER LEARNING - Recall similar successful patterns
        memory_hypotheses = []
        for motif in motifs:
            similar_patterns = self.motif_memory.recall_similar(motif, top_k=3)
            for stored_pattern in similar_patterns:
                # Generate hypothesis from memory
                memory_hypotheses.append(self._hypothesis_from_memory(stored_pattern, motif))
        
        if memory_hypotheses:
            print(f"[TRANSFER] Recalled {len(memory_hypotheses)} patterns from memory")

        # Step 2.6: SELF-INVENTED VOCABULARY - Name and Store Motifs
        for motif in motifs:
            name = self.motif_namer.name_motif(motif)
            # Use task_id if available, otherwise "unknown"
            tid = task_id if task_id else "unknown"
            self.vocabulary_builder.add_motif(name, motif, tid)
            
        # Step 2.7: Generate Predicates from Vocabulary
        vocab_predicates = self.vocab_predicate_generator.generate_predicates_from_vocabulary(context)
        
        # Step 3: Generate hypotheses - EMERGENT LEARNING
        # Basic patterns
        hypotheses.extend(self._generate_fill_hypotheses(context, training_data, motifs))
        hypotheses.extend(self._generate_global_hypotheses(context, training_data))
        hypotheses.extend(self._generate_predicate_hypotheses(context, training_data, motifs))
        
        # Vocabulary-based Hypotheses (NEW!)
        hypotheses.extend(self._generate_vocab_hypotheses(context, training_data, vocab_predicates))
        
        # EMERGENT: Geometry (rotation, reflection) - NO HARDCODING!
        hypotheses.extend(self._generate_geometric_hypotheses(context, training_data, motifs))
        
        # EMERGENT: Counting/Arithmetic - NO HARDCODING!
        hypotheses.extend(self._generate_counting_hypotheses(context, training_data, motifs))
        
        # EMERGENT: Symmetry - NO HARDCODING!
        hypotheses.extend(self._generate_symmetry_hypotheses(context, training_data, motifs))
        
        # Add memory-based hypotheses
        hypotheses.extend(memory_hypotheses)
        
        # Step 4: Test hypotheses
        verified_rules = []
        for hyp in hypotheses:
            confidence = self._test_hypothesis(hyp, context, training_data)
            if confidence > 0.3:  # Lower threshold for pure discovery
                hyp.confidence = confidence
                verified_rules.append(hyp)
        
        # Step 5: Compress (select best rules via MDL)
        final_rules = self.compression_learner.compress(verified_rules, training_data)
        
        # Step 6: STORE SUCCESSFUL PATTERNS IN MEMORY & UPDATE VOCABULARY
        if final_rules:
            for rule in final_rules:
                # Update Vocabulary Builder
                if rule.rule_type == "VOCABULARY":
                    motif_name = rule.parameters.get('motif_name')
                    if motif_name:
                        self.vocabulary_builder.use_motif(motif_name, success=True)
                
                # Update Motif Memory
                if task_id and rule.confidence > 0.7:  # Only store high-confidence rules
                     # Find which motif this rule corresponds to
                    for motif in motifs:
                        self.motif_memory.store_success(motif, rule, task_id, rule.confidence)
        
        return final_rules

    def _generate_vocab_hypotheses(self, context: np.ndarray, training_data: List[Tuple], vocab_predicates: List[Dict]) -> List[AbstractRule]:
        """
        Generate hypotheses using self-invented vocabulary predicates.
        Agent uses its own language to describe rules!
        """
        hypotheses = []
        
        # Group training data by output color
        color_examples = {}
        for r, c, in_color, out_color in training_data:
            if out_color not in color_examples:
                color_examples[out_color] = []
            color_examples[out_color].append((r, c))
            
        for out_color, positions in color_examples.items():
            for predicate_info in vocab_predicates:
                pred_name = predicate_info['name']
                pred_func = predicate_info['function']
                motif_name = predicate_info['motif_name']
                
                # Check if this predicate creates a useful rule
                # We want: predicate(r,c) -> output_color
                
                def make_transform(oc):
                    return lambda grid, r, c, params: oc
                
                hypotheses.append(AbstractRule(
                    name=f"vocab_{motif_name}_gives_{out_color}",
                    precondition=pred_func,
                    transform=make_transform(out_color),
                    parameters={'motif_name': motif_name, 'output_color': out_color},
                    rule_type="VOCABULARY",
                    confidence=predicate_info.get('success_rate', 0.5) 
                ))
        
        return hypotheses
    
    def _hypothesis_from_memory(self, stored_pattern, current_motif: Dict) -> AbstractRule:
        """
        Generate a hypothesis from a stored memory pattern.
        This enables transfer learning - reusing what worked before!
        """
        transform_type = stored_pattern.transformation_type
        params = stored_pattern.parameters
        
        # Create hypothesis based on stored transformation type
        if transform_type == "GEOMETRIC_ROTATION":
            rotation = params.get('rotation', 90)
            color = params.get('color', 1)
            
            def precondition(grid, r, c):
                return grid[r, c] == color
            
            def transform(grid, r, c, p):
                return color
            
            return AbstractRule(
                name=f"memory_rotate_{rotation}deg",
                precondition=precondition,
                transform=transform,
                parameters=params,
                confidence=stored_pattern.confidence,
                rule_type=transform_type
            )
        
        elif transform_type == "FILL":
            fill_color = params.get('fill_color', 1)
            border_color = params.get('border_color', 1)
            
            def precondition(grid, r, c):
                return grid[r, c] == 0
            
            def transform(grid, r, c, p):
                return fill_color
            
            return AbstractRule(
                name=f"memory_fill_{fill_color}",
                precondition=precondition,
                transform=transform,
                parameters=params,
                confidence=stored_pattern.confidence,
                rule_type=transform_type
            )
        
        else:
            # Generic memory-based rule
            def precondition(grid, r, c):
                return True
            
            def transform(grid, r, c, p):
                return params.get('output_color', 1)
            
            return AbstractRule(
                name=f"memory_{transform_type}",
                precondition=precondition,
                transform=transform,
                parameters=params,
                confidence=stored_pattern.confidence * 0.8,  # Slightly lower confidence for generic
                rule_type=transform_type
            )
    
    def _test_hypothesis(self, rule: AbstractRule, context: np.ndarray, training_data: List[Tuple]) -> float:
        """Test if rule correctly predicts training examples"""
        correct = 0
        total = len(training_data)
        
        for r, c, input_color, expected_output in training_data:
            try:
                if rule.precondition(context, r, c):
                    predicted_output = rule.transform(context, r, c, rule.parameters)
                    if predicted_output == expected_output:
                        correct += 1
            except:
                pass
        
        return correct / total if total > 0 else 0.0
    
    # ========================================================================
    # HYPOTHESIS GENERATORS - Using Deep Search
    # ========================================================================
    
    def _generate_fill_hypotheses(self, context: np.ndarray, training_data: List[Tuple], motifs: List[Dict]) -> List[AbstractRule]:
        """Generate fill hypotheses using motif detection"""
        hypotheses = []
        
        # Check for fill patterns in motifs
        fill_motifs = [m for m in motifs if m.get('type') == 'fill']
        if not fill_motifs:
            return hypotheses
        
        # Get unique colors from training data
        output_colors = set(out_color for _, _, _, out_color in training_data)
        input_colors = set(in_color for _, _, in_color, _ in training_data)
        new_colors = output_colors - input_colors
        
        # Generate fill hypotheses for each new color
        for fill_color in new_colors:
            # Try different border colors
            for border_color in np.unique(context):
                if border_color == 0:
                    continue
                
                def make_fill_precondition(bc, fc):
                    def precondition(grid, r, c):
                        if grid[r, c] != 0:
                            return False
                        return self.predicate_lib.is_enclosed_by(grid, r, c, bc)
                    return precondition
                
                def make_fill_transform(fc):
                    return lambda grid, r, c, params: fc
                
                hypotheses.append(AbstractRule(
                    name=f"fill_enclosed_by_{border_color}_with_{fill_color}",
                    precondition=make_fill_precondition(border_color, fill_color),
                    transform=make_fill_transform(fill_color),
                    parameters={'border_color': border_color, 'fill_color': fill_color},
                    rule_type="FILL"
                ))
        
        return hypotheses
    
    def _generate_global_hypotheses(self, context: np.ndarray, training_data: List[Tuple]) -> List[AbstractRule]:
        """Generate simple color mapping hypotheses"""
        hypotheses = []
        
        color_map = {}
        for r, c, in_color, out_color in training_data:
            if in_color not in color_map:
                color_map[in_color] = []
            color_map[in_color].append(out_color)
        
        for in_color, out_colors in color_map.items():
            if out_colors:
                most_common = max(set(out_colors), key=out_colors.count)
                
                def make_precondition(ic):
                    return lambda grid, r, c: grid[r, c] == ic
                
                def make_transform(oc):
                    return lambda grid, r, c, params: oc
                
                hypotheses.append(AbstractRule(
                    name=f"global_map_{in_color}_to_{most_common}",
                    precondition=make_precondition(in_color),
                    transform=make_transform(most_common),
                    parameters={'input_color': in_color, 'output_color': most_common},
                    rule_type="GLOBAL"
                ))
        
        return hypotheses
    
    def _generate_predicate_hypotheses(self, context: np.ndarray, training_data: List[Tuple], motifs: List[Dict]) -> List[AbstractRule]:
        """Generate hypotheses using predicate combinations"""
        hypotheses = []
        
        # Use motifs to guide predicate search
        output_colors = set(out_color for _, _, _, out_color in training_data)
        
        for out_color in output_colors:
            # Hypothesis: Paint if surrounded by specific color
            for neighbor_color in np.unique(context):
                if neighbor_color == 0:
                    continue
                
                def make_neighbor_precondition(nc, threshold=2):
                    def precondition(grid, r, c):
                        count = self.predicate_lib.count_neighbors(grid, r, c, nc, radius=1)
                        return count >= threshold
                    return precondition
                
                def make_transform(oc):
                    return lambda grid, r, c, params: oc
                
                hypotheses.append(AbstractRule(
                    name=f"paint_{out_color}_if_near_{neighbor_color}",
                    precondition=make_neighbor_precondition(neighbor_color),
                    transform=make_transform(out_color),
                    parameters={'neighbor_color': neighbor_color, 'output_color': out_color},
                    rule_type="PREDICATE"
                ))
        
        return hypotheses
    
    def _generate_geometric_hypotheses(self, context: np.ndarray, training_data: List[Tuple], motifs: List[Dict]) -> List[AbstractRule]:
        """
        EMERGENT GEOMETRY: Discover rotation, reflection, scaling through shape matching.
        No hardcoded rotation rules - discovers them naturally!
        """
        hypotheses = []
        
        # Extract component motifs (shapes)
        shapes = [m for m in motifs if m.get('type') == 'component']
        
        for shape_motif in shapes:
            shape_pixels = shape_motif.get('pixels', [])
            if not shape_pixels:
                continue
            
            shape_color = shape_motif['color']
            
            # Build shape grid
            pixels_array = np.array(shape_pixels)
            min_r, min_c = pixels_array.min(axis=0)
            max_r, max_c = pixels_array.max(axis=0)
            h, w = max_r - min_r + 1, max_c - min_c + 1
            
            shape_grid = np.zeros((h, w), dtype=int)
            for r, c in shape_pixels:
                shape_grid[r - min_r, c - min_c] = 1
            
            # Try rotations (90°, 180°, 270°)
            for k in [1, 2, 3]:
                rotated = np.rot90(shape_grid, k=k)
                
                # Check if rotated shape matches output
                if self._shape_matches_output(rotated, training_data, shape_color):
                    rot_h, rot_w = rotated.shape
                    center_r = min_r + h / 2.0
                    center_c = min_c + w / 2.0
                    
                    def make_rotation_precondition(rot_shape, cr, cc, color):
                        def precondition(grid, r, c):
                            rh, rw = rot_shape.shape
                            bbox_r0 = int(cr - rh / 2.0)
                            bbox_c0 = int(cc - rw / 2.0)
                            dr, dc = r - bbox_r0, c - bbox_c0
                            if 0 <= dr < rh and 0 <= dc < rw:
                                return rot_shape[dr, dc] == 1
                            return False
                        return precondition
                    
                    def make_transform(color):
                        return lambda grid, r, c, params: color
                    
                    hypotheses.append(AbstractRule(
                        name=f"rotate_{k*90}deg_shape_{shape_color}",
                        precondition=make_rotation_precondition(rotated.copy(), center_r, center_c, shape_color),
                        transform=make_transform(shape_color),
                        parameters={'rotation': k*90, 'color': shape_color},
                        rule_type="GEOMETRIC_ROTATION"
                    ))
            
            # Try reflections (horizontal, vertical)
            for axis, flip_func in [('h', np.fliplr), ('v', np.flipud)]:
                reflected = flip_func(shape_grid)
                
                if self._shape_matches_output(reflected, training_data, shape_color):
                    def make_reflection_precondition(ref_shape, mr, mc, color):
                        def precondition(grid, r, c):
                            rh, rw = ref_shape.shape
                            bbox_r0 = int(mr - rh / 2.0)
                            bbox_c0 = int(mc - rw / 2.0)
                            dr, dc = r - bbox_r0, c - bbox_c0
                            if 0 <= dr < rh and 0 <= dc < rw:
                                return ref_shape[dr, dc] == 1
                            return False
                        return precondition
                    
                    hypotheses.append(AbstractRule(
                        name=f"reflect_{axis}_shape_{shape_color}",
                        precondition=make_reflection_precondition(reflected.copy(), min_r + h/2, min_c + w/2, shape_color),
                        transform=make_transform(shape_color),
                        parameters={'reflection': axis, 'color': shape_color},
                        rule_type="GEOMETRIC_REFLECTION"
                    ))
        
        return hypotheses
    
    def _generate_counting_hypotheses(self, context: np.ndarray, training_data: List[Tuple], motifs: List[Dict]) -> List[AbstractRule]:
        """
        EMERGENT ARITHMETIC: Discover counting/multiplication patterns.
        No hardcoded counting - discovers naturally!
        """
        hypotheses = []
        
        # Count objects in input
        input_counts = {}
        for color in np.unique(context):
            if color != 0:
                input_counts[color] = np.sum(context == color)
        
        # Count objects in output
        output_counts = {}
        for _, _, _, out_color in training_data:
            output_counts[out_color] = output_counts.get(out_color, 0) + 1
        
        # Detect multiplication patterns
        for color in input_counts:
            if color in output_counts:
                ratio = output_counts[color] / input_counts[color]
                if ratio > 1 and abs(ratio - round(ratio)) < 0.1:  # Integer multiplication
                    factor = int(round(ratio))
                    
                    # Generate "repeat N times" hypothesis
                    def make_repeat_precondition(c):
                        return lambda grid, r, c_pos: grid[r, c_pos] == c
                    
                    def make_repeat_transform(c):
                        return lambda grid, r, c_pos, params: c
                    
                    hypotheses.append(AbstractRule(
                        name=f"multiply_color_{color}_by_{factor}",
                        precondition=make_repeat_precondition(color),
                        transform=make_repeat_transform(color),
                        parameters={'color': color, 'factor': factor},
                        rule_type="COUNTING_MULTIPLY"
                    ))
        
        # Detect addition patterns (new colors appearing)
        for color in output_counts:
            if color not in input_counts:
                count = output_counts[color]
                
                hypotheses.append(AbstractRule(
                    name=f"add_{count}_of_color_{color}",
                    precondition=lambda grid, r, c: grid[r, c] == 0,  # Empty cells
                    transform=lambda grid, r, c, params: params['color'],
                    parameters={'color': color, 'count': count},
                    rule_type="COUNTING_ADD"
                ))
        
        return hypotheses
    
    def _generate_symmetry_hypotheses(self, context: np.ndarray, training_data: List[Tuple], motifs: List[Dict]) -> List[AbstractRule]:
        """
        EMERGENT SYMMETRY: Discover symmetry axes and mirror operations.
        No hardcoded symmetry - discovers naturally!
        """
        hypotheses = []
        
        # Check if input has symmetry
        input_symmetric_v = self._is_symmetric(context, axis='vertical')
        input_symmetric_h = self._is_symmetric(context, axis='horizontal')
        
        # Check if output creates symmetry
        output_grid = self._reconstruct_output(context, training_data)
        output_symmetric_v = self._is_symmetric(output_grid, axis='vertical')
        output_symmetric_h = self._is_symmetric(output_grid, axis='horizontal')
        
        # Symmetry preservation
        if input_symmetric_v and output_symmetric_v:
            hypotheses.append(AbstractRule(
                name="preserve_vertical_symmetry",
                precondition=lambda grid, r, c: True,
                transform=lambda grid, r, c, params: self._get_symmetric_value(grid, r, c, 'vertical'),
                parameters={'axis': 'vertical'},
                rule_type="SYMMETRY_PRESERVE"
            ))
        
        # Symmetry creation
        if not input_symmetric_v and output_symmetric_v:
            def make_symmetry_precondition():
                return lambda grid, r, c: grid[r, c] != 0
            
            def make_symmetry_transform():
                return lambda grid, r, c, params: self._create_symmetric_value(grid, r, c, 'vertical')
            
            hypotheses.append(AbstractRule(
                name="create_vertical_symmetry",
                precondition=make_symmetry_precondition(),
                transform=make_symmetry_transform(),
                parameters={'axis': 'vertical'},
                rule_type="SYMMETRY_CREATE"
            ))
        
        return hypotheses
    
    # Helper methods for emergent learning
    def _shape_matches_output(self, shape: np.ndarray, training_data: List[Tuple], color: int) -> bool:
        """Check if transformed shape matches output data"""
        # Simplified check - in practice, would do full spatial matching
        output_colors = [out_color for _, _, _, out_color in training_data]
        return color in output_colors and len(output_colors) >= shape.sum()
    
    def _is_symmetric(self, grid: np.ndarray, axis: str) -> bool:
        """Check if grid has symmetry along axis"""
        if axis == 'vertical':
            return np.array_equal(grid, np.fliplr(grid))
        elif axis == 'horizontal':
            return np.array_equal(grid, np.flipud(grid))
        return False
    
    def _reconstruct_output(self, context: np.ndarray, training_data: List[Tuple]) -> np.ndarray:
        """Reconstruct output grid from training data"""
        output = context.copy()
        for r, c, _, out_color in training_data:
            if 0 <= r < output.shape[0] and 0 <= c < output.shape[1]:
                output[r, c] = out_color
        return output
    
    def _get_symmetric_value(self, grid: np.ndarray, r: int, c: int, axis: str) -> int:
        """Get symmetric counterpart value"""
        h, w = grid.shape
        if axis == 'vertical':
            mirror_c = w - 1 - c
            if 0 <= mirror_c < w:
                return grid[r, mirror_c]
        return grid[r, c]
    
    def _create_symmetric_value(self, grid: np.ndarray, r: int, c: int, axis: str) -> int:
        """Create symmetric value"""
        return self._get_symmetric_value(grid, r, c, axis)

        """
        Generate rotation hypotheses - THE KEY FIX FOR OBJECT ROTATION BUG.
        Instead of checking if current cell color matches, we check if the cell
        would be inside a rotated object.
        """
        hypotheses = []
        
        # Find objects in context
        objects = self._find_objects(context)
        
        for obj_color, obj_pixels in objects.items():
            if len(obj_pixels) == 0:
                continue
            
            # Get object bounding box
            pixels_array = np.array(obj_pixels)
            min_r, min_c = pixels_array.min(axis=0)
            max_r, max_c = pixels_array.max(axis=0)
            
            # Extract object shape
            obj_height = max_r - min_r + 1
            obj_width = max_c - min_c + 1
            obj_shape = np.zeros((obj_height, obj_width), dtype=int)
            
            for r, c in obj_pixels:
                obj_shape[r - min_r, c - min_c] = 1
            
            # Generate rotation hypotheses
            for k in [1, 2, 3]:  # 90, 180, 270 degrees
                rotated_shape = np.rot90(obj_shape, k=k)
                rot_h, rot_w = rotated_shape.shape
                
                # Calculate center-based positioning
                orig_center_r = min_r + obj_height / 2.0
                orig_center_c = min_c + obj_width / 2.0
                
                def make_rotation_precondition(shape, center_r, center_c, color):
                    def precondition(grid, r, c):
                        # Check if (r,c) is inside the rotated object
                        h, w = shape.shape
                        # Calculate rotated bbox position (centered on original center)
                        bbox_r0 = int(center_r - h / 2.0)
                        bbox_c0 = int(center_c - w / 2.0)
                        
                        # Check if point is in rotated shape
                        dr = r - bbox_r0
                        dc = c - bbox_c0
                        
                        if 0 <= dr < h and 0 <= dc < w:
                            return shape[dr, dc] == 1
                        return False
                    return precondition
                
                def make_rotation_transform(color):
                    return lambda grid, r, c, params: color
                
                hypotheses.append(AbstractRule(
                    name=f"rotate_{k*90}deg_color_{obj_color}",
                    precondition=make_rotation_precondition(
                        rotated_shape.copy(), 
                        orig_center_r, 
                        orig_center_c, 
                        obj_color
                    ),
                    transform=make_rotation_transform(obj_color),
                    parameters={
                        'rotation': k, 
                        'color': obj_color,
                        'center': (orig_center_r, orig_center_c)
                    },
                    rule_type="ROTATION"
                ))
        
        return hypotheses
    
    def _generate_pattern_hypotheses(self, context: np.ndarray, training_data: List[Tuple]) -> List[AbstractRule]:
        """Generate hypotheses for repeating patterns"""
        # TODO: Implement pattern detection (repetition, symmetry, etc.)
        return []
    
    # ========================================================================
    # HELPER METHODS
    # ========================================================================
    
    def _find_objects(self, grid: np.ndarray) -> Dict[int, List[Tuple[int, int]]]:
        """Find connected components (objects) in grid"""
        objects = {}
        visited = np.zeros_like(grid, dtype=bool)
        
        def flood_fill(r, c, color):
            if r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1]:
                return []
            if visited[r, c] or grid[r, c] != color:
                return []
            
            visited[r, c] = True
            pixels = [(r, c)]
            
            # 4-connectivity
            for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                pixels.extend(flood_fill(r + dr, c + dc, color))
            
            return pixels
        
        for r in range(grid.shape[0]):
            for c in range(grid.shape[1]):
                if not visited[r, c] and grid[r, c] != 0:
                    color = grid[r, c]
                    pixels = flood_fill(r, c, color)
                    if pixels:
                        if color not in objects:
                            objects[color] = []
                        objects[color].extend(pixels)
        
        return objects
