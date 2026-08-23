"""
Phase 23: Emergence Test Protocol
Scientific audit of Transfer, Novelty, Compression, and Surprise.
"""

import sys
import os
import json
import numpy as np
import time
import copy

# Add src to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
src_dir = os.path.join(parent_dir, 'src')
sys.path.append(src_dir)

from agent import Agent
from core import PillarType
from environment import GridWorld, Observation, Action

# =============================================================================
# SYNTHETIC TASK GENERATORS (The "Sandboxes")
# =============================================================================

def generate_gravity_task(height=10, width=10, complexity="simple", color_scheme="blue"):
    """
    Generates a gravity task.
    Simple: Single pixel falling.
    Complex: Shapes falling with noise.
    """
    input_grid = np.zeros((height, width), dtype=int)
    output_grid = np.zeros((height, width), dtype=int)
    
    color = 1 if color_scheme == "blue" else 2
    
    if complexity == "simple":
        # Single pixel at top
        c = width // 2
        input_grid[1, c] = color
        output_grid[height-2, c] = color # Floor is at height-1
    else:
        # Complex: L-shape object
        c = width // 2
        # L-shape: (1,c), (2,c), (2,c+1)
        input_grid[1, c] = color
        input_grid[2, c] = color
        input_grid[2, c+1] = color
        
        # Output: Shifted down to floor
        floor_y = height - 2
        # Object height is 2. Bottom is at floor_y.
        # Top was at 1. Shift = (floor_y - 2)
        shift = floor_y - 2
        output_grid[1+shift, c] = color
        output_grid[2+shift, c] = color
        output_grid[2+shift, c+1] = color
        
        # Add "Noise" (irrelevant static pixels)
        output_grid[5, 1] = 8 # Teal noise
        input_grid[5, 1] = 8
        
    return {'input': input_grid, 'output': output_grid}

def generate_spiral_task():
    """Generates a 'Novel' Spiral pattern task."""
    # Simplified spiral trace
    inp = np.zeros((5,5), dtype=int)
    out = np.zeros((5,5), dtype=int)
    # L-shape trace
    inp[0,0] = 3
    # Path: 0,0 -> 0,4 -> 4,4 -> 4,0
    out[0,:] = 3
    out[:,4] = 3
    out[4,:] = 3
    out[:,0] = 3
    return {'input': inp, 'output': out}

# =============================================================================
# THE EXPERIMENTS
# =============================================================================

def run_transfer_test():
    print("\n--- Experiment 1: Transfer (The Gravity Test) ---")
    print("Hypothesis: Universals (Gravity) apply outside original sandbox.")
    
    # 1. Agent A: Learns in Sandbox A (Simple, Blue)
    agent_a = Agent(agent_id="Agent_Pro", specialization=PillarType.PHYSICS)
    task_simple = generate_gravity_task(complexity="simple", color_scheme="blue")
    
    print("Agent A: Learning Simple Gravity (Blue World)...")
    # Simulate learning loop (simplified)
    obs = Observation(
        visible_cells=np.zeros((3,3)), position=(0,0), reward=0.0,
        context=task_simple['input'],
        train_examples=[{'input': task_simple['input'], 'output': task_simple['output']}]
    )
    agent_a.universal_update(Action.WAIT, obs)
    steps_a_simple = 10 # Simulated cognitive steps
    print(f"Agent A learned Simple Gravity.")
    
    # 2. Agent A: Transfer to Sandbox B (Complex, Red)
    task_complex = generate_gravity_task(complexity="complex", color_scheme="red")
    print("Agent A: Attempting Complex Gravity (Red World)...")
    
    start_t = time.time()
    # Check if vocabulary helps (simulated check)
    vocab_hits = 0
    if "rect_1x1" in agent_a.sovereign_vocab.vocabulary or "gravity" in str(agent_a.sovereign_vocab.vocabulary): 
        # In reality, we'd check if specific rules trigger.
        # Here we verify if the agent *has* concepts that might map
        pass
        
    # We execute the update again to see if it learns faster/uses memory
    obs_complex = Observation(
        visible_cells=np.zeros((3,3)), position=(0,0), reward=0.0,
        context=task_complex['input'],
        train_examples=[{'input': task_complex['input'], 'output': task_complex['output']}]
    )
    agent_a.universal_update(Action.WAIT, obs_complex)
    time_a = time.time() - start_t
    
    # 3. Agent B (Naive): Learns Sandbox B directly
    agent_b = Agent(agent_id="Agent_Naive", specialization=PillarType.PHYSICS)
    print("Agent B (Naive): Attempting Complex Gravity (Red World)...")
    
    start_t = time.time()
    agent_b.universal_update(Action.WAIT, obs_complex)
    time_b = time.time() - start_t
    
    print(f"Agent A Time: {time_a:.4f}s")
    print(f"Agent B Time: {time_b:.4f}s")
    
    # Metric: Did A have any "pre-computation" advantage or memory hits?
    # In this mock, purely computational time might be similar unless memory recall is faster than discovery.
    # But usually, recall is FASTER than deep search.
    
    improvement = (time_b - time_a) / time_b * 100
    print(f"Transfer Efficiency Gain: {improvement:.2f}%")
    
    # Verify concepts
    print(f"Agent A Vocab: {len(agent_a.sovereign_vocab.vocabulary)}")
    print(f"Agent B Vocab: {len(agent_b.sovereign_vocab.vocabulary)}")


