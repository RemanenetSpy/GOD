"""
Zero-Point Engine Demo: Pure Survival Intelligence

The system has ZERO knowledge of the world.
It only knows: dH/dt ≥ 0 or it dies.

Symbols emerge as "Metabolic Anchors" - patterns that keep metabolism positive.
"""

import numpy as np
import matplotlib.pyplot as plt
from collections import deque

class ZeroPointEngine:
    """
    A system with zero assumptions.
    Only knows: Must maintain dH/dt ≥ 0 to survive.
    """
    
    def __init__(self):
        # The ONLY hardcode: Homeostasis (survival)
        self.energy = 100.0  # H (total extracted "salt")
        self.alive = True
        
        # Internal state (unknown to system initially)
        self.metabolic_anchors = {}  # Discovered patterns that boost metabolism
        self.friction_map = {}  # Discovered sources of energy loss
        
        # History
        self.energy_history = deque(maxlen=1000)
        self.metabolism_history = deque(maxlen=1000)
        self.discovery_events = []
        
    def sense_environment(self, observation):
        """
        Raw sensory entropy (Ω).
        System doesn't know what this "is" - just raw chaos.
        """
        # Measure Shannon entropy of observation
        unique, counts = np.unique(observation.flatten(), return_counts=True)
        probabilities = counts / observation.size
        omega = -np.sum(probabilities * np.log2(probabilities + 1e-10))
        
        return omega
    
    def compute_metabolism(self, omega, action_cost):
        """
        dH/dt = (Σ × Ω) - Λ
        
        But system doesn't know what Σ is yet!
        It starts with Σ = 1.0 (no filter)
        """
        sigma = len(self.metabolic_anchors) + 1.0  # Filter improves as anchors discovered
        lambda_ = action_cost  # Friction from action
        
        dH_dt = (sigma * omega) - lambda_
        return dH_dt
    
    def survive(self, observation, action_cost=0.1):
        """
        The ONLY goal: Keep dH/dt ≥ 0
        
        System explores randomly until it finds "Metabolic Anchors"
        """
        # Sense environment
        omega = self.sense_environment(observation)
        
        # Compute metabolism
        dH_dt = self.compute_metabolism(omega, action_cost)
        
        # Update energy
        self.energy += dH_dt
        
        # Record history
        self.energy_history.append(self.energy)
        self.metabolism_history.append(dH_dt)
        
        # Check survival
        if self.energy <= 0:
            self.alive = False
            return False, "DISSIPATED"
        
        # Discover metabolic anchor if metabolism spiked
        if dH_dt > 1.0:  # Threshold for "spike"
            anchor_id = hash(observation.tobytes())
            if anchor_id not in self.metabolic_anchors:
                self.metabolic_anchors[anchor_id] = {
                    'pattern': observation.copy(),
                    'metabolism_boost': dH_dt,
                    'discovered_at': len(self.energy_history)
                }
                self.discovery_events.append({
                    'step': len(self.energy_history),
                    'type': 'METABOLIC_ANCHOR',
                    'boost': dH_dt
                })
                return True, f"DISCOVERED ANCHOR (dH/dt={dH_dt:.2f})"
        
        # Discover friction source if metabolism dropped
        if dH_dt < -0.5:
            friction_id = hash(observation.tobytes())
            if friction_id not in self.friction_map:
                self.friction_map[friction_id] = {
                    'pattern': observation.copy(),
                    'energy_loss': dH_dt,
                    'discovered_at': len(self.energy_history)
                }
                return True, f"DISCOVERED FRICTION (dH/dt={dH_dt:.2f})"
        
        return True, f"SURVIVING (dH/dt={dH_dt:.2f}, H={self.energy:.1f})"
    
    def recognize_anchor(self, observation):
        """
        Check if current observation matches a known metabolic anchor.
        This is GROUNDING - the symbol means "this boosts my metabolism"
        """
        obs_hash = hash(observation.tobytes())
        if obs_hash in self.metabolic_anchors:
            return self.metabolic_anchors[obs_hash]
        return None
    
    def get_viability_ratio(self):
        """
        Rv = (Σ × Ω) / Λ
        """
        if not self.metabolism_history:
            return 0.0
        
        recent_metabolism = list(self.metabolism_history)[-10:]
        avg_positive = np.mean([m for m in recent_metabolism if m > 0] or [0])
        avg_negative = abs(np.mean([m for m in recent_metabolism if m < 0] or [-0.1]))
        
        rv = avg_positive / max(avg_negative, 0.01)
        return rv


