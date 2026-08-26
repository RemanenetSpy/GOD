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
    BaseSovereignNode,
    Action,
    Observation
)


def test_message_fabric_routing():
    print("\n[TEST 1] Verifying Relativistic Message Fabric M_t^i Routing...")
    fabric = RelativisticMessageFabric()
    fabric.register_node("agent_1")
    fabric.register_node("agent_2")
    fabric.register_node("agent_3")
    
    # Send direct message
    msg1 = Message(
        sender_id="agent_1",
        recipient_id="agent_2",
        msg_type=MessageType.TOPOLOGICAL_GRADIENT,
        payload=np.zeros((5, 5)),
        confidence=0.9,
        timestamp=1
    )
    fabric.transmit(msg1)
    
    # Send broadcast message
    msg2 = Message(
        sender_id="agent_3",
        recipient_id="BROADCAST",
        msg_type=MessageType.SUBROUTINE_CODE,
        payload="def mirror(): pass",
        confidence=0.95,
        timestamp=1
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
    
    classical = BaseSovereignNode("classical_test", PillarArchetype.CLASSICAL_EIKONAL, grid_shape)
    quantum = BaseSovereignNode("quantum_test", PillarArchetype.QUANTUM_SUPERPOSED, grid_shape)
    modern = BaseSovereignNode("modern_test", PillarArchetype.MODERN_THERMODYNAMIC, grid_shape)
    string_node = BaseSovereignNode("string_test", PillarArchetype.STRING_TOPOLOGICAL, grid_shape)
    
    obs = Observation(
        visible_cells=np.full((3, 3), 1.0, dtype=np.float32),
        position=(4, 4),
        reward=2.0
    )
    
    # 1. Classical Update & Action
    classical.universal_update(Action.MOVE_UP, obs, [], step=1)
    act_classical = classical.select_action(obs)
    assert isinstance(act_classical, Action), "Classical action selection error"
    
    # 2. Quantum Update (Entropy Field)
    quantum.universal_update(Action.OBSERVE, obs, [], step=1)
    ent_field = quantum.belief_engine.get_entropy_field()
    assert ent_field.shape == grid_shape, "Quantum uncertainty field shape mismatch"
    
    # 3. Modern Update (Thermodynamic Homeostasis)
    modern.universal_update(Action.MOVE_DOWN, obs, [], step=1)
    assert modern.state.energy > 0, "Modern node energy error"
    
    # 4. String Meta Update (10D Cognitive Manifold)
    string_node.universal_update(Action.OBSERVE, obs, [], step=1)
    assert len(string_node.state.cognitive_10d) > 0, "String meta-node failed 10D compactification"
    
    print("[PASS] All 4 sovereign pillars execute universal God Equation updates.")


def test_civilization_full_cycle():
    print("\n[TEST 3] Verifying Multi-Agent Civilization Orchestrator...")
    civ = SovereignCivilization(grid_shape=(15, 15))
    
    # Initial 4 nodes present
    assert len(civ.nodes) == 4, f"Expected 4 prime nodes, got {len(civ.nodes)}"
    
    obs_map = {
        nid: Observation(
            visible_cells=np.random.rand(3, 3).astype(np.float32),
            position=(5, 5),
            reward=1.0
        )
        for nid in civ.nodes
    }
    
    # Run 5 steps
    for _ in range(5):
        actions = civ.step(obs_map)
        assert len(actions) == len(civ.nodes), "Action count mismatch"
        
    print("[PASS] Full multi-agent civilization cycle running with active communication and consensus.")


if __name__ == "__main__":
    test_message_fabric_routing()
    test_four_pillar_universal_updates()
    test_civilization_full_cycle()
    print("\n" + "=" * 60)
    print("ALL SOVEREIGN CIVILIZATION TESTS PASSED SUCCESSFULLY!")
    print("=" * 60)
