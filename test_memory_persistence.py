"""
Test Memory Persistence - Verify agents can learn across episodes
"""
from src.agent import Agent
from src.core import PillarType
from src.pacman_env import PacManWorld

print("="*60)
print("MEMORY PERSISTENCE TEST")
print("="*60)

# Episode 1: Learn something
print("\n📚 Episode 1: Learning...")
agent1 = Agent(agent_id="test", grid_size=15, use_memory=True, specialization=PillarType.QUANTUM)
agent1.load_memory(999)  # Initialize for seed 999
env = PacManWorld(size=15, seed=999)

obs = env.observe()
for i in range(50):
    action, state = agent1.act(obs)
    obs, reward, done = env.step(action)
    if done:
        break

patterns_ep1 = len(agent1.state.world_model.patterns)
rules_ep1 = len(agent1.state.world_model.rules)
print(f"   Patterns learned: {patterns_ep1}")
print(f"   Rules learned: {rules_ep1}")
print(f"   Score: {env.score}")

# Save memory
agent1.save_memory(episode_score=env.score, episode_steps=i)
print("   💾 Memory saved!")

# Episode 2: Load and verify
print("\n📖 Episode 2: Loading memory...")
agent2 = Agent(agent_id="test2", grid_size=15, use_memory=True, specialization=PillarType.QUANTUM)
loaded = agent2.load_memory(999)

patterns_ep2 = len(agent2.state.world_model.patterns)
rules_ep2 = len(agent2.state.world_model.rules)

print(f"   Memory loaded: {loaded}")
print(f"   Patterns loaded: {patterns_ep2}")
print(f"   Rules loaded: {rules_ep2}")

# Verification
print("\n🔍 Verification:")
if patterns_ep2 == patterns_ep1:
    print(f"   ✅ Patterns persisted correctly ({patterns_ep2} == {patterns_ep1})")
else:
    print(f"   ❌ Patterns NOT persisted ({patterns_ep2} != {patterns_ep1})")

if rules_ep2 == rules_ep1:
    print(f"   ✅ Rules persisted correctly ({rules_ep2} == {rules_ep1})")
else:
    print(f"   ❌ Rules NOT persisted ({rules_ep2} != {rules_ep1})")

# Run episode 2 to see if it performs better
env2 = PacManWorld(size=15, seed=999)
obs2 = env2.observe()
for j in range(50):
    action, state = agent2.act(obs2)
    obs2, reward, done = env2.step(action)
    if done:
        break

print(f"\n📊 Performance Comparison:")
print(f"   Episode 1 Score: {env.score}")
print(f"   Episode 2 Score: {env2.score}")

if env2.score >= env.score:
    print(f"   ✅ Agent maintained or improved performance!")
else:
    print(f"   ⚠️  Agent performed worse (but memory is loading)")

print("\n" + "="*60)
print("TEST COMPLETE")
print("="*60)
