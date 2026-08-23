import numpy as np
import random
from enum import Enum, auto

class AtomicType(Enum):
    SET_PIXEL = auto()
    DRAW_LINE = auto()
    DRAW_RECT = auto()
    FILL = auto()
    COPY_PASTE = auto()
    SWAP_COLOR = auto()
    ROTATE = auto()
    FLIP = auto()
    MEMETIC_PLACE = auto() # Phase 4: Smart Mutation

class AtomicPhysics:
    """
    Defines the fundamental laws of the grid universe.
    """
    
    @staticmethod
    def mutate(grid: np.ndarray, anchors: list = None) -> np.ndarray:
        """Apply a random atomic (or memetic) mutation to the grid."""
        h, w = grid.shape
        new_grid = grid.copy()
        
        # Select random action
        # Phase 4: Higher probability of Memetic if anchors exist
        options = list(AtomicType)
        if anchors:
            # 50% chance to use Smart Mutation if we have knowledge
            if random.random() < 0.5:
                action_type = AtomicType.MEMETIC_PLACE
            else:
                action_type = random.choice(options)
        else:
            action_type = random.choice(options)
            if action_type == AtomicType.MEMETIC_PLACE: action_type = AtomicType.SET_PIXEL
        
        # Colors (0-9)
        color = random.randint(0, 9)
        
        if action_type == AtomicType.MEMETIC_PLACE and anchors:
            # Place a learned concept
            anchor = random.choice(anchors)
            ah, aw = anchor.shape
            
            # Phase 4 Fix: Ensure anchor fits
            if ah > h or aw > w:
                return new_grid # Skip mutation if anchor is too big
            
            # Random position
            r = random.randint(0, h - ah)
            c = random.randint(0, w - aw)
            
            # Paste anchor (handle mask/transparency if 0? No, for now unconditional paste)
            # Actually, usually 0 is background in ARC, so maybe we respect it.
            # Let's try "Overwrite Non-Zero"
            roi = new_grid[r:r+ah, c:c+aw]
            mask = (anchor != 0)
            roi[mask] = anchor[mask]
            
        elif action_type == AtomicType.SET_PIXEL:
            r, c = random.randint(0, h-1), random.randint(0, w-1)
            new_grid[r, c] = color
            
        elif action_type == AtomicType.DRAW_LINE:
            # Random Start/End
            r1, c1 = random.randint(0, h-1), random.randint(0, w-1)
            r2, c2 = random.randint(0, h-1), random.randint(0, w-1)
            # Simple Bresenham-like or just axis-aligned for now
            if random.random() < 0.5: # Horiz
                new_grid[r1, min(c1, c2):max(c1, c2)+1] = color
            else: # Vert
                new_grid[min(r1, r2):max(r1, r2)+1, c1] = color
                
        elif action_type == AtomicType.DRAW_RECT:
            r1, c1 = random.randint(0, h-1), random.randint(0, w-1)
            r2, c2 = random.randint(0, h-1), random.randint(0, w-1)
            new_grid[min(r1,r2):max(r1,r2)+1, min(c1,c2):max(c1,c2)+1] = color
            
        elif action_type == AtomicType.FILL:
            # Flood fill attempt (simplified: color replacement of connected region)
            # For efficiency in mutation, maybe just global swap or simple region fill
            # Let's do Global Color Swap for now (very common in ARC)
            r, c = random.randint(0, h-1), random.randint(0, w-1)
            target_color = new_grid[r, c]
            if target_color != color:
                new_grid[new_grid == target_color] = color
                
        elif action_type == AtomicType.COPY_PASTE:
            # Copy random chunk to random location
            # Source
            rh, rw = random.randint(1, h//2 + 1), random.randint(1, w//2 + 1)
            sr, sc = random.randint(0, h-rh), random.randint(0, w-rw)
            # Dest
            dr, dc = random.randint(0, h-rh), random.randint(0, w-rw)
            
            chunk = grid[sr:sr+rh, sc:sc+rw]
            new_grid[dr:dr+rh, dc:dc+rw] = chunk
            
        elif action_type == AtomicType.SWAP_COLOR:
            c1, c2 = random.randint(0, 9), random.randint(0, 9)
            if c1 != c2:
                mask1 = (grid == c1)
                mask2 = (grid == c2)
                new_grid[mask1] = c2
                new_grid[mask2] = c1

        elif action_type == AtomicType.ROTATE:
             k = random.randint(1, 3)
             new_grid = np.rot90(new_grid, k=k)
             # Resize handling? For now, if rotate changes aspect ratio, we might fail 
             # if fixed size is expected. But ARC allows size change.
             # Note: Mutation should probably respect constraints or Actuator handles resizing.
             
        elif action_type == AtomicType.FLIP:
            axis = random.choice([0, 1])
            new_grid = np.flip(new_grid, axis=axis)
            
        return new_grid
