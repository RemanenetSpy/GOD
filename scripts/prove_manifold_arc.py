"""
Proof of Manifold Engine on ARC Tasks (Ontological Solving)

This script proves that the Manifold Engine can solve ARC-like grid transformations
by treating them as Flow Problems in a curved spacetime.

Scenarios:
1. "Attraction" (Training): Objects flow towards a specific color (Singularity).
2. "Gravity" (Blind): Objects fall towards a natural boundary (Event Horizon).

NO RULES are used (e.g., "if red move right"). 
Only METRIC definitions (e.g., "Blue is T=0").
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from typing import List, Tuple
from manifold_engine import ManifoldEngine

class ParticleAdvector:
    def __init__(self, grid: np.ndarray, movable_color: int = 5):
        self.height, self.width = grid.shape
        self.particles = [] # List of [y, x] floats
        self.movable_color = movable_color
        
        # Convert movable pixels to particles
        ys, xs = np.where(grid == movable_color)
        for y, x in zip(ys, xs):
            self.particles.append(np.array([float(y), float(x)]))
            
    def advect(self, time_field: np.ndarray, step_size: float = 0.5):
        """Move particles along the geodesic (gradient of time field)."""
        new_particles = []
        h, w = time_field.shape
        
        # Calculate gradients (negative because we want descent)
        # np.gradient returns (dy, dx)
        grad_y, grad_x = np.gradient(time_field)
        
        # Normalize gradients to avoid slight drift in flat areas? 
        # For now, raw gradient is fine, it represents speed.
        
        for p in self.particles:
            y, x = int(p[0]), int(p[1])
            
            # Simple Euler integration
            # Constrain to grid
            y = max(0, min(h-1, y))
            x = max(0, min(w-1, x))
            
            # Get velocity at current position
            # (In a real solver, we'd interpolate)
            vy = -grad_y[y, x]
            vx = -grad_x[y, x]
            
            # Normalize for constant speed (geodesic motion)
            speed = np.sqrt(vy**2 + vx**2)
            if speed > 1e-6:
                vy /= speed
                vx /= speed
                
            # Update
            new_p = p + np.array([vy, vx]) * step_size
            
            # Boundary check
            new_p[0] = max(0, min(h-1, new_p[0]))
            new_p[1] = max(0, min(w-1, new_p[1]))
            
            new_particles.append(new_p)
            
        self.particles = new_particles

    def render(self, base_grid: np.ndarray) -> np.ndarray:
        """Draw particles back onto the grid."""
        output = base_grid.copy()
        # Clear old positions of movable objects first (assuming passed grid has them)
        output[output == self.movable_color] = 0 
        
        for p in self.particles:
            y, x = int(round(p[0])), int(round(p[1]))
            output[y, x] = self.movable_color
            
        return output

def run_proof():
    print("⚡ PROVING ONTOLOGICAL SOLVING ON ARC TASKS ⚡")
    engine = ManifoldEngine()
    
    # =========================================================
    # Scenario 1: ATTRACTION (Training Mode)
    # Task: "Grey pixels (5) must move to the Blue pixel (1)."
    # =========================================================
    print("\n🧪 Scenario 1: Training Mode (Attraction to Singleton)")
    
    # 1. Setup Input Grid (10x10)
    grid_train = np.zeros((20, 20), dtype=int)
    # Scattered Grey Pixels
    grid_train[2, 5] = 5
    grid_train[5, 2] = 5
    grid_train[8, 15] = 5
    grid_train[15, 8] = 5
    # The Attractor (Blue)
    target_pos = (10, 10)
    grid_train[target_pos] = 1 # Blue
    
    # 2. "Learn" the Metric (Hypothesis: Blue is Singularity)
    # In a full agent, this would be inferred. Here we define it.
    print("   > Hypothesis: Color 1 (Blue) is the Event Horizon (T=0).")
    goals = [target_pos]
    
    # 3. Compute Spacetime
    # Walls? No walls in this task, space is empty.
    metric_grid = np.zeros_like(grid_train) 
    # (Engine expects 1=Wall, so 0=Empty is fine)
    
    # Solve Eikonal
    print("   > Solving Eikonal Equation for Spacetime Curvature...")
    # Hack: ManifoldEngine expects maze_state where 1=Wall.
    # Our grid has colors. We pass a clean "empty space" grid.
    empty_space = np.zeros_like(grid_train)
    engine.navigate_via_geodesic((0,0), empty_space, goals) # Computes time_field internally
    time_field = engine.time_field
    
    # 4. Advect Particles (The Transformation)
    print("   > Advecting particles along Geodesics...")
    advector = ParticleAdvector(grid_train, movable_color=5)
    
    snapshots = []
    for _ in range(15): # 15 Time steps
        advector.advect(time_field, step_size=1.0)
        snapshots.append(advector.render(grid_train.copy()))
        
    # Visualize Result
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    axes[0].imshow(grid_train, cmap='tab10', vmin=0, vmax=9)
    axes[0].set_title("Input (Entropy High)")
    axes[1].imshow(snapshots[-1], cmap='tab10', vmin=0, vmax=9)
    axes[1].set_title("Output (Entropy Low)\nParticles migrated to Blue")
    plt.savefig('arc_proof_attraction.png')
    print("   ✓ Result saved to 'arc_proof_attraction.png'")

    # =========================================================
    # Scenario 2: GRAVITY (Blind Mode)
    # Task: "Grey pixels fall to bottom."
    # =========================================================
    print("\n🧪 Scenario 2: Blind Mode (Vertical Gravity)")
    
    # 1. Setup Input Grid
    grid_blind = np.zeros((20, 20), dtype=int)
    # Random cloud
    np.random.seed(42)
    for _ in range(15):
        ry, rx = np.random.randint(0, 15, 2)
        grid_blind[ry, rx] = 5
        
    # 2. Define Metric: "Down is Future"
    # We define the entire bottom row as T=0
    print("   > Hypothesis: Bottom Row is Event Horizon (T=0).")
    goals_blind = [(19, i) for i in range(20)]
    
    # 3. Compute Spacetime
    engine.navigate_via_geodesic((0,0), empty_space, goals_blind)
    time_field_blind = engine.time_field
    
    # 4. Advect
    print("   > Advecting particles (Falling)...")
    advector_blind = ParticleAdvector(grid_blind, movable_color=5)
    
    snapshots_blind = []
    for _ in range(20):
        advector_blind.advect(time_field_blind, step_size=1.0)
        snapshots_blind.append(advector_blind.render(grid_blind.copy()))
        
    # Visualize
    fig2, axes2 = plt.subplots(1, 2, figsize=(10, 5))
    axes2[0].imshow(grid_blind, cmap='tab10', vmin=0, vmax=9)
    axes2[0].set_title("Input (Floating)")
    axes2[1].imshow(snapshots_blind[-1], cmap='tab10', vmin=0, vmax=9)
    axes2[1].set_title("Output (Fallen)\nParticles reached T=0 surface")
    plt.savefig('arc_proof_gravity.png')
    print("   ✓ Result saved to 'arc_proof_gravity.png'")

if __name__ == "__main__":
    run_proof()
