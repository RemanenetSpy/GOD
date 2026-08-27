"""
Phase 18: Self-Invented Vocabulary - Motif Naming System
Agents discover patterns and name them, building their own vocabulary.
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

@dataclass
class NamedMotif:
    """A motif with a self-invented name"""
    name: str
    definition: Dict
    discovered_in: str
    usage_count: int = 0
    success_rate: float = 0.0

class MotifNamer:
    """
    Generates unique, descriptive names for discovered motifs.
    Names encode structural properties - agent's own vocabulary!
    """
    
    def name_motif(self, motif: Dict) -> str:
        """
        Create a descriptive name for a motif.
        
        Examples:
        - "rect_5x3_c2" (5x3 rectangle of color 2)
        - "L_shape_4px_c1" (L-shape, 4 pixels, color 1)
        - "diagonal_6_c3" (diagonal line, 6 cells, color 3)
        - "cross_5px_c4" (cross pattern, 5 pixels, color 4)
        
        This is the agent inventing its own language!
        """
        motif_type = motif.get('type', 'unknown')
        
        if motif_type == 'rectangle':
            return self._name_rectangle(motif)
        elif motif_type == 'component':
            return self._name_component(motif)
        elif motif_type == 'fill':
            return self._name_fill(motif)
        else:
            return f"{motif_type}_generic"
    
    def _name_rectangle(self, motif: Dict) -> str:
        """Name a rectangle motif"""
        bbox = motif.get('bbox', (0, 0, 1, 1))
        h = bbox[2] - bbox[0]
        w = bbox[3] - bbox[1]
        color = motif.get('color', 0)
        return f"rect_{h}x{w}_c{color}"
    
    def _name_component(self, motif: Dict) -> str:
        """Name a connected component motif"""
        size = motif.get('size', 0)
        color = motif.get('color', 0)
        pixels = motif.get('pixels', [])
        
        if not pixels:
            return f"component_{size}px_c{color}"
        
        # Compute shape signature
        shape_sig = self._compute_shape_signature(pixels)
        return f"{shape_sig}_{size}px_c{color}"
    
    def _name_fill(self, motif: Dict) -> str:
        """Name a fill pattern motif"""
        fill_colors = motif.get('fill_colors', [])
        border_color = motif.get('border_color', 0)
        
        if fill_colors:
            colors_str = '_'.join(map(str, sorted(fill_colors)))
            return f"fill_{colors_str}_border{border_color}"
        return "fill_generic"
    
    def _compute_shape_signature(self, pixels: List[Tuple[int, int]]) -> str:
        """
        Compute a signature for a shape.
        Agent discovers common patterns and names them!
        
        Examples:
        - "L_shape" for L-shaped patterns
        - "cross" for + patterns
        - "diagonal" for diagonal lines
        - "line_h" for horizontal lines
        - "line_v" for vertical lines
        """
        if len(pixels) < 2:
            return "single"
        
        # Convert to numpy array
        pixels_array = np.array(pixels)
        min_r, min_c = pixels_array.min(axis=0)
        max_r, max_c = pixels_array.max(axis=0)
        h, w = max_r - min_r + 1, max_c - min_c + 1
        
        # Create normalized shape grid
        shape_grid = np.zeros((h, w), dtype=int)
        for r, c in pixels:
            shape_grid[r - min_r, c - min_c] = 1
        
        # Detect common patterns - ORDER MATTERS!
        # Check specific exact shapes first
        if self._is_square(shape_grid):
            return "square"
        elif self._is_L_shape(shape_grid):
            return "L_shape"
        elif self._is_cross(shape_grid):
            return "cross"
        elif self._is_T_shape(shape_grid):
            return "T_shape"
        elif self._is_diagonal(shape_grid):
            return "diagonal"
        elif self._is_horizontal_line(shape_grid):
            return "line_h"
        elif self._is_vertical_line(shape_grid):
            return "line_v"
        else:
            # Generic signature based on dimensions
            return f"shape_{h}x{w}"
    
    def _is_L_shape(self, grid: np.ndarray) -> bool:
        """Detect L-shape pattern"""
        h, w = grid.shape
        if h < 2 or w < 2:
            return False
            
        # Must not be a full rectangle/square (handled by other checks)
        if grid.sum() == h * w:
            return False
        
        # L-shape has two perpendicular lines
        # Check all 4 orientations
        
        # ┌ shape (top-left) - missing bottom-right
        if (grid[0, :].sum() >= 2 and grid[:, 0].sum() >= 2 and grid[0, 0] == 1):
             # Ensure the "empty" part roughly exists if it's a 2x2 or 3x3 L
             if grid[-1, -1] == 0: return True
             # If bigger, loose check
             return True
        
        # ┐ shape (top-right) - missing bottom-left
        if (grid[0, :].sum() >= 2 and grid[:, -1].sum() >= 2 and grid[0, -1] == 1):
             if grid[-1, 0] == 0: return True
             return True
        
        # └ shape (bottom-left) - missing top-right
        if (grid[-1, :].sum() >= 2 and grid[:, 0].sum() >= 2 and grid[-1, 0] == 1):
             if grid[0, -1] == 0: return True
             return True
        
        # ┘ shape (bottom-right) - missing top-left
        if (grid[-1, :].sum() >= 2 and grid[:, -1].sum() >= 2 and grid[-1, -1] == 1):
             if grid[0, 0] == 0: return True
             return True
        
        return False
    
    def _is_cross(self, grid: np.ndarray) -> bool:
        """Detect cross/plus pattern"""
        h, w = grid.shape
        if h < 3 or w < 3:
            return False
        
        # Cross has center point with 4 arms
        center_r, center_c = h // 2, w // 2
        
        if grid[center_r, center_c] != 1:
            return False
        
        # Check for arms in 4 directions
        has_up = center_r > 0 and grid[center_r - 1, center_c] == 1
        has_down = center_r < h - 1 and grid[center_r + 1, center_c] == 1
        has_left = center_c > 0 and grid[center_r, center_c - 1] == 1
        has_right = center_c < w - 1 and grid[center_r, center_c + 1] == 1
        
        return has_up and has_down and has_left and has_right
    
    def _is_T_shape(self, grid: np.ndarray) -> bool:
        """Detect T-shape pattern"""
        h, w = grid.shape
        if h < 2 or w < 3:
            return False
        
        # T-shape has horizontal bar and vertical stem
        # Check top T
        if grid[0, :].sum() >= 3 and grid[:, w // 2].sum() >= 2:
            return True
        
        # Check bottom T (upside down)
        if grid[-1, :].sum() >= 3 and grid[:, w // 2].sum() >= 2:
            return True
        
        return False
    
    def _is_diagonal(self, grid: np.ndarray) -> bool:
        """Detect diagonal line"""
        h, w = grid.shape
        if h < 2 or w < 2:
            return False
        
        # Check main diagonal
        main_diag = sum(1 for i in range(min(h, w)) if grid[i, i] == 1)
        if main_diag >= min(h, w) * 0.8:  # 80% of diagonal filled
            return True
        
        # Check anti-diagonal
        anti_diag = sum(1 for i in range(min(h, w)) if grid[i, w - 1 - i] == 1)
        if anti_diag >= min(h, w) * 0.8:
            return True
        
        return False
    
    def _is_horizontal_line(self, grid: np.ndarray) -> bool:
        """Detect horizontal line"""
        h, w = grid.shape
        if h > 2 or w < 2:
            return False
        
        # Check if any row is mostly filled
        for row in grid:
            if row.sum() >= w * 0.8:
                return True
        return False
    
    def _is_vertical_line(self, grid: np.ndarray) -> bool:
        """Detect vertical line"""
        h, w = grid.shape
        if w > 2 or h < 2:
            return False
        
        # Check if any column is mostly filled
        for c in range(w):
            if grid[:, c].sum() >= h * 0.8:
                return True
        return False
    
    def _is_square(self, grid: np.ndarray) -> bool:
        """Detect square/filled rectangle"""
        h, w = grid.shape
        if abs(h - w) > 1:  # Not square-ish
            return False
        
        # Check if mostly filled
        filled_ratio = grid.sum() / (h * w)
        return filled_ratio >= 0.8


class VocabularyBuilder:
    """
    Builds and maintains agent's self-invented vocabulary.
    Tracks which motifs work, prunes unsuccessful ones.
    """
    
    def __init__(self, persistence_file: str = "agent_vocabulary.pkl"):
        self.vocabulary: Dict[str, NamedMotif] = {}
        self.persistence_file = persistence_file
        self.load()
    
    def add_motif(self, name: str, motif: Dict, task_id: str):
        """
        Add a discovered motif to vocabulary.
        Agent is building its own language!
        """
        if name not in self.vocabulary:
            self.vocabulary[name] = NamedMotif(
                name=name,
                definition=motif,
                discovered_in=task_id,
                usage_count=0,
                success_rate=0.0
            )
            print(f"[VOCABULARY] Agent invented new concept: '{name}'")
    
    def use_motif(self, name: str, success: bool):
        """
        Track usage and success of a motif.
        Agent learns which concepts are useful!
        """
        if name not in self.vocabulary:
            return
        
        motif = self.vocabulary[name]
        motif.usage_count += 1
        
        # Update success rate (running average)
        old_rate = motif.success_rate
        count = motif.usage_count
        new_rate = (old_rate * (count - 1) + (1.0 if success else 0.0)) / count
        motif.success_rate = new_rate
    
    def get_top_motifs(self, k: int = 10) -> List[NamedMotif]:
        """
        Get most successful motifs.
        Agent's most useful concepts!
        """
        scored_motifs = [
            (name, motif.success_rate * min(motif.usage_count, 10))
            for name, motif in self.vocabulary.items()
        ]
        scored_motifs.sort(key=lambda x: x[1], reverse=True)
        
        return [self.vocabulary[name] for name, _ in scored_motifs[:k]]
    
    def prune_vocabulary(self, min_usage: int = 3, min_success: float = 0.1):
        """
        Remove rarely used or unsuccessful motifs.
        Agent forgets useless concepts!
        """
        to_remove = []
        for name, motif in self.vocabulary.items():
            if motif.usage_count >= min_usage and motif.success_rate < min_success:
                to_remove.append(name)
            elif motif.usage_count < min_usage and motif.usage_count > 0:
                # Give it a chance, but if used and failed, remove
                if motif.success_rate < 0.2:
                    to_remove.append(name)
        
        for name in to_remove:
            print(f"[VOCABULARY] Agent forgot useless concept: '{name}'")
            del self.vocabulary[name]
    
    def get_statistics(self) -> Dict:
        """Get vocabulary statistics"""
        if not self.vocabulary:
            return {
                'total_concepts': 0,
                'avg_usage': 0,
                'avg_success': 0,
                'top_concepts': []
            }
        
        return {
            'total_concepts': len(self.vocabulary),
            'avg_usage': np.mean([m.usage_count for m in self.vocabulary.values()]),
            'avg_success': np.mean([m.success_rate for m in self.vocabulary.values()]),
            'top_concepts': [m.name for m in self.get_top_motifs(5)]
        }
    
    def save(self):
        """Save vocabulary to disk"""
        try:
            import pickle
            with open(self.persistence_file, 'wb') as f:
                pickle.dump(self.vocabulary, f)
        except Exception as e:
            print(f"Warning: Could not save vocabulary: {e}")
    
    def load(self):
        """Load vocabulary from disk"""
        try:
            import pickle
            import os
            if os.path.exists(self.persistence_file):
                with open(self.persistence_file, 'rb') as f:
                    self.vocabulary = pickle.load(f)
                print(f"[VOCABULARY] Loaded {len(self.vocabulary)} concepts from memory")
        except Exception as e:
            print(f"Warning: Could not load vocabulary: {e}")
    
    def harmonize(self):
        """
        Autonomous Harmonization cycle.
        The agent 'dreams' and reorganizes its vocabulary to be more efficient.
        Consolidates isomorphic concepts (e.g., same shape, different colors) into generic ones.
        """
        print("[VOCABULARY] Starting autonomous harmonization cycle...")
        
        # 1. Group motifs by Shape Signature (ignoring color)
        shape_groups = {}  # signature -> [motif_names]
        
        # Helper to get pure shape signature
        namer = MotifNamer()
        
        for name, motif in self.vocabulary.items():
            # Skip if already generic
            if "_generic" in name or "_c" not in name:
                continue
            
            # Extract shape properties
            definition = motif.definition
            m_type = definition.get('type')
            
            signature = None
            if m_type == 'rectangle':
                bbox = definition.get('bbox', (0,0,1,1))
                h, w = bbox[2]-bbox[0], bbox[3]-bbox[1]
                signature = f"rect_{h}x{w}"
                
            elif m_type == 'component':
                pixels = definition.get('pixels', [])
                shape_sig = namer._compute_shape_signature(pixels)
                size = definition.get('size', 0)
                signature = f"comp_{shape_sig}_{size}"
                
            if signature:
                if signature not in shape_groups:
                    shape_groups[signature] = []
                shape_groups[signature].append(name)
        
        # 2. Merge groups with multiple entries
        merged_count = 0
        for signature, names in shape_groups.items():
            if len(names) > 1:
                # FOUND REDUNDANCY!
                # e.g., ['rect_2x2_c1', 'rect_2x2_c2', 'rect_2x2_c3']
                
                # Create Generic Concept
                generic_name = signature  # e.g., "rect_2x2"
                
                # Calculate aggregated stats
                total_usage = sum(self.vocabulary[n].usage_count for n in names)
                avg_success = np.mean([self.vocabulary[n].success_rate for n in names])
                
                # Create the generic motif entry
                # We base definition on the first one, but flag color as variable
                base_def = self.vocabulary[names[0]].definition.copy()
                base_def['color'] = -1  # Mark as color-invariant
                
                generic_motif = NamedMotif(
                    name=generic_name,
                    definition=base_def,
                    discovered_in="harmonization",
                    usage_count=total_usage,
                    success_rate=avg_success
                )
                
                self.vocabulary[generic_name] = generic_motif
                
                print(f"[HARMONIZATION] Merged {names} -> '{generic_name}'")
                merged_count += 1
                
                # Optional: Remove old specific ones? 
                # Better: Keep them but decay them, or mark them as children.
                # For now, let's keep specific ones because sometimes color matters!
                # But the EXISTENCE of the generic one allows the optimizer to pick it.
                
        print(f"[VOCABULARY] Harmonization complete. Created {merged_count} generic concepts.")
        self.save()


class SelfInventedPredicateGenerator:
    """
    Generates predicates dynamically from vocabulary.
    No hand-designed predicates!
    """
    
    def __init__(self, vocabulary_builder: VocabularyBuilder):
        self.vocab = vocabulary_builder
    
    def generate_predicates_from_vocabulary(self, grid: np.ndarray) -> List[Dict]:
        """
        Generate predicates based on learned vocabulary.
        Each motif becomes a predicate!
        """
        predicates = []
        
        # Get top motifs to avoid checking everything
        top_motifs = self.vocab.get_top_motifs(k=20)
        
        for motif in top_motifs:
            motif_name = motif.name
            motif_def = motif.definition
            
            # Create a predicate that checks if (r,c) matches this motif
            # We use a factory method to capture the specific motif definition closure
            def make_motif_predicate(m_def):
                def predicate(grid, r, c):
                    return self._matches_motif_at(grid, r, c, m_def)
                return predicate
            
            predicates.append({
                'name': f"is_{motif_name}",
                'function': make_motif_predicate(motif_def),
                'success_rate': motif.success_rate,
                'motif_name': motif_name # Store reference for usage tracking
            })
        
        return predicates
    
    def _matches_motif_at(self, grid: np.ndarray, r: int, c: int, motif: Dict) -> bool:
        """Check if grid matches motif at position (r,c)"""
        motif_type = motif.get('type')
        
        try:
            if motif_type == 'rectangle':
                bbox = motif.get('bbox', (0,0,1,1))
                h = bbox[2] - bbox[0]
                w = bbox[3] - bbox[1]
                color = motif.get('color', -1)
                
                # Check if (r,c) is top-left of such rectangle
                return self._is_rectangle_at(grid, r, c, h, w, color)
            
            elif motif_type == 'component':
                # Check if (r,c) is part of a component matching this shape
                return self._is_component_at(grid, r, c, motif)
            
            elif motif_type == 'fill':
                # Simple check: if color matches one of fill colors
                fill_colors = motif.get('fill_colors', [])
                if 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]:
                    return grid[r, c] in fill_colors
                return False
                
        except Exception:
            return False
            
        return False

    def _is_rectangle_at(self, grid: np.ndarray, r: int, c: int, h: int, w: int, color: int) -> bool:
        """Check if there is a specific rectangle at (r,c)"""
        rows, cols = grid.shape
        if r + h > rows or c + w > cols:
            return False
        
        # Check region
        region = grid[r:r+h, c:c+w]
        if color != -1:
            return np.all(region == color)
        else:
            # Check if region is uniform color
            first_color = region[0, 0]
            if first_color == 0: return False # Ignore black rectangles usually
            return np.all(region == first_color)

    def _is_component_at(self, grid: np.ndarray, r: int, c: int, motif: Dict) -> bool:
        """
        Check if (r,c) is the top-left or 'anchor' of a matching component.
        For simplicity, we check if the shape starting at (r,c) matches.
        """
        pixels = motif.get('pixels', [])
        if not pixels: return False
        
        motif_color = motif.get('color', -1)
        
        # Convert motif pixels to relative coordinates from top-left
        pixels_array = np.array(pixels)
        min_r, min_c = pixels_array.min(axis=0)
        
        relative_pixels = []
        for pr, pc in pixels:
            relative_pixels.append((pr - min_r, pc - min_c))
            
        rows, cols = grid.shape
        
        # Check if all relative pixels match on grid starting at (r,c)
        for dr, dc in relative_pixels:
            gr, gc = r + dr, c + dc
            if not (0 <= gr < rows and 0 <= gc < cols):
                return False
            
            if motif_color != -1:
                if grid[gr, gc] != motif_color:
                    return False
            else:
                # If motif has no fixed color, we might match shape only
                # But typically component motifs have color. 
                # If not, we'd need to check consistency.
                if grid[gr, gc] == 0: # Assuming 0 is background
                    return False

        # Check neighbor pixels to ensure it's the exact shape (basic check)
        # For strict component matching, we'd need to ensure no extra connected pixels
        # But for predicate matching "is_L_shape", containment is often enough
        return True
