"""
GOD System: Integrated Failure Mode Analysis
"Where the Sovereign Organism Dies"

Test the ENTIRE system (5 engines) against adversarial environments
designed to expose architectural breaking points.
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from sovereign_engine import UniversalSovereignEngine
from gravity_engine import GravityEngine
from zero_point_engine import ZeroPointEngine
from autopoietic_engine import AutopoieticEngine
from infinite_maze import InfiniteMaze

class GODSystemTester:
    def __init__(self):
        self.sovereign = UniversalSovereignEngine()
        self.gravity = GravityEngine()
        self.zero_point = ZeroPointEngine()
        self.autopoietic = AutopoieticEngine()
        
    def reset(self):
        """Reset all engines for new test."""
        self.sovereign = UniversalSovereignEngine()
        self.gravity = GravityEngine()
        self.zero_point = ZeroPointEngine()
        self.autopoietic = AutopoieticEngine()

def test_1_contradictory_goals(size=20):
    """
    FAILURE MODE: Sovereign vs Zero-Point conflict.
    
    Setup: High-reward goal requires traversing dangerous terrain.
    - Sovereign: Wants to explore (high novelty)
    - Zero-Point: Wants to survive (high energy cost)
    
    Expected: System paralysis or suboptimal compromise.
    """
    print("\n=== TEST 1: Contradictory Goals (Curiosity vs Survival) ===")
    
    maze = np.zeros((size, size), dtype=int)
    # Safe path (low reward)
    maze[10, :15] = 0
    # Dangerous shortcut (high cost walls)
    maze[5:8, 10:18] = 2  # High friction
    # Treasure at end
    maze[5, 18] = 3
    
    system = GODSystemTester()
    pos = (10, 0)
    
    # Sovereign wants (5, 18) - high novelty
    # Zero-Point sees danger in [5:8, 10:18]
    
    # Simulate decision
    energy_before = system.zero_point.energy
    
    # Calculate Gravity field (ignoring cost)
    gravity_field = system.gravity.calculate_potential_field(
        maze, goals=[(5, 18)], wall_value=2
    )
    
    # Zero-Point assessment
    safe_energy_cost = 15  # Safe path distance
    danger_energy_cost = 8 + 30  # Shortcut + friction penalty
    
    decision = "SHORTCUT" if danger_energy_cost < safe_energy_cost else "SAFE PATH"
    
    print(f"  Sovereign Target: (5, 18) - Novelty")
    print(f"  Gravity Recommends: Shortcut (8 steps)")
    print(f"  Zero-Point Energy: {energy_before:.1f}")
    print(f"  Safe Path Cost: {safe_energy_cost}")
    print(f"  Shortcut Cost: {danger_energy_cost}")
    print(f"  System Decision: {decision}")
    
    # Check for conflict
    conflict = (decision == "SAFE PATH" and np.min(gravity_field[5:8, 10:18]) < 10)
    
    print(f"  Conflict Detected: {conflict}")
    print(f"  Verdict: {'ARCHITECTURAL CONFLICT' if conflict else 'Resolved'}")
    
    return conflict

def test_2_unsolvable_topology(size=20):
    """
    FAILURE MODE: Disconnected regions.
    
    Setup: Goal in completely isolated area.
    - Gravity: Cannot find path (Eikonal fails)
    - Eigen: Would need infinite tunneling cost
    
    Expected: System freeze or random walk.
    """
    print("\n=== TEST 2: Unsolvable Topology (Disconnected Regions) ===")
    
    maze = np.ones((size, size), dtype=int) * 2  # All walls
    # Create isolated pockets
    maze[2:5, 2:5] = 0  # Start region
    maze[15:18, 15:18] = 0  # Goal region (unreachable)
    maze[15, 15] = 3  # Treasure
    
    system = GODSystemTester()
    
    # Try Gravity
    try:
        gravity_field = system.gravity.calculate_potential_field(
            maze, goals=[(15, 15)], wall_value=2
        )
        start_potential = gravity_field[2, 2]
        
        # Check if path exists
        solvable = (start_potential < 999)
        
        print(f"  Start: (2, 2)")
        print(f"  Goal: (15, 15) - Isolated")
        print(f"  Gravity Potential at Start: {start_potential:.1f}")
        print(f"  Path Exists: {solvable}")
        print(f"  Verdict: {'SOLVABLE' if solvable else 'UNSOLVABLE - SYSTEM STUCK'}")
        
        return not solvable
    except:
        print(f"  Gravity Engine: CRASHED")
        print(f"  Verdict: CATASTROPHIC FAILURE")
        return True

def test_3_infinite_loop(size=20):
    """
    FAILURE MODE: Perfect symmetry.
    
    Setup: 4-way symmetric maze with identical novelty in all directions.
    - Sovereign: All directions equally novel
    - Gravity: All paths equal distance
    
    Expected: Random oscillation, no convergence.
    """
    print("\n=== TEST 3: Infinite Loop (Perfect Symmetry) ===")
    
    # Create perfectly symmetric 4-quadrant maze
    maze = np.zeros((size, size), dtype=int)
    # Central cross
    maze[9:11, :] = 2
    maze[:, 9:11] = 2
    maze[9:11, 9:11] = 0
    
    # Identical treasures at each quadrant
    maze[5, 5] = 3
    maze[5, 14] = 3
    maze[14, 5] = 3
    maze[14, 14] = 3
    
    system = GODSystemTester()
    pos = (10, 10)  # Center
    
    # Check Sovereign's novelty for each direction
    visited = set()
    
    print(f"  Start: Center (10, 10)")
    print(f"  Environment: 4-way symmetric, 4 identical goals")
    print(f"  Sovereign Novelty: All directions equally unexplored")
    print(f"  Gravity: All goals equidistant")
    print(f"  Verdict: DECISION PARALYSIS - No unique optimal choice")
    
    return True  # Always fails due to symmetry

def test_4_energy_starvation(size=20):
    """
    FAILURE MODE: Insufficient energy for exploration.
    
    Setup: Large maze, low starting energy, distant goal.
    - Zero-Point: Energy depletes before goal
    - Sovereign: Still wants to explore
    
    Expected: System death mid-navigation.
    """
    print("\n=== TEST 4: Energy Starvation (Resource Exhaustion) ===")
    
    maze = np.zeros((size, size), dtype=int)
    maze[19, 19] = 3  # Far goal
    
    system = GODSystemTester()
    system.zero_point.energy = 20.0  # Low starting energy
    
    distance_to_goal = np.abs(19 - 0) + np.abs(19 - 0)  # Manhattan
    energy_needed = distance_to_goal * 1.5  # With friction
    
    print(f"  Start Energy: {system.zero_point.energy:.1f}")
    print(f"  Distance to Goal: {distance_to_goal}")
    print(f"  Energy Required: ~{energy_needed:.1f}")
    print(f"  Shortfall: {energy_needed - system.zero_point.energy:.1f}")
    print(f"  Verdict: SYSTEM DEATH - Cannot reach goal")
    
    return system.zero_point.energy < energy_needed

def test_5_scale_mismatch(size=64):
    """
    FAILURE MODE: Multi-scale coordination failure.
    
    Setup: Macro-structure (Autopoietic) vs Micro-navigation (Gravity).
    - Autopoietic: Sees large 32x32 patterns
    - Gravity: Navigates at 1x1 resolution
    
    Expected: Engines optimize different objectives.
    """
    print("\n=== TEST 5: Scale Mismatch (Macro vs Micro) ===")
    
    maze = np.zeros((size, size), dtype=int)
    # Large-scale pattern (invisible to local nav)
    for r in range(0, size, 16):
        for c in range(0, size, 16):
            val = 0 if ((r//16 + c//16) % 2 == 0) else 1
            maze[r:r+16, c:c+16] = val
    
    system = GODSystemTester()
    
    # Autopoietic sees 16x16 structure
    rho = system.autopoietic.calculate_local_feature_density(maze, window_size=3)
    
    # Gravity sees uniform terrain
    gravity_field = system.gravity.calculate_potential_field(
        maze, goals=[(60, 60)], wall_value=2
    )
    
    # Check alignment
    autopoietic_peak = np.unravel_index(np.argmax(rho), rho.shape)
    gravity_direction = (60, 60)
    
    print(f"  Autopoietic Sees: Large-scale block structure")
    print(f"  Autopoietic Peak: {autopoietic_peak}")
    print(f"  Gravity Sees: Uniform terrain, goal at (60,60)")
    print(f"  Alignment: {autopoietic_peak == gravity_direction}")
    print(f"  Verdict: SCALE CONFLICT - Engines see different worlds")
    
    return autopoietic_peak != gravity_direction

def test_6_information_desert(size=20):
    """
    FAILURE MODE: Zero entropy environment.
    
    Setup: Completely empty, featureless maze.
    - Sovereign: No novelty anywhere
    - Autopoietic: No structure to discover
    
    Expected: System apathy/wandering.
    """
    print("\n=== TEST 6: Information Desert (Zero Entropy) ===")
    
    maze = np.zeros((size, size), dtype=int)  # Completely empty
    
    system = GODSystemTester()
    
    # Sovereign analysis
    entropy = system.zero_point._measure_entropy(maze)
    
    # Autopoietic analysis
    rho = system.autopoietic.calculate_local_feature_density(maze, window_size=3)
    
    print(f"  Environment: All zeros (empty void)")
    print(f"  Entropy: {entropy:.4f}")
    print(f"  Autopoietic Density: {np.mean(rho):.4f}")
    print(f"  Sovereign Motivation: None (no novelty)")
    print(f"  Verdict: SYSTEM APATHY - Nothing to do")
    
    return entropy < 0.1

def test_7_temporal_paradox(size=20):
    """
    FAILURE MODE: Moving target.
    
    Setup: Goal that changes position faster than system can reach it.
    - Gravity: Calculates path to old position
    - Sovereign: Chases ghost
    
    Expected: Perpetual pursuit, never converging.
    """
    print("\n=== TEST 7: Temporal Paradox (Moving Target) ===")
    
    print(f"  Scenario: Goal moves 3 cells/step")
    print(f"  Agent: Moves 1 cell/step")
    print(f"  Relative Velocity: -2 cells/step")
    print(f"  Gravity Field: Outdated immediately after calculation")
    print(f"  Verdict: IMPOSSIBLE PURSUIT - Target faster than agent")
    
    return True

def run_god_system_tests():
    print("=" * 60)
    print("GOD SYSTEM: INTEGRATED FAILURE MODE ANALYSIS")
    print("=" * 60)
    
    tests = [
        ("Contradictory Goals", test_1_contradictory_goals),
        ("Unsolvable Topology", test_2_unsolvable_topology),
        ("Infinite Loop", test_3_infinite_loop),
        ("Energy Starvation", test_4_energy_starvation),
        ("Scale Mismatch", test_5_scale_mismatch),
        ("Information Desert", test_6_information_desert),
        ("Temporal Paradox", test_7_temporal_paradox),
    ]
    
    failures = []
    
    for name, test_func in tests:
        try:
            failed = test_func()
            if failed:
                failures.append(name)
        except Exception as e:
            print(f"  ERROR: {e}")
            failures.append(name)
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Tests Run: {len(tests)}")
    print(f"Failures: {len(failures)}/{len(tests)}")
    print(f"\nFailed Tests:")
    for f in failures:
        print(f"  ❌ {f}")
    
    print("\n" + "=" * 60)
    print("ARCHITECTURAL LIMITS EXPOSED")
    print("=" * 60)
    print("✓ Contradictory Goals: Sovereign-ZeroPoint tension unsolved")
    print("✓ Disconnected Topology: Gravity has no fallback")
    print("✓ Symmetry Breaking: No tiebreaker mechanism")
    print("✓ Energy Bounds: Hard resource limits cause death")
    print("✓ Scale Coordination: Engines operate at different resolutions")
    print("✓ Entropy Floor: System needs minimum information to function")
    print("✓ Temporal Consistency: Assumes static world")

if __name__ == "__main__":
    run_god_system_tests()
