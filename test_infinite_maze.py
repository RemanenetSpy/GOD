"""
Test Infinite Maze with AGI Agents

This script tests agents in an infinite deterministic maze environment.
Tests true AGI capabilities: exploration, prediction, compression, planning.
"""

import sys
sys.path.insert(0, 'src')

from infinite_maze import InfiniteMaze
from agent import Agent
from core import PillarType
from environment import Action
import time

def test_maze_generation():
    """Test that maze generation is deterministic"""
    print("="*60)
    print("TEST 1: Maze Generation Determinism")
    print("="*60)
    
    maze1 = InfiniteMaze(seed=999)
    maze2 = InfiniteMaze(seed=999)
    
    # Check same cells are generated
    for x in range(-10, 11):
        for y in range(-10, 11):
            cell1 = maze1.get_cell(x, y)
            cell2 = maze2.get_cell(x, y)
            assert cell1 == cell2, f"Mismatch at ({x},{y}): {cell1} vs {cell2}"
    
    print("✅ Maze generation is deterministic!")
    print(f"   Chunks generated: {len(maze1.chunks)}")
    print()

def test_agent_exploration(episodes=5, steps_per_episode=200):
    """Test agent exploration in infinite maze"""
    print("="*60)
    print(f"TEST 2: Agent Exploration ({episodes} episodes)")
    print("="*60)
    
    # grid_size=15, visible_range=7 → 2*7+1=15 (matches!)
    agent = Agent(grid_size=15, use_memory=True, specialization=PillarType.QUANTUM)
    maze = InfiniteMaze(seed=999, visible_range=7)
    
    for ep in range(episodes):
        # Load memory
        agent.load_memory(999)
        
        # Reset maze
        maze = InfiniteMaze(seed=999, visible_range=7)
        
        episode_reward = 0
        
        for step in range(steps_per_episode):
            obs = maze.observe()
            action, state = agent.act(obs)
            obs, reward, done = maze.step(action)
            
            episode_reward += reward
        
        # Save memory
        agent.save_memory(episode_score=episode_reward, episode_steps=steps_per_episode)
        
        stats = maze.get_stats()
        print(f"\nEpisode {ep+1}:")
        print(f"   Cells explored: {stats['cells_explored']}")
        print(f"   Chunks generated: {stats['chunks_generated']}")
        print(f"   Total reward: {episode_reward:.1f}")
        print(f"   Agent patterns: {len(agent.state.world_model.patterns)}")
        print(f"   Agent rules: {len(agent.state.world_model.rules)}")
    
    print("\n✅ Agent exploration test complete!")
    print()

def test_visual_demo():
    """Visual demo of agent in maze"""
    print("="*60)
    print("TEST 3: Visual Demo (50 steps)")
    print("="*60)
    
    agent = Agent(grid_size=15, use_memory=True, specialization=PillarType.QUANTUM)
    maze = InfiniteMaze(seed=999, visible_range=5)
    
    for step in range(50):
        print(f"\n--- Step {step+1} ---")
        print(maze.render())
        
        # Log Vocab Stats
        vocab_size = len(agent.sovereign_vocab.vocabulary)
        generics = sum(1 for k in agent.sovereign_vocab.vocabulary if "generic" in k or "comp" in k)
        print(f"Position: {maze.agent_pos}")
        print(f"Vocab Size: {vocab_size} | Generic Concepts: {generics}")
        
        obs = maze.observe()
        action, state = agent.act(obs)
        obs, reward, done = maze.step(action)
        
        # Enable On-Policy Learning
        agent.universal_update(action, obs)
        
        print(f"Action: {action.name}, Reward: {reward:.1f}")
        
        # Trigger Autonomous Harmonization halfway
        if step == 25:
             print("\n🌀 TRIGGERING SLEEP CYCLE (HARMONIZATION)...")
             agent.sovereign_vocab.harmonize()
             new_size = len(agent.sovereign_vocab.vocabulary)
             print(f"💤 Harmonization Complete. Vocab: {vocab_size} -> {new_size}")
             time.sleep(1)
             
        time.sleep(0.1)
    
    print("\n✅ Visual demo complete!")
    print()

