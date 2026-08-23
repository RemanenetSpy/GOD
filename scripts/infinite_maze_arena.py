"""
Infinite Maze Arena - Engine Battle Royale

Tests all engine types × all pillar types in the infinite maze.
Visualizes performance and crowns the champion.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.colors import ListedColormap
import time

from agent import Agent, PillarType
from infinite_maze import InfiniteMaze
from environment import Action

class MazeArena:
    def __init__(self, seed=42, steps_per_agent=500):
        self.seed = seed
        self.steps_per_agent = steps_per_agent
        
        # Competitors
        self.engines = ['sovereign', 'zero_point', 'gravity']
        self.pillars = [PillarType.QUANTUM, PillarType.PHYSICS, PillarType.RELATIVITY, PillarType.INFORMATION]
        
        # Results tracking
        self.results = {}
        
        # Visualization
        plt.ion()
        self.fig = None
        
    def run_battle(self, visualize=True):
        """Run the complete battle royale."""
        print("=" * 80)
        print("🏟️  INFINITE MAZE ARENA - ENGINE BATTLE ROYALE")
        print("=" * 80)
        print(f"\nEngines: {self.engines}")
        print(f"Pillars: {[p.name for p in self.pillars]}")
        print(f"Steps per agent: {self.steps_per_agent}")
        print(f"Seed: {self.seed}\n")
        
        total_combos = len(self.engines) * len(self.pillars)
        current = 0
        
        for engine in self.engines:
            for pillar in self.pillars:
                current += 1
                combo_name = f"{engine}_{pillar.name}"
                
                print(f"\n[{current}/{total_combos}] Testing: {combo_name}")
                print("-" * 60)
                
                result = self.run_single_agent(engine, pillar, visualize=visualize)
                self.results[combo_name] = result
                
                print(f"✓ Completed: {combo_name}")
                print(f"  Cells Explored: {result['cells_explored']}")
                print(f"  Total Reward: {result['total_reward']:.1f}")
                print(f"  Treasures: {result['treasures']}")
        
        self.display_leaderboard()
        self.visualize_results()
    
    def run_single_agent(self, engine_type, pillar, visualize=False):
        """Run a single agent configuration."""
        # Create fresh maze
        maze = InfiniteMaze(seed=self.seed, visible_range=7)
        
        # Create agent
        agent = Agent(
            agent_id=f"{engine_type}_{pillar.name}",
            grid_size=30,
            specialization=pillar,
            engine_type=engine_type
        )
        
        # Setup visualization if enabled
        if visualize:
            self._setup_visualization(agent, maze)
        
        # Run simulation
        obs = maze.observe()
        total_reward = 0
        cells_explored = 0
        treasures = 0
        
        for step in range(self.steps_per_agent):
            # Agent acts
            action, _ = agent.act(obs)
            
            # Environment responds
            obs, reward, done = maze.step(action)
            total_reward += reward
            
            # Track treasures
            if reward > 10:  # Treasure bonus
                treasures += 1
            
            cells_explored = maze.cells_explored
            
            # Update visualization
            if visualize and step % 5 == 0:
                self._update_visualization(agent, maze, step, total_reward)
            
            if done:
                break
        
        if visualize:
            plt.close()
        
        return {
            'engine': engine_type,
            'pillar': pillar.name,
            'cells_explored': cells_explored,
            'total_reward': total_reward,
            'treasures': treasures,
            'steps': step + 1
        }
    
    def _setup_visualization(self, agent, maze):
        """Setup live visualization."""
        self.fig = plt.figure(figsize=(16, 10))
        self.fig.canvas.manager.set_window_title(f"Arena: {agent.agent_id}")
        
        gs = gridspec.GridSpec(2, 2, figure=self.fig)
        
        self.ax_maze = self.fig.add_subplot(gs[:, 0])
        self.ax_maze.set_title("Maze View")
        
        self.ax_metrics = self.fig.add_subplot(gs[0, 1])
        self.ax_metrics.set_title("Performance Metrics")
        
        self.ax_engine = self.fig.add_subplot(gs[1, 1])
        self.ax_engine.set_title("Engine State")
        
        self.reward_history = []
        self.explore_history = []
    
    def _update_visualization(self, agent, maze, step, total_reward):
        """Update visualization frames."""
        # Clear axes
        self.ax_maze.clear()
        self.ax_metrics.clear()
        self.ax_engine.clear()
        
        # 1. Maze view
        x, y = maze.agent_pos
        size = 41
        half = size // 2
        
        maze_view = np.zeros((size, size))
        for i in range(size):
            for j in range(size):
                wx = x + (i - half)
                wy = y + (j - half)
                cell = maze.get_cell(wx, wy)
                
                if cell.value == 2:  # OBSTACLE
                    maze_view[i, j] = 0.3
                elif cell.value == 1:  # PATH
                    if (wx, wy) in maze.visited_cells:
                        maze_view[i, j] = 0.7
                    else:
                        maze_view[i, j] = 1.0
                elif cell.value == 3:  # GOAL
                    maze_view[i, j] = 0.5
        
        self.ax_maze.imshow(maze_view, cmap='viridis', origin='upper')
        self.ax_maze.plot(half, half, 'r*', markersize=20)  # Agent
        self.ax_maze.set_title(f"Maze View (Step {step})")
        self.ax_maze.axis('off')
        
        # 2. Metrics
        self.reward_history.append(total_reward)
        self.explore_history.append(maze.cells_explored)
        
        self.ax_metrics.plot(self.reward_history, label='Total Reward', color='green')
        self.ax_metrics.set_xlabel('Steps (x5)')
        self.ax_metrics.set_ylabel('Reward', color='green')
        self.ax_metrics.tick_params(axis='y', labelcolor='green')
        
        ax2 = self.ax_metrics.twinx()
        ax2.plot(self.explore_history, label='Cells Explored', color='blue')
        ax2.set_ylabel('Cells', color='blue')
        ax2.tick_params(axis='y', labelcolor='blue')
        
        self.ax_metrics.set_title("Performance Metrics")
        self.ax_metrics.grid(alpha=0.3)
        
        # 3. Engine state
        dash = agent.sovereign_engine.get_dashboard()
        
        self.ax_engine.axis('off')
        engine_text = f"""Engine: {agent.engine_type.upper()}
