"""
Verify Gravity and Eigen Logic
Mimics engine_maze_battle environment (Walls=2)
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import numpy as np
from gravity_engine import GravityEngine
from eigen_solver import EigenSolver

def test_gravity():
    print("Testing Gravity Engine...")
    engine = GravityEngine()
    
    # Create 11x11 grid (like visible view)
    size = 11
    maze_state = np.zeros((size, size), dtype=int)
    
    # Walls = 2
    wall_value = 2
    maze_state[5, 8] = wall_value # Wall to the right
    maze_state[5, 6:8] = wall_value
    
    # Agent at center (5, 5)
    center = (5, 5)
    
    # Goal at (5, 9) (Behind wall)
    goals = [(5, 9)]
    
    print(f"Goal: {goals}")
    print(f"Walls at: {np.argwhere(maze_state==wall_value)}")
    
    # Run Potential Field
    field = engine.calculate_potential_field(
        maze_state, goal_pos=None, wall_value=wall_value, goals=goals
    )
    
    print(f"Field at agent {center}: {field[center]}")
    print(f"Field around agent:")
    print(field[4:7, 4:7])
    
    action = engine.navigate_via_gradient(field, center)
    print(f"Gravity Action: {action} (0=UP, 1=DOWN, 2=LEFT, 3=RIGHT)")
    
    # Expectation: Should move UP or DOWN to go around wall, or WAIT if trapped?
    # Wall is at (5, 6), (5, 7), (5, 8).
    # Goal is at (5, 9).
    # Path should go (4, 6) or (6, 6).
    # So Action should be 0 (UP) or 1 (DOWN).
    
    # Check Infinity
    if np.isinf(field[center]):
        print("FAIL: Infinite potential at agent!")

def test_eigen():
    print("\nTesting Eigen Solver...")
    solver = EigenSolver()
    
    # Same setup
    size = 11
    maze_state = np.zeros((size, size), dtype=int)
    wall_value = 2
    
    # U-Trap
    maze_state[4:7, 7] = wall_value # Back
    maze_state[4, 5:7] = wall_value # Top
    maze_state[6, 5:7] = wall_value # Bottom
    
    # Agent at (5, 5). Surrounded by Top, Bottom, and Right?
    # (4, 5) is Wall? Yes. (6, 5) is Wall? Yes.
    # (5, 6) is implied empty? No, wait.
    # Maze coords (row, col).
    # Agent (5, 5).
    # (4, 5) = Top neighbor. Wall.
    # (6, 5) = Bottom neighbor. Wall.
    # (5, 6) = Right neighbor. Empty?
    # Wait, (4, 5:7) means (4, 5) and (4, 6).
    # So Top and Top-Right are walls.
    
    # Let's make a clear U-shape opening to Left.
    # Agent at (5, 5).
    # Wall at (5, 6) (Right).
    maze_state[5, 6] = wall_value
    # Wall at (4, 6) (Top Right)
    # Wall at (6, 6) (Bottom Right)
    # Wall at (4, 5) (Top)
    maze_state[4, 5] = wall_value
    # Wall at (6, 5) (Bottom)
    maze_state[6, 5] = wall_value
    
    # Only Way out is LEFT (0, -1).
    # Goal is RIGHT (5, 9).
    
    goals = (5, 9)
    valid_neighbors = [(0, 4, 5), (1, 6, 5), (2, 5, 4), (3, 5, 6)]
    # Filter valid neighbors (remove walls)
    # (4, 5) is wall -> remove.
    # (6, 5) is wall -> remove.
    # (5, 6) is wall -> remove.
    # (5, 4) is empty -> Keep.
    
    real_valid = []
    actions = [(0, -1, 0), (1, 1, 0), (2, 0, -1), (3, 0, 1)]
    for idx, dy, dx in actions:
        ny, nx = 5+dy, 5+dx
        if maze_state[ny, nx] != wall_value:
             real_valid.append((idx, ny, nx))
             
    print(f"Valid Neighbors: {real_valid}") # Should be only LEFT (Idx 2)
    
    visit_history = {}
    
    action = solver.navigate_via_flow_field(
        (5, 5), goals, maze_state, visit_history, real_valid, wall_value=wall_value
    )
    
    print(f"Eigen Action: {action}")
    # Expect 2 (LEFT).
    
if __name__ == "__main__":
    test_gravity()
    test_eigen()
