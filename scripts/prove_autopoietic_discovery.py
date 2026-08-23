"""
Prove Autopoietic Discovery: Finding Order in Chaos without Instructions.

Hypothesis: 
The Autopoietic Engine can identify a hidden pattern in random noise 
solely by detecting the 'Information Density' (LPMI) of the region.

We do NOT tell it "Find the blue square".
We calculate the Discovery Metric, and the Blue Square should 'light up' as a massive object.
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from autopoietic_engine import AutopoieticEngine

def create_chaos_with_hidden_order(size=30):
    """
    Create a grid of random noise, then inject a structured artifact.
    """
    np.random.seed(42)
    # 1. Chaos (Uniform Noise)
    grid = np.random.randint(0, 10, (size, size))
    
    # 2. Hidden Order (A 10x10 Checkerboard Artifact)
    # Checkerboard is highly structured (predictable neighbors)
    # but not a single color.
    start = 10
    end = 20
    for r in range(start, end):
        for c in range(start, end):
            if (r + c) % 2 == 0:
                grid[r, c] = 1 # Pattern A
            else:
                grid[r, c] = 2 # Pattern B
                
    return grid

def run_discovery_proof():
    print("Initializing Autopoietic Engine V2 (Discovery Mode)...")
    engine = AutopoieticEngine()
    
    print("Generating Chaos with Hidden Order...")
    grid = create_chaos_with_hidden_order()
    
    print("Calculating Local Feature Density (LPMI)...")
    rho = engine.calculate_local_feature_density(grid, window_size=3)
    
    print("Calculating Discovery Metric (Warp Factor)...")
    warp = engine.get_discovery_metric(grid)
    
    # Visualize
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # 1. Input
    axes[0].imshow(grid, cmap='tab10')
    axes[0].set_title("Input: Chaos + Hidden Artifact")
    
    # 2. Information Density (Rho)
    im2 = axes[1].imshow(rho, cmap='inferno')
    axes[1].set_title("Information Density (Rho_D)")
    plt.colorbar(im2, ax=axes[1])
    
    # 3. Metric Warp (Gravity)
    im3 = axes[2].imshow(warp, cmap='gray_r') # Dark = Low Cost = Well
    axes[2].set_title("Metric Tensor (Gravity Well)")
    plt.colorbar(im3, ax=axes[2])
    
    plt.savefig("autopoietic_discovery_proof.png")
    print("Saved autopoietic_discovery_proof.png")
    
    # Check if peak density aligns with artifact
    # Artifact is at 10:20, 10:20
    # Let's check mean density inside vs outside
    mask = np.zeros_like(grid, dtype=bool)
    mask[10:20, 10:20] = True
    
    mean_inside = np.mean(rho[mask])
    mean_outside = np.mean(rho[~mask])
    
    print(f"Mean Density Inside Artifact: {mean_inside:.4f}")
    print(f"Mean Density Outside Artifact: {mean_outside:.4f}")
    
    if mean_inside > mean_outside * 1.5:
        print("\n🏆 SUCCESS: The Engine Discovered the Pattern by itself!")
    else:
        print("\nFAILURE: Signal to Noise ratio too low.")

if __name__ == "__main__":
    run_discovery_proof()
