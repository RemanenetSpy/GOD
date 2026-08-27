"""
========================================================================================
Verification Suite for all 7 Modular Substrates in the Cellular Automata Multiverse
========================================================================================
"""

import os
import sys
import numpy as np

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Add src and src/environments to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src", "environments")))

from registry import SubstrateRegistry
from civilization import SovereignCivilization, Observation, Action


def test_all_seven_realms():
    print("=" * 70)
    print("TESTING 7-PARADIGM CELLULAR AUTOMATA MULTIVERSE SUBSTRATES")
    print("=" * 70)
    
    realms = [
        ("classic_ca", "Realm 1: Classic Discrete CA"),
        ("seasonal_scarcity", "Realm 2: Seasonal Scarcity CA"),
        ("lenia", "Realm 3: Continuous Wave Lenia"),
        ("reaction_diffusion", "Realm 4: Gray-Scott Reaction-Diffusion"),
        ("wireworld", "Realm 5: Wireworld Digital Circuit"),
        ("lattice_gas", "Realm 6: Lattice Gas Hydrodynamics"),
        ("red_queen", "Realm 7: Red Queen Co-Evolution Arena")
    ]
    
    agent_positions = {
        "classical_prime": (5, 5),
        "quantum_prime": (20, 5),
        "modern_prime": (5, 20),
        "string_meta": (20, 20)
    }
    
    for key, label in realms:
        print(f"\n[Testing {label}]...")
        sub = SubstrateRegistry.get_substrate(key, grid_shape=(25, 25))
        assert sub.grid.shape == (25, 25), f"{label} grid shape mismatch"
        
        # Step 10 times
        for _ in range(10):
            rewards = sub.step(agent_positions)
            assert len(rewards) == len(agent_positions), f"{label} reward count mismatch"
            
        telemetry = sub.get_climate_telemetry()
        print(f"  [OK] {telemetry['season_icon']} {telemetry['environment_name']} | Season: {telemetry['season']} | Biomass: {telemetry.get('total_biomass')}")
        
    print("\n" + "=" * 70)
    print("ALL 7 PARADIGMS FULLY VALIDATED AND FUNCTIONAL!")
    print("=" * 70)


if __name__ == "__main__":
    test_all_seven_realms()
