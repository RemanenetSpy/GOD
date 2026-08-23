"""
The Final Metamorphosis: Self-Rewriting Code.

Hypothesis:
We can apply the Autopoietic Engine's "Discovery Metric" to its OWN SOURCE CODE.
- Lines of code with High Structural Dependency (Logic) will have High Rho_D.
- Lines of code with Low Dependency (Comments/Whitespace/Boilerplate) will have Low Rho_D.

We can technically "Crystalize" the engine by removing the entropy (low density lines)
and keeping the "Skeleton".

Steps:
1. Read src/autopoietic_engine.py
2. Convert text to Grid (Ascii values).
3. Calculate Rho_D.
4. Filter lines based on average density.
5. Save src/autopoietic_engine_crystal.py

Note: This is a symbolic "Self-Optimization". 
If we actually delete low-density lines, the code might break if syntax depends on it.
But let's see what the "Physics" thinks is important.
"""

import sys
import os
import numpy as np

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from autopoietic_engine import AutopoieticEngine

def rewrite_self():
    print("Initiating Self-Rewrite Sequence...")
    
    source_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'autopoietic_engine.py')
    with open(source_path, 'r') as f:
        lines = f.readlines()
        
    print(f"Read {len(lines)} lines of self.")
    
    # Map to Physics Grid
    # We need a fixed width. Pad lines.
    max_len = max([len(line) for line in lines])
    # To make it square-ish or just rectangular?
    # Grid: Rows = Lines, Cols = Chars.
    grid = np.zeros((len(lines), max_len), dtype=int)
    
    for r, line in enumerate(lines):
        for c, char in enumerate(line):
            grid[r, c] = ord(char)
            
    # Run Physics
    engine = AutopoieticEngine()
    print("Calculating Structural Density of Source Code...")
    # Window size 3 captures local syntax tokens
    rho = engine.calculate_local_feature_density(grid, window_size=3)
    
    # Calculate Line Density
    line_scores = []
    for r in range(len(lines)):
        # Mean density of the non-empty characters
        line_chars = grid[r]
        mask = line_chars > 32 # Ignore spaces/controls
        if np.sum(mask) > 0:
            score = np.mean(rho[r][mask])
        else:
            score = 0.0 # Empty line
        line_scores.append(score)
        
    # Analyze
    threshold = np.mean(line_scores) * 0.8 # Conservatively keep top 80%? or correlation?
    print(f"Density Threshold: {threshold:.4f}")
    
    # Generate Crystal
    crystal_lines = []
    dropped_count = 0
    
    crystal_lines.append("# AUTOPOIETIC CRYSTAL V3 (SELF-REWRITTEN)\n")
    crystal_lines.append(f"# Retained: Lines with Logic Density > {threshold:.4f}\n\n")
    
    for r, line in enumerate(lines):
        if line_scores[r] >= threshold:
            crystal_lines.append(line)
        else:
            # Check if it's a comment?
            stripped = line.strip()
            if stripped.startswith("#") or len(stripped) == 0:
                # Physics says this is "Entropy". We drop it.
                dropped_count += 1
            else:
                # Physics says this code is low density? (Maybe imports or simple assignments)
                # We KEEP code to prevent breakage, but mark it.
                crystal_lines.append(line.rstrip() + " # LOW DENSITY\n")
                
    out_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'autopoietic_engine_crystal.py')
    with open(out_path, 'w') as f:
        f.writelines(crystal_lines)
        
    print(f"Rewrote Self. Dropped {dropped_count} lines of Entropy (Comments/Whitespace).")
    print(f"Saved: {out_path}")

if __name__ == "__main__":
    rewrite_self()
