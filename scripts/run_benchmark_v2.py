"""
Phase 22: Benchmark V2 (Sovereign Harmonization)
Runs 20 diverse tasks with a Sovereign Agent.
Triggers Autonomous Harmonization periodically to observe vocabulary compression.
"""

import sys
import os
import json
import numpy as np
import time

# Add src to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
src_dir = os.path.join(parent_dir, 'src')
sys.path.append(src_dir)

from agent import Agent
from core import PillarType
from environment import GridWorld, Observation, Action

def load_arc_task(task_id: str, data_dir: str):
    with open(os.path.join(data_dir, task_id), 'r') as f:
        return json.load(f)

def run_benchmark():
    print("=== Phase 22: Sovereign Agent Benchmark ===")
    
    # 1. Setup
    tasks_dir = os.path.join(parent_dir, "ARC-AGI-master", "data", "training")
    # Same 20 tasks as Phase 20 for direct comparison
    task_files = [f for f in os.listdir(tasks_dir) if f.endswith('.json')]
    selected_tasks = sorted(task_files)[:20]
    
    agent = Agent(agent_id="Agent_Benchmark", specialization=PillarType.GENERAL, use_memory=True)
    
    results = {
        'tasks': [],
        'vocab_growth': [],
        'generic_concepts': [],
        'total_solved': 0
    }
    
    start_time = time.time()
    
    # 2. Sequential Run
    for i, task_file in enumerate(selected_tasks):
        print(f"\n[{i+1}/{len(selected_tasks)}] Processing {task_file}...")
        
        task_data = load_arc_task(task_file, tasks_dir)
        train_examples = task_data['train']
        
        # Simulate solving (Learning Step)
        
        # Step 1: Learn from examples
        obs = Observation(
            visible_cells=np.zeros((3,3)), # Dummy visible view
            position=(0,0),
            reward=0.0,
            context=np.array(train_examples[0]['input']), # Initial context
            train_examples=[
                {'input': np.array(ex['input']), 'output': np.array(ex['output'])}
                for ex in train_examples
            ]
        )
        
        # Trigger Agent Update (Learning)
        # We act "WAIT" just to trigger the update cycle
        agent.universal_update(Action.WAIT, obs)
        
        # Step 2: Harmonize Periodically (The "Sleep" Cycle)
        if (i + 1) % 5 == 0:
            print("\n Agent is engaging in autonomous harmonization (Sleep Cycle)...")
            initial_size = len(agent.sovereign_vocab.vocabulary)
            agent.sovereign_vocab.harmonize()
            final_size = len(agent.sovereign_vocab.vocabulary)
            print(f"💤 Harmonization result: {initial_size} -> {final_size} concepts")
            
        # Logging
        vocab_size = len(agent.sovereign_vocab.vocabulary)
        generic_count = sum(1 for n in agent.sovereign_vocab.vocabulary if "rect_" in n and "_c" not in n) # Rough check for generics
        
        results['vocab_growth'].append(vocab_size)
        results['generic_concepts'].append(generic_count)
        
        print(f"   Current Vocab Size: {vocab_size} (Generics: {generic_count})")
        
    duration = time.time() - start_time
    
    # 3. Save Results
    with open("benchmark_v2_results.json", "w") as f:
        json.dump(results, f, indent=2)
        
    print("\n=== Benchmark Complete ===")
    print(f"Time: {duration:.2f}s")
    print(f"Final Vocab Size: {results['vocab_growth'][-1]}")
    print(f"Generic Concepts: {results['generic_concepts'][-1]}")
    
    # ASCII Plot of Vocab Growth
    print("\nVocabulary Growth Curve:")
    max_v = max(results['vocab_growth'])
    for v in results['vocab_growth']:
        bar = "#" * int((v / max_v) * 20)
        print(f"{v:3d} | {bar}")

if __name__ == "__main__":
    run_benchmark()
