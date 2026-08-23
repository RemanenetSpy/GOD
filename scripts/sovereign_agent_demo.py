"""
Phase 21: Sovereign Agent & Harmonization Demo
Verifies that:
1. Agents have separate, sovereign vocabularies.
2. Agents can autonomously harmonize (merge) their own concepts.
"""

import sys
import os
import shutil
import numpy as np

import sys
import os
import shutil
import numpy as np

# Add src to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir) # GOD root
src_dir = os.path.join(parent_dir, 'src')
sys.path.append(src_dir)

from agent import Agent
from core import PillarType

# Cleanup previous test files
for f in os.listdir("."):
    if f.startswith("vocab_demo") or f.startswith("memory_demo"):
        try:
            os.remove(f)
        except:
            pass

print("=== Phase 21: Sovereign Agent Verification ===")

# 1. Initialize Two Sovereign Agents
print("\n[PART 1] Initializing Sovereign Agents...")
agent_quantum = Agent(agent_id="demo_Quantum", specialization=PillarType.QUANTUM)
agent_physics = Agent(agent_id="demo_Physics", specialization=PillarType.PHYSICS)

print(f"Agent Quantum Vocab File: {agent_quantum.sovereign_vocab.persistence_file}")
print(f"Agent Physics Vocab File: {agent_physics.sovereign_vocab.persistence_file}")

# 2. Simulate Divergent Experiences
print("\n[PART 2] Simulating Divergent Learning...")

# Quantum sees a Red Square (Color 2)
motif_red_square = {
    'type': 'rectangle',
    'bbox': (0,0,2,2),
    'color': 2
}
agent_quantum.sovereign_vocab.add_motif("rect_2x2_c2", motif_red_square, "task_A")

# Physics sees a Blue Square (Color 1)
motif_blue_square = {
    'type': 'rectangle',
    'bbox': (0,0,2,2),
    'color': 1
}
agent_physics.sovereign_vocab.add_motif("rect_2x2_c1", motif_blue_square, "task_B")

# Verify Isolation
quantum_keys = list(agent_quantum.sovereign_vocab.vocabulary.keys())
physics_keys = list(agent_physics.sovereign_vocab.vocabulary.keys())

print(f"Quantum knows: {quantum_keys}")
print(f"Physics knows: {physics_keys}")

if "rect_2x2_c1" not in quantum_keys and "rect_2x2_c2" in quantum_keys:
    print("✅ SUCCESS: Memories are isolated.")
else:
    print("❌ FAILURE: Memories leaked!")

# 3. Autonomous Harmonization Test
print("\n[PART 3] Testing Autonomous Harmonization...")

# Give Quantum more experience - tell it about Blue and Green squares too
agent_quantum.sovereign_vocab.add_motif("rect_2x2_c1", motif_blue_square, "task_B")
agent_quantum.sovereign_vocab.add_motif("rect_2x2_c3", {
    'type': 'rectangle', 'bbox': (0,0,2,2), 'color': 3
}, "task_C")

print(f"Quantum before harmonization: {list(agent_quantum.sovereign_vocab.vocabulary.keys())}")

# Trigger Harmonization Cycle (The 'Sleep' Cycle)
agent_quantum.sovereign_vocab.harmonize()

quantum_keys_post = list(agent_quantum.sovereign_vocab.vocabulary.keys())
print(f"Quantum after harmonization: {quantum_keys_post}")

if "rect_2x2" in quantum_keys_post:
    print("✅ SUCCESS: Agent autonomously merged concepts into 'rect_2x2'.")
    # Verify definition is generic
    generic_def = agent_quantum.sovereign_vocab.vocabulary["rect_2x2"].definition
    print(f"Generic Definition Color: {generic_def.get('color')}") # Should be -1
else:
    print("❌ FAILURE: Harmonization did not create generic concept.")

print("\n=== Demo Complete ===")
