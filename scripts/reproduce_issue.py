import sys
import os
import json
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.arc_adapter import ARCWorld, run_agent_with_motion
from src.agent import Agent
from src.environment import Observation

def reproduce(task_filename):
    task_file = os.path.join("ARC-AGI-master", "data", "training", task_filename)
    if not os.path.exists(task_file):
        print(f"Task file not found: {task_file}")
        return

    print(f"--- Reproducing Issue for {task_file} ---")
    
    with open(task_file, 'r') as f:
        task_data = json.load(f)

    # Use a dummy environment to learn rules from training examples
    # (The agent learns in universal_update if train_examples are provided)
    agent = Agent(grid_size=30)
    
    # Simulate first observation with training examples to trigger learning
    first_train = task_data['train'][0]
    obs = Observation(
        visible_cells=np.array(first_train['input']),
        position=(0, 0),
        reward=0.0,
        context=np.array(first_train['input']),
        train_examples=[{
            'input': np.array(p['input']),
            'output': np.array(p['output'])
        } for p in task_data['train']]
    )
    
    # This should trigger rule learning
    agent.universal_update(None, obs)
    
    # Check learned rules
    rules = agent.state.world_model.learned_transformations
    print(f"\nLearned {len(rules)} rules:")
    for i, r in enumerate(rules):
        print(f"  {i}: Type={r.condition_type}, In={r.input_color}, Out={r.output_color}, Param={r.parameter}")

    # Now run on test input
    test_input = np.array(task_data['test'][0]['input'])
    print(f"\nRunning on test input (shape {test_input.shape})...")
    
    # Sweep across the grid
    rows, cols = test_input.shape
    output_grid = np.zeros_like(test_input)
    
    for r in range(rows):
        for c in range(cols):
            # Observe current state
            obs = Observation(
                visible_cells=np.zeros((3,3)), # Local view not used for reflex
                position=(r, c),
                reward=0.0,
                context=test_input
            )
            # Sync agent's grid
            agent.state.world_model.grid[(r, c)] = output_grid[r, c]
            
            # Act
            action = agent.choose_action(obs)
            if action.value >= 10:
                output_grid[r, c] = action.value - 10
    
    print("\nResulting Output Grid (first 5 rows/cols):")
    print(output_grid[:5, :10])
    
    # Check if any non-zero pixels were painted
    if np.any(output_grid != 0):
        print("\nAgent painted non-zero colors.")
    else:
        print("\nAgent painted EVERYTHING as color 0 (Filling Background).")
        
    # Check task 0 specific expectation: col 5 is 3, col 10 is 4? 
    # (Actually depends on the test input, let's see)
    test_expected = np.array(task_data['test'][0]['output'])
    matches = np.array_equal(output_grid, test_expected)
    if matches:
        print("\n✅ SUCCESS: Agent solved the task!")
    else:
        print("\n❌ FAILURE: Agent output does not match expected output.")

if __name__ == "__main__":
    reproduce("0a938d79.json")
    print("\n" + "="*50 + "\n")
    reproduce("00d62c1b.json")
