"""
Quick test of Sovereign Engine integration
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from agent import Agent
from core import PillarType
from environment import Observation, Action
import numpy as np

print("=" * 60)
print("Testing Sovereign Engine Integration")
print("=" * 60)

# Create agent with sovereign engine
agent = Agent(agent_id='test_sovereign', specialization=PillarType.QUANTUM)

print(f"\n✓ Agent initialized successfully")
print(f"  Pillar: {agent.specialization.name}")
print(f"  Has Sovereign Engine: {hasattr(agent, 'sovereign_engine')}")

# Get initial engine state
dashboard = agent.sovereign_engine.get_dashboard()
print(f"\n📊 Initial Engine State:")
print(f"  Σ (Filter Efficiency): {dashboard['sigma']:.3f}")
print(f"  Ω (Entropy): {dashboard['omega']:.3f}")
print(f"  Λ (Friction): {dashboard['lambda']:.3f}")
print(f"  Rv (Viability Ratio): {dashboard['viability_ratio']:.3f}")
print(f"  Prescribed Action: {dashboard['prescribed_action']}")

# Simulate a few updates
print(f"\n🔄 Simulating 10 update cycles...")
for i in range(10):
    # Create dummy observation
    obs = Observation(
        visible_cells=np.random.randint(0, 3, (5, 5)),
        position=(i, i),
        reward=np.random.randn() * 0.5,
        context=np.random.randint(0, 3, (5, 5))
    )
    
    # Update agent
    agent.universal_update(Action.WAIT, obs)
    
    if i % 3 == 0:
        dashboard = agent.sovereign_engine.get_dashboard()
        print(f"  Step {i}: Σ={dashboard['sigma']:.2f}, Ω={dashboard['omega']:.2f}, "
              f"Λ={dashboard['lambda']:.2f}, Rv={dashboard['viability_ratio']:.2f}, "
              f"Action={dashboard['prescribed_action']}")

# Final state
dashboard = agent.sovereign_engine.get_dashboard()
print(f"\n📊 Final Engine State:")
print(f"  Σ: {dashboard['sigma']:.3f}")
print(f"  Ω: {dashboard['omega']:.3f}")
print(f"  Λ: {dashboard['lambda']:.3f}")
print(f"  Rv: {dashboard['viability_ratio']:.3f}")
print(f"  Metabolism (dH/dt): {dashboard['metabolism']:.3f}")
print(f"  Prescribed Action: {dashboard['prescribed_action']}")
print(f"  Diagnostic: {dashboard['diagnostic']}")

print(f"\n✅ Sovereign Engine Integration Test PASSED")
print("=" * 60)
