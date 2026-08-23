"""
Multi-Agent Arena for Phase 5.5 (Tournament).

Pits the Four Pillars Agents against 4 Specialized Environments.
"""

import time
import argparse
import numpy as np
import sys
import csv
import os
import sys

# Add 'src' to python path to allow imports
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, '..', 'src')
sys.path.append(src_path)


from pacman_env import PacManWorld
from specialized_env import QuantumMaze, PhysicsMaze, RelativityMaze, InformationMaze
from infinite_maze import InfiniteMaze
from agent import Agent
from core import PillarType
from environment import Action

def run_tournament(episodes=1, speed=0.05, use_memory=True, fixed_seed=None):
    print(f"🏟️  WELCOME TO THE FOUR PILLARS TOURNAMENT 🏟️")
    print(f"   Episodes: {episodes} per Agent per Game | Memory: {use_memory}")
    print("---------------------------------------")
    
    pillars = [
        PillarType.QUANTUM,
        PillarType.PHYSICS,
        PillarType.RELATIVITY,
        PillarType.INFORMATION
    ]
    
    # Define the Tournament Games
    games = {
        "Standard": PacManWorld,
        "QuantumMaze": QuantumMaze,
        "PhysicsMaze": PhysicsMaze,
        "RelativityMaze": RelativityMaze,
        "InformationMaze": InformationMaze,
        "InfiniteMaze": InfiniteMaze  # NEW: Infinite procedural maze
    }
    
    for game_name, game_class in games.items():
        print(f"\n🌍 STARTING GAME: {game_name.upper()}")
        print("=" * 40)
        
        for pillar in pillars:
            print(f"\n🧪 Testing Agent: {pillar.name} in {game_name}")
            scores = []
            survival_times = []
            
            # Unique ID per Agent per Game (so they don't confuse rules between worlds)
            unique_id = f"arena_{game_name}_{pillar.name.lower()}"
            for ep in range(episodes):
                # Seed Logic: Fixed or Progressive
                if fixed_seed is not None:
                    current_seed = fixed_seed
                else:
                    current_seed = 42 + ep

                # Initialize specific game environment
                # FORCE SIZE 15 for consistency/fairness across all games
                # QuantumMaze/InformationMaze default to 15, others 20.
                if game_name == 'InfiniteMaze':
                    # Infinite maze uses different parameters
                    env = game_class(seed=current_seed, chunk_size=16, visible_range=7)
                    max_steps = 1000  # Longer episodes for exploration
                elif 'size' in game_class.__init__.__code__.co_varnames:
                     env = game_class(size=15, seed=current_seed)
                     max_steps = 200
                else:
                     env = game_class(seed=current_seed) # Fallback
                     max_steps = 200

                agent = Agent(agent_id=unique_id, grid_size=15, use_memory=use_memory, specialization=pillar)

                # CRITICAL FIX: Load memory from previous episodes
                if use_memory:
                    agent.load_memory(current_seed)

                obs = env.observe()
                done = False
                step = 0

                # Run Episode
                while not done and step < max_steps:
                    action, state = agent.act(obs)
                    obs, reward, done = env.step(action)
                    step += 1

                    if speed > 0:
                       print("\033[H\033[J", end="")
                       print(f"Game: {game_name} | Agent: {pillar.name} | Ep: {ep+1}/{episodes} | Step: {step}")
                       print(env.render())
                       time.sleep(speed)

                # Save memory
                if use_memory and agent.memory:
                    # Get score based on game type
                    if game_name == 'InfiniteMaze':
                        stats = env.get_stats()
                        episode_score = stats['cells_explored']  # Use exploration as score
                        agent.save_memory(episode_score=episode_score, episode_steps=step)
                    else:
                        agent.save_memory(episode_score=env.score, episode_steps=step)

                # Record results
                if game_name == 'InfiniteMaze':
                    stats = env.get_stats()
                    scores.append(stats['cells_explored'])
                else:
                    scores.append(env.score)
                survival_times.append(step)

                # Log to CSV
                # Ensure data directory exists
                data_dir = os.path.join(current_dir, '..', 'data')
                if not os.path.exists(data_dir):
                    os.makedirs(data_dir)
                
                stats_file = os.path.join(data_dir, 'arena_results.csv')
                file_exists = os.path.isfile(stats_file)

                with open(stats_file, mode='a', newline='') as f:
                    writer = csv.writer(f)
                    if not file_exists:
                        writer.writerow(['Timestamp', 'Game', 'Agent', 'Episode', 'Score', 'Steps', 'Memory'])

                    writer.writerow([
                        time.strftime("%Y-%m-%d %H:%M:%S"),
                        game_name,
                        pillar.name,
                        ep + 1,
                        env.score,
                        step,
                        use_memory
                    ])

                # Progress logging
                seed_msg = f"(Seed {current_seed})"
                if (ep + 1) % 10 == 0 or episodes <= 5:
                     print(f"   -> Ep {ep+1} {seed_msg}: Score {env.score}, Steps {step}")
                else:
                     print(f"   -> Ep {ep+1} {seed_msg}: Score {env.score}, Steps {step}", end='\r')

            avg_score = np.mean(scores)
            print(f"   🏁 Average Score: {avg_score:.1f}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--episodes', type=int, default=1, help='Episodes per agent per game')
    parser.add_argument('--speed', type=float, default=0.05, help='Visual speed (0 for silent)')
    parser.add_argument('--memory', action='store_true', help='Enable persistent memory')
    parser.add_argument('--seed', type=int, default=None, help='Fixed level seed (optional)')
    args = parser.parse_args()

    # Force memory=True if not specified, since user wanted learning
    run_tournament(episodes=args.episodes, speed=args.speed, use_memory=args.memory, fixed_seed=args.seed)
