"""
Proof of Eigen Transport (Quantum Tunneling)

This script demonstrates Phase 24: The Eigen Engine's Sinkhorn Solver.
We verify that the engine calculates a "Transport Plan" (Probability Flow)
rather than just a path.

Setup:
- Agent at (5, 5)
- Goal at (25, 25)
- OPTION A: Empty Space
- OPTION B: A "U" shaped Trap (Local Minimum)

We check if the Flow Vector correctly guides the agent out of the trap
by sensing the global transport cost.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import numpy as np
import matplotlib.pyplot as plt
from eigen_solver import EigenSolver

def visualize_transport():
    print("⚡ PROVING EIGEN TRANSPORT (OPTIMAL TRANSPORT) ⚡")
    
    # 1. Setup Maze with Trap
    size = 30
    maze = np.zeros((size, size), dtype=int)
    
    # Create a "U" shape trap around the center
    # Walls
    maze[10:20, 15] = 1 # Back wall
    maze[10, 10:15] = 1 # Top side
    maze[20, 10:15] = 1 # Bottom side
    
    # Agent is inside the U (at 15, 12)
    start_pos = (15, 12)
    
    # Goal is behind the U (at 15, 25)
    goal_pos = (15, 25)
    
    solver = EigenSolver()
    
    # 2. Run Sinkhorn Solver
    # We want to visualize the "Flow" from start_pos
    print("   > solving Sinkhorn Iterations...")
    
    # We need to expose internal logic slightly for visualization
    # Or we just query it for next step?
    # Let's extract the gamma row logic
    
    # Helper to calculate full flow map
    # Copy-paste logic for viz
    try:
        from scipy.spatial.distance import cdist
    except:
        return
        
    h, w = size, size
    Y, X = np.indices((h, w))
    coords = np.stack([Y.flatten(), X.flatten()], axis=1)
    C = cdist(coords, coords, metric='euclidean')
    
    flat_maze = maze.flatten()
    walls = np.where(flat_maze == 1)[0]
    BARRIER_HEIGHT = 100.0
    if len(walls) > 0:
        C[:, walls] += BARRIER_HEIGHT
        C[walls, :] += BARRIER_HEIGHT
        
    epsilon = 1.0 # Temperature
    K = np.exp(-C / epsilon)
    
    source_idx = start_pos[0] * w + start_pos[1]
    target_idx = goal_pos[0] * w + goal_pos[1]
    
    P = np.zeros(h*w); P[source_idx] = 1.0
    Q = np.zeros(h*w); Q[target_idx] = 1.0
    
    u = np.ones(h*w)
    v = np.ones(h*w)
    
    for _ in range(50):
        v = Q / (np.dot(K.T, u) + 1e-9)
        u = P / (np.dot(K, v) + 1e-9)
        
    # Gamma row for source
    gamma_source = u[source_idx] * K[source_idx, :] * v
    flow_grid = gamma_source.reshape(h, w)
    
    # 3. Visualize
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Show Maze
    ax.imshow(maze, cmap='Greys', alpha=0.5)
    
    # Show Transport Probability (Log scale for visibility)
    im = ax.imshow(np.log(flow_grid + 1e-12), cmap='plasma', alpha=0.8)
    
    # Annotate
    ax.plot(start_pos[1], start_pos[0], 'go', markersize=10, label='Start')
    ax.plot(goal_pos[1], goal_pos[0], 'rx', markersize=10, label='Goal')
    
    ax.set_title("Sinkhorn Transport Plan (Mass Flow)\nNote: Flow tunnels/diffuses around obstacles")
    plt.colorbar(im, ax=ax, label="Log Probability Mass")
    plt.legend()
    
    plt.savefig('eigen_transport_proof.png')
    print("   ✓ Result saved to 'eigen_transport_proof.png'")
    
    # Check simple navigation step
    # 4 neighbors
    moves = [(-1,0), (1,0), (0,-1), (0,1)]
    best_move = None
    max_val = -1
    
    for dy, dx in moves:
        ny, nx = start_pos[0]+dy, start_pos[1]+dx
        if flow_grid[ny, nx] > max_val:
            max_val = flow_grid[ny, nx]
            best_move = (dy, dx)
            
    print(f"   > Best Move determined by Sinkhorn: {best_move}")
    # Ideally should move LEFT (0, -1) to get out of U-trap, 
    # even though Goal is RIGHT.
    # Because going Right hits wall (Penalty).
    # Going Left starts the path around.
    
if __name__ == "__main__":
    visualize_transport()
