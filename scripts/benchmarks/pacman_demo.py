"""
Pac-Man Demo for Hybrid ToE-Inspired AGI.

Run this script to watch the agent play Pac-Man!
"""

import time
import argparse
import numpy as np
from pacman_env import PacManWorld
from agent import Agent
from environment import Action

def run_demo(mode='agi', seed=42, delay=0.1):
    """Run the Pac-Man demo."""
    print(f"Starting Pac-Man Demo (Mode: {mode}, Seed: {seed})")
    
    # Initialize
    env = PacManWorld(size=10, num_ghosts=2, seed=seed)
    
    if mode == 'agi':
        agent = Agent(grid_size=10, use_memory=True)
        # Load memory if exists
        agent.load_memory(seed)
        # Give agent more energy for this game
        # Note: In real implementation, energy should be managed by environment
        # Here we just ensure agent doesn't quit early
    
    obs = env.observe()
    
    try:
        for step in range(500):
            # clear screen (simple way)
            print("\033[H\033[J", end="")
            
            print(f"\n--- Step {step} ---")
            print(env.render())
            
            if mode == 'agi':
                action, state = agent.act(obs)
                
                # Print internal thought process
                print(f"\nACTION: {action.name}")
                print(f"Planning Depth: {state.frame_of_ref.planning_depth}")
                print(f"Energy Level: High") # Placeholder
                print(f"Uncertainty: {state.belief_state.get_uncertainty_map().mean():.3f}")
                
            else:
                # Random agent
                action = np.random.choice(list(Action))
            
            # Step environment
            obs, reward, done = env.step(action)
            
            if done:
                print("\n" + "="*30)
                if env.lives > 0:
                    print("VICTORY! All pellets collected!")
                else:
                    print("GAME OVER! Ghosts got you.")
                print(f"Final Score: {env.score}")
                print("="*30)
                
                # Save memory
                if mode == 'agi':
                    agent.save_memory()
                break
            
            time.sleep(delay)
            
    except KeyboardInterrupt:
        print("\nDemo stopped by user.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['agi', 'random'], default='agi', help='Agent mode')
    parser.add_argument('--seed', type=int, default=42, help='Random seed')
    parser.add_argument('--speed', type=float, default=0.1, help='Step delay in seconds')
    
    args = parser.parse_args()
    
    run_demo(mode=args.mode, seed=args.seed, delay=args.speed)