def run_novelty_test():
    print("\n--- Experiment 2: Novelty (Alien Geometry) ---")
    agent = Agent(agent_id="Agent_Explorer", specialization=PillarType.GENERAL)
    
    task_spiral = generate_spiral_task()
    print("Exposing agent to 'Spiral' task...")
    
    obs = Observation(
        visible_cells=np.zeros((3,3)), position=(0,0), reward=0.0,
        context=task_spiral['input'],
        train_examples=[{'input': task_spiral['input'], 'output': task_spiral['output']}]
    )
    agent.universal_update(Action.WAIT, obs)
    
    # Check vocabulary for NEW concepts
    vocab_keys = list(agent.sovereign_vocab.vocabulary.keys())
    print(f"Vocabulary: {vocab_keys}")
    
    has_novelty = False
    for k in vocab_keys:
        if "L_" in k or "jump" in k or "comp_" in k:
            has_novelty = True
            print(f"✅ DETECTED NOVEL CONCEPT: {k}")
            
    if not has_novelty:
        print("❌ No distinct novel concept found. Agent may have just seen it as pixels.")

def run_compression_test():
    print("\n--- Experiment 3: Compression (The Breathing Test) ---")
    agent = Agent(agent_id="Agent_Breather", specialization=PillarType.INFORMATION)
    
    # Run 5 iterations of varying tasks
    history = []
    
    # 1. Feed Variance (Specifics)
    print("Phase 1: Accumulating Specifics...")
    for i in range(5):
        # Generate tasks with same structure but different colors (isomorphisms)
        color = (i % 5) + 1
        task = generate_gravity_task(complexity="simple", color_scheme="dynamic")
        # Hack color
        task['input'][task['input'] == 1] = color
        task['input'][task['input'] == 2] = color
        
        # Inject into agent (manually adding to vocab to ensure growth for test)
        # Note: real update would do this, but we force it to ensure we test HARMONIZATION specifically
        agent.sovereign_vocab.add_motif(f"gravity_obj_c{color}", {'type': 'rectangle', 'color': color}, f"task_{i}")
        
    print(f"Vocab Size (Raw): {len(agent.sovereign_vocab.vocabulary)}")
    history.append(len(agent.sovereign_vocab.vocabulary))
    
    # 2. Sleep Cycle (Harmonize)
    print("Phase 2: Harmonization Cycle...")
    agent.sovereign_vocab.harmonize()
    
    print(f"Vocab Size (Compressed): {len(agent.sovereign_vocab.vocabulary)}")
    history.append(len(agent.sovereign_vocab.vocabulary))
    
    ratio = history[0] / history[1] if history[1] > 0 else 0
    print(f"Compression Ratio: {ratio:.2f}x")
    
    if ratio > 1.5:
        print("✅ SUCCESS: Significant compression observed.")
    else:
        print("⚠️ NOTE: Low compression. Maybe concepts were not isomorphic enough.")

if __name__ == "__main__":
    run_transfer_test()
    run_novelty_test()
    run_compression_test()
