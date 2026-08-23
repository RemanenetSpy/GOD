"""
ARC-AGI Battle: Sovereign vs Zero-Point

Head-to-head comparison of Phase 1 (Concepts) vs Phase 2 (Survival).
"""

import sys
import os
import json
import time
import numpy as np
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Any

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from agent import Agent, PillarType
from environment import Observation, Action

class ARCBattle:
    def __init__(self, data_dir: str = "ARC-AGI-master/data", pillar: str = "QUANTUM"):
        self.data_dir = Path(data_dir)
        self.pillar = PillarType[pillar.upper()]
        
        # Initialize combatants
        self.agent_alpha = Agent(agent_id="ALPHA_SOVEREIGN", engine_type="sovereign", specialization=self.pillar)
        self.agent_beta = Agent(agent_id="BETA_ZEROPOINT", engine_type="zero_point", specialization=self.pillar)
        
        self.results = {
            'alpha': {'solved': 0, 'vocab_growth': 0, 'metabolism_avg': 0},
            'beta': {'solved': 0, 'vocab_growth': 0, 'metabolism_avg': 0},
            'tasks': []
        }
    
    def load_arc_tasks(self, split: str = 'training') -> Dict:
        """Load ARC tasks (same as old benchmark)."""
        tasks = {}
        task_dir = self.data_dir / split
        if not task_dir.exists(): return {}
        
        for json_file in sorted(task_dir.glob('*.json')):
            with open(json_file, 'r') as f:
                task_data = json.load(f)
                tasks[json_file.stem] = {
                    'train': task_data.get('train', []),
                    'test': task_data.get('test', [])
                }
        return tasks

    def run_battle(self, max_tasks: int = 10):
        print(f"\n{'='*60}")
        print(f"ARC BATTLE: SOVEREIGN (Alpha) vs ZERO-POINT (Beta)")
        print(f"{'='*60}\n")
        
        tasks = self.load_arc_tasks('training')
        task_ids = list(tasks.keys())[:max_tasks]
        
        print(f"Loaded {len(task_ids)} tasks for combat.\n")
        
        for i, task_id in enumerate(task_ids):
            print(f"[{i+1}/{max_tasks}] Task {task_id}...", end=' ')
            
            task_data = tasks[task_id]
            res_alpha = self._run_agent(self.agent_alpha, task_data, "Alpha")
            res_beta = self._run_agent(self.agent_beta, task_data, "Beta")
            
            # Compare
            winner = "DRAW"
            if res_alpha['solved'] and not res_beta['solved']: winner = "ALPHA"
            elif res_beta['solved'] and not res_alpha['solved']: winner = "BETA"
            
            print(f"Winner: {winner}")
            print(f"   Alpha (Sov): Solved={res_alpha['solved']}, dH/dt={res_alpha['metabolism']:.2f}, Anchors={res_alpha['anchors']}")
            print(f"   Beta (Zero): Solved={res_beta['solved']}, dH/dt={res_beta['metabolism']:.2f}, Anchors={res_beta['anchors']}")
            
            self.results['tasks'].append({
                'task_id': task_id,
                'alpha': res_alpha,
                'beta': res_beta,
                'winner': winner
            })
            
            if res_alpha['solved']: self.results['alpha']['solved'] += 1
            if res_beta['solved']: self.results['beta']['solved'] += 1
        
        self._print_summary()

    def _run_agent(self, agent, task_data, name):
        """Run single agent on task."""
        # Setup observation
        test_case = task_data['test'][0]
        test_input = np.array(test_case['input'])
        expected = np.array(test_case['output'])
        
        train_examples = []
        for ex in task_data['train']:
            train_examples.append({
                'input': np.array(ex['input']),
                'output': np.array(ex['output'])
            })
            
        obs = Observation(
            visible_cells=np.zeros((3,3)),
            position=(0,0),
            reward=0.0,
            context=test_input,
            train_examples=train_examples
        )
        
        # Run update
        start = time.time()
        agent.universal_update(Action.WAIT, obs)
        elapsed = time.time() - start
        
        # Check engine stats
        dash = agent.sovereign_engine.get_dashboard()
        
        # Check if solved (dummy check for now since we don't have full solving logic yet)
        # In real benchmark, we'd check prediction vs expected
        # For now, we simulate solve based on metabolism > threshold (just for demo)
        # REAL CHECK: In future, use agent.predict()
        is_solved = dash['viability_ratio'] > 2.0 # Proxy for solve in this demo
        
        # Count anchors
        anchors = 0
        if name == "Beta":
            anchors = dash['anchors_found']
        else:
            # Alpha uses vocab size as proxy
            anchors = len(agent.sovereign_vocab.vocabulary)
            
        return {
            'solved': is_solved,
            'metabolism': dash['metabolism'],
            'anchors': anchors,
            'time': elapsed
        }

    def _print_summary(self):
        print(f"\n{'='*60}")
        print("BATTLE RESULTS SUMMARY")
        print(f"{'='*60}")
        
        alpha_score = self.results['alpha']['solved']
        beta_score = self.results['beta']['solved']
        
        print(f"Alpha (Sovereign Phase 1): {alpha_score} / {len(self.results['tasks'])}")
        print(f"Beta (Zero-Point Phase 2): {beta_score} / {len(self.results['tasks'])}")
        
        if beta_score > alpha_score:
            print("\n🏆 WINNER: ZERO-POINT ENGINE (Beta)")
            print("The Survival Core outperformed the Concept Core.")
        elif alpha_score > beta_score:
            print("\n🏆 WINNER: SOVEREIGN ENGINE (Alpha)")
            print("The Concept Core is still superior.")
        else:
            print("\nResult: DRAW")
            
        print(f"{'='*60}\n")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--max_tasks', type=int, default=10, help='Number of tasks to run')
    args = parser.parse_args()
    
    battle = ARCBattle()
    battle.run_battle(max_tasks=args.max_tasks)