Pillar: {agent.specialization.name}

Σ (Filter): {dash['sigma']:.2f}
Ω (Entropy): {dash['omega']:.2f}
Λ (Friction): {dash['lambda']:.2f}
Rv (Viability): {dash['viability_ratio']:.2f}

Position: ({x}, {y})
Explored: {maze.cells_explored} cells
Treasures: {len(maze.treasures_collected)}
"""
        
        self.ax_engine.text(0.1, 0.5, engine_text, fontsize=11, 
                           family='monospace', verticalalignment='center')
        
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        plt.pause(0.01)
    
    def display_leaderboard(self):
        """Display final leaderboard."""
        print("\n" + "=" * 80)
        print("🏆 LEADERBOARD - CELLS EXPLORED")
        print("=" * 80)
        
        sorted_by_explore = sorted(
            self.results.items(),
            key=lambda x: x[1]['cells_explored'],
            reverse=True
        )
        
        for rank, (name, result) in enumerate(sorted_by_explore, 1):
            print(f"{rank}. {name:30s} | Cells: {result['cells_explored']:5d} | "
                  f"Reward: {result['total_reward']:7.1f} | Treasures: {result['treasures']}")
        
        print("\n" + "=" * 80)
        print("🏆 LEADERBOARD - TOTAL REWARD")
        print("=" * 80)
        
        sorted_by_reward = sorted(
            self.results.items(),
            key=lambda x: x[1]['total_reward'],
            reverse=True
        )
        
        for rank, (name, result) in enumerate(sorted_by_reward, 1):
            print(f"{rank}. {name:30s} | Reward: {result['total_reward']:7.1f} | "
                  f"Cells: {result['cells_explored']:5d} | Treasures: {result['treasures']}")
        
        # Crown the champion
        champion_explore = sorted_by_explore[0]
        champion_reward = sorted_by_reward[0]
        
        print("\n" + "=" * 80)
        print("👑 CHAMPIONS")
        print("=" * 80)
        print(f"Best Explorer: {champion_explore[0]} ({champion_explore[1]['cells_explored']} cells)")
        print(f"Best Survivor: {champion_reward[0]} ({champion_reward[1]['total_reward']:.1f} reward)")
    
    def visualize_results(self):
        """Create results visualization."""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle("Infinite Maze Arena - Final Results", fontsize=16, fontweight='bold')
        
        # Extract data
        names = list(self.results.keys())
        cells = [r['cells_explored'] for r in self.results.values()]
        rewards = [r['total_reward'] for r in self.results.values()]
        treasures = [r['treasures'] for r in self.results.values()]
        
        # Colors by engine
        colors = []
        for name in names:
            if 'sovereign' in name:
                colors.append('purple')
            elif 'zero_point' in name:
                colors.append('orange')
            elif 'gravity' in name:
                colors.append('blue')
        
        # 1. Cells explored
        axes[0, 0].barh(names, cells, color=colors)
        axes[0, 0].set_xlabel('Cells Explored')
        axes[0, 0].set_title('Exploration Performance')
        axes[0, 0].grid(axis='x', alpha=0.3)
        
        # 2. Total reward
        axes[0, 1].barh(names, rewards, color=colors)
        axes[0, 1].set_xlabel('Total Reward')
        axes[0, 1].set_title('Survival Performance')
        axes[0, 1].grid(axis='x', alpha=0.3)
        
        # 3. Treasures
        axes[1, 0].barh(names, treasures, color=colors)
        axes[1, 0].set_xlabel('Treasures Found')
        axes[1, 0].set_title('Treasure Hunting')
        axes[1, 0].grid(axis='x', alpha=0.3)
        
        # 4. Engine comparison (grouped)
        axes[1, 1].axis('off')
        
        # Calculate engine averages
        engine_stats = {}
        for engine in self.engines:
            engine_results = [r for name, r in self.results.items() if engine in name]
            if engine_results:
                engine_stats[engine] = {
                    'avg_cells': np.mean([r['cells_explored'] for r in engine_results]),
                    'avg_reward': np.mean([r['total_reward'] for r in engine_results]),
                    'avg_treasures': np.mean([r['treasures'] for r in engine_results])
                }
        
        stats_text = "Engine Averages:\n\n"
        for engine, stats in engine_stats.items():
            stats_text += f"{engine.upper()}:\n"
            stats_text += f"  Cells: {stats['avg_cells']:.1f}\n"
            stats_text += f"  Reward: {stats['avg_reward']:.1f}\n"
            stats_text += f"  Treasures: {stats['avg_treasures']:.1f}\n\n"
        
        axes[1, 1].text(0.1, 0.5, stats_text, fontsize=10, family='monospace', verticalalignment='center')
        
        plt.tight_layout()
        plt.savefig('maze_arena_results.png', dpi=150, bbox_inches='tight')
        print(f"\n📊 Results saved to: maze_arena_results.png")
        
        plt.show(block=True)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Infinite Maze Arena - Engine Battle')
    parser.add_argument('--steps', type=int, default=500, help='Steps per agent')
    parser.add_argument('--visualize', action='store_true', help='Enable live visualization')
    parser.add_argument('--seed', type=int, default=42, help='Random seed')
    
    args = parser.parse_args()
    
    arena = MazeArena(seed=args.seed, steps_per_agent=args.steps)
    arena.run_battle(visualize=args.visualize)
