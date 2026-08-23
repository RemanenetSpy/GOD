"""
Main Entry Point for Hybrid ToE-Inspired AGI
Demonstrates the complete system in action.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from src.agent import Agent, run_episode
from src.environment import GridWorld, Action, CellType
import time


def visualize_episode(num_steps: int = 100, seed: int = 123, save_animation: bool = False):
    """
    Run and visualize an episode with real-time plotting.
    
    Shows:
    - Grid world with agent position
    - Belief state (uncertainty map)
    - Reward over time
    - Exploration progress
    """
    # Create environment and agent
    env = GridWorld(size=10, num_resources=5, num_obstacles=9, seed=seed)
    agent = Agent(grid_size=10)
    
    # Initialize
    observation = env.observe()
    
    # Tracking
    rewards_history = []
    exploration_history = []
    uncertainty_history = []
    
    # Setup plot
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('Hybrid ToE-Inspired AGI - Live Visualization', fontsize=14, fontweight='bold')
    
    # Run episode
    print("Running episode with visualization...")
    print("=" * 60)
    
    for step in range(num_steps):
        # Agent perceives and acts
        action, state = agent.act(observation)
        
        # Environment responds
        observation, reward, done = env.step(action)
        
        # Track metrics
        stats = agent.get_stats()
        rewards_history.append(stats['total_reward'])
        exploration_history.append(stats['exploration_rate'] * 100)
        uncertainty_history.append(stats['avg_uncertainty'])
        
        # Update visualization every 5 steps
        if step % 5 == 0 or done:
            # Clear axes
            for ax in axes.flat:
                ax.clear()
            
            # 1. Grid World
            ax1 = axes[0, 0]
            grid_display = env.grid.copy().astype(float)
            x, y = env.agent_position
            grid_display[x, y] = 3  # Mark agent position
            
            im1 = ax1.imshow(grid_display, cmap='tab10', vmin=0, vmax=3)
            ax1.set_title(f'Grid World (Step {step})')
            ax1.set_xlabel('X')
            ax1.set_ylabel('Y')
            
            # Add legend
            legend_elements = [
                plt.Rectangle((0,0),1,1, fc='#1f77b4', label='Empty'),
                plt.Rectangle((0,0),1,1, fc='#ff7f0e', label='Resource'),
                plt.Rectangle((0,0),1,1, fc='#2ca02c', label='Obstacle'),
                plt.Rectangle((0,0),1,1, fc='#d62728', label='Agent')
            ]
            ax1.legend(handles=legend_elements, loc='upper right', fontsize=8)
            
            # 2. Belief Uncertainty Map
            ax2 = axes[0, 1]
            uncertainty_map = agent.state.belief_state.get_uncertainty_map()
            im2 = ax2.imshow(uncertainty_map, cmap='hot', vmin=0, vmax=2)
            ax2.set_title('Belief Uncertainty (Entropy)')
            ax2.set_xlabel('X')
            ax2.set_ylabel('Y')
            plt.colorbar(im2, ax=ax2, label='Uncertainty')
            
            # 3. Cumulative Reward
            ax3 = axes[1, 0]
            ax3.plot(rewards_history, 'b-', linewidth=2)
            ax3.set_title('Cumulative Reward Over Time')
            ax3.set_xlabel('Step')
            ax3.set_ylabel('Total Reward')
            ax3.grid(True, alpha=0.3)
            
            # 4. Exploration Progress
            ax4 = axes[1, 1]
            ax4.plot(exploration_history, 'g-', linewidth=2, label='Exploration')
            ax4.plot(uncertainty_history, 'r-', linewidth=2, label='Avg Uncertainty')
            ax4.set_title('Learning Metrics')
            ax4.set_xlabel('Step')
            ax4.set_ylabel('Percentage / Uncertainty')
            ax4.legend()
            ax4.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.pause(0.01)
        
        # Print progress
        if step % 10 == 0:
            print(f"Step {step}/{num_steps} | Action: {action.name} | "
                  f"Reward: {stats['total_reward']:.2f} | "
                  f"Exploration: {stats['exploration_rate']*100:.1f}%")
        
        if done:
            print(f"\nEpisode ended at step {step} (energy depleted)")
            break
    
    # Keep plot open
    if save_animation:
        plt.savefig('agi_visualization.png', dpi=150, bbox_inches='tight')
        print("\nVisualization saved to 'agi_visualization.png'")
    
    plt.show()
    
    # Final statistics
    print("\n" + "=" * 60)
    print("Episode Complete")
    print("=" * 60)
    
    final_stats = agent.get_stats()
    print(f"\nFinal Agent Stats:")
    for key, value in final_stats.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.3f}")
        else:
            print(f"  {key}: {value}")
    
    return agent, env


def run_simple_demo():
    """Run a simple text-based demo."""
    print("\n" + "=" * 60)
    print("HYBRID ToE-INSPIRED AGI - SIMPLE DEMO")
    print("=" * 60)
    print("\nThis demonstrates the 'God Equation' in action:")
    print("  S_{t+1} = U(S_t, A_t, O_t)")
    print("\nWhere U simultaneously updates:")
    print("  - Beliefs (quantum-like)")
    print("  - Perspective (relativity-like)")
    print("  - Model (information-theoretic)")
    print("  - Internal laws (computational-physics)")
    print("=" * 60)
    
    agent, env = run_episode(num_steps=1000, render=True, seed=42)
    
    print("\n✓ Demo complete!")
    return agent, env


def main():
    """Main entry point."""
    import sys
    
    print("\n" + "=" * 70)
    print(" " * 15 + "HYBRID ToE-INSPIRED AGI")
    print(" " * 10 + "A Universe Inside the Universe")
    print("=" * 70)
    
    print("\nSelect mode:")
    print("  1. Simple text demo (fast)")
    print("  2. Visual demo with plots (requires matplotlib)")
    print("  3. Run both")
    
    try:
        choice = input("\nEnter choice (1-3): ").strip()
    except:
        choice = "1"  # Default to simple demo
    
    if choice == "1":
        run_simple_demo()
    elif choice == "2":
        try:
            visualize_episode(num_steps=100, seed=123, save_animation=True)
        except Exception as e:
            print(f"\nVisualization error: {e}")
            print("Falling back to simple demo...")
            run_simple_demo()
    elif choice == "3":
        run_simple_demo()
        print("\n\nStarting visual demo...")
        time.sleep(2)
        try:
            visualize_episode(num_steps=100, seed=123, save_animation=True)
        except Exception as e:
            print(f"\nVisualization error: {e}")
    else:
        print("Invalid choice. Running simple demo...")
        run_simple_demo()
    
    print("\n" + "=" * 70)
    print("Thank you for exploring the Hybrid ToE-Inspired AGI!")
    print("=" * 70)


if __name__ == "__main__":
    main()
