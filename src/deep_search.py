"""
Phase 17.2: Pure Discovery - Deep Search Implementation
Predicate library, motif induction, compression learning, and invariant detection.
Zero hardcoded rules - agents learn through abstraction.
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Callable, Dict, Any, Tuple, Optional, Set
import copy
from collections import deque

# ============================================================================
# PREDICATE LIBRARY - Rich Vocabulary for Pattern Discovery
# ============================================================================

class PredicateLibrary:
    """
    Library of atomic predicates that can be combined to describe patterns.
    These are the building blocks for rule discovery.
    """
    
    @staticmethod
    def is_enclosed_by(grid: np.ndarray, r: int, c: int, color: int) -> bool:
        """Check if cell is enclosed by a specific color"""
        if grid[r, c] == color:
            return False
        
        # Flood fill from borders to find reachable cells
        visited = np.zeros_like(grid, dtype=bool)
        queue = deque()
        
        # Add all border cells to queue
        h, w = grid.shape
        for i in range(h):
            queue.append((i, 0))
            queue.append((i, w-1))
        for j in range(w):
            queue.append((0, j))
            queue.append((h-1, j))
        
        # BFS from borders
        while queue:
            cr, cc = queue.popleft()
            if cr < 0 or cr >= h or cc < 0 or cc >= w:
                continue
            if visited[cr, cc] or grid[cr, cc] == color:
                continue
            
            visited[cr, cc] = True
            queue.append((cr-1, cc))
            queue.append((cr+1, cc))
            queue.append((cr, cc-1))
            queue.append((cr, cc+1))
        
        # If cell not visited, it's enclosed
        return not visited[r, c]
    
    @staticmethod
    def distance_to_nearest(grid: np.ndarray, r: int, c: int, color: int) -> int:
        """BFS to find distance to nearest cell of color"""
        if grid[r, c] == color:
            return 0
        
        visited = np.zeros_like(grid, dtype=bool)
        queue = deque([(r, c, 0)])
        visited[r, c] = True
        
        while queue:
            cr, cc, dist = queue.popleft()
            
            for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                nr, nc = cr + dr, cc + dc
                if 0 <= nr < grid.shape[0] and 0 <= nc < grid.shape[1]:
                    if grid[nr, nc] == color:
                        return dist + 1
                    if not visited[nr, nc]:
                        visited[nr, nc] = True
                        queue.append((nr, nc, dist + 1))
        
        return 999  # Not found
    
    @staticmethod
    def count_neighbors(grid: np.ndarray, r: int, c: int, color: int, radius: int = 1) -> int:
        """Count cells of color within radius"""
        count = 0
        for dr in range(-radius, radius+1):
            for dc in range(-radius, radius+1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < grid.shape[0] and 0 <= nc < grid.shape[1]:
                    if grid[nr, nc] == color:
                        count += 1
        return count
    
    @staticmethod
    def is_on_line(grid: np.ndarray, r: int, c: int, color: int) -> bool:
        """Check if cell is on a horizontal or vertical line of color"""
        # Check horizontal
        row = grid[r, :]
        if np.sum(row == color) >= 3:  # At least 3 cells in a line
            return True
        
        # Check vertical
        col = grid[:, c]
        if np.sum(col == color) >= 3:
            return True
        
        return False
    
    @staticmethod
    def has_symmetry(grid: np.ndarray, r: int, c: int, axis: str = 'vertical') -> bool:
        """Check if cell has symmetric counterpart"""
        h, w = grid.shape
        
        if axis == 'vertical':
            # Mirror across vertical center
            mirror_c = w - 1 - c
            if 0 <= mirror_c < w:
                return grid[r, c] == grid[r, mirror_c]
        elif axis == 'horizontal':
            # Mirror across horizontal center
            mirror_r = h - 1 - r
            if 0 <= mirror_r < h:
                return grid[r, c] == grid[mirror_r, c]
        
        return False

# ============================================================================
# MOTIF INDUCTOR - Pattern Discovery
# ============================================================================

class MotifInductor:
    """
    Discovers recurring patterns (motifs) in transformations.
    """
    
    def induce_motifs(self, context: np.ndarray, training_data: List[Tuple]) -> List[Dict]:
        """Find common patterns in the data"""
        motifs = []
        
        # Detect geometric shapes
        motifs.extend(self._detect_rectangles(context))
        motifs.extend(self._detect_connected_components(context))
        
        # Detect transformation patterns
        motifs.extend(self._detect_fill_patterns(context, training_data))
        
        return motifs
    
    def _detect_rectangles(self, grid: np.ndarray) -> List[Dict]:
        """Find rectangular regions of single colors"""
        rectangles = []
        unique_colors = np.unique(grid)
        
        for color in unique_colors:
            if color == 0:  # Skip background
                continue
            
            # Find bounding boxes of color regions
            coords = np.argwhere(grid == color)
            if len(coords) > 0:
                min_r, min_c = coords.min(axis=0)
                max_r, max_c = coords.max(axis=0)
                
                # Check if it forms a rectangle
                region = grid[min_r:max_r+1, min_c:max_c+1]
                if np.all(region == color):
                    rectangles.append({
                        'type': 'rectangle',
                        'color': int(color),
                        'bbox': (min_r, min_c, max_r, max_c)
                    })
        
        return rectangles
    
    def _detect_connected_components(self, grid: np.ndarray) -> List[Dict]:
        """Find connected regions (objects)"""
        components = []
        visited = np.zeros_like(grid, dtype=bool)
        
        def flood_fill(r, c, color):
            if r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1]:
                return []
            if visited[r, c] or grid[r, c] != color:
                return []
            
            visited[r, c] = True
            pixels = [(r, c)]
            
            for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                pixels.extend(flood_fill(r + dr, c + dc, color))
            
            return pixels
        
        for r in range(grid.shape[0]):
            for c in range(grid.shape[1]):
                if not visited[r, c] and grid[r, c] != 0:
                    color = grid[r, c]
                    pixels = flood_fill(r, c, color)
                    if pixels:
                        components.append({
                            'type': 'component',
                            'color': int(color),
                            'pixels': pixels,
                            'size': len(pixels)
                        })
        
        return components
    
    def _detect_fill_patterns(self, context: np.ndarray, training_data: List[Tuple]) -> List[Dict]:
        """Detect if pattern is filling empty regions"""
        patterns = []
        
        # Check if outputs are filling zeros in input
        filled_colors = set()
        for r, c, in_color, out_color in training_data:
            if in_color == 0 and out_color != 0:
                filled_colors.add(out_color)
        
        if filled_colors:
            patterns.append({
                'type': 'fill',
                'fill_colors': list(filled_colors)
            })
        
        return patterns

# ============================================================================
# COMPRESSION LEARNER - Minimum Description Length
# ============================================================================

class CompressionLearner:
    """
    Selects rules that minimize total description length (MDL principle).
    Best rule = shortest description of data.
    """
    
    def compress(self, candidate_rules: List, training_data: List[Tuple]) -> List:
        """Select rules via compression"""
        if not candidate_rules:
            return []
        
        # Score each rule
        scored_rules = []
        for rule in candidate_rules:
            score = self._mdl_score(rule, training_data)
            scored_rules.append((rule, score))
        
        # Sort by score (lower is better)
        scored_rules.sort(key=lambda x: x[1])
        
        # Return top rules
        return [r for r, s in scored_rules[:10]]  # Top 10
    
    def _mdl_score(self, rule, training_data: List[Tuple]) -> float:
        """
        Minimum Description Length score.
        MDL = rule_complexity + exception_cost
        """
        # Rule complexity (simpler rules are better)
        rule_complexity = 1.0  # Base cost
        
        # Exception cost (how many points does rule NOT explain)
        exceptions = 0
        for r, c, in_color, out_color in training_data:
            # Simplified: assume rule doesn't explain if confidence < 1
            if hasattr(rule, 'confidence') and rule.confidence < 1.0:
                exceptions += 1
        
        exception_cost = exceptions * 2.0  # Penalty per exception
        
        return rule_complexity + exception_cost

# ============================================================================
# INVARIANT DETECTOR
# ============================================================================

class InvariantDetector:
    """
    Finds properties preserved across transformations.
    """
    
    def detect(self, context: np.ndarray, training_data: List[Tuple]) -> List[Dict]:
        """Find invariants"""
        invariants = []
        
        # Check color count preservation
        input_colors = {}
        output_colors = {}
        
        for r, c, in_color, out_color in training_data:
            input_colors[in_color] = input_colors.get(in_color, 0) + 1
            output_colors[out_color] = output_colors.get(out_color, 0) + 1
        
        # Check if any color count is preserved
        for color in input_colors:
            if color in output_colors and input_colors[color] == output_colors[color]:
                invariants.append({
                    'type': 'color_count_preserved',
                    'color': color,
                    'count': input_colors[color]
                })
        
        return invariants
