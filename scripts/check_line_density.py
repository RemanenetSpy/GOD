"""
Check Line Density
Inspects the calculated information density for EVERY line in a target file.
"""
import sys
import os
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from autopoietic_engine import AutopoieticEngine

def check_file(file_path):
    print(f"Scanning: {os.path.basename(file_path)}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    engine = AutopoieticEngine()
    
    # Grid construction
    max_len = max(len(line) for line in lines)
    grid_size = max(len(lines), max_len)
    grid = np.zeros((grid_size, grid_size), dtype=int)
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if j < grid_size:
                grid[i, j] = ord(char)
                
    # Calculate Density
    rho = engine.calculate_local_feature_density(grid, window_size=3)
    
    print("\nLine Density Report:")
    print(f"{'Line':<5} | {'Density':<8} | {'Content'}")
    print("-" * 60)
    
    densities = []
    
    for i, line in enumerate(lines):
        line_len = len(line)
        if line_len > 0:
            row_vals = rho[i, :line_len]
            # avg_density = np.mean(row_vals) if len(row_vals) > 0 else 0
            # Let's use the Max density in the line - usually identifying the "core" structure
            avg_density = np.mean(row_vals)
        else:
            avg_density = 0
            
        densities.append(avg_density)
        
        # Highlight interesting lines (Attack lines for BridgeReentrancyAttack)
        prefix = " "
        if i+1 in [33, 42]: prefix = "->" # Vulnerable lines
        
        print(f"{prefix} {i+1:<4} | {avg_density:.6f} | {line.strip()[:60]}")

    print("-" * 60)
    print(f"Mean Density: {np.mean(densities):.6f}")
    
target_file = os.path.join(os.path.dirname(__file__), '..', 'SolvBTC.sol')

check_file(target_file)
