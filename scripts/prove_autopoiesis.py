"""
Proof of Autopoiesis (Self-Organizing Universe)

This script demonstrates Phase 23: The Autopoietic Engine.
We initialize a CHAOTIC UNIVERSE (random pixels).
There is NO external rule saying "Sort these".
There is NO target image.

The System:
1. Calculates the "Center of Mass" (Singularity) for each color.
2. Warps spacetime so that Color X falls towards Center X.
3. Advects particles.
4. Repeats (Dynamic Update).

Result: The universe spontaneously crystallizes into ordered blobs.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import numpy as np
import matplotlib.pyplot as plt
from typing import List
from autopoietic_engine import AutopoieticEngine

class UniversalAdvector:
    def __init__(self, grid: np.ndarray):
        self.height, self.width = grid.shape
        # Store particles as (y, x, color)
        self.particles = []
        
        ys, xs = np.where(grid != 0)
        for y, x in zip(ys, xs):
            color = grid[y, x]
            self.particles.append({'y': float(y), 'x': float(x), 'c': color})
            
    def update(self, engine: AutopoieticEngine, grid_shape: tuple):
        """
        The Physics Loop:
        1. Calculate Singularities (Centers of Mass) based on CURRENT positions.
        2. Advect each particle towards its color's singularity.
        """
        # Reconstruct grid approximation for inputs
        temp_grid = np.zeros(grid_shape, dtype=int)
        for p in self.particles:
            y, x = int(max(0, min(grid_shape[0]-1, p['y']))), int(max(0, min(grid_shape[1]-1, p['x'])))
            temp_grid[y, x] = p['c']
            
        # 1. System calculates its own motivation
        singularities = engine.calculate_singularities(temp_grid)
        
        # Cache fields for performance (one per color)
        fields = {}
        unique_colors = set(p['c'] for p in self.particles)
        for c in unique_colors:
            if c in singularities:
                # Calculate the manifold shape for this color
                fields[c] = engine.get_metric_for_color(temp_grid, c)
                
        # 2. Advection (Gravity)
        new_particles = []
        step_size = 1.0
        
        for p in self.particles:
            c = p['c']
            if c not in fields:
                new_particles.append(p)
                continue
                
            field = fields[c]
            h, w = field.shape
            
            y_int, x_int = int(p['y']), int(p['x'])
            y_int = max(0, min(h-1, y_int))
            x_int = max(0, min(w-1, x_int))
            
            # Local Gradient
            # (Simple efficient gradient check)
            # Find neighbor with lowest T
            best_y, best_x = y_int, x_int
            min_t = field[y_int, x_int]
            
            # Look at immediate neighbors for gradient direction
            dy, dx = 0.0, 0.0
            
            # Simple stochastic gradient descent-ish movement
            # In continuous space, we'd use np.gradient, but for particle swarm
            # towards a clear sink, simply moving towards lower T is fine.
            
            # Let's use the field gradient logic from ManifoldEngine but continuous
            # We can cheat slightly and just move towards the singularity directly?
            # NO! That's "fake" gravity. We MUST use the field.
            
            # Get gradient at (y,x)
            # Central difference
            t_up = field[max(0, y_int-1), x_int]
            t_down = field[min(h-1, y_int+1), x_int]
            t_left = field[y_int, max(0, x_int-1)]
            t_right = field[y_int, min(w-1, x_int+1)]
            
            grad_y = (t_down - t_up) * 0.5
            grad_x = (t_right - t_left) * 0.5
            
            # Move DOWNHILL (negative gradient)
            vy = -grad_y
            vx = -grad_x
            
            # Normalize speed
            speed = np.sqrt(vy**2 + vx**2) + 1e-9
            vy /= speed
            vx /= speed
            
            # Apply
            p['y'] += vy * step_size
            p['x'] += vx * step_size
            
            # Bounds
            p['y'] = max(0, min(h-1, p['y']))
            p['x'] = max(0, min(w-1, p['x']))
            
            new_particles.append(p)
            
        self.particles = new_particles

    def render(self, shape: tuple) -> np.ndarray:
        output = np.zeros(shape, dtype=int)
        for p in self.particles:
            y, x = int(round(p['y'])), int(round(p['x']))
            y = max(0, min(shape[0]-1, y))
            x = max(0, min(shape[1]-1, x))
            output[y, x] = p['c']
        return output

def run_proof():
    print("⚡ PROVING AUTOPOIESIS (SELF-UPDATING MACHINE) ⚡")
    
    # 1. Setup Chaotic Universe
    size = 30
    grid = np.zeros((size, size), dtype=int)
    
    # Random Noise of 3 colors
    # Color 1: Red, Color 2: Green, Color 3: Blue
    np.random.seed(42)
    for _ in range(150): # 150 particles
        ry, rx = np.random.randint(0, size, 2)
        c = np.random.randint(1, 4)
        grid[ry, rx] = c
        
    print("   > Initial State: Chaos (High Entropy)")
    
    # 2. Initialize Engine
    engine = AutopoieticEngine()
    advector = UniversalAdvector(grid)
    
    # 3. Evolution Loop
    steps = 30
    snapshots = [grid.copy()]
    
    for i in range(steps):
        sys.stdout.write(f"\r   > Time Step {i+1}/{steps}: Calculating Singularities & Warping Space...")
        sys.stdout.flush()
        
        advector.update(engine, grid.shape)
        snapshots.append(advector.render(grid.shape))
        
    print("\n   > Evolution Complete.")
    
    # 4. Compare Entropy (Visual)
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    
    axes[0].imshow(snapshots[0], cmap='nipy_spectral', vmin=0, vmax=9)
    axes[0].set_title("Initial Chaos\n(Random Distribution)")
    
    axes[1].imshow(snapshots[-1], cmap='nipy_spectral', vmin=0, vmax=9)
    axes[1].set_title("Self-Organized Order\n(Spontaneous Sorting via Gravity)")
    
    plt.savefig('autopoiesis_proof.png')
    print("   ✓ Result saved to 'autopoiesis_proof.png'")

if __name__ == "__main__":
    run_proof()