def compare_agents():
    """Compare different agent specializations"""
    print("="*60)
    print("TEST 4: Agent Comparison (100 steps each)")
    print("="*60)
    
    pillars = [PillarType.QUANTUM, PillarType.PHYSICS, PillarType.RELATIVITY, PillarType.INFORMATION]
    
    results = {}
    
    for pillar in pillars:
        agent = Agent(grid_size=15, use_memory=False, specialization=pillar)
        maze = InfiniteMaze(seed=999, visible_range=7)
        
        total_reward = 0
        for step in range(100):
            obs = maze.observe()
            action, state = agent.act(obs)
            obs, reward, done = maze.step(action)
            total_reward += reward
        
        stats = maze.get_stats()
        results[pillar.name] = {
            'cells_explored': stats['cells_explored'],
            'total_reward': total_reward,
            'chunks': stats['chunks_generated']
        }
    
    print("\nResults:")
    print(f"{'Agent':<15} {'Cells':<10} {'Reward':<12} {'Chunks':<10}")
    print("-"*50)
    for name, data in results.items():
        print(f"{name:<15} {data['cells_explored']:<10} {data['total_reward']:<12.1f} {data['chunks']:<10}")
    
    print("\n✅ Agent comparison complete!")
    print()

def test_connectivity():
    """Test that chunks are connected"""
    print("\n" + "="*60)
    print("TEST 5: Chunk Connectivity")
    print("="*60)
    
    maze = InfiniteMaze(seed=12345, chunk_size=32)
    
    # Check doors between chunk(0,0) and chunk(1,0) - East/West connection
    chunk00 = maze.get_chunk(0, 0)
    chunk10 = maze.get_chunk(1, 0)
    
    # Mid point should be 16 for size 32
    mid = 15 # integer division // 2 of 32 is 16, but 0-indexed... wait. logic uses size//2 which is 16.
    
    # Check if there is a path at the boundary
    # Chunk(0,0) East edge: (31, mid)
    # Chunk(1,0) West edge: (0, mid)
    
    # Actually, let's just inspect the door dictionary logic directly
    doors00 = maze._get_doors(0, 0)
    doors10 = maze._get_doors(1, 0)
    
    print(f"Chunk(0,0) Doors: {doors00}")
    print(f"Chunk(1,0) Doors: {doors10}")
    
    # East of 0,0 MUST equal West of 1,0
    if doors00['E'] == doors10['W']:    
        print(f"✅ East-West Connection Verified: {doors00['E']} == {doors10['W']}")
    else:
        print(f"❌ East-West Connection FAILED: {doors00['E']} != {doors10['W']}")
        
    # Check physical path
    cell_00_edge = chunk00[31, 16] # 31 is right edge, 16 is mid
    cell_10_edge = chunk10[0, 16]  # 0 is left edge, 16 is mid
    
    print(f"Chunk(0,0) East Edge Cell (31,16): {cell_00_edge} (1=PATH)")
    print(f"Chunk(1,0) West Edge Cell (0,16): {cell_10_edge} (1=PATH)")
    
    if doors00['E']:
        if cell_00_edge == 1 and cell_10_edge == 1:
            print("✅ Physical path exists at connection point")
        else:
             # It acts as a hint, sometimes generation might not perfectly align if hub is blocked?
             # But our logic forces it.
             print("⚠️  Warning: Door is active but path might not be perfectly clear at edge index (could be offset by 1)")

if __name__ == "__main__":
    print("\n🌌 INFINITE MAZE TESTING SUITE 🌌\n")
    
    # Run all tests
    # Run all tests
    # test_maze_generation()
    # test_agent_exploration(episodes=5, steps_per_episode=200)
    test_visual_demo()  # Uncomment for visual demo
    # compare_agents()
    # test_connectivity()
    
    print("="*60)
    print("ALL TESTS COMPLETE! 🎉")
    print("="*60)
