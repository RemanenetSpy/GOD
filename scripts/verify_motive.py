import sys
import os
import numpy as np
import time

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from src.agent import Agent
from src.active_motives import MotiveType, MotivePhysics

def create_gravity_task_grid():
    """Create a grid that looks like it needs gravity."""
    # 10x10 Grid
    grid = np.zeros((10, 10), dtype=int)
    
    # Scattered pixels (high entropy if considered as random)
    # But if pushed down, they form a solid line (low entropy)
    for c in range(10):
        # Random height
        r = np.random.randint(0, 5)
        grid[r, c] = 1 # Red
        
    return grid

def verify_dream():
    print("==========================================")
    print("PHASE 5: VERIFYING SOVEREIGN MOTIVE")
    print("==========================================")
    
    # 1. Setup
    agent = Agent(engine_type='zero_point')
    input_grid = create_gravity_task_grid()
    
    print("\n1. Input Grid (High Entropy State)")
    # print(input_grid)
    
    # 2. Dream Loop
    print("\n2. Agent Dreaming...")
    start_time = time.time()
    
    motive, score = agent.dream(input_grid)
    
    elapsed = time.time() - start_time
    print(f"\n3. Awakening (Time: {elapsed:.2f}s)")
    print(f"   Selected Motive: {motive.name}")
    print(f"   Simulated Resonance: {score:.4f}")
    
    # 3. Verification
    # We expect GRAVITY_DOWN or maybe IDENTITY if resonance calculation is weird.
    # But GRAVITY_DOWN should produce a solid line at bottom -> Very low entropy -> High Resonance.
    
    if motive == MotiveType.GRAVITY_DOWN:
        print("\nSUCCESS: Agent correctly inferred 'Gravity' as the Sovereign Motive.")
    else:
        print(f"\nWARNING: Agent selected {motive.name}. (Expected GRAVITY_DOWN)")
        
    # Apply
    result = MotivePhysics.apply_motive(input_grid, motive)
    # print("\nResulting Grid:")
    # print(result)

if __name__ == "__main__":
    verify_dream()
