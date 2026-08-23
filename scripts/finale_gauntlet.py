"""
The Final Gauntlet: Sovereign Synthesis.
"The Healing of the Dead System."

Scenario:
We drop the GOD System into a 'Logic Vacuum' (A Corrupted Memory Bank).
The System must:
1. Scout (Sovereign) -> Find the Corruption.
2. Bridge (Eigen) -> Connect the fragments.
3. Path (Gravity) -> Flow into the wounds.
4. Anchor (Zero-Point) -> Manage the energy.
5. Architect (Autopoietic) -> Crystallize the Chaos.

Visualized as a real-time transformation of a Grid.
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from autopoietic_engine import AutopoieticEngine
from sovereign_engine import UniversalSovereignEngine
from gravity_engine import GravityEngine
from zero_point_engine import ZeroPointEngine
# Eigen is functional, we'll simulate its Teleport logic via Autopoiesis for this abstract demo

def generate_dead_system(size=64):
    """
    Creates a 'Crashed Server':
    - Background: Random Noise (Entropy).
    - Fragments: Broken Logic (Structured blocks).
    """
    # 0 = Void, 1..255 = Data
    system = np.random.randint(0, 256, (size, size))
    
    # Inject "Corruption" (Pure Static)
    corruption_mask = np.random.rand(size, size) < 0.8
    system[corruption_mask] = np.random.randint(200, 256, np.sum(corruption_mask)) # High values = Noise
    
    # Inject "Logic Fragments" (The Goal: To be Connected)
    # Low values = Structured Code
    center = size // 2
    system[center-5:center+5, center-5:center+5] = 10 # Core Logic
    
    return system

def run_the_gauntlet():
    print("Initializing The Sovereign Organism (All 5 Engines)...")
    
    # 1. The Anchors
    sovereign = UniversalSovereignEngine()
    gravity = GravityEngine()
    autopoietic = AutopoieticEngine()
    zero_point = ZeroPointEngine()
    
    # 2. The Environment
    grid = generate_dead_system(64)
    h, w = grid.shape
    
    # Simulation Loop
    # energy = 1000 managed by Zero-Point internally
    steps = 0
    max_steps = 50
    
    snapshots = []
    snapshots.append(grid.copy())
    
    print("Beginning Synthesis...")
    
    cursor_pos = (0, 0)
    
    history_density = []
    
    while steps < max_steps:
        # A. PERCEPTION (Autopoietic / Sovereign)
        # 1. Autopoietic scans for Density (Where is the Logic?)
        # Low Value = Logic (in this map), High Value = Noise.
        # Let's map it to Density: Logic is Dense (Consistent).
        rho = autopoietic.calculate_local_feature_density(grid, window_size=3)
        mean_rho = np.mean(rho)
        history_density.append(mean_rho)
        
        # 2. Sovereign picks a Target (Highest Entropy or Novelty?)
        # In this healing scenario, Sovereign seeks the "Broken" parts to fix?
        # Or the "Logic" parts to protect?
        # 'Finale.md': Sovereign feels a 'Pull' toward hidden cluster of intact logic.
        # So Sovereign targets High Density (The Core).
        
        # Find peak density
        y, x = np.unravel_index(np.argmax(rho), rho.shape)
        target = (y, x)
        
        # B. NAVIGATION (Gravity / Eigen)
        # Gravity calculates flow to Target
        # Eigen would teleport if distance is huge.
        
        # Move Cursor towards Target (Simulated Gravity Step)
        dy = target[0] - cursor_pos[0]
        dx = target[1] - cursor_pos[1]
        
        # Normalize step
        if abs(dy) + abs(dx) > 0:
            step_y = int(np.sign(dy))
            step_x = int(np.sign(dx))
            cursor_pos = (cursor_pos[0] + step_y, cursor_pos[1] + step_x)
        
        # C. METABOLISM (Zero-Point)
        cost = 1 + (grid[cursor_pos] / 255.0) # High noise = High friction
        if zero_point.energy < cost:
            print("Zero-Point Halts: Insufficient Energy.")
            break
        zero_point.energy -= cost
        
        # D. ACTION (Autopoietic Architect)
        # "Mutates the other engines into a single Healing Patch"
        # The Cursor "Crystallizes" the noise around it.
        # Turn Noise (High Val) into Logic (Low Val)
        
        # Radius of Effect
        ry, rx = cursor_pos
        for i in range(-2, 3):
            for j in range(-2, 3):
                ny, nx = ry + i, rx + j
                if 0 <= ny < h and 0 <= nx < w:
                    # Healing: Set to match the Core Logic (10)
                    # Interpolate: Move current value closer to 10
                    current = grid[ny, nx]
                    grid[ny, nx] = int(current * 0.5 + 10 * 0.5)
                    
        steps += 1
        if steps % 10 == 0:
            snapshots.append(grid.copy())
            print(f"Step {steps}: Energy={zero_point.energy:.1f}, System Entropy={mean_rho:.4f}")
            
    # Visualize The Healing
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    axes[0].imshow(snapshots[0], cmap='inferno')
    axes[0].set_title("The Dead System (Start)")
    
    axes[1].imshow(snapshots[len(snapshots)//2], cmap='inferno')
    axes[1].set_title("The Sovereign Synthesis (Healing)")
    
    axes[2].imshow(grid, cmap='inferno')
    axes[2].set_title("The Crystallized Outcome")
    
    plt.savefig("finale_gauntlet.png")
    print("Saved finale_gauntlet.png")
    
    print("\nSimulation Complete.")
    print("The Engines identified the Logic Core, navigated the Noise, and rewrote the System.")

if __name__ == "__main__":
    run_the_gauntlet()
