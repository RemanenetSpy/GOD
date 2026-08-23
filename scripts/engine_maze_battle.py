"""
Pure Engine Maze Battle

Just like ARC-AGI achieved 99% with Gravity Engine alone,
this tests engines DIRECTLY without Agent wrapper.

Engines drive navigation via pure metabolism/viability signals.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, Dict, List
import time

from infinite_maze import InfiniteMaze, CellType
from sovereign_engine import UniversalSovereignEngine
from zero_point_engine import ZeroPointEngine
from gravity_engine import GravityEngine
from eigen_solver import EigenSolver
from environment import Action

class EngineNavigator:
    """Pure engine-driven navigation (no Agent)."""
    
    def __init__(self, engine, engine_name):
        self.engine = engine
        self.engine_name = engine_name
        self.action_history = []
        self.visit_history = {}  # (x,y) -> count
        self.known_treasures = {}  # (x,y) -> reward
        
    def choose_action(self, observation, maze_pos) -> Action:
        """
        Physics-based navigation using engine-specific methods:
        - Gravity: GR potential fields (Laplace equation)
        - Zero-Point: Survival/metabolism-driven
        - Sovereign: Information-theoretic (Σ, Ω, Λ)
        """
        visible = observation.visible_cells
        x, y = maze_pos
        
        # Track visits
        self.visit_history[(x, y)] = self.visit_history.get((x, y), 0) + 1
        
        # Get valid neighbors
        valid_neighbors = []
        actions_map = [
            (0, Action.MOVE_UP, -1, 0),
            (1, Action.MOVE_DOWN, 1, 0),
            (2, Action.MOVE_LEFT, 0, -1),
            (3, Action.MOVE_RIGHT, 0, 1)
        ]
        
        center = visible.shape[0] // 2
        maze_size = visible.shape[0]
        
        for action_idx, action, dx, dy in actions_map:
            target_x = center + dx
            target_y = center + dy
            
            if 0 <= target_x < visible.shape[0] and 0 <= target_y < visible.shape[1]:
                target_cell = visible[target_x, target_y]
                
                # Not a wall
                if target_cell != 2:  # not OBSTACLE
                    nx, ny = x + dx, y + dy
                    valid_neighbors.append((action_idx, nx, ny))
                    
                    # Learn treasure locations
                    if target_cell == 1:  # RESOURCE
                        if (nx, ny) not in self.known_treasures:
                            self.known_treasures[(nx, ny)] = 50.0
        
        if not valid_neighbors:
            return Action.WAIT
        
        # ==============================================
        # ENGINE-SPECIFIC NAVIGATION
        # ==============================================
        
        if self.engine_name == 'gravity':
            # GENERAL RELATIVITY (Manifold Injection Upgrade)
            maze_size = visible.shape[0]
            maze_state = np.zeros((maze_size, maze_size))
            
            # Map visible state to local maze_state
            # GravityEngine now expects wall_value parameter.
            # We copy visible map directly. visible uses 2 for Wall.
            maze_state = visible.copy()
            
            # GOAL SELECTION (Frontier Gravity)
            # We use the same powerful logic as Manifold Engine:
            # Goals = Treasures + Unknowns (as Sinks)
            goals = []
            
            # 1. Treasures (High Priority Sinks)
            for (tx, ty), val in self.known_treasures.items():
                if val > 0:
                    # Tx, Ty are global. We need local invisible frame.
                    # visible map is centered on x,y with size 30 or similar.
                    # Wait, visible is local view.
                    # But known_treasures stores GLOBAL.
                    # We need to find if treasure is in local view.
                    dx = tx - (x - center)
                    dy = ty - (y - center)
                    if 0 <= dx < maze_size and 0 <= dy < maze_size:
                        goals.append((dx, dy))
                        
            # 2. Unknowns (Frontier Sinks)
            # We want UNVISITED cells.
            if len(goals) == 0:
                 # Iterate to find unvisited
                 for i in range(maze_size):
                    for j in range(maze_size):
                        if visible[i, j] != 2: # Not wall
                             # Map to world coords to check history
                             wx = x + (i - center)
                             wy = y + (j - center)
                             if self.visit_history.get((wx, wy), 0) == 0:
                                 # Checking density: add to goals
                                 goals.append((i, j))
                                 
            # 3. Fallback: Least Visited
            if len(goals) == 0:
                 best_visit_count = float('inf')
                 best_pos = None
                 for i in range(maze_size):
                    for j in range(maze_size):
                        if visible[i, j] != 2:
                             wx = x + (i - center)
                             wy = y + (j - center)
                             v = self.visit_history.get((wx, wy), 0)
                             if v < best_visit_count:
                                 best_visit_count = v
                                 best_pos = (i, j)
                                 
                 if best_pos:
                     goals.append(best_pos)

            # Calculate GR potential field (Eikonal)
            try:
                # Pass wall_value=2 because visible map uses 2 for walls!
                field = self.engine.calculate_potential_field(
                    maze_state, goal_pos=None, wall_value=2, max_iterations=100, goals=goals
                )
                
                # Follow gradient
                action_idx = self.engine.navigate_via_gradient(field, (center, center))
                
                # Convert action_idx to Action
                action_map = [Action.MOVE_UP, Action.MOVE_DOWN, 
                             Action.MOVE_LEFT, Action.MOVE_RIGHT, Action.WAIT]
                return action_map[action_idx]
            except Exception as e:
                # Fallback
                return Action.WAIT
                
        elif self.engine_name == 'eigen':
            # SPECTRAL TUNNELING (Sinkhorn)
            best_goal = None
            min_dist = float('inf')
            
            # 1. Treasures
            for (tx, ty), val in self.known_treasures.items():
                if val > 0:
                    dx = tx - (x - center)
                    dy = ty - (y - center)
                    if 0 <= dx < maze_size and 0 <= dy < maze_size:
                        dist = abs(dx - center) + abs(dy - center)
                        if dist < min_dist and dist > 0:
                            min_dist = dist
                            best_goal = (dx, dy)
                            
            # 2. Nearest Unvisited
            if best_goal is None:
                for i in range(maze_size):
                    for j in range(maze_size):
                        if visible[i, j] != 2:
                             wx = x + (i - center)
                             wy = y + (j - center)
                             if self.visit_history.get((wx, wy), 0) == 0:
                                 dist = abs(i - center) + abs(j - center)
                                 # Must be > 0 (not current pos)
                                 if dist < min_dist and dist > 0:
                                     min_dist = dist
                                     best_goal = (i, j)
                                     
            # 3. Fallback: Edge or Random
            if best_goal is None:
                 best_goal = (maze_size - 2, maze_size - 2)
                 
            # Action
            # Pass wall_value=2
            action_idx = self.engine.navigate_via_flow_field(
                (center, center),
                best_goal,
                visible, # Observations (2=wall)
                self.visit_history,
                valid_neighbors,
                wall_value=2
            )
            
            action_map = [Action.MOVE_UP, Action.MOVE_DOWN, 
                          Action.MOVE_LEFT, Action.MOVE_RIGHT, Action.WAIT]
            return action_map[action_idx]
        
        elif self.engine_name == 'zero_point':
            # SURVIVAL: Metabolism-driven navigation
            uncertainty_map = np.ones_like(visible, dtype=float)
            
            action_idx = self.engine.navigate_via_survival(
                current_pos=(x, y),
                known_treasures=self.known_treasures,
                visit_history=self.visit_history,
                valid_neighbors=valid_neighbors
            )
            
            action_map = [Action.MOVE_UP, Action.MOVE_DOWN,
                         Action.MOVE_LEFT, Action.MOVE_RIGHT, Action.WAIT]
            return action_map[action_idx]
        
        elif self.engine_name == 'sovereign':
            # INFORMATION THEORY: Σ, Ω, Λ navigation
            # Build uncertainty map (1 = unknown, 0 = known)
            uncertainty_map = np.ones_like(visible, dtype=float)
            
            for i in range(visible.shape[0]):
                for j in range(visible.shape[1]):
                    # Known cells have low uncertainty
                    if visible[i, j] != -1:  # Not unknown
                        uncertainty_map[i, j] = 0.1
            
            action_idx = self.engine.navigate_via_information(
                current_pos=(x, y),
                uncertainty_map=uncertainty_map,
                visit_history=self.visit_history,
                valid_neighbors=valid_neighbors
            )
            
            action_map = [Action.MOVE_UP, Action.MOVE_DOWN,
                         Action.MOVE_LEFT, Action.MOVE_RIGHT, Action.WAIT]
            return action_map[action_idx]
        
        elif self.engine_name == 'eigen':
            # OPTIMAL TRANSPORT: Zero-time flow field navigation
            # Find goal (nearest treasure or least visited)
            maze_size = visible.shape[0]
            
            goal_pos = None
            min_dist = float('inf')
            
            # Look for treasure
            for i in range(maze_size):
                for j in range(maze_size):
                    if visible[i, j] == 1:  # Treasure
                        dist = abs(i - center) + abs(j - center)
                        if dist < min_dist and dist > 0:
                            min_dist = dist
                            goal_pos = (i, j)
            
            # If no treasure, find least visited
            if goal_pos is None:
                best_visit_count = float('inf')
                for i in range(maze_size):
                    for j in range(maze_size):
                        if visible[i, j] != 2:  # Not wall
                            wx = x + (i - center)
                            wy = y + (j - center)
                            visit_count = self.visit_history.get((wx, wy), 0)
                            if visit_count < best_visit_count:
                                best_visit_count = visit_count
                                goal_pos = (i, j)
                
                if goal_pos is None:
                    goal_pos = (maze_size - 2, maze_size - 2)
            
            # Build maze state for OT
            maze_state = np.zeros((maze_size, maze_size))
            for i in range(maze_size):
                for j in range(maze_size):
                    if visible[i, j] == 2:
                        maze_state[i, j] = 1
            
            # Navigate via optimal transport
            action_idx = self.engine.navigate_via_flow_field(
                current_pos=(center, center),
                goal_pos=goal_pos,
                maze_state=maze_state,
                visit_history=self.visit_history,
                valid_neighbors=valid_neighbors
            )
            
            action_map = [Action.MOVE_UP, Action.MOVE_DOWN,
                         Action.MOVE_LEFT, Action.MOVE_RIGHT, Action.WAIT]
            return action_map[action_idx]
        
        else:
            # Fallback: random
            import random
            _, action, _, _ = random.choice(actions_map)
            return action


class EngineMazeBattle:
    def __init__(self, seed=42, steps=1000):
        self.seed = seed
        self.steps = steps
        self.results = {}
        
    def run_battle(self, visualize=True):
        """Run pure engine battle."""
        print("=" * 80)
        print("⚡ PURE ENGINE MAZE BATTLE (No Agent)")
        print("=" * 80)
        print("Testing engines AS-IS (like 99% ARC success)")
        print(f"Steps: {self.steps}, Seed: {self.seed}\n")
        
        # Test each engine
        engines = [
            ('sovereign', UniversalSovereignEngine()),
            ('zero_point', ZeroPointEngine()),
            ('gravity', GravityEngine()),
            ('eigen', EigenSolver())
        ]
        
        for engine_name, engine in engines:
            print(f"\n🔬 Testing: {engine_name.upper()}")
            print("-" * 60)
            
            result = self.run_single_engine(engine, engine_name, visualize=visualize)
            self.results[engine_name] = result
            
            print(f"✓ {engine_name}: {result['cells_explored']} cells, {result['total_reward']:.1f} reward, {result['treasures']} treasures")
        
        self.display_results()
    
    def run_single_engine(self, engine, engine_name, visualize=False):
        """Test single engine."""
        # Fresh maze
        maze = InfiniteMaze(seed=self.seed, visible_range=7)
        navigator = EngineNavigator(engine, engine_name)
        
        # Setup viz
        if visualize:
            fig, axes = plt.subplots(1, 2, figsize=(14, 6))
            fig.canvas.manager.set_window_title(f"Engine: {engine_name}")
            reward_history = []
            explore_history = []
        
        # Run
        obs = maze.observe()
        total_reward = 0
        treasures = 0
        
        for step in range(self.steps):
            # Engine decides
            action = navigator.choose_action(obs, maze.agent_pos)
            
            # Execute
            obs, reward, done = maze.step(action)
            total_reward += reward
            
            # Update engine (so it learns)
            engine.update(obs, action, reward)
            
            if reward > 10:
                treasures += 1
            
            # Visualize
            if visualize and step % 10 == 0:
                reward_history.append(total_reward)
                explore_history.append(maze.cells_explored)
                
                # Maze view
                axes[0].clear()
                x, y = maze.agent_pos
                size = 21
                half = size // 2
                
                view = np.zeros((size, size))
                for i in range(size):
                    for j in range(size):
                        wx = x + (i - half)
                        wy = y + (j - half)
                        cell = maze.get_cell(wx, wy)
                        
                        if cell.value == 2:
                            view[i, j] = 0.3
                        elif (wx, wy) in maze.visited_cells:
                            view[i, j] = 0.7
                        else:
                            view[i, j] = 1.0
                
                axes[0].imshow(view, cmap='viridis')
                axes[0].plot(half, half, 'r*', markersize=15)
                axes[0].set_title(f"{engine_name.upper()} - Step {step}")
                axes[0].axis('off')
                
                # Metrics
                axes[1].clear()
                axes[1].plot(reward_history, 'g-', label='Reward')
                axes[1].set_ylabel('Reward', color='g')
                axes[1].tick_params(axis='y', labelcolor='g')
                
                ax2 = axes[1].twinx()
                ax2.plot(explore_history, 'b-', label='Explored')
                ax2.set_ylabel('Cells', color='b')
                ax2.tick_params(axis='y', labelcolor='b')
                
                axes[1].set_xlabel('Steps (x10)')
                axes[1].set_title(f"Explored: {maze.cells_explored}")
                axes[1].grid(alpha=0.3)
                
                plt.pause(0.01)
        
        if visualize:
            plt.close()
        
        return {
            'cells_explored': maze.cells_explored,
            'total_reward': total_reward,
            'treasures': treasures,
            'final_pos': maze.agent_pos
        }
    
    def display_results(self):
        """Show leaderboard."""
        print("\n" + "=" * 80)
        print("🏆 PURE ENGINE BATTLE RESULTS")
        print("=" * 80)
        
        sorted_results = sorted(
            self.results.items(),
            key=lambda x: x[1]['cells_explored'],
            reverse=True
        )
        
        for rank, (name, result) in enumerate(sorted_results, 1):
            print(f"{rank}. {name.upper():15s} | "
                  f"Cells: {result['cells_explored']:5d} | "
                  f"Reward: {result['total_reward']:8.1f} | "
                  f"Treasures: {result['treasures']:2d} | "
                  f"Pos: {result['final_pos']}")
        
        winner = sorted_results[0]
        print(f"\n👑 WINNER: {winner[0].upper()} with {winner[1]['cells_explored']} cells explored!")
        
        # Visualization
        self.plot_comparison()
    
    def plot_comparison(self):
        """Plot comparison chart."""
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        fig.suptitle("Pure Engine Performance Comparison", fontsize=14, fontweight='bold')
        
        names = list(self.results.keys())
        cells = [r['cells_explored'] for r in self.results.values()]
        rewards = [r['total_reward'] for r in self.results.values()]
        treasures = [r['treasures'] for r in self.results.values()]
        
        colors = ['purple', 'orange', 'blue']
        
        axes[0].bar(names, cells, color=colors)
        axes[0].set_ylabel('Cells Explored')
        axes[0].set_title('Exploration')
        axes[0].grid(axis='y', alpha=0.3)
        
        axes[1].bar(names, rewards, color=colors)
        axes[1].set_ylabel('Total Reward')
        axes[1].set_title('Survival')
        axes[1].grid(axis='y', alpha=0.3)
        
        axes[2].bar(names, treasures, color=colors)
        axes[2].set_ylabel('Treasures')
        axes[2].set_title('Treasure Hunting')
        axes[2].grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('engine_battle_results.png', dpi=150, bbox_inches='tight')
        print(f"\n📊 Results saved to: engine_battle_results.png")
        plt.show(block=True)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Pure Engine Maze Battle')
    parser.add_argument('--steps', type=int, default=1000, help='Steps per engine')
    parser.add_argument('--visualize', action='store_true', help='Live visualization')
    parser.add_argument('--seed', type=int, default=42, help='Random seed')
    
    args = parser.parse_args()
    
    battle = EngineMazeBattle(seed=args.seed, steps=args.steps)
    battle.run_battle(visualize=args.visualize)
