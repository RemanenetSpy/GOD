import sys
import os
import numpy as np
import time

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from src.agent import Agent
from src.environment import Observation
from src.active_motives import MotiveType, MotivePhysics
from src.causal_hypotheses import HypothesisEngine, ConditionType

def create_selective_gravity_task():
    """
    Task: Red (1) pixels fall. Blue (2) pixels stay.
    """
    input_grid = np.zeros((10, 10), dtype=int)
    output_grid = np.zeros((10, 10), dtype=int)
    
    # Setup
    for c in range(5):
        # Red pixel (Falls)
        input_grid[2, c] = 1 
        output_grid[9, c] = 1
        
    for c in range(5, 10):
        # Blue pixel (Stays)
        input_grid[2, c] = 2
        output_grid[2, c] = 2
        
    return input_grid, output_grid

def verify_causal_leap():
    print("==========================================")
    print("PHASE 6: VERIFYING CAUSAL LEAP")
    print("==========================================")
    
    # 1. Setup
    agent = Agent(engine_type='zero_point')
    inp, out = create_selective_gravity_task()
    
    train_examples = [{'input': inp, 'output': out}]
    
    # Manually load examples into agent
    agent.active_train_examples = train_examples
    
    print("\n1. Scenario: Red falls, Blue stays.")
    print("   Input has 5 Red, 5 Blue pixels.")
    
    # 2. Dream (Expect Gravity)
    print("\n2. Dreaming of Motives (on Input)...")
    motive, score = agent.dream(inp)
    print(f"   Sovereign Motive: {motive.name}")
    
    # 3. Reason
    print("\n3. Reasoning (Searching for Constraints)...")
    rule = HypothesisEngine.reason(motive, train_examples)
    
    print(f"\n4. Discovery: {rule}")
    
    # 4. Verify
    if rule.condition_type == ConditionType.IS_COLOR and rule.condition_value == 1 and rule.motive == MotiveType.GRAVITY_DOWN:
        print("SUCCESS: Agent discovered 'IF Red THEN Gravity Down'.")
    elif rule.condition_type == ConditionType.IS_NOT_COLOR and rule.condition_value == 2 and rule.motive == MotiveType.GRAVITY_DOWN:
        print("SUCCESS: Agent discovered 'IF NOT Blue THEN Gravity Down'.") # Also valid
    else:
        print(f"FAILURE: Agent discovered {rule} (Expected IF Red THEN Gravity)")
        
    # Test Application
    res = rule.apply(inp)
    match = np.array_equal(res, out)
    print(f"   Application Result Match: {match}")

if __name__ == "__main__":
    verify_causal_leap()
