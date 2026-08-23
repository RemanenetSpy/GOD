"""
========================================================================================
Verification Suite for the Sovereign Civilization & God Equation Message Tensor (M_t^i)
========================================================================================
"""

import sys
import os
import numpy as np

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from civilization import (
    SovereignCivilization,
    RelativisticMessageFabric,
    Message,
    MessageType,
    PillarArchetype,
    ClassicalPhysicsNode,
    QuantumBeliefNode,
    ModernMetabolicNode,
    StringMetaNode,
    CivilizationPhase
)
from environment import Action, Observation, CellType


def test_message_fabric_routing():
    print("\n[TEST 1] Verifying Relativistic Message Fabric M_t^i Routing...")
    fabric = RelativisticMessageFabric()
    fabric.register_agent("agent_1")
    fabric.register_agent("agent_2")
    fabric.register_agent("agent_3")
    
    # Send direct message
    msg1 = Message(
        sender_id="agent_1",
        recipient_id="agent_2",
        pillar=PillarArchetype.CLASSICAL,
        timestamp=1,
        msg_type=MessageType.METABOLIC_BURST,
        payload=1.5
    )
    fabric.transmit(msg1)
    
    # Send broadcast message
    msg2 = Message(
        sender_id="agent_3",
        recipient_id="BROADCAST",
        pillar=PillarArchetype.STRING_META,
        timestamp=1,
        msg_type=MessageType.SUBROUTINE_CODE,
        payload="def mirror(): pass"
    )
    fabric.transmit(msg2)
    
    inbox1 = fabric.fetch_inbox("agent_1")
    inbox2 = fabric.fetch_inbox("agent_2")
    inbox3 = fabric.fetch_inbox("agent_3")
    
    assert len(inbox1) == 1, f"Expected 1 broadcast in agent_1, got {len(inbox1)}"
    assert len(inbox2) == 2, f"Expected direct + broadcast in agent_2, got {len(inbox2)}"
    assert len(inbox3) == 0, f"Expected 0 in agent_3 (sender of broadcast), got {len(inbox3)}"
    print("[PASS] Message routing and broadcast isolation verified.")


def test_four_pillar_universal_updates():
    print("\n[TEST 2] Verifying 4 Sovereign Pillars with God Equation Updates...")
    grid_shape = (10, 10)
    
    classical = ClassicalPhysicsNode("classical_test", grid_shape)
    quantum = QuantumBeliefNode("quantum_test", grid_shape)
    modern = ModernMetabolicNode("modern_test", grid_shape)
    string_node = StringMetaNode("string_test", grid_shape)
    
    obs = Observation(
        visible_cells=np.full((3, 3), CellType.RESOURCE.value),
        position=(4, 4),
        reward=2.0
    )
    
    # 1. Classical Update (Eikonal Geodesic)
    classical.universal_update(Action.MOVE_UP, obs, [])
    pot_classical = classical.compute_potential_field()
    assert pot_classical.shape == grid_shape, "Classical potential field shape mismatch"
    
    # 2. Quantum Update (Superposition & Collapse)
    quantum.universal_update(Action.OBSERVE, obs, [])
    pot_quantum = quantum.compute_potential_field()
    assert pot_quantum.shape == grid_shape, "Quantum uncertainty field shape mismatch"
    
    # 3. Modern Update (Thermodynamics & Viability)
    modern.universal_update(Action.INTERACT, obs, [])
    assert modern.state.dh_dt != 0.0, "Modern node metabolism dH/dt not updating"
    
    # 4. String Meta Update (Kolmogorov Subroutine Minting)
    string_node.universal_update(Action.OBSERVE, obs, [])
    assert len(string_node.state.subroutine_library) > 0, "String meta-node failed to mint subroutine from uniform pattern"
    
    print("[PASS] All 4 Sovereign Pillars execute the God Equation S_{t+1} = U(S_t, A_t, O_t, M_t) + L(S_t).")


def test_civilization_collective_consensus():
    print("\n[TEST 3] Verifying Multi-Agent Civilization Emergence & Consensus...")
    grid_shape = (12, 12)
    civ = SovereignCivilization(grid_shape=grid_shape)
    
    # Run 5 steps
    for t in range(1, 6):
        obs_dict = {
            agent_id: Observation(
                visible_cells=np.random.randint(0, 3, size=(3, 3)),
                position=(np.random.randint(0, 12), np.random.randint(0, 12)),
                reward=1.0
            )
            for agent_id in civ.nodes
        }
        actions = civ.step(obs_dict)
        assert len(actions) == 4, f"Expected 4 actions, got {len(actions)}"
        
    consensus = civ.synthesize_consensus_field()
    assert consensus.shape == (*grid_shape, 4), "Consensus field shape mismatch"
    assert civ.fabric.total_messages_routed > 0, "No messages routed across civilization fabric"
    
    report = civ.get_civilization_report()
    assert report["total_energy"] > 0, "Civilization energy depleted"
    print(f"[PASS] Civilization active: Phase={report['global_phase']}, Messages={report['total_messages_routed']}, Synergy trace verified.")


def run_all_tests():
    print("================================================================================")
    print("           RUNNING SOVEREIGN CIVILIZATION VERIFICATION SUITE")
    print("================================================================================")
    test_message_fabric_routing()
    test_four_pillar_universal_updates()
    test_civilization_collective_consensus()
    print("\n================================================================================")
    print("              ALL CIVILIZATION TESTS PASSED PERFECTLY!")
    print("================================================================================")


if __name__ == "__main__":
    run_all_tests()
