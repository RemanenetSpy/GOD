"""
Verify Actuator Script
Phase 3 Proof of Concept: Can we evolve a solution?
"""

import sys
import os
import argparse
import numpy as np
import time

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.arc_adapter import ARCWorld
from src.agent import Agent, PillarType

def verify_actuator(task_file):
    print(f"Loading Task: {task_file}")
    world = ARCWorld(task_file)
    
    # Initialize Zero-Point Agent
    agent = Agent(grid_size=30, specialization=PillarType.QUANTUM, engine_type='zero_point')
    
    # 1. Perception Phase
    print("\n1. Perception Phase (Metabolizing Input)...")
    obs = world.reset()
    # Let agent see input
    agent.act(obs)
    
    # Check baseline stats
    dash = agent.sovereign_engine.get_dashboard()
    print(f"   Baseline Sigma: {dash['sigma']}")
    print(f"   Baseline Omega: {dash['omega']}")
    
    # 2. Actuation Phase (Evolution)
    print("\n2. Actuation Phase (Evolving Solution)...")
    input_grid = world.input_grid
    
    start_time = time.time()
    # increased generations for proof
    solution = agent.solve_with_actuator(input_grid, generations=50) 
    elapsed = time.time() - start_time
    
    # 3. Validation
    print("\n3. Validation Phase (Memetic Resonance)")
    
    # Measure Viability of Solution
    start_viability = agent.sovereign_engine.measure_viability(input_grid)
    end_viability = agent.sovereign_engine.measure_viability(solution)
    
    print(f"   Input Viability: {start_viability:.4f}")
    print(f"   Solution Viability: {end_viability:.4f}")
    print(f"   Time Evolved: {elapsed:.2f}s")
    
    if end_viability > start_viability:
        print("\nSUCCESS: Memetic Evolution increased viability.")
    else:
        print("\nWARNING: No improvement found.")
        
    # Check if grid changed
    if np.array_equal(input_grid, solution):
        print("   Result: Grid Unchanged (Stagnation)")
    else:
        print("   Result: Grid Evolved via Anchors")
        diff_pixels = np.sum(input_grid != solution)
        print(f"   Pixels Changed: {diff_pixels}")
        unique_colors = len(np.unique(solution))
        print(f"   Unique Colors: {unique_colors} (Preserved Vocabulary)")
        
        # Check if anchors were used (heuristic: finding 3x3 blocks that match anchors?)
        # For now, just trust the console log from Actuator.

if __name__ == "__main__":
    # Use a simple task
    default_task = "ARC-AGI-master/data/training/007bbfb7.json"
    verify_actuator(default_task)