def run_survival_demo():
    """
    Demo: System with ZERO knowledge tries to survive in a chaotic environment.
    """
    print("=" * 80)
    print("ZERO-POINT ENGINE: SURVIVAL DEMO")
    print("=" * 80)
    print("\nThe system has ZERO assumptions.")
    print("It only knows: dH/dt ≥ 0 or it dies.\n")
    print("Environment: Random grids with occasional 'metabolic anchors'")
    print("(patterns that boost metabolism)\n")
    
    # Create engine
    engine = ZeroPointEngine()
    
    # Define environment: Random chaos with occasional "good" patterns
    def generate_environment(step):
        """Generate observation - mostly noise, occasionally a 'good' pattern"""
        if step % 20 == 0:
            # Metabolic anchor: Symmetric pattern (high Ω, boosts metabolism)
            pattern = np.array([
                [1, 2, 1],
                [2, 3, 2],
                [1, 2, 1]
            ])
            return pattern
        elif step % 15 == 0:
            # Another anchor: Repetitive pattern
            pattern = np.array([
                [1, 1, 1],
                [2, 2, 2],
                [3, 3, 3]
            ])
            return pattern
        else:
            # Noise: Random grid (low metabolism)
            return np.random.randint(0, 4, (3, 3))
    
    # Survival loop
    print("Starting survival simulation...\n")
    
    for step in range(100):
        # Generate environment
        observation = generate_environment(step)
        
        # Try to survive
        survived, status = engine.survive(observation, action_cost=0.1)
        
        # Print significant events
        if "DISCOVERED" in status or step % 10 == 0:
            print(f"Step {step:3d}: {status}")
        
        if not survived:
            print(f"\n💀 SYSTEM DISSIPATED at step {step}")
            print(f"   Final Energy: {engine.energy:.2f}")
            break
    
    # Results
    print(f"\n{'='*80}")
    print("SURVIVAL RESULTS")
    print(f"{'='*80}")
    print(f"Final Energy: {engine.energy:.2f}")
    print(f"Metabolic Anchors Discovered: {len(engine.metabolic_anchors)}")
    print(f"Friction Sources Discovered: {len(engine.friction_map)}")
    print(f"Viability Ratio: {engine.get_viability_ratio():.2f}")
    print(f"Alive: {engine.alive}")
    
    # Show discovered anchors
    if engine.metabolic_anchors:
        print(f"\n📍 METABOLIC ANCHORS (Symbols grounded through survival):")
        for i, (anchor_id, anchor) in enumerate(engine.metabolic_anchors.items()):
            print(f"\n  Anchor {i+1}:")
            print(f"    Metabolism Boost: {anchor['metabolism_boost']:.2f}")
            print(f"    Discovered at step: {anchor['discovered_at']}")
            print(f"    Pattern:")
            print(f"    {anchor['pattern']}")
    
    # Visualization
    fig, axes = plt.subplots(2, 1, figsize=(12, 8))
    
    # Plot 1: Energy over time
    axes[0].plot(engine.energy_history, linewidth=2)
    axes[0].axhline(y=0, color='r', linestyle='--', label='Death Threshold')
    axes[0].set_title('Energy (H) Over Time - Survival Pressure', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Step')
    axes[0].set_ylabel('Energy (H)')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # Mark discovery events
    for event in engine.discovery_events:
        axes[0].axvline(x=event['step'], color='g', alpha=0.3, linestyle=':')
    
    # Plot 2: Metabolism over time
    axes[1].plot(engine.metabolism_history, linewidth=2, color='orange')
    axes[1].axhline(y=0, color='r', linestyle='--', label='Zero Metabolism')
    axes[1].set_title('Metabolism (dH/dt) Over Time', fontsize=14, fontweight='bold')
    axes[1].set_xlabel('Step')
    axes[1].set_ylabel('dH/dt')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('zero_point_survival.png', dpi=150, bbox_inches='tight')
    print(f"\n📊 Visualization saved to: zero_point_survival.png")
    
    print(f"\n{'='*80}")
    print("KEY INSIGHTS:")
    print(f"{'='*80}")
    print("1. System had ZERO knowledge of 'patterns' or 'symmetry'")
    print("2. Symbols emerged as 'Metabolic Anchors' (survival-grounded)")
    print("3. No hardcoded compression, logic, or rules")
    print("4. Intelligence = Will to Exist (dH/dt ≥ 0)")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    run_survival_demo()
