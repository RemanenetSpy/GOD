import numpy as np
from enum import Enum, auto
import random

class MotiveType(Enum):
    # Global Symmetries
    ROTATE_90 = auto()
    ROTATE_180 = auto()
    ROTATE_270 = auto()
    FLIP_H = auto()
    FLIP_V = auto()
    
    # Physics / Cellular Automata
    GRAVITY_DOWN = auto() # Push non-black pixels down
    GRAVITY_UP = auto()
    FILL_ENCLOSED = auto() # Fill holes
    
    # Memetic / Structural
    REPEATER = auto() # Tile the input
    SYMMETRY_COMPLETE = auto() # Mirror half to other half
    
    # Identity (Null Hypothesis)
    IDENTITY = auto()

class MotivePhysics:
    """
    High-Level Transformations (Motives).
    These are 'Global Wills' that the agent applies to the entire grid.
    """
    
    @staticmethod
    def apply_motive(grid: np.ndarray, motive: MotiveType) -> np.ndarray:
        h, w = grid.shape
        new_grid = grid.copy()
        
        if motive.name == 'IDENTITY':
            return new_grid
            
        # Debug 
        # print(f"   [MotivePhysics] Applying {motive}")
        # if motive == MotiveType.GRAVITY_DOWN or motive.name == 'GRAVITY_DOWN':
        #      # print(f"   [MotivePhysics] GRAVITY DETECTED. ID match? {motive is MotiveType.GRAVITY_DOWN}")
        #      pass
        # else:
        #      print(f"   [MotivePhysics] Unknown Motive: {motive} (Name: {motive.name}). Expected GRAVITY_DOWN ID: {MotiveType.GRAVITY_DOWN}")

        if motive.name == 'ROTATE_90':
            return np.rot90(grid, k=1)
            
        elif motive.name == 'ROTATE_180':
            return np.rot90(grid, k=2)
            
        elif motive.name == 'ROTATE_270':
            return np.rot90(grid, k=3)
            
        elif motive.name == 'FLIP_H':
            return np.fliplr(grid)
            
        elif motive.name == 'FLIP_V':
            return np.flipud(grid)
            
        elif motive.name == 'GRAVITY_DOWN':
            return MotivePhysics._apply_gravity(grid, direction=(1, 0))

        elif motive.name == 'GRAVITY_UP':
            return MotivePhysics._apply_gravity(grid, direction=(-1, 0))
            
        elif motive.name == 'FILL_ENCLOSED':
            # Simple hole filling (flood fill background, invert)
            return MotivePhysics._fill_holes(grid)
            
        elif motive.name == 'REPEATER':
            # Tile 2x2
            return np.tile(grid, (2, 2))
            
        return new_grid

    @staticmethod
    def _apply_gravity(grid: np.ndarray, direction) -> np.ndarray:
        """Push all non-zero pixels in direction until they hit edge or other pixel."""
        # Simple simulation: Sort columns/rows?
        # Gravity Down: For each column, move non-zeros to bottom
        result = np.zeros_like(grid)
        h, w = grid.shape
        
        if direction == (1, 0): # Down
            for c in range(w):
                col = grid[:, c]
                pixels = col[col != 0]
                if len(pixels) > 0:
                   # Debug: Trace one column 
                   # if c == 0 or c == 5: 
                   print(f"   [Gravity] Col {c}: Found {len(pixels)} px. Placing at {h-len(pixels)}")
                   pass
                # Place at bottom
                # Debug assignment
                # print(f"   [Gravity] Assigning Col {c}: result[{h-len(pixels)}:, {c}] = {pixels}")
                result[h-len(pixels):, c] = pixels
                if c == 0:
                     print(f"   [Gravity] Result after Col 0:\n{result}")
        elif direction == (-1, 0): # Up
            for c in range(w):
                col = grid[:, c]
                pixels = col[col != 0]
                result[:len(pixels), c] = pixels
        
        # Debug
        # print(f"   [Gravity] Result Sum: {np.sum(result)}. Input Sum: {np.sum(grid)}")
        return result

    @staticmethod
    def _fill_holes(grid: np.ndarray) -> np.ndarray:
        """Crude flood fill to close loops."""
        # 1. Mask non-zero
        from scipy.ndimage import binary_fill_holes
        mask = (grid != 0)
        filled_mask = binary_fill_holes(mask)
        
        # 2. Fill holes with... most common color? or Red?
        # Let's fill with a default 'active' color (e.g., 1 or same as neighbor)
        # For simple implementation: Fill with '8' (Blue) as marker
        res = grid.copy()
        holes = filled_mask & (~mask)
        res[holes] = 8 
        return res
