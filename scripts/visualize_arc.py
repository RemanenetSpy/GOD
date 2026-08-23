import sys
import os
import argparse
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.arc_adapter import ARCWorld
from src.agent import Agent, PillarType
from src.environment import Action

class ARCVisualizer:

    def __init__(self, task_file, agent_type='INFORMATION', engine_type='sovereign', pair_index=0):
        self.world = ARCWorld(task_file, pair_index=pair_index)
        pillar = PillarType[agent_type.upper()]
        
        # Phase 27: Plug-and-Play Engine
        self.agent = Agent(grid_size=30, specialization=pillar, engine_type=engine_type)
        
        # ARC Color Map
        colors = ['#000000', '#0074D9', '#FF4136', '#2ECC40', '#FFDC00', 
                  '#AAAAAA', '#F012BE', '#FF851B', '#7FDBFF', '#870C25']
        self.cmap = mcolors.ListedColormap(colors)
        self.norm = mcolors.Normalize(vmin=0, vmax=9)
        
        # Setup Plot (Enhanced Dashboard)
        plt.ion()
        self.fig = plt.figure(figsize=(16, 12))
        self.fig.canvas.manager.set_window_title(f"ARC-AGI: {agent_type} ({engine_type.upper()})")
        
        # Layout:
        # [Input] [Output]
        # [Metabolism] [Viability] [Anchors]
        
        gs = self.fig.add_gridspec(2, 3)
        self.ax_in = self.fig.add_subplot(gs[0, 0])
        self.ax_out = self.fig.add_subplot(gs[0, 1])
        self.ax_meta = self.fig.add_subplot(gs[1, 0])
        self.ax_via = self.fig.add_subplot(gs[1, 1])
        self.ax_stat = self.fig.add_subplot(gs[0, 2])
        self.ax_anchors = self.fig.add_subplot(gs[1, 2])
        
        self.im_in = None
        self.im_out = None
        
        # History
        self.history = {
            'metabolism': [],
            'viability': [],
            'anchors': []
        }

    def render(self):
        # Render Input
        if self.im_in is None:
            self.ax_in.set_title("Input (Context)")
            self.im_in = self.ax_in.imshow(self.world.input_grid, cmap=self.cmap, norm=self.norm)
            self.ax_in.axis('off')
        
        # Render Output
        display_grid = self.world.current_grid.copy()
        if self.im_out is None:
            self.ax_out.set_title("Output (Agent Canvas)")
            self.im_out = self.ax_out.imshow(display_grid, cmap=self.cmap, norm=self.norm)
            self.ax_out.axis('off')
        else:
            self.im_out.set_data(display_grid)
            
        # Get Engine Dashboard
        dash = self.agent.sovereign_engine.get_dashboard()
        
        # Update History
        self.history['metabolism'].append(dash['metabolism'])
        self.history['viability'].append(dash['viability_ratio'])
        
        # Count Anchors/Concepts
        if self.agent.engine_type == 'zero_point':
            anchor_count = dash.get('anchors_found', 0)
        else:
            anchor_count = len(self.agent.sovereign_vocab.vocabulary)
        self.history['anchors'].append(anchor_count)
        
        # Render Metrics
        
        # 1. Metabolism (dH/dt)
        self.ax_meta.clear()
        self.ax_meta.plot(self.history['metabolism'], color='orange')
        self.ax_meta.set_title("Metabolism (dH/dt)")
        self.ax_meta.axhline(0, color='red', linestyle='--')
        self.ax_meta.grid(True, alpha=0.3)
        
        # 2. Viability Ratio (Rv)
        self.ax_via.clear()
        self.ax_via.plot(self.history['viability'], color='green')
        self.ax_via.set_title("Viability Ratio (Rv)")
        self.ax_via.axhline(1.0, color='red', linestyle='--')
        self.ax_via.grid(True, alpha=0.3)
        
        # 3. Stats Text
        self.ax_stat.clear()
        self.ax_stat.axis('off')
        stats = [
            f"Step: {len(self.history['metabolism'])}",
            f"Σ (Filter): {dash['sigma']:.2f}",
            f"Ω (Entropy): {dash['omega']:.2f}",
            f"Λ (Friction): {dash['lambda']:.2f}",
            f"Rv: {dash['viability_ratio']:.2f}",
            f"Action: {dash['prescribed_action']}",
            f"Diagnostic: {dash['diagnostic']}"
        ]
        self.ax_stat.text(0.1, 0.5, "\n".join(stats), fontsize=12, transform=self.ax_stat.transAxes, verticalalignment='center')
        
        # 4. Anchors / Concepts
        self.ax_anchors.clear()
        self.ax_anchors.plot(self.history['anchors'], color='purple')
        label = "Metabolic Anchors" if self.agent.engine_type == 'zero_point' else "Concepts Learned"
        self.ax_anchors.set_title(label)
        self.ax_anchors.grid(True, alpha=0.3)
        
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        
    def run(self, steps=100):
        print(f"Goal: Match {self.world.target_grid.shape} grid.")
        obs = self.world.reset()
        
        for i in range(steps):
            # Agent act
            action, _ = self.agent.act(obs)
            obs, reward, done = self.world.step(action)
            
            self.render()
            # Slow down for visualization
            plt.pause(0.05)
            
            if done:
                print("\nSolved! (Or Max Steps Reached)")
                # Hold final frame
                plt.ioff()
                plt.show(block=True)
                break
        plt.ioff()
        plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('task_file', help='Path to .json task file')
    parser.add_argument('--agent', default='INFORMATION', help='Agent Specialization')
    parser.add_argument('--engine', default='sovereign', choices=['sovereign', 'zero_point'], help='Engine Type')
    args = parser.parse_args()
    
    viz = ARCVisualizer(args.task_file, agent_type=args.agent, engine_type=args.engine)
    viz.run()
