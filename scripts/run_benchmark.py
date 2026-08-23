#!/usr/bin/env python3
"""
10-Task Benchmark Script
Tests agent on 10 different ARC tasks and reports statistics
"""

import subprocess
import json
from pathlib import Path

# 10 diverse ARC tasks for benchmarking
TASKS = [
    "00d62c1b.json",  # Previously solved
    "0ca9ddb6.json",  # Color swapping
    "0a938d79.json",  # Pattern repetition
    "1cf80156.json",  # Penalty loop test
    "007bbfb7.json",  # Spatial transformation
    "00576224.json",  # Object manipulation
    "025d127b.json",  # Grid filling
    "05f2a901.json",  # Pattern recognition
    "0520fde7.json",  # Color mapping
    "05269061.json",  # Complex transform
]

AGENTS = ["QUANTUM", "PHYSICS", "RELATIVITY", "INFORMATION"]
ARC_DATA_DIR = Path("c:/Users/reman/OneDrive/Desktop/mine data/GOD/ARC-AGI-master/data/training")

results = []

print("=" * 60)
print("10-TASK ARC BENCHMARK")
print("=" * 60)

for i, task_file in enumerate(TASKS, 1):
    task_path = ARC_DATA_DIR / task_file
    agent = AGENTS[i % len(AGENTS)]  # Rotate through agents
    
    print(f"\n[{i}/10] Testing {task_file} with {agent} agent...")
    
    try:
        cmd = f'python scripts/visualize_arc.py "{task_path}" --agent {agent}'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
        
        # Parse output for Solved status
        output = result.stdout
        solved = "Solved!" in output or "Reward=101.00" in output
        
        # Extract final reward
        lines = output.strip().split('\n')
        final_reward = 0.0
        for line in reversed(lines):
            if "Reward=" in line:
                try:
                    reward_str = line.split("Reward=")[1].split()[0]
                    final_reward = float(reward_str)
                    break
                except:
                    pass
        
        results.append({
            "task": task_file,
            "agent": agent,
            "solved": solved,
            "final_reward": final_reward
        })
        
        status = "✅ SOLVED" if solved else f"❌ FAILED (reward={final_reward})"
        print(f"   {status}")
        
    except subprocess.TimeoutExpired:
        print(f"   ⏱️ TIMEOUT")
        results.append({
            "task": task_file,
            "agent": agent,
            "solved": False,
            "final_reward": 0.0
        })
    except Exception as e:
        print(f"   ⚠️ ERROR: {e}")
        results.append({
            "task": task_file,
            "agent": agent,
            "solved": False,
            "final_reward": 0.0
        })

# Calculate statistics
solved_count = sum(1 for r in results if r["solved"])
success_rate = (solved_count / len(results)) * 100

print("\n" + "=" * 60)
print("BENCHMARK RESULTS")
print("=" * 60)
print(f"Tasks Solved: {solved_count}/{len(results)}")
print(f"Success Rate: {success_rate:.1f}%")
print(f"\nDetailed Results:")
for r in results:
    status = "✅" if r["solved"] else "❌"
    print(f"  {status} {r['task']:20} ({r['agent']:12}) - Reward: {r['final_reward']:.2f}")

# Save results to JSON
with open("benchmark_results.json", "w") as f:
    json.dump({
        "total_tasks": len(results),
        "solved": solved_count,
        "success_rate": success_rate,
        "results": results
    }, f, indent=2)

print(f"\nResults saved to benchmark_results.json")
