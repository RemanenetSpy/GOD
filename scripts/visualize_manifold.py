"""
Visualization of Manifold Gravity (Ontology Proof)

This script demonstrates that the Manifold Engine is not just a "maze solver",
but a generator of Curved Spacetime (Information Manifold).

We visualize:
1. The Metric Field (Time Dilation)
2. The Scalar Potential T(x) (Proper Time to Future)
3. The Geodesic Flow (The inevitable path of the agent)

This proves the engine creates a "Universe" where motion is a property of space.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import numpy as np
import matplotlib.pyplot as plt
from manifold_engine import ManifoldEngine

def visualize_gravity():
    # 1. Setup the "Universe" (Empty Space, 50x50)
    size = 50
    universe = np.zeros((size, size), dtype=int)
    
    # 2. Add "Masses" (Obstacles/High Curvature)
    # A generic obstacle in the center
    universe[20:30, 20:30] = 1 
    
    # 3. Add "Future" (Goals/Sink)
    # The agent's destination is the "Big Bang" or "Big Crunch"
    goals = [(45, 45), (5, 45)]
    
    # 4. Initialize Engine
    engine = ManifoldEngine()
    
    # 5. Compute the Field
    # This invokes the "Physics" of the engine
    print("Computing Spacetime Curvature...")
    
    # We use the internal method to get the full field
    # (metric construction logic duplicated for visualization)
    refractive_index = np.ones((size, size), dtype=float)
    refractive_index[universe == 1] = 1000.0 # Infinite curvature/mass
    
    time_field = engine._solve_eikonal(refractive_index, goals)
    
    # 6. Visualize
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    
    # Plot 1: The Scalar Field T(x) (Time to Future)
    # This shows the "Slope" of the universe.
    im1 = axes[0].imshow(time_field, cmap='plasma', origin='upper')
    axes[0].set_title("Scalar Potential T(x)\n(Darker = Closer to Future)")
    fig.colorbar(im1, ax=axes[0], label="Proper Time")
    
    # Plot 2: Geodesic Flow (Vector Field)
    # This shows the "River" of gravity.
    Y, X = np.mgrid[0:size, 0:size]
    mask = np.zeros_like(time_field, dtype=bool)
    mask[::2, ::2] = True # Subsample for cleaner arrows
    
    # Compute gradients (Flow)
    dy, dx = np.gradient(-time_field) # Negative gradient = Downhill
    
    axes[1].imshow(universe, cmap='Greys', alpha=0.3, origin='upper')
    axes[1].quiver(X[mask], Y[mask], dx[mask], dy[mask], color='blue', scale=20, width=0.002)
    
    # Plot Goals
    for gy, gx in goals:
        axes[1].plot(gx, gy, 'r*', markersize=15, label='Future (Goal)')
        axes[0].plot(gx, gy, 'w*', markersize=10)
        
    axes[1].set_title("Geodesic Flow Field\n(The 'Shape' of Space)")
    axes[1].legend()
    
    plt.tight_layout()
    plt.savefig('manifold_gravity_proof.png')
    print("✓ Visualization saved to 'manifold_gravity_proof.png'")
    # plt.show() # Uncomment if interactive

if __name__ == "__main__":
    visualize_gravity()
