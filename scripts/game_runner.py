"""
Universal Game Runner for Hybrid AGI.

Runs ANY compatible game environment file by name.
Usage:
    python game_runner.py --game <filename_no_py> --visual <gui|text> --agent <agi|random>

Example:
    python game_runner.py --game pacman_env --visual gui --agent agi
"""

import argparse
import importlib
import sys
import time
import numpy as np
import os

# Add 'src' to python path to allow imports
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, '..', 'src')
sys.path.append(src_path)

# Add project root to path (for legacy)
sys.path.append('.')

from agent import Agent
from environment import Action

def run_game(game_module_name, visual_mode='text', agent_mode='agi', seed=None, speed=0.1):
    print(f"🚀 Launching Game: {game_module_name}")
    print(f"   - Visual: {visual_mode}")
    print(f"   - Agent:  {agent_mode}")
    print(f"   - Seed:   {seed if seed is not None else 'Random'}")

    # 1. Dynamically Load Environment
    try:
        game_module = importlib.import_module(game_module_name)
        # Look for the main class. Convention: PascalCase of snake_case name or generic "World"
        # Strategy: Look for class ending in "World" or containing "Game" or "Env"
        valid_class = None
        for name, obj in vars(game_module).items():
            if isinstance(obj, type) and (name.endswith('World') or 'Env' in name) and name != 'GridWorld':
                valid_class = obj
                break
        
        if not valid_class:
            print(f"❌ Error: Could not find a 'World' class in {game_module_name}")
            return
            
        print(f"✅ Loaded Environment Class: {valid_class.__name__}")
        
    except ImportError as e:
        print(f"❌ Error: Could not import module '{game_module_name}'. {e}")
        return

    # 2. Initialize Environment
    # Assuming standard init signature: size, seed, etc.
    try:
        if seed is None:
            env = valid_class(size=10) # Default size
        else:
            env = valid_class(size=10, seed=seed)
    except Exception as e:
        print(f"⚠️ Init failed with standard args, trying no-args. Error: {e}")
        try:
            env = valid_class()
        except:
             print("❌ Fatal: Could not initialize environment.")
             return

    # 3. Initialize Visualizer
    renderer = None
    if visual_mode == 'gui':
        try:
            from gui_renderer import PyGameRenderer
            renderer = PyGameRenderer(grid_size=env.size if hasattr(env, 'size') else 10)
        except Exception as e:
            print(f"⚠️ GUI init failed: {e}. Falling back to text.")
            visual_mode = 'text'

    # 4. Initialize Agent
    agent = None
    if agent_mode == 'agi':
        # Match grid size if possible
        grid_size = env.size if hasattr(env, 'size') else 10
        agent = Agent(grid_size=grid_size, use_memory=True)
        if seed is not None:
            agent.load_memory(seed)
        else:
            # Try to load general memory or just start FRESH
            pass

    # 5. Game Loop
    obs = env.observe() if hasattr(env, 'observe') else env.reset()
    done = False
    step = 0
    total_steps = 1000

    try:
        while not done and step < total_steps:
            # Handle GUI Events
            if renderer:
                renderer.handle_events()
            
            # --- AGENT DECISION ---
            if agent_mode == 'agi':
                action, state = agent.act(obs)
                planning_depth = state.frame_of_ref.planning_depth
                energy_status = "High" # Placeholder
            else:
                # Random
                action = np.random.choice(list(Action))
                planning_depth = 0
                energy_status = "N/A"
            
            # --- STEP ENVIRONMENT ---
            # Standard interface: step(action) -> obs, reward, done
            obs, reward, done = env.step(action)
            step += 1
            
            # --- VISUALIZE ---
            stats = {
                'score': getattr(env, 'score', 0),
                'steps': step,
                'energy': energy_status,
                'planning_depth': planning_depth
            }
            
            if visual_mode == 'gui':
                renderer.draw(env, stats)
                # Renderer handles timing via clock.tick()
            else:
                # Text Mode
                print("\033[H\033[J", end="") # Clear screen
                print(f"Step: {step} | Score: {stats['score']}")
                if hasattr(env, 'render'):
                    print(env.render())
                # Only sleep in text mode to make it readable
                time.sleep(speed)
        
        # Cleanup
        print("\n=== GAME OVER ===")
        print(f"Final Score: {getattr(env, 'score', 'N/A')}")
        if agent_mode == 'agi' and seed is not None:
            agent.save_memory()
            
        if visual_mode == 'gui':
            # Hold window open for a moment
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\nStopped by user.")
    except Exception as e:
        print(f"\n❌ Runtime Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Universal Game Runner")
    parser.add_argument('--game', type=str, required=True, help="Name of game file (e.g. pacman_env)")
    parser.add_argument('--visual', type=str, choices=['text', 'gui'], default='gui', help="Visualization mode")
    parser.add_argument('--agent', type=str, choices=['agi', 'random'], default='agi', help="Agent type")
    parser.add_argument('--seed', type=int, default=None, help="Random seed (optional)")
    parser.add_argument('--speed', type=float, default=0.1, help="Speed delay")
    
    args = parser.parse_args()
    
    # Strip .py extension if provided
    game_name = args.game.replace('.py', '')
    
    run_game(game_name, args.visual, args.agent, args.seed, args.speed)
