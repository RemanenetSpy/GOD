"""
Lifespan Spatial Memory for ARC Sovereign Survival Ecology
Maintains intra-lifespan spatial working memory strictly for the duration of a single organism's life.
Resets completely upon starvation death / birth of a new generation.
"""

from typing import Dict, Tuple, List, Any


class LifespanSpatialMemory:
    """
    Tracks tiles visited and visit frequency within the current organism's single lifespan.
    Provides novelty bias to prevent looping/camping and guide exploration across the canvas.
    """

    def __init__(self):
        # Maps (r, c) -> number of times visited in this lifetime
        self.visit_counts: Dict[Tuple[int, int], int] = {}
        # Chronological sequence of visited tiles
        self.visit_history: List[Tuple[int, int]] = []

    def record_visit(self, r: int, c: int):
        """Records that the organism occupied / visited tile (r, c)."""
        pos = (int(r), int(c))
        self.visit_counts[pos] = self.visit_counts.get(pos, 0) + 1
        self.visit_history.append(pos)

    def has_visited(self, r: int, c: int) -> bool:
        """Returns True if the organism has already visited (r, c) in its current life."""
        return (int(r), int(c)) in self.visit_counts

    def get_visit_count(self, r: int, c: int) -> int:
        """Returns the number of times (r, c) has been visited in this lifetime."""
        return self.visit_counts.get((int(r), int(c)), 0)

    def unique_tiles_count(self) -> int:
        """Returns total unique tiles visited in this lifetime."""
        return len(self.visit_counts)

    def total_steps(self) -> int:
        """Returns total step count in this lifetime."""
        return len(self.visit_history)

    def reset(self):
        """Clears all spatial memory upon death."""
        self.visit_counts.clear()
        self.visit_history.clear()

    def to_dict(self) -> Dict[str, Any]:
        """Serializes current lifespan spatial state for telemetry."""
        return {
            "unique_tiles_count": len(self.visit_counts),
            "total_steps": len(self.visit_history),
            "visited_coords": [list(pos) for pos in self.visit_counts.keys()]
        }
