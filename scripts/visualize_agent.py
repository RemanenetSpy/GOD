import sys
import os
import time
import argparse
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import matplotlib.gridspec as gridspec

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.infinite_maze import InfiniteMaze
from src.environment import Action, CellType
from src.agent import Agent, PillarType

class AgentVisualizer:
    def __init__(self, agent_type='QUANTUM', seed=42):
        self.agent_type = agent_type
        self.maze = InfiniteMaze(seed=seed, chunk_size=32, visible_range=7)
        
        # Initialize agent
        pillar = PillarType[agent_type.upper()]
        
        # Physics Agent needs deep planning
        if agent_type == 'PHYSICS':
            # Ensure agent is configured for physics
             self.agent = Agent(grid_size=15, specialization=pillar)
        else:
             self.agent = Agent(grid_size=15, specialization=pillar) 
        
        # Setup Figure
        plt.ion()
        self.fig = plt.figure(figsize=(14, 10))
        self.fig.canvas.manager.set_window_title(f"🧠 {agent_type} Agent Dashboard")
        
        gs = gridspec.GridSpec(2, 2, height_ratios=[1, 1])
        
        # Panel 1: Local Maze
        self.ax_maze = self.fig.add_subplot(gs[0, 0])
        self.ax_maze.set_title(f"Local Maze View (Radius 20)")
        self.maze_im = None
        
        # Panel 2: Agent Specific View
        self.ax_panel2 = self.fig.add_subplot(gs[0, 1])
        if agent_type == 'RELATIVITY':
            self.ax_panel2.set_title("Future Prediction Map")
        elif agent_type == 'PHYSICS':
            self.ax_panel2.set_title("Safety Map (Risk Analysis)")
        elif agent_type == 'INFORMATION':
            self.ax_panel2.set_title("Pattern Confidence Map")
        else:
            self.ax_panel2.set_title("Belief Uncertainty Map")
        self.panel2_im = None
        
        # Panel 3: Exploration
        self.ax_explore = self.fig.add_subplot(gs[1, 0])
        self.ax_explore.set_title("Exploration Over Time")
        self.ax_explore.set_xlabel("Steps")
        self.ax_explore.set_ylabel("Unique Cells")
        self.line_explore, = self.ax_explore.plot([], [], 'g-', linewidth=2)
        
        # Panel 4: Metrics
        self.ax_metrics = self.fig.add_subplot(gs[1, 1])
        self.ax_metrics.set_title(f"{agent_type} Metrics")
        
        # Initialize lines based on agent type
        if agent_type == 'RELATIVITY':
            self.line_m1, = self.ax_metrics.plot([], [], 'b-', label='Prediction Error')
            self.line_m2, = self.ax_metrics.plot([], [], 'r-', label='Perspective Shifts')
            self.line_m3, = self.ax_metrics.plot([], [], 'y-', label='_nolegend_', alpha=0.0) # Hidden
        elif agent_type == 'PHYSICS':
            self.line_m1, = self.ax_metrics.plot([], [], 'b-', label='Optimality')
            self.line_m2, = self.ax_metrics.plot([], [], 'g-', label='Safety')
            self.line_m3, = self.ax_metrics.plot([], [], 'y-', label='risk', alpha=0.0)
        elif agent_type == 'INFORMATION':
            self.line_m1, = self.ax_metrics.plot([], [], 'b-', label='Compression')
            self.line_m2, = self.ax_metrics.plot([], [], 'm-', label='Surprise')
            self.line_m3, = self.ax_metrics.plot([], [], 'y-', label='_nolegend_', alpha=0.0)
        else: # QUANTUM
            self.line_m1, = self.ax_metrics.plot([], [], 'b-', label='Curiosity/Reward')
            self.line_m2, = self.ax_metrics.plot([], [], 'r-', label='Risk', alpha=0.6)
            self.line_m3, = self.ax_metrics.plot([], [], 'y-', label='Novelty', alpha=0.6)
            
        self.ax_metrics.legend(loc='upper right')
        
    def get_local_grid(self, center_pos, size=41):
        """Extract local grid around agent for visualization"""
        cx, cy = center_pos
        half = size // 2
        grid = np.zeros((size, size))
        
        for i in range(size):
            for j in range(size):
                wx = cx + (i - half)
                wy = cy + (j - half)
                cell = self.maze.get_cell(wx, wy)
                
                # Integer Encoding for Visualization
                # 0 = Wall (Black)
                # 1 = Visited (Gray/Blue)
                # 2 = Unvisited Path (White)
                # 3 = Goal (Gold)
                # 4 = Agent (Red)
                
                val = 0 # Default Wall
                
                # Check ground truth
                if cell.value == 1: val = 2 # PATH -> White
                elif cell.value == 2: val = 1 # VISITED -> Gray
                elif cell.value == 3: val = 3 # GOAL -> Gold
                elif cell.value == 4: val = 2 # START -> White
                
                # Overlay agent visited history (Client side memory)
                if (wx, wy) in self.maze.visited_cells:
                    val = 1 # Visited
                
                # Overlay current position (Agent)
                grid[i, j] = val
                
        grid[half, half] = 4 # Agent
        return grid

    def get_feature_map(self, center_pos, size=41):
        """Generate specific heatmap based on agent type"""
        cx, cy = center_pos
        calc_size = 21
        offset = (size - calc_size) // 2
        grid = np.zeros((size, size))
        
        for i in range(calc_size):
            for j in range(calc_size):
                wx = cx + (i - calc_size//2)
                wy = cy + (j - calc_size//2)
                
                # Default: Belief Map
                val = 0.0
                cell_val = self.agent.state.world_model.grid.get((wx, wy), CellType.UNKNOWN.value)
                
                if self.agent_type == 'RELATIVITY': # PREDICTION MAP
                    # Score = Expected Reward
                    if cell_val == CellType.OBSTACLE.value: val = -5.0
                    elif cell_val == CellType.UNKNOWN.value: val = 0.1
                    elif cell_val == CellType.EMPTY.value: val = 0.0
                    elif cell_val == CellType.RESOURCE.value: val = 1.0
                    
                    visits = self.agent.state.world_model.current_run_visits.get((wx, wy), 0)
                    if visits == 0 and cell_val != CellType.OBSTACLE.value: val += 2.0
                    else: val -= 0.1 * visits
                
                elif self.agent_type == 'PHYSICS': # SAFETY MAP
                    # Score = Safety (High = Safe, Low = Dangerous)
                    val = 1.0 # Default safe
                    if cell_val == CellType.OBSTACLE.value: val = -1.0 # Lethal
                    elif cell_val == CellType.UNKNOWN.value: val = 0.5 # Caution
                    
                    # Proximity to known obstacles reduces safety
                    # Check neighbors in world model
                    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                        nb_val = self.agent.state.world_model.grid.get((wx+dx, wy+dy), CellType.UNKNOWN.value)
                        if nb_val == CellType.OBSTACLE.value:
                            val -= 0.3
                            
                elif self.agent_type == 'INFORMATION': # PATTERN MAP
                    # Score = Pattern Confidence
                    # Check if this cell matches any high-confidence pattern
                    val = 0.0
                    for p in self.agent.state.world_model.patterns:
                         if p.get('position') == (wx, wy):
                             val = p.get('confidence', 0.5)
                             if p.get('type') == 'high_reward_cell': val *= 2.0
                             if p.get('type') == 'danger_zone': val *= -1.0 # Highlight danger differently?
                
                else: # QUANTUM (Belief Uncertainty)
                     dist = np.sqrt((i-calc_size//2)**2 + (j-calc_size//2)**2)
                     val = min(1.0, dist / 10.0)

                grid[offset+i, offset+j] = val
                
        return grid

    def update(self, step):
        # 1. Update Maze View
        local_grid = self.get_local_grid(self.maze.agent_pos)
        cmap = ListedColormap(['black', 'gray', 'white', 'gold', 'cyan'])
        if self.maze_im is None:
            self.maze_im = self.ax_maze.imshow(local_grid, cmap=cmap, vmin=0, vmax=4)
        else:
            self.maze_im.set_data(local_grid)
            
        # 2. Update Feature Map
        feature_grid = self.get_feature_map(self.maze.agent_pos)
        
        # Color maps
        f_cmap = 'viridis'
        v_min, v_max = 0, 1
        if self.agent_type == 'RELATIVITY': 
            f_cmap = 'coolwarm'
            v_min, v_max = -5, 5
        elif self.agent_type == 'PHYSICS':
            f_cmap = 'RdYlGn'
            v_min, v_max = -1, 1
        elif self.agent_type == 'INFORMATION':
            f_cmap = 'plasma'
            v_min, v_max = 0, 1
            
        if self.panel2_im is None:
            self.panel2_im = self.ax_panel2.imshow(feature_grid, cmap=f_cmap, vmin=v_min, vmax=v_max)
        else:
            self.panel2_im.set_data(feature_grid)
            # Update cmap/norm if switching agents technically (not needed for 1 run)

        # 3. Update Exploration
        steps = self.agent.history['steps']
        cells = self.agent.history['cells_visited']
        if steps:
            self.line_explore.set_data(steps, cells)
            self.ax_explore.set_xlim(0, max(100, steps[-1]))
            self.ax_explore.set_ylim(0, max(10, max(cells) * 1.1))

        # 4. Update Metrics
        if steps:
            m1, m2, m3 = [], [], []
            if self.agent_type == 'RELATIVITY':
                m1 = self.agent.history.get('prediction_error', [])
                m2 = self.agent.history.get('perspective_shifts', [])
            elif self.agent_type == 'PHYSICS':
                m1 = self.agent.history.get('optimality', [])
                m2 = self.agent.history.get('safety', [])
            elif self.agent_type == 'INFORMATION':
                m1 = self.agent.history.get('compression', [])
                m2 = self.agent.history.get('surprise', [])
            else:
                m1 = self.agent.history['curiosity']
                m2 = self.agent.history['risk']
                m3 = self.agent.history['novelty']

            min_len = min(len(steps), len(m1))
            self.line_m1.set_data(steps[:min_len], m1[:min_len])
            
            if m2: 
                min_len_m2 = min(len(steps), len(m2))
                self.line_m2.set_data(steps[:min_len_m2], m2[:min_len_m2])
            
            if m3:
                min_len_m3 = min(len(steps), len(m3))
                self.line_m3.set_data(steps[:min_len_m3], m3[:min_len_m3])
                
            self.ax_metrics.set_xlim(0, max(100, steps[-1]))
            # Dynamic Y-lim
            all_vals = m1 + m2 + m3
            if all_vals:
                self.ax_metrics.set_ylim(min(min(all_vals), -1), max(max(all_vals), 1) * 1.2)

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def run(self, steps=200):
        print(f"Starting visualization for {steps} steps...")
        obs = self.maze.observe()
        
        for i in range(steps):
            action, _ = self.agent.act(obs)
            obs, reward, done = self.maze.step(action)
            
            self.agent.universal_update(action, obs)
            
            if i % 2 == 0: 
                self.update(i)
            
            print(f"Step {i}: Pos={self.maze.agent_pos} Reward={reward:.2f}", end='\r')
            
        print("\nSimulation Complete.")
        plt.ioff()
        plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--agent', default='QUANTUM', help='Agent type: QUANTUM, RELATIVITY, PHYSICS, INFORMATION')
    parser.add_argument('--steps', type=int, default=500, help='Number of steps')
    args = parser.parse_args()
    
    viz = AgentVisualizer(agent_type=args.agent.upper())
    viz.run(steps=args.steps)
