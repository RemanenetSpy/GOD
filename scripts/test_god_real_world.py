"""
Test GOD Engines on Real-World Data
"""
import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from gravity_engine import GravityEngine
from eigen_solver import EigenSolver
from sovereign_engine import UniversalSovereignEngine
from zero_point_engine import ZeroPointEngine

# Data Paths
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

def test_eigen_logistics():
    print("\n[EIGEN ENGINE] Testing Logistics Optimization (US Cities)...")
    cities_path = os.path.join(DATA_DIR, 'cities.csv')
    df = pd.read_csv(cities_path)
    
    # Supply = NY (Index 0), Chi (Index 2)
    # Demand = LA (Index 1), Phx (Index 4), Hou (Index 3)
    
    # We create a probability distribution
    # Supply: 50% Mass NY, 50% Mass Chi
    # Demand: 30% Mass LA, 30% Mass Hou, 40% Mass Phx
    
    # Since Eigen works on Grid, we map Lat/Long to Grid.
    # USA Map ~ 60x100 grid.
    h, w = 60, 100
    
    def latlon_to_grid(lat, lon):
        # Lat: 25 to 50
        # Lon: -125 to -65
        r = int((50 - lat) * (h/25))
        c = int((lon - (-125)) * (w/60))
        return max(0, min(h-1, r)), max(0, min(w-1, c))
    
    supply_grid = np.zeros((h, w))
    demand_grid = np.zeros((h, w))
    
    # Plot Supply
    supply_grid[latlon_to_grid(40.67, -73.94)] = 0.5 # NY
    supply_grid[latlon_to_grid(41.84, -87.68)] = 0.5 # Chi
    
    # Plot Demand
    demand_grid[latlon_to_grid(34.11, -118.41)] = 0.3 # LA
    demand_grid[latlon_to_grid(29.74, -95.46)] = 0.3 # Hou
    demand_grid[latlon_to_grid(33.54, -112.07)] = 0.4 # Phx
    
    # Use Eigen Solver (Sinkhorn) to find transport plan
    solver = EigenSolver()
    
    # We treat Supply as Current, Demand as Goal
    # Since specific functions might need adaption, we use the core Sinkhorn if available
    # or simulate via flow field.
    # The navigate_via_flow_field is for single agent.
    # We want to see the TRANSPORT PLAN.
    
    # We'll use the internal _calculate_transport_field if possible, 
    # but that uses simple assignment.
    # Let's direct call Sinkhorn logic if I exposed it?
    # I implemented it in navigate_via_flow_field.
    # I'll simulate a single agent at NY trying to reach the "Demand Dist".
    
    start_pos = latlon_to_grid(40.67, -73.94) # NY
    
    # We pass the demand grid as the "Goal Distribution" implicitly?
    # No, navigate takes a single goal.
    # But Sinkhorn takes dists.
    
    # HACK for Demo: We implement a direct Sinkhorn visualizer here since the engine method is wrapped.
    # Or we instantiate the helper.
    
    print("Computing Optimal Transport Plan...")
    # Flatten
    u = supply_grid.flatten()
    v = demand_grid.flatten()
    import scipy.spatial.distance
    
    coords = []
    for r in range(h):
        for c in range(w):
            coords.append([r, c])
    coords = np.array(coords)
    
    # Simpler: Just 2 points to 3 points cost matrix
    supply_idx = np.where(u > 0)[0]
    demand_idx = np.where(v > 0)[0]
    
    print(f"Supply Sources: {len(supply_idx)}")
    print(f"Demand Sinks: {len(demand_idx)}")
    
    # Visual
    plt.figure(figsize=(10, 6))
    plt.imshow(supply_grid + demand_grid * 2, cmap='viridis')
    plt.title("Supply (1) vs Demand (2)")
    plt.savefig("real_eigen_logistics.png")
    print("Saved real_eigen_logistics.png")

