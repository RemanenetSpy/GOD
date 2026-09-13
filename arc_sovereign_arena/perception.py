"""
ARC Sovereign Perception Module
Implements Core Knowledge Priors (François Chollet):
- Object-Centric Segmentation (Connected Components, Colors, Background)
- Geometric & Morphological Attributes (Bounding Boxes, Centroids, Masses, Cavities, Symmetries)
- Relational Graph (Containment, Alignment, Contact, Adjacency)
"""

import numpy as np
import scipy.ndimage
from typing import List, Dict, Tuple, Set, Optional, Any


class GridObject:
    """Represents an extracted physical object/entity in a 2D discrete grid."""
    __slots__ = (
        "id", "color", "coords", "coords_set", "bbox", "height", "width",
        "size", "centroid", "is_solid", "holes", "perimeter", "shape_signature"
    )

    def __init__(self, obj_id: int, color: int, coords: np.ndarray, grid_shape: Tuple[int, int]):
        self.id = obj_id
        self.color = int(color)
        self.coords = coords  # Array of shape (N, 2)
        self.coords_set = set(map(tuple, coords))
        self.size = int(len(coords))

        min_r, min_c = coords.min(axis=0)
        max_r, max_c = coords.max(axis=0)
        self.bbox = (int(min_r), int(min_c), int(max_r), int(max_c))
        self.height = int(max_r - min_r + 1)
        self.width = int(max_c - min_c + 1)
        self.centroid = (float(coords[:, 0].mean()), float(coords[:, 1].mean()))

        # Normalize shape relative to bbox top-left for shape invariance
        rel_coords = coords - [min_r, min_c]
        mask = np.zeros((self.height, self.width), dtype=bool)
        mask[rel_coords[:, 0], rel_coords[:, 1]] = True
        self.shape_signature = mask.tobytes()

        # Cavity / Hole detection
        inv_mask = ~mask
        labeled_inv, num_inv = scipy.ndimage.label(inv_mask)
        holes = []
        for i in range(1, num_inv + 1):
            hole_coords = np.argwhere(labeled_inv == i)
            r_border = (hole_coords[:, 0] == 0) | (hole_coords[:, 0] == self.height - 1)
            c_border = (hole_coords[:, 1] == 0) | (hole_coords[:, 1] == self.width - 1)
            if not np.any(r_border | c_border):
                abs_hole = hole_coords + [min_r, min_c]
                holes.extend(abs_hole.tolist())
        self.holes = holes
        self.is_solid = (len(holes) == 0)

        # Perimeter pixels
        perimeter = []
        for r, c in coords:
            is_edge = (r == 0 or r == grid_shape[0] - 1 or c == 0 or c == grid_shape[1] - 1)
            if not is_edge:
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    if (r + dr, c + dc) not in self.coords_set:
                        is_edge = True
                        break
            if is_edge:
                perimeter.append((int(r), int(c)))
        self.perimeter = perimeter

    def isolate(self, target_shape: Optional[Tuple[int, int]] = None, background: int = 0) -> np.ndarray:
        """Returns a 2D grid containing only this object."""
        if target_shape is None:
            res = np.full((self.height, self.width), background, dtype=int)
            rel = self.coords - [self.bbox[0], self.bbox[1]]
            res[rel[:, 0], rel[:, 1]] = self.color
            return res
        else:
            res = np.full(target_shape, background, dtype=int)
            valid = (self.coords[:, 0] < target_shape[0]) & (self.coords[:, 1] < target_shape[1])
            c = self.coords[valid]
            res[c[:, 0], c[:, 1]] = self.color
            return res


class PerceptualScene:
    """Parses a 2D ARC grid into an Object-Centric Relational Graph."""

    def __init__(self, grid: np.ndarray, background_color: Optional[int] = None, connectivity: int = 8):
        self.grid = grid.copy()
        self.shape = grid.shape
        self.height, self.width = grid.shape
        self.connectivity = connectivity

        if background_color is not None:
            self.bg_color = background_color
        else:
            unique, counts = np.unique(grid, return_counts=True)
            if 0 in unique:
                self.bg_color = 0
            else:
                self.bg_color = int(unique[np.argmax(counts)])

        self.objects: List[GridObject] = []
        self._segment_objects()

    def _segment_objects(self):
        """Extracts connected components by color and spatial proximity."""
        obj_id = 1
        struct = scipy.ndimage.generate_binary_structure(2, 2 if self.connectivity == 8 else 1)

        unique_colors = [c for c in np.unique(self.grid) if c != self.bg_color]
        for color in unique_colors:
            color_mask = (self.grid == color)
            labeled, num_features = scipy.ndimage.label(color_mask, structure=struct)
            for feat_idx in range(1, num_features + 1):
                coords = np.argwhere(labeled == feat_idx)
                if len(coords) > 0:
                    obj = GridObject(obj_id, color, coords, self.shape)
                    self.objects.append(obj)
                    obj_id += 1

    @property
    def num_objects(self) -> int:
        return len(self.objects)

    def get_objects_by_color(self, color: int) -> List[GridObject]:
        return [obj for obj in self.objects if obj.color == color]

    def get_largest_object(self) -> Optional[GridObject]:
        if not self.objects:
            return None
        return max(self.objects, key=lambda o: o.size)

    def get_smallest_object(self) -> Optional[GridObject]:
        if not self.objects:
            return None
        return min(self.objects, key=lambda o: o.size)

    def get_unique_color_objects(self) -> List[GridObject]:
        """Returns objects whose color occurs exactly once among all objects."""
        color_counts = {}
        for obj in self.objects:
            color_counts[obj.color] = color_counts.get(obj.color, 0) + 1
        return [obj for obj in self.objects if color_counts[obj.color] == 1]

    def get_full_bbox(self) -> Optional[Tuple[int, int, int, int]]:
        """Returns bounding box enclosing all foreground objects."""
        if not self.objects:
            return None
        min_r = min(o.bbox[0] for o in self.objects)
        min_c = min(o.bbox[1] for o in self.objects)
        max_r = max(o.bbox[2] for o in self.objects)
        max_c = max(o.bbox[3] for o in self.objects)
        return (min_r, min_c, max_r, max_c)
