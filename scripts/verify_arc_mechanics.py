import sys
import os
import time
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.arc_adapter import ARCWorld
from src.environment import Action

def verify_mechanics():
    print("--- 🧪 Verifying ARC Agent Capabilities ---")
    
    # Load Task
    task_path = os.path.join("ARC-AGI-master", "data", "training", "007bbfb7.json")
    if not os.path.exists(task_path):
        print(f"❌ Task file not found: {task_path}")
        return

    world = ARCWorld(task_path)
    print(f"✅ Loaded Task 007bbfb7. Target Grid Size: {world.target_grid.shape}")
    
    # "Cheat" to generate perfect actions
    target = world.target_grid
    h, w = target.shape
    
    total_steps = 0
    total_reward = 0
    
    # Strategy: Raster scan and paint
    # We will verify that:
    # 1. Navigation works (Agent moves)
    # 2. Painting works (Grid updates)
    # 3. Reward system emits signal
    
    print("\n--- 🤖 Commencing Auto-Pilot (Perfect Solver) ---")
    
    # Reset
    obs = world.reset()
    start_pos = obs.position
    print(f"Start Pos: {start_pos}")
    
    # Move to 0,0 (already there)
    
    success = True
    
    for r in range(h):
        for c in range(w):
            # 1. Navigate to (r, c)
            curr_r, curr_c = world.agent_position
            
            # Simple Manhattan routing
            curr_r, curr_c = world.agent_position
            
            while curr_r < r:
                obs, _, _ = world.step(Action.MOVE_DOWN)
                curr_r, curr_c = obs.position
            while curr_r > r:
                obs, _, _ = world.step(Action.MOVE_UP)
                curr_r, curr_c = obs.position
            while curr_c < c:
                obs, _, _ = world.step(Action.MOVE_RIGHT)
                curr_c = obs.position[1]
            while curr_c > c:
                obs, _, _ = world.step(Action.MOVE_LEFT)
                curr_c = obs.position[1]
            
            # Verify Position
            if obs.position != (r, c) and list(obs.position) != [r, c]:
                print(f"❌ Navigation Failed. Expected {[r, c]}, Got {obs.position}")
                success = False
                break
                
            # 2. Paint
            color = target[r, c]
            # Map Integer to Action
            # PAINT_0 is 10
            action = Action(10 + color)
            
            obs, reward, done = world.step(action)
            total_reward += reward
            
            # Verify Paint
            actual_color = world.current_grid[r, c]
            if actual_color != color:
                print(f"❌ Painting Failed at {[r, c]}. Expected {color}, Got {actual_color}")
                success = False
                break
                
            # print(f"Painted ({r},{c}) -> {color} (Reward: {reward})")
            
    if success:
        # Check Final State
        if np.array_equal(world.current_grid, world.target_grid):
            print("\n✅ SUCCESS: Agent successfully replicated the Target Grid!")
            print(f"🏆 Total Reward: {total_reward}")
            print("Proof: The Agent Body (Actions/Sensors) is fully capable of passing the test.")
        else:
            print("\n❌ FAILURE: Grids do not match after perfect run.")
            
    print("-------------------------------------------")

if __name__ == "__main__":
    verify_mechanics()
