"""
The Synthetic Merger: The Universal Geometry of Search.

Hypothesis: 
RNA Folding and Maze Solving are isomorphic. 
They are both "Search Processes" on a potentially infinite tree.
The Autopoietic Engine should detect the "Eigen-Logic" (Branching & Backtracking) 
as the high-gravity structure in both, ignoring the domain-specific details.

We define 'Search' as a sequence of States:
0: Move Forward / Pair Base
1: Branch / Fork
2: Dead End / Mismatch
3: Backtrack / Undo

We generate traces for both systems and check if the Engine lights up the 'Branching' points.
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from autopoietic_engine import AutopoieticEngine

# SYMBOLS (The Universal Alphabet of Search)
S_FORWARD = 0   # Deterministic Step
S_BRANCH = 1    # Decision Point (High Info)
S_DEADEND = 2   # Failure (Low Info?)
S_BACKTRACK = 3 # Correction

def generate_maze_trace(length=100):
    """
    Simulate a Depth-First Search in a Maze.
    Sequence: Forward -> Branch -> Forward -> DeadEnd -> Backtrack -> Branch...
    """
    trace = []
    stack = [0] # Depth
    
    while len(trace) < length:
        state = stack[-1]
        
        # Probabilities logic
        # If just started, forward.
        r = np.random.rand()
        
        if r < 0.90: 
            # Forward (deterministic corridor) - The Crystal
            trace.append(S_FORWARD)
            pass 
        elif r < 0.95:
            # Branching Point (New option) - The Defect
            trace.append(S_BRANCH)
            stack.append(state + 1) # Go deeper
        elif r < 0.98:
            # Dead End!
            trace.append(S_DEADEND)
            # Must backtrack next
        else:
            # Backtrack
            if len(stack) > 1:
                trace.append(S_BACKTRACK)
                stack.pop()
            else:
                trace.append(S_FORWARD) # Can't pop root
                
    return np.array(trace[:length])

def generate_rna_trace(length=100):
    """
    Simulate RNA Folding (Nussinov/Zuker Logic).
    Sequence: Pair -> Stack -> Bulge(Branch) -> Hairpin(DeadEnd) -> Backtrack
    Isomorphic to Maze!
    """
    # Just reuse logic but seeded differently to mimic 'biological' burstiness?
    # RNA tends to have long runs of Pairing (Forward) then sudden Loops.
    trace = []
    
    current_stem = 0
    t = 0
    while t < length:
        r = np.random.rand()
        if current_stem < 5:
            # Strong tendency to pair (Stem Formation)
            trace.append(S_FORWARD) 
            current_stem += 1
        elif r < 0.3:
            # Branch (Bulge/Multiloop)
            trace.append(S_BRANCH)
            current_stem = 0 # New stem starts
        elif r < 0.6:
            # Hairpin Turn (Dead End of stem)
            trace.append(S_DEADEND)
            # Will trigger unwind
        else:
            # Unwind/Backtrack to find optimal energy
            trace.append(S_BACKTRACK)
            if current_stem > 0: current_stem -= 1
            
        t += 1
    return np.array(trace[:length])

def run_synthetic_merger():
    print("Initializing Autopoietic Engine (Universal Logic Mode)...")
    engine = AutopoieticEngine()
    
    L = 64
    print(f"Generating Maze Logic Trace (L={L})...")
    trace_maze = generate_maze_trace(L)
    
    print(f"Generating RNA Logic Trace (L={L})...")
    trace_rna = generate_rna_trace(L)
    
    # Create the "Merger Grid"
    # We stack them to see if the Engine handles both as "One Physics".
    # Grid: Rows = Time, Cols = System (Maze vs RNA)
    # Actually let's make a grid where top half is Maze, bottom is RNA.
    
    width = 30
    # Map trace to 2D
    # Maze Grid
    maze_grid = trace_maze.reshape((-1, 8)) # 8cols
    # RNA Grid
    rna_grid = trace_rna.reshape((-1, 8))
    
    # Combine with a "Void" separator
    separator = np.zeros((2, 8), dtype=int) + 9 # 9 = Void
    
    merged_grid = np.vstack([maze_grid, separator, rna_grid])
    
    print("Calculating Universal Feature Density...")
    rho = engine.calculate_local_feature_density(merged_grid, window_size=3)
    
    # Visualize
    fig, axes = plt.subplots(1, 2, figsize=(10, 6))
    
    # Input
    axes[0].imshow(merged_grid, cmap='tab10')
    axes[0].set_title("Maze Logic (Top) vs RNA Logic (Bot)")
    
    # Output
    axes[1].imshow(rho, cmap='magma')
    axes[1].set_title("Universal Eigen-Logic (Density)")
    
    plt.savefig("synthetic_merger_proof.png")
    print("Saved synthetic_merger_proof.png")
    
    # Analysis: Do Branch points (1) have higher density than Forward (0)?
    # We need to check the rho values at locations where grid == S_BRANCH.
    
    mask_branch = (merged_grid == S_BRANCH)
    mask_forward = (merged_grid == S_FORWARD)
    
    rho_branch = np.mean(rho[mask_branch])
    rho_forward = np.mean(rho[mask_forward])
    
    print(f"Mean Density of BRANCH Points (Decision): {rho_branch:.4f}")
    print(f"Mean Density of FORWARD Points (Linear):  {rho_forward:.4f}")
    
    if rho_branch > rho_forward:
        print("\n🏆 SUCCESS: The Engine identified 'Decision Points' as High Gravity.")
        print("It found the Geometry of Search (Entropy) > Geometry of Flatness.")
    else:
        print("\nINCONCLUSIVE: Branching density not distinct.")

if __name__ == "__main__":
    run_synthetic_merger()
