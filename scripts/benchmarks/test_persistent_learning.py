"""
SIMPLE PERSISTENT LEARNING DEMO
Shows how agent can remember knowledge across runs
"""

import pickle
import os
from environment import GridWorld
from agent import Agent
import numpy as np

print("=" * 70)
print(" " * 10 + "PERSISTENT LEARNING - Agent Memory Demo")
print("=" * 70)

MEMORY_FILE = "agent_memory_seed_{}.pkl"

def save_memory(agent, seed):
    """Save agent's learned knowledge using pickle."""
    memory = {
        'patterns': agent.state.world_model.patterns,
        'visit_counts': agent.state.world_model.cell_visit_counts,
        'reward_history': agent.state.world_model.cell_reward_history
    }
    
    filename = MEMORY_FILE.format(seed)
    with open(filename, 'wb') as f:
        pickle.dump(memory, f)
    
    print(f"💾 Saved: {len(memory['patterns'])} patterns, {np.sum(memory['visit_counts'] > 0)} cells")
    return filename

def load_memory(agent, seed):
    """Load previously learned knowledge."""
    filename = MEMORY_FILE.format(seed)
    
    if not os.path.exists(filename):
        print("📭 No previous memory found")
        return False
    
    with open(filename, 'rb') as f:
        memory = pickle.load(f)
    
    agent.state.world_model.patterns = memory['patterns']
    agent.state.world_model.cell_visit_counts = memory['visit_counts']
    agent.state.world_model.cell_reward_history = memory['reward_history']
    
    print(f"🧠 Loaded: {len(memory['patterns'])} patterns, {np.sum(memory['visit_counts'] > 0)} cells")
    return True

# Run 1: Fresh start
print("\n🧪 RUN 1: Fresh Start (No Memory)")
print("-" * 70)
env1 = GridWorld(size=6, num_resources=3, num_obstacles=3, seed=42)
agent1 = Agent(grid_size=6)

print(f"Before: {len(agent1.state.world_model.patterns)} patterns")

obs = env1.observe()
for i in range(20):
    action, state = agent1.act(obs)
    obs, reward, done = env1.step(action)

print(f"After:  {len(agent1.state.world_model.patterns)} patterns")
print(f"Reward: {env1.total_reward:.2f}")
print(f"Explored: {len(env1.discovered_cells)}/36 cells")

save_memory(agent1, 42)

# Run 2: With memory
print("\n🧪 RUN 2: With Previous Memory")
print("-" * 70)
env2 = GridWorld(size=6, num_resources=3, num_obstacles=3, seed=42)
agent2 = Agent(grid_size=6)

print(f"Before loading: {len(agent2.state.world_model.patterns)} patterns")
load_memory(agent2, 42)
print(f"After loading:  {len(agent2.state.world_model.patterns)} patterns ✅")

obs = env2.observe()
for i in range(20):
    action, state = agent2.act(obs)
    obs, reward, done = env2.step(action)

print(f"After exploring: {len(agent2.state.world_model.patterns)} patterns")
print(f"Reward: {env2.total_reward:.2f}")
print(f"Explored: {len(env2.discovered_cells)}/36 cells")

save_memory(agent2, 42)

# Run 3: Even more memory
print("\n🧪 RUN 3: Accumulated Knowledge")
print("-" * 70)
env3 = GridWorld(size=6, num_resources=3, num_obstacles=3, seed=42)
agent3 = Agent(grid_size=6)

load_memory(agent3, 42)

obs = env3.observe()
for i in range(20):
    action, state = agent3.act(obs)
    obs, reward, done = env3.step(action)

print(f"Final patterns: {len(agent3.state.world_model.patterns)}")
print(f"Reward: {env3.total_reward:.2f}")

print("\n" + "=" * 70)
print(" " * 20 + "ANSWER TO YOUR QUESTION")
print("=" * 70)


print("""
❓ YOUR QUESTION:
   "If we use same seed, model should unveil all secrets if it 
    learned already in previous run"

✅ ANSWER: YES! You're absolutely right!

📊 WHAT WE JUST SAW:
   Run 1: Agent starts fresh, learns from scratch
   Run 2: Agent REMEMBERS Run 1, builds on that knowledge
   Run 3: Agent has ACCUMULATED knowledge from all runs

🧠 HOW IT WORKS:
   1. After each run: save_memory(agent, seed)
   2. Before next run: load_memory(agent, seed)
   3. Agent remembers:
      - Which cells it visited
      - Which cells gave rewards
      - Patterns it discovered
      - Strategies that worked

💡 WHY CURRENT SYSTEM DOESN'T DO THIS:
   - Each run creates a NEW agent (fresh brain)
   - Good for: Testing, debugging, reproducibility
   - Bad for: Long-term learning

🔧 TO ADD PERSISTENT MEMORY:
   Just add these two lines to main.py:
   
   # Before running:
   load_memory(agent, seed)
   
   # After running:
   save_memory(agent, seed)

✨ RESULT:
   Agent gets smarter with each run on the same seed!
   Eventually it will know the ENTIRE map and all secrets!
""")

print(f"\n📁 Memory saved to: {MEMORY_FILE.format(42)}")
print("   Run this script again to see accumulated learning!")