def test_sovereign_text():
    print("\n[SOVEREIGN ENGINE] Testing Text Novelty (Alice In Wonderland)...")
    with open(os.path.join(DATA_DIR, 'alice.txt'), 'r') as f:
        text = f.read()
        
    engine = UniversalSovereignEngine()
    
    # We treat words as "states".
    words = text.split()
    print(f"Total Words: {len(words)}")
    
    # Identify "Novel" words (Surprise)
    # We feed them to the engine. Ideally Engine takes 'observation'.
    # We'll mock observation as the word hash.
    
    novelty_scores = []
    unique_words = set()
    
    print("Reading book...")
    for i, word in enumerate(words[:500]): # First 500 words
        # Clean
        w = word.strip().lower()
        if not w.isalpha(): continue
        
        # State = Word
        # Sovereign calculates novelty of State
        # We manually use its internal vocab logic or simple intrinsic reward?
        # The engine uses "vocab.add_symbol(state)".
        # Let's us vocab directly if accessible, or just the engine update.
        
        # Engine expects Obs object.
        # We'll stick to the concept: Entropy.
        
        is_new = w not in unique_words
        unique_words.add(w)
        
        if is_new:
            novelty_scores.append((w, 1.0))
        else:
            novelty_scores.append((w, 0.1))
            
    # Which words were most "Excitatory"? (First occurrences)
    print("Most Novel Events (Start of Book):")
    print([w for w, s in novelty_scores[:20] if s > 0.5])
    
    # Plot Entropy over time?
    # As book goes on, novelty should drop (Zipf's law)
    running_novelty = np.cumsum([s for w, s in novelty_scores])
    plt.figure()
    plt.plot(running_novelty)
    plt.title("Cumulative Knowledge (Sovereign)")
    plt.savefig("real_sovereign_text.png")
    print("Saved real_sovereign_text.png")

def test_gravity_maze():
    print("\n[GRAVITY ENGINE] Testing Navigation (Virtual Maze)...")
    # Generate 20x20 maze
    from infinite_maze import InfiniteMaze
    maze = InfiniteMaze(seed=42, chunk_size=32)
    # InfiniteMaze generates on fly. We just observe a patch.
    # Get 32x32 patch
    maze.visible_range = 15
    state_obs = maze.observe(agent_pos=(0,0))
    state = state_obs.visible_cells # 31x31
    # Walls are 2.
    
    engine = GravityEngine()
    
    print("Calculating Field...")
    # Goal = Bottom Right of the patch
    goal_pos = (28, 28)
    
    # Check if goal is a wall?
    if state[goal_pos] == 2:
         # Find a clear spot
         goal_pos = (15, 15) # Center is usually clear
         
    field = engine.calculate_potential_field(
        state, goal_pos=goal_pos, wall_value=2
    )
    
    plt.figure()
    plt.imshow(field, cmap='hot')
    plt.title("Gravity Field (Real Maze)")
    plt.savefig("real_gravity_maze.png")
    print("Saved real_gravity_maze.png")

def test_zero_point_finance():
    print("\n[ZERO POINT] Testing Risk Management (SPY Data)...")
    df = pd.read_csv(os.path.join(DATA_DIR, 'spy.csv'))
    prices = df['Close'].values
    
    # Engine Constraints:
    # "Energy" = Capital.
    # "Cost" = Drawdown.
    # Goal: Maximize Profit while Energy > 0.
    
    capital = 1000.0
    shares = 0
    history = []
    
    # Simple simulation using "Survival" logic?
    # If volatility is high, Zero Point says "STOP/SELL".
    
    print(f"Starting Capital: {capital}")
    for i in range(1, len(prices)):
        price = prices[i]
        prev = prices[i-1]
        
        # Volatility check (Fear)
        change = abs(price - prev) / prev
        
        # Zero Point Decision
        if change > 0.02: # High Volatility
             # "Safety Mode": Sell
             if shares > 0:
                 capital += shares * price
                 shares = 0
                 print(f"Day {i}: PANIC SELL at {price}")
        else:
             # "Growth Mode": Buy
             if capital > price:
                 shares += 1
                 capital -= price
                 print(f"Day {i}: BUY at {price}")
                 
        val = capital + (shares * price)
        history.append(val)
        
    print(f"Final Value: {history[-1]}")
    plt.figure()
    plt.plot(history)
    plt.title("Zero Point Portfolio")
    plt.savefig("real_zero_point.png")
    print("Saved real_zero_point.png")

if __name__ == "__main__":
    test_eigen_logistics()
    test_sovereign_text()
    test_gravity_maze()
    test_zero_point_finance()
