
import sys
import os
import time
import argparse
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import matplotlib.gridspec as gridspec
from matplotlib.patches import Circle

# Add src to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
src_dir = os.path.join(parent_dir, 'src')
sys.path.append(src_dir)

from infinite_maze import InfiniteMaze, CellType as MazeCellType
from environment import Action, Observation
from agent import Agent, PillarType

class MultiAgentSwarmByGod:
    def __init__(self, seed=42):
        self.maze = InfiniteMaze(seed=seed, chunk_size=32, visible_range=7)
        self.agents = {}
        
        # Initialize The Four Pillars
        colors = {
            'QUANTUM': 'purple',        # Explorer
            'RELATIVITY': 'blue',       # Social / Follower
            'PHYSICS': 'red',           # Safety / Avoiding
            'INFORMATION': 'green'      # Pattern / Tagger
        }
        
        self.colors = colors
        
        for name, color in colors.items():
            specialization = PillarType[name]
            # Create agent
            agent = Agent(grid_size=15, specialization=specialization, agent_id=f"Agent_{name}")
            # Space them out slightly so they don't overlap perfectly at start
            start_offset = {
                'QUANTUM': (0, 0),
                'RELATIVITY': (1, 0),
                'PHYSICS': (0, 1),
                'INFORMATION': (1, 1)
            }
            # We manage position externally for the shared maze, 
            # but Agent class thinks it is at (0,0) usually. 
            # We need to sync them.
            # Actually, InfiniteMaze tracks `agent_pos`.
            # For multi-agent, we need to track positions in THIS class.
            
            self.agents[name] = {
                'entity': agent,
                'pos': start_offset[name],
                'color': color,
                'history': [start_offset[name]],
                'symbol_cache': set() # What symbols has this agent invented?
            }
            
        # Visualization Setup
        plt.ion()
        self.fig = plt.figure(figsize=(15, 10))
        self.fig.canvas.manager.set_window_title("🌌 Swarm Intelligence: Emergent Communication")
        
        gs = gridspec.GridSpec(2, 2)
        self.ax_map = self.fig.add_subplot(gs[:, 0])
        self.ax_map.set_title("Shared World (Signals + Trails)")
        
        self.ax_vocab = self.fig.add_subplot(gs[0, 1])
        self.ax_vocab.set_title("Vocabulary Growth (Sovereignty)")
        
        self.ax_stats = self.fig.add_subplot(gs[1, 1])
        self.ax_stats.set_title("Exploration Leaderboard")
        self.ax_stats.axis('off')
        
        self.map_img = None
        
    def render(self, step):
        # 1. Base Map (Radius 20 around center of group? Or just origin)
        # Let's track the group center
        positions = [data['pos'] for data in self.agents.values()]
        mean_x = int(np.mean([p[0] for p in positions]))
        mean_y = int(np.mean([p[1] for p in positions]))
        
        # Extract grid
        size = 41
        half = size // 2
        grid = np.zeros((size, size))
        
        for i in range(size):
            for j in range(size):
                wx = mean_x + (i - half)
                wy = mean_y + (j - half)
                
                cell = self.maze.get_cell(wx, wy)
                val = 0 # Wall
                if cell.value == 1: val = 1 # Path
                elif cell.value == 2: val = 0.5 # Visited path (global)
                
                grid[i, j] = val
        
        # Render Map
        cmap = 'gray'
        self.ax_map.clear()
        self.ax_map.imshow(grid.T, cmap=cmap, origin='upper', extent=[mean_x-half, mean_x+half, mean_y+half, mean_y-half])
        
        # 2. Render Signals (Pheromones)
        # Iterate over visible range in map
        signal_x, signal_y = [], []
        signal_labels = []
        
        visible_signals = {k:v for k,v in self.maze.signals.items() 
                           if abs(k[0]-mean_x) < half and abs(k[1]-mean_y) < half}
        
        for pos, symbols in visible_signals.items():
            if symbols:
                self.ax_map.text(pos[0], pos[1], "★", color='yellow', fontsize=12, ha='center', va='center')
                # self.ax_map.text(pos[0], pos[1], symbols[-1][:3], color='orange', fontsize=6)
        
        # 3. Render Agents
        for name, data in self.agents.items():
            p = data['pos']
            # Draw trail
            hist = data['history'][-20:]
            if len(hist) > 1:
                hx, hy = zip(*hist)
                self.ax_map.plot(hx, hy, color=data['color'], alpha=0.5, linewidth=1)
            
            # Draw Agent
            self.ax_map.plot(p[0], p[1], marker='o', color=data['color'],  markersize=10, label=name)
            self.ax_map.text(p[0], p[1]-1, name[0], color='white', ha='center', fontsize=6)

        self.ax_map.set_xlim(mean_x - half, mean_x + half)
        self.ax_map.set_ylim(mean_y + half, mean_y - half) # Flip Y to match matrix
        self.ax_map.legend(loc='upper right', fontsize='small')

        # 4. Render Vocab Growth
        self.ax_vocab.clear()
        self.ax_vocab.set_title("Sovereign Vocabulary Size")
        for name, data in self.agents.items():
            vocab_size = len(data['entity'].sovereign_vocab.vocabulary)
            self.ax_vocab.bar(name, vocab_size, color=data['color'])
        
        # 5. Leaderboard
        self.ax_stats.clear()
        self.ax_stats.axis('off')
        self.ax_stats.set_title("Unique Cells Explored")
        text_str = ""
        # Calculate unique cells per agent (from history)
        sorted_agents = sorted(self.agents.items(), key=lambda item: len(set(item[1]['history'])), reverse=True)
        
        for i, (name, data) in enumerate(sorted_agents):
            unique = len(set(data['history']))
            text_str += f"{i+1}. {name}: {unique} cells\n"
            
        self.ax_stats.text(0.1, 0.5, text_str, fontsize=14, family='monospace')

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def run(self, steps=1000):
        print(f"Starting Multi-Agent Swarm for {steps} steps...")
        
        for step in range(steps):
            # Round Robin
            for name, data in self.agents.items():
                agent = data['entity']
                pos = data['pos']
                
                # 1. Observe
                # Pass explicit position to get local view
                obs = self.maze.observe(agent_pos=pos)
                
                # 2. Act
                action, _ = agent.act(obs)
                
                # 3. Apply Move
                dx, dy = 0, 0
                if action == Action.MOVE_UP: dy = -1
                elif action == Action.MOVE_DOWN: dy = 1
                elif action == Action.MOVE_LEFT: dx = -1
                elif action == Action.MOVE_RIGHT: dx = 1
                
                # Check collision with wall
                target_pos = (pos[0] + dx, pos[1] + dy)
                cell = self.maze.get_cell(target_pos[0], target_pos[1])
                
                if cell == MazeCellType.WALL:
                    # Bump! Stay in place
                    pass
                else:
                    # Move
                    data['pos'] = target_pos
                    data['history'].append(target_pos)
                    
                    # Log 'Visited' in maze (Signal 1: Physical Trail)
                    if target_pos not in self.maze.visited_cells:
                        self.maze.visited_cells.add(target_pos)
                        
                # 4. COMMUNICATE (The Stigmergic Step)
                # If agent has a high-confidence concept for this location, DROP IT.
                # For demo, we simulate "Confidence" based on re-visiting or dead-ends.
                
                # Simple logic: If 'Information' agent finds a wall, tag it 'WALL_C1'
                if name == 'INFORMATION': 
                    # Tag neighbors that are walls
                    for nx, ny in [(0,1), (0,-1), (1,0), (-1,0)]:
                        np_x, np_y = data['pos'][0]+nx, data['pos'][1]+ny
                        if self.maze.get_cell(np_x, np_y) == MazeCellType.WALL:
                             self.maze.drop_signal(np_x, np_y, "SOLID_BLOCK")
                             
                # If 'Physics' agent finds a 'SOLID_BLOCK' signal, it avoids it (simulated via act logic eventually)
                # Currently agent.act() is opaque, but we feed `obs` which has signals.
                # The agent will learn: Signal 'SOLID_BLOCK' -> Reward -1 (if it bumps).
                
                # 5. Learn
                agent.universal_update(action, obs)

            if step % 2 == 0:
                self.render(step)
            
            print(f"Step {step}/{steps}", end='\r')
            # time.sleep(0.01) # Fast mode

if __name__ == "__main__":
    sim = MultiAgentSwarmByGod()
    sim.run(steps=500)
