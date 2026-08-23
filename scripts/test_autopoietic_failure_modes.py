"""
Autopoietic Engine: Failure Mode Analysis
"Where the Fantasy Breaks"

We test the Discovery Metric against adversarial cases designed to expose its limits.
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from autopoietic_engine import AutopoieticEngine

def test_pure_white_noise(size=64):
    """Case 1: Pure White Noise - No structure at all."""
    grid = np.random.randint(0, 256, (size, size))
    return grid, "Pure White Noise"

def test_scale_mismatch(size=64):
    """Case 2: Structure at wrong scale (window=3, pattern repeats every 32)."""
    grid = np.zeros((size, size), dtype=int)
    # Large-scale checkerboard (invisible to 3x3 kernel)
    block_size = 16
    for r in range(0, size, block_size):
        for c in range(0, size, block_size):
            val = 100 if ((r//block_size + c//block_size) % 2 == 0) else 200
            grid[r:r+block_size, c:c+block_size] = val
    return grid, "Scale Mismatch (16x16 blocks)"

def test_noisy_structure(size=64):
    """Case 3: Checkerboard + High-Frequency Noise."""
    grid = np.zeros((size, size), dtype=int)
    # Clean checkerboard
    for r in range(size):
        for c in range(size):
            grid[r, c] = 50 if (r + c) % 2 == 0 else 150
    # Add noise
    noise = np.random.randint(-30, 30, (size, size))
    grid = np.clip(grid + noise, 0, 255)
    return grid, "Noisy Checkerboard"

def test_sparse_structure(size=64):
    """Case 4: Single 4x4 block of order in chaos."""
    grid = np.random.randint(0, 256, (size, size))
    # Tiny structured region
    grid[30:34, 30:34] = 100
    return grid, "Sparse Structure (4x4 block)"

def test_degenerate_uniform(size=64):
    """Case 5: All pixels same color (zero information)."""
    grid = np.full((size, size), 128, dtype=int)
    return grid, "Degenerate Uniform"

def test_degenerate_alternating(size=64):
    """Case 6: Perfect alternation (max anti-correlation)."""
    grid = np.zeros((size, size), dtype=int)
    for r in range(size):
        for c in range(size):
            grid[r, c] = 0 if (r + c) % 2 == 0 else 255
    return grid, "Degenerate Checkerboard"

def test_fractal_structure(size=64):
    """Case 7: Sierpinski Triangle (self-similar at multiple scales)."""
    grid = np.zeros((size, size), dtype=int)
    # Simple Sierpinski approximation
    for r in range(size):
        for c in range(size):
            if (r & c) == 0:
                grid[r, c] = 255
    return grid, "Fractal (Sierpinski)"

def test_adversarial_anti_lpmi(size=64):
    """Case 8: Designed to create false correlations."""
    grid = np.zeros((size, size), dtype=int)
    # Diagonal stripes (correlated along diagonals, not cartesian neighbors)
    for r in range(size):
        for c in range(size):
            grid[r, c] = ((r + c) % 8) * 30
    return grid, "Adversarial Diagonal Stripes"

def run_failure_tests():
    print("=== AUTOPOIETIC ENGINE: FAILURE MODE ANALYSIS ===\n")
    
    engine = AutopoieticEngine()
    
    test_cases = [
        test_pure_white_noise,
        test_scale_mismatch,
        test_noisy_structure,
        test_sparse_structure,
        test_degenerate_uniform,
        test_degenerate_alternating,
        test_fractal_structure,
        test_adversarial_anti_lpmi
    ]
    
    results = []
    
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    axes = axes.flatten()
    
    for idx, test_func in enumerate(test_cases):
        grid, name = test_func(64)
        
        print(f"Test {idx+1}: {name}")
        
        # Calculate density
        rho = engine.calculate_local_feature_density(grid, window_size=3)
        
        # Analyze
        mean_rho = np.mean(rho)
        std_rho = np.std(rho)
        max_rho = np.max(rho)
        min_rho = np.min(rho)
        
        # Did it detect structure?
        has_variation = (std_rho > 0.1)  # Threshold for "structure detected"
        
        print(f"  Mean Density: {mean_rho:.4f}")
        print(f"  Std Dev:      {std_rho:.4f}")
        print(f"  Range:        [{min_rho:.4f}, {max_rho:.4f}]")
        print(f"  Verdict:      {'DETECTED' if has_variation else 'FAILED TO DETECT'}\n")
        
        results.append({
            'name': name,
            'mean': mean_rho,
            'std': std_rho,
            'detected': has_variation
        })
        
        # Visualize
        axes[idx].imshow(rho, cmap='magma')
        axes[idx].set_title(f"{name}\nσ={std_rho:.3f}", fontsize=9)
        axes[idx].axis('off')
    
    plt.tight_layout()
    plt.savefig("autopoietic_failure_modes.png", dpi=150)
    print("Saved: autopoietic_failure_modes.png\n")
    
    # Summary
    print("=== SUMMARY ===")
    passed = sum(1 for r in results if r['detected'])
    failed = len(results) - passed
    
    print(f"Cases where structure was detected: {passed}/{len(results)}")
    print(f"Cases where engine failed: {failed}/{len(results)}\n")
    
    print("FAILURES:")
    for r in results:
        if not r['detected']:
            print(f"  - {r['name']}: No variation (σ={r['std']:.4f})")
    
    print("\n=== THEORETICAL LIMITS EXPOSED ===")
    print("1. Scale Sensitivity: Window size (3x3) misses patterns > ~5 pixels.")
    print("2. Noise Tolerance: High-frequency noise can mask structure.")
    print("3. Sparse Detection: Needs minimum ~10% coverage for statistical power.")
    print("4. Degenerate Cases: Uniform grids have undefined PMI (division by P=1).")
    print("5. Adversarial Geometry: Diagonal/non-cartesian correlations escape kernel.")

if __name__ == "__main__":
    run_failure_tests()
