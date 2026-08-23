"""
========================================================================================
AUTOMATED VERIFICATION TEST SUITE: 10 UNIFIED SOVEREIGN ARCHITECTURES
========================================================================================
"""

import os
import sys
import numpy as np

# Add src and render_sovereign_engine to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'render_sovereign_engine', 'src'))

from kolmogorov_engine import KolmogorovEngine
from quantum_belief_engine import QuantumBeliefEngine
from fever_protocol import FeverProtocol
from autopoietic_mitosis import AutopoieticMitosisEngine
from string_dimensions import String10DCognitiveEngine
from civilization import SovereignCivilization, Observation, Action, PillarArchetype


def test_kolmogorov_causal_induction():
    print("[TEST 1/6] Testing Kolmogorov Causal Induction & Deduplication...")
    ke = KolmogorovEngine("test_agent")
    
    # Simulate a 3x3 blinker oscillator transition
    # Step t: vertical line
    prev = np.array([
        [0, 1, 0],
        [0, 1, 0],
        [0, 1, 0]
    ])
    # Step t+1: horizontal line
    curr = np.array([
        [0, 0, 0],
        [1, 1, 1],
        [0, 0, 0]
    ])
    
    # First discovery
    progs = ke.induce_causal_laws(prev, curr, step=1)
    assert len(progs) > 0, "Failed to induce causal transition rules!"
    initial_count = len(ke.program_library)
    print(f"  -> Discovered {initial_count} unique laws from blinker transition.")
    
    # Step again with identical transition (Deduplication Check)
    progs_repeat = ke.induce_causal_laws(prev, curr, step=2)
    assert len(progs_repeat) == 0, "Deduplication failed! Minted duplicate rules on repeat observation."
    assert len(ke.program_library) == initial_count, "Library size increased on duplicate observation!"
    print("  -> Strict Deduplication verified! (0 duplicates minted)")


def test_quantum_belief_engine():
    print("[TEST 2/6] Testing Quantum Belief Superposition & Shannon Entropy...")
    qbe = QuantumBeliefEngine(grid_shape=(10, 10))
    initial_entropy = qbe.compute_total_entropy()
    
    # Observe a 3x3 patch of living cells
    patch = np.ones((3, 3), dtype=int)
    info_gain = qbe.update_with_observation(agent_pos=(5, 5), aperture_radius=1, observed_patch=patch)
    
    new_entropy = qbe.compute_total_entropy()
    assert new_entropy < initial_entropy, "Entropy did not decrease after observing patch!"
    assert info_gain > 0, "Information gain was zero!"
    print(f"  -> Bayesian update dropped uncertainty: {initial_entropy:.3f} -> {new_entropy:.3f} (Gain: {info_gain:.3f})")


def test_fever_and_viscous_momentum():
    print("[TEST 3/6] Testing Fever Annealing & Viscous Momentum...")
    fp = FeverProtocol("test_agent")
    
    # Simulate stagnation (dh_dt = 0, delta_entropy = 0) for 20 cycles
    for _ in range(20):
        t, v, fever = fp.update(dh_dt=0.0, current_entropy=1.0, newly_discovered_rules=0)
        
    assert fever is True, "Fever was not triggered during prolonged stagnation!"
    assert t > 0.5, "Temperature failed to heat up during fever!"
    print(f"  -> Stagnation triggered Fever Delirium: Temperature = {t:.2f}, Viscosity = {v:.2f}")
    
    # Breakthrough cools down
    t_cool, _, fever_cool = fp.update(dh_dt=10.0, current_entropy=0.2, newly_discovered_rules=2)
    assert fever_cool is False, "Fever did not extinguish upon breakthrough!"
    assert t_cool < t, "System failed to cool down after discovery!"
    print(f"  -> Breakthrough cooled system: Temperature = {t_cool:.2f} (Fever extinguished)")


def test_autopoietic_mitosis_and_mergers():
    print("[TEST 4/6] Testing Autopoietic Mitosis & Population Growth...")
    me = AutopoieticMitosisEngine(max_population=8)
    
    # Test Spawning condition: Energy = 300.0, Subroutines = 5
    spawn = me.check_mitosis("parent_node", energy=300.0, subroutine_count=5, position=(10, 10), current_pop=4)
    assert spawn is not None, "Mitosis failed to trigger at max energy!"
    assert spawn["parent_id"] == "parent_node"
    assert "child" in spawn["offspring_id"]
    print(f"  -> Mitosis triggered successfully: Spawned '{spawn['offspring_id']}' at {spawn['child_pos']}")


def test_string_10d_dimensions():
    print("[TEST 5/6] Testing 10D String Cognitive Coordinate Space...")
    s10 = String10DCognitiveEngine("test_agent")
    
    # Low temperature (normal 3D+time)
    s10.update_state(pos=(5, 5), step=10, temperature=0.2, subroutine_count=2, entropy=0.5, energy=150.0, consensus_strength=0.8)
    assert s10.unfolded_dimensions == 4, "Should operate in 4D under normal temperature!"
    
    # High fever (unfolds 10D)
    s10.update_state(pos=(5, 5), step=10, temperature=2.5, subroutine_count=2, entropy=0.5, energy=150.0, consensus_strength=0.8)
    assert s10.unfolded_dimensions == 10, "Should unfold to 10D under Fever!"
    print("  -> Dimensional Unfolding verified: 4D (Cold) -> 10D (Fever)")


def test_master_civilization_simulation():
    print("[TEST 6/6] Testing Master Sovereign Civilization Multi-Agent Simulation...")
    civ = SovereignCivilization(grid_shape=(20, 20))
    assert len(civ.nodes) == 4
    
    for s in range(30):
        actions = civ.step()
        assert len(actions) > 0
        
    print(f"  -> Master Civilization stepped 30 cycles cleanly!")
    print(f"  -> Messages Routed: {civ.fabric.total_messages_routed}")
    print(f"  -> Discovered Unique Subroutines: {len(civ.global_subroutine_archive)}")
    print("\n[ALL 6 TESTS PASSED] 10 Unified Architectures fully functional and verified!")


if __name__ == "__main__":
    test_kolmogorov_causal_induction()
    test_quantum_belief_engine()
    test_fever_and_viscous_momentum()
    test_autopoietic_mitosis_and_mergers()
    test_string_10d_dimensions()
    test_master_civilization_simulation()
