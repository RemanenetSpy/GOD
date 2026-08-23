"""
Test Safe Integration of Zero-Point Engine

Verifies that:
1. Agent can serve as host for Zero-Point Engine
2. Old "Concept" engine is preserved
3. Switching works via 'engine_type' flag
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from agent import Agent
from zero_point_engine import ZeroPointEngine
from sovereign_engine import UniversalSovereignEngine

def test_switching():
    print("TEST: Engine Switching")
    
    # 1. Test Default (Sovereign)
    agent_classic = Agent(agent_id="CLASSIC_001")
    assert isinstance(agent_classic.sovereign_engine, UniversalSovereignEngine)
    print("✅ Default Agent uses Sovereign Engine (Phase 1 preserved)")
    
    # 2. Test Zero-Point
    agent_zero = Agent(agent_id="ZERO_001", engine_type="zero_point")
    assert isinstance(agent_zero.sovereign_engine, ZeroPointEngine)
    print("✅ Zero-Point Agent uses ZeroPointEngine (Phase 2 enabled)")
    
    # 3. Verify Independence
    print(f"Classic Engine: {type(agent_classic.sovereign_engine).__name__}")
    print(f"Zero Engine:    {type(agent_zero.sovereign_engine).__name__}")

def test_zero_point_operation():
    print("\nTEST: Zero-Point Operation inside Agent")
    agent = Agent(agent_id="ZERO_TEST", engine_type="zero_point")
    
    # Simulate update cycle
    print("Simulating 100 steps of survival...")
    for i in range(100):
        # Fake observation (random noise)
        import numpy as np
        obs = np.random.randint(0, 5, (10, 10))
        
        # Agent cycle
        # We manually trigger engine update via private method for unit testing
        agent.sovereign_engine.update(obs, "WAIT", 0.0)
        
    dashboard = agent.sovereign_engine.get_dashboard()
    print("Dashboard after 100 steps:")
    for k, v in dashboard.items():
        print(f"  {k}: {v}")
        
    assert dashboard['energy'] != 100.0  # Energy should have changed
    print("✅ Zero-Point Engine is ALIVE inside Agent")

if __name__ == "__main__":
    print("="*60)
    print("PLUG-AND-PLAY ARCHITECTURE VERIFICATION")
    print("="*60)
    test_switching()
    test_zero_point_operation()
    print("\nALL SYSTEMS GREEN.")
