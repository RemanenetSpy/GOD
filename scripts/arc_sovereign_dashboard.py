"""
Enhanced ARC Benchmark with Sovereign Engine Dashboard
Shows Σ, Ω, Λ evolution during task solving
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from agent import Agent
from core import PillarType
from environment import Observation, Action
import numpy as np
import json
from pathlib import Path

print("=" * 80)
print("ARC Benchmark with Sovereign Engine Dashboard")
print("=" * 80)

# Load a single ARC task
arc_dir = Path("ARC-AGI-master/data/training")
task_files = sorted(arc_dir.glob('*.json'))[:5]  # First 5 tasks

agent = Agent(agent_id='sovereign_arc', specialization=PillarType.QUANTUM)

print(f"\n🧠 Agent: {agent.specialization.name}")
print(f"📊 Initial Engine State:")
dashboard = agent.sovereign_engine.get_dashboard()
print(f"  Σ={dashboard['sigma']:.3f}, Ω={dashboard['omega']:.3f}, Λ={dashboard['lambda']:.3f}")
print(f"  Rv={dashboard['viability_ratio']:.3f}, Action={dashboard['prescribed_action']}")

print(f"\n{'='*80}")
print("Processing Tasks...")
print(f"{'='*80}\n")

for i, task_file in enumerate(task_files):
    with open(task_file) as f:
        task_data = json.load(f)
    
    print(f"[{i+1}/5] Task: {task_file.stem}")
    
    # Process training examples
    for j, example in enumerate(task_data['train'][:2]):  # First 2 examples
        obs = Observation(
            visible_cells=np.zeros((3, 3)),
            position=(0, 0),
            reward=0.0,
            context=np.array(example['input']),
            train_examples=[{
                'input': np.array(ex['input']),
                'output': np.array(ex['output'])
            } for ex in task_data['train']]
        )
        
        agent.universal_update(Action.WAIT, obs)
    
    # Get engine state after task
    dashboard = agent.sovereign_engine.get_dashboard()
    print(f"  Engine: Σ={dashboard['sigma']:.2f}, Ω={dashboard['omega']:.2f}, "
          f"Λ={dashboard['lambda']:.2f}, Rv={dashboard['viability_ratio']:.2f}")
    print(f"  Status: {dashboard['diagnostic']} → {dashboard['prescribed_action']}")
    print(f"  Metabolism: {dashboard['metabolism']:.3f}")
    print()

print(f"{'='*80}")
print("Final Engine State")
print(f"{'='*80}")
dashboard = agent.sovereign_engine.get_dashboard()
print(f"Σ (Filter Efficiency): {dashboard['sigma']:.3f}")
print(f"Ω (Entropy): {dashboard['omega']:.3f}")
print(f"Λ (Friction): {dashboard['lambda']:.3f}")
print(f"Rv (Viability Ratio): {dashboard['viability_ratio']:.3f}")
print(f"Metabolism (dH/dt): {dashboard['metabolism']:.3f}")
print(f"Extinction: {dashboard['extinction']:.3f}")
print(f"\nDiagnostic: {dashboard['diagnostic']}")
print(f"Prescribed Action: {dashboard['prescribed_action']}")
print(f"\nVocabulary Size: {len(agent.sovereign_vocab.vocabulary)}")
print(f"{'='*80}")
