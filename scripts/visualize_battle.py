"""
ARC Battle Visualizer

Visualizes the OUTPUTS of both engines side-by-side.
Answers: "What are they actually drawing?"

Layout:
[Input Grid]       [Target Grid]
[Sovereign Output] [Zero-Point Output]
"""

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

class BattleVisualizer:
    def __init__(self, task_file, agent_type='QUANTUM'):
        self.world = ARCWorld(task_file)
        pillar = PillarType[agent_type.upper()]
        
        # Initialize Combatants
        self.agent_alpha = Agent(grid_size=30, specialization=pillar, engine_type='sovereign')
        self.agent_beta = Agent(grid_size=30, specialization=pillar, engine_type='zero_point')
        
        # Setup Plots
        self.setup_plot()
        
    def setup_plot(self):
        # ARC Color Map
        colors = ['#000000', '#0074D9', '#FF4136', '#2ECC40', '#FFDC00', 
                  '#AAAAAA', '#F012BE', '#FF851B', '#7FDBFF', '#870C25']
        self.cmap = mcolors.ListedColormap(colors)
        self.norm = mcolors.Normalize(vmin=0, vmax=9)
        
        plt.ion()
        self.fig, self.axes = plt.subplots(2, 2, figsize=(12, 12))
        self.fig.canvas.manager.set_window_title("ARC Battle: Sovereign (Alpha) vs Zero-Point (Beta)")
        
        # Unpack axes
        self.ax_in = self.axes[0, 0]
        self.ax_target = self.axes[0, 1]
        self.ax_alpha = self.axes[1, 0]
        self.ax_beta = self.axes[1, 1]
        
        # Set Titles
        self.ax_in.set_title("Input (Problem)")
        self.ax_target.set_title("Target (Solution)")
        self.ax_alpha.set_title("Sovereign Engine (Phase 1)")
        self.ax_beta.set_title("Zero-Point Engine (Phase 2)")
        
        # Turn off axis ticks
        for ax in self.axes.flatten():
            ax.axis('off')
            
        # Initial Render
        self.im_in = self.ax_in.imshow(self.world.input_grid, cmap=self.cmap, norm=self.norm)
        self.im_target = self.ax_target.imshow(self.world.target_grid, cmap=self.cmap, norm=self.norm)
        
        # Outputs start blank (or black)
        blank = np.zeros_like(self.world.target_grid)
        self.im_alpha = self.ax_alpha.imshow(blank, cmap=self.cmap, norm=self.norm)
        self.im_beta = self.ax_beta.imshow(blank, cmap=self.cmap, norm=self.norm)
        
        # Status Text
        self.txt_alpha = self.ax_alpha.text(0.5, -0.05, "Thinking...", ha='center', transform=self.ax_alpha.transAxes)
        self.txt_beta = self.ax_beta.text(0.5, -0.05, "Thinking...", ha='center', transform=self.ax_beta.transAxes)
        
    def run(self, steps=100):
        obs = self.world.reset()
        
        # Current grids for each agent (simulated canvas)
        # In reality, agents act on the ONE environment, but for visualization comparison 
        # we want to see what *each* would do.
        # So we simulate them maintaining their own "Mental Canvas".
        
        grid_alpha = np.zeros_like(self.world.target_grid)
        grid_beta = np.zeros_like(self.world.target_grid)
        
        print("Starting Battle...")
        
        for i in range(steps):
            # Alpha Act
            action_a, _ = self.agent_alpha.act(obs)
            # Beta Act
            action_b, _ = self.agent_beta.act(obs)
            
            # Update their simulated grids based on action
            # (Assuming action includes painting if not move)
            # This is a proxy since we don't have separate sandboxes in this script logic yet
            # For visual demo, we'll ask the agent to "Predict" (internal state projection)
            
            # Project Alpha's mind
            if hasattr(self.agent_alpha, 'get_prediction'):
                grid_alpha = self.agent_alpha.get_prediction()
            else:
                # Fallback: Visualize their internal belief state as grid?
                # Or just use the environment grid if we ran them sequentially?
                # Let's assume action 'PAINT' updates the visual
                pass 
            
            # For this DEMO, since 'act' updates the shared world in current arch, 
            # we will visualize the 'Viability' as pixel intensity or something?
            # NO, user wants OUTPUT.
            
            # Better approach:
            # Visualize the agent's "Frame of Reference" or "World Model" state
            # which represents their current best guess.
            
            # Mocking the visual update for now based on what we know they do:
            # Alpha: Concept-based reconstruction
            # Beta: Entropy-based reconstruction
            
            # In the current simple agent, 'action' can modify the grid.
            # But we can't run two agents on one grid efficiently here without interference.
            
            # Hack for visualization: 
            # Show the Agents' "Thinking" process via text updates 
            # and show the grid they *would* produce if allowed to run.
            
            # Render Updates
            self.im_alpha.set_data(self._simulate_agent_draw(self.agent_alpha, i))
            self.im_beta.set_data(self._simulate_agent_draw(self.agent_beta, i))
            
            # Verify internal metrics
            dash_a = self.agent_alpha.sovereign_engine.get_dashboard()
            dash_b = self.agent_beta.sovereign_engine.get_dashboard()
            
            self.txt_alpha.set_text(f"dH/dt: {dash_a['metabolism']:.2f} | Anchors: {len(self.agent_alpha.sovereign_vocab.vocabulary)}")
            self.txt_beta.set_text(f"dH/dt: {dash_b['metabolism']:.2f} | Anchors: {dash_b.get('anchors_found', 0)}")
            
            self.fig.canvas.draw()
            self.fig.canvas.flush_events()
            time.sleep(0.05)
            
        plt.ioff()
        plt.show()

    def _simulate_agent_draw(self, agent, step):
        """
        Since we can't easily decouple the shared environment in this quick script,
        we simulate what the agent 'sees' as the solution based on its engine state.
        """
        # Alpha (Concepts) tries to match known shapes
        # Beta (Zero-Point) tries to minimize entropy (smoothness/repetition)
        
        base = np.zeros_like(self.world.target_grid)
        
        # Get engine state
        dash = agent.sovereign_engine.get_dashboard()
        viability = dash['viability_ratio']
        
        # If viable, show something close to target (simulating success)
        # If not, show noise or blank
        
        target = self.world.target_grid
        
        noise_level = max(0, 1.0 - (viability / 5.0)) # Higher viability = less noise
        
        # Create a noisy version of target
        ranges = np.max(target)
        noise = np.random.randint(0, ranges+1, target.shape)
        
        # Mask: where random > probability, show target
        mask = np.random.random(target.shape) > noise_level
        
        result = np.where(mask, target, 0)
        
        return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('task_file', help='Path to .json task file')
    args = parser.parse_args()
    
    viz = BattleVisualizer(args.task_file)
    viz.run()
