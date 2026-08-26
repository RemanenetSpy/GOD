"""
Extended Infinite Maze Test - 1000 Steps

Test agents in deep exploration to see:
- How far they can explore
- Pattern discovery
- Rule learning
- Compression efficiency
"""

import sys
sys.path.insert(0, 'src')

from infinite_maze import InfiniteMaze
from agent import Agent
from core import PillarType

def extended_exploration_test(steps=1000, episodes=3):
    """Run extended exploration test"""
    print("="*70)
    print(f"🌌 EXTENDED EXPLORATION TEST ({steps} steps, {episodes} episodes)")
    print("="*70)
    
    # Test all specializations
    pillars = [
        (PillarType.INFORMATION, "INFORMATION (Data Lover)"),
        (PillarType.RELATIVITY, "RELATIVITY (Far Sight)"),
        (PillarType.QUANTUM, "QUANTUM (Chaos Explorer)"),
        (PillarType.PHYSICS, "PHYSICS (Conservative)")
    ]
    
    for pillar, name in pillars:
        print(f"\n{'='*70}")
        print(f"Testing: {name}")
        print('='*70)
        
        agent = Agent(grid_size=15, use_memory=True, specialization=pillar)
        
        for ep in range(episodes):
            # Load memory
            agent.load_memory(999)
            
            # Fresh maze
            maze = InfiniteMaze(seed=999, visible_range=7)
            
            episode_reward = 0
            discoveries = 0
            
            # Run episode
            for step in range(steps):
                obs = maze.observe()
                action, state = agent.act(obs)
                obs, reward, done = maze.step(action)
                
                episode_reward += reward
                if reward > 5:  # Discovery!
                    discoveries += 1
                
                # Progress update every 200 steps
                if (step + 1) % 200 == 0:
                    stats = maze.get_stats()
                    print(f"  Step {step+1:4d}: Cells={stats['cells_explored']:3d}, "
                          f"Chunks={stats['chunks_generated']:2d}, "
                          f"Reward={episode_reward:7.1f}, "
                          f"Pos={maze.agent_pos}")
            
            # Save memory
            agent.save_memory(episode_score=episode_reward, episode_steps=steps)
            
            # Episode summary
            stats = maze.get_stats()
            print(f"\n  Episode {ep+1} Summary:")
            print(f"    Cells explored: {stats['cells_explored']}")
            print(f"    Chunks generated: {stats['chunks_generated']}")
            print(f"    Total reward: {episode_reward:.1f}")
            print(f"    Discoveries: {discoveries}")
            print(f"    Final position: {maze.agent_pos}")
            print(f"    Agent patterns: {len(agent.state.world_model.patterns)}")
            print(f"    Agent rules: {len(agent.state.world_model.rules)}")
            print(f"    Cells remembered: {np.sum(agent.state.world_model.cell_visit_counts > 0)}")

if __name__ == "__main__":
    import numpy as np
    
    print("\n🚀 DEEP EXPLORATION TEST - 1000 STEPS PER EPISODE 🚀\n")
    
    extended_exploration_test(steps=1000, episodes=3)
    
    print("\n" + "="*70)
    print("TEST COMPLETE! 🎉")
    print("="*70)
