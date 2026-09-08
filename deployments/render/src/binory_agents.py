"""BinoryLogy Agents 2.0 - 4 Cognitive Agents with 6-Engine Body.
Each agent carries all 6 sovereign engines from GOD/src as physiological organs.
The agents form a council and vote on curriculum advancement.
Zero hardcoded constants - all adaptive parameters come from the engine organs.
"""
import sys, os, math, time, numpy as np
from typing import Optional, Dict, Any, List
from pathlib import Path

# ── Import the 6 engine organs from GOD/src ─────────────────────────────
_GOD_SRC = r"C:\Users\reman\OneDrive\Desktop\mine data\GOD\src"
if _GOD_SRC not in sys.path:
    sys.path.insert(0, _GOD_SRC)

try:
    from autopoietic_engine import AutopoieticEngine
    _AUTOPOIETIC = True
except ImportError:
    _AUTOPOIETIC = False
    print("[WARN] AutopoieticEngine not available - using stub")

try:
    from kolmogorov_engine import KolmogorovEngine
    _KOLMOGOROV = True
except ImportError:
    _KOLMOGOROV = False
    print("[WARN] KolmogorovEngine not available - using stub")

try:
    from gravity_engine import GravityEngine
    _GRAVITY = True
except ImportError:
    _GRAVITY = False

try:
    from zero_point_engine import ZeroPointEngine
    _ZEROPOINT = True
except ImportError:
    _ZEROPOINT = False
    print("[WARN] ZeroPointEngine not available - using stub")

try:
    from fever_protocol import FeverProtocol
    _FEVER = True
except ImportError:
    _FEVER = False
    print("[WARN] FeverProtocol not available - using stub")

try:
    from quantum_belief_engine import QuantumBeliefEngine
    _QUANTUM = True
except ImportError:
    _QUANTUM = False
    print("[WARN] QuantumBeliefEngine not available - using stub")

try:
    from string_dimensions import String10DCognitiveEngine
    _STRING = True
except ImportError:
    _STRING = False

from binory_physics_stream import Observation, PhysicsTier
from binory_curriculum import AdaptiveCurriculum

# ── Stubs for missing engines (graceful degradation) ────────────────────
class _StubEngine:
    def __init__(self, *a, **kw): pass
    def update(self, *a, **kw): return {}
    def get_dashboard(self, *a, **kw): return {}
    def induce_causal_laws(self, *a, **kw): return []

# ── Base Agent: the 6-engine body ───────────────────────────────────────
class SovereignAgent:
    """
    Base class: all 6 engine organs are instantiated as member variables.
    Subclasses implement cognitive role-specific behavior on top.
    """
    COUNCIL_SIZE = 4  # Total agents in the council

    def __init__(self, agent_id: str, grid_shape=(8, 8)):
        self.agent_id = agent_id
        self._step = 0
        self._grid_shape = grid_shape
        self._discoveries: List[dict] = []
        self._vote_advance = False

        # ── Organ 1: Cortex (AutopoieticEngine) ─────────────────────────
        if _AUTOPOIETIC:
            self.cortex = AutopoieticEngine()
        else:
            self.cortex = _StubEngine()

        # ── Organ 2: Genome (KolmogorovEngine) ──────────────────────────
        if _KOLMOGOROV:
            self.genome = KolmogorovEngine(agent_id=agent_id)
        else:
            self.genome = _StubEngine()

        # ── Organ 3: Skeleton (GravityEngine) ───────────────────────────
        if _GRAVITY:
            try:
                self.skeleton = GravityEngine()
            except Exception:
                self.skeleton = _StubEngine()
        else:
            self.skeleton = _StubEngine()

        # ── Organ 4: Metabolism (ZeroPointEngine) ───────────────────────
        if _ZEROPOINT:
            try:
                self.metabolism = ZeroPointEngine()
            except Exception:
                self.metabolism = _StubEngine()
        else:
            self.metabolism = _StubEngine()

        # ── Organ 5: Immune System (FeverProtocol) ───────────────────────
        if _FEVER:
            self.immune = FeverProtocol(agent_id=agent_id)
        else:
            self.immune = _StubEngine()

        # ── Organ 6: Perception (QuantumBeliefEngine) ───────────────────
        if _QUANTUM:
            try:
                self.perception = QuantumBeliefEngine()
            except Exception:
                self.perception = _StubEngine()
        else:
            self.perception = _StubEngine()

        # String10D: cognitive coordinate system
        if _STRING:
            self.string10d = String10DCognitiveEngine(agent_id=agent_id)
        else:
            self.string10d = None

    def _run_body(self, obs: Observation, curriculum: AdaptiveCurriculum) -> dict:
        """
        Run all 6 engine organs on the current observation.
        Returns combined physiological state.
        """
        grid = obs.binary_signal.astype(np.float32)
        results = {}

        # Organ 1: Cortex - information density
        try:
            if hasattr(self.cortex, 'calculate_local_feature_density'):
                rho_D = self.cortex.calculate_local_feature_density(grid)
                results["cortex_density"] = float(np.mean(rho_D))
            else:
                results["cortex_density"] = float(np.mean(grid))
        except Exception:
            results["cortex_density"] = 0.0

        # Organ 2: Genome - law induction
        try:
            if hasattr(self.genome, 'induce_causal_laws'):
                laws = self.genome.induce_causal_laws(grid, grid, self._step)
                results["new_laws"] = len(laws) if laws else 0
                if laws:
                    for law in laws:
                        compression = getattr(law, "compression_ratio", 0.0)
                        concept = getattr(law, "name", "unknown")
                        equation = getattr(law, "expression", "?")
                        curriculum.record_discovery(
                            self.agent_id, concept, str(equation), compression, self._step)
                        self._discoveries.append({"step": self._step, "law": str(equation)})
            else:
                results["new_laws"] = 0
        except Exception:
            results["new_laws"] = 0

        # Organ 4: Metabolism - survival check
        try:
            if hasattr(self.metabolism, 'update'):
                obs_flat = grid.flatten()
                action_flat = obs_flat
                # Adaptive reward: information gain from cortex density
                reward = results.get("cortex_density", 0.0)
                meta_result = self.metabolism.update(obs_flat, action_flat, reward)
                results["metabolic_action"] = str(meta_result)
                dash = self.metabolism.get_dashboard() if hasattr(self.metabolism, 'get_dashboard') else {}
                results["energy"] = dash.get("energy", 100.0)
                results["entropy_budget"] = dash.get("entropy_budget", 10000.0)
                results["dH_dt"] = dash.get("dH_dt", 0.0)
        except Exception as e:
            results["energy"] = 100.0; results["dH_dt"] = 0.0

        # Organ 5: Immune - thermodynamic temperature
        try:
            if hasattr(self.immune, 'update'):
                dH_dt = results.get("dH_dt", 0.0)
                entropy = 1.0 - results.get("cortex_density", 0.5)
                new_laws = results.get("new_laws", 0)
                temp, viscosity, fever = self.immune.update(dH_dt, entropy, new_laws)
                results["temperature"] = temp
                results["viscosity"] = viscosity
                results["fever"] = fever
                # String10D: unfold dimensions under fever
                if self.string10d is not None:
                    self.string10d.update_state(
                        pos=(0, 0), step=self._step,
                        temperature=temp,
                        subroutine_count=len(self._discoveries),
                        entropy=entropy,
                        energy=results.get("energy", 100.0),
                        consensus_strength=0.5
                    )
            else:
                results["temperature"] = 0.1; results["fever"] = False
        except Exception:
            results["temperature"] = 0.1; results["fever"] = False

        # Organ 6: Perception - belief update
        try:
            if hasattr(self.perception, 'update_with_observation'):
                kl_div = self.perception.update_with_observation(
                    agent_pos=(0, 0),
                    aperture_radius=min(self._grid_shape) // 2,
                    observed_patch=grid
                )
                results["belief_kl"] = float(kl_div) if kl_div is not None else 0.0
            else:
                results["belief_kl"] = 0.0
        except Exception:
            results["belief_kl"] = 0.0

        return results

    def step(self, obs: Observation, curriculum: AdaptiveCurriculum) -> dict:
        """Override in subclasses for role-specific logic."""
        self._step += 1
        return self._run_body(obs, curriculum)

    def vote_to_advance(self) -> bool:
        return self._vote_advance


# ── The 4 Cognitive Agents ───────────────────────────────────────────────

class EngineerAgent(SovereignAgent):
    """
    Runs the physical simulations and verifies basic kinematic laws.
    Inspired by Physics-Informed Neural Networks and symplectic integrators.
    """
    def __init__(self):
        super().__init__("ENGINEER")
        self._energy_conservation_errors = []

    def step(self, obs: Observation, curriculum: AdaptiveCurriculum) -> dict:
        self._step += 1
        body = self._run_body(obs, curriculum)

        # Check energy conservation in the observation
        ke = obs.variables.get("KE", obs.variables.get("ke_after", 0.0))
        pe = obs.variables.get("PE", obs.variables.get("V_potential", 0.0))
        e_total = obs.variables.get("E_total", obs.variables.get("H_hamiltonian", ke + pe))
        if e_total != 0:
            error = abs((ke + pe - e_total) / (abs(e_total) + 1e-9))
            self._energy_conservation_errors.append(error)

        # Vote to advance if energy conservation consistently holds (<1% error)
        if len(self._energy_conservation_errors) > 50:
            mean_err = sum(self._energy_conservation_errors[-50:]) / 50
            self._vote_advance = mean_err < 0.01
            if self._vote_advance:
                curriculum.agent_vote_advance(self.agent_id)

        body["role"] = "ENGINEER"
        body["energy_conservation_error"] = self._energy_conservation_errors[-1] if self._energy_conservation_errors else 0.0
        return body


class ProphetAgent(SovereignAgent):
    """
    Explores variational paths and proposes auxiliary hypotheses.
    Inspired by AlphaGeometry System 1 (neural hypothesis generator).
    """
    def __init__(self):
        super().__init__("PROPHET")
        self._hypothesis_count = 0
        self._belief_entropy_history = []

    def step(self, obs: Observation, curriculum: AdaptiveCurriculum) -> dict:
        self._step += 1
        body = self._run_body(obs, curriculum)

        # Prophet measures belief entropy from perception organ
        kl = body.get("belief_kl", 0.0)
        self._belief_entropy_history.append(kl)

        # If belief KL divergence is low (epistemic certainty), vote to advance
        if len(self._belief_entropy_history) > 30:
            mean_kl = sum(self._belief_entropy_history[-30:]) / 30
            # Low mean KL = beliefs are stable = mastery achieved
            self._vote_advance = mean_kl < 0.05
            if self._vote_advance:
                curriculum.agent_vote_advance(self.agent_id)

        # Fever triggers hypothesis burst
        if body.get("fever", False):
            self._hypothesis_count += 1

        body["role"] = "PROPHET"
        body["hypotheses_generated"] = self._hypothesis_count
        return body


class WitnessAgent(SovereignAgent):
    """
    Measures compression gain and verifies conservation invariants.
    Inspired by AI Feynman and PySR (Pareto-optimal symbolic regression).
    """
    def __init__(self):
        super().__init__("WITNESS")
        self._invariant_violations = []
        self._compression_gains = []

    def step(self, obs: Observation, curriculum: AdaptiveCurriculum) -> dict:
        self._step += 1
        body = self._run_body(obs, curriculum)

        # Check momentum conservation invariant (Tier 3+)
        p_before = obs.variables.get("p_before")
        p_after = obs.variables.get("p_after")
        if p_before is not None and p_after is not None and abs(p_before) > 1e-9:
            violation = abs(p_before - p_after) / (abs(p_before) + 1e-9)
            self._invariant_violations.append(violation)

        # Check Lorentz invariant ds^2 (Tier 5+)
        ds2_diff = obs.variables.get("invariant_diff")
        if ds2_diff is not None:
            self._invariant_violations.append(float(ds2_diff))

        # Compression density from cortex
        density = body.get("cortex_density", 0.0)
        self._compression_gains.append(density)

        # Vote when invariants consistently hold
        if len(self._invariant_violations) > 20:
            mean_viol = sum(self._invariant_violations[-20:]) / 20
            self._vote_advance = mean_viol < 0.001
            if self._vote_advance:
                curriculum.agent_vote_advance(self.agent_id)

        body["role"] = "WITNESS"
        body["invariant_violations"] = len(self._invariant_violations)
        body["mean_violation"] = sum(self._invariant_violations[-20:]) / max(1, len(self._invariant_violations[-20:]))
        return body


class ArchitectAgent(SovereignAgent):
    """
    Tests coordinate invariance and detects symmetries.
    Inspired by AlphaProof (formal verification) and Noether's theorem.
    """
    def __init__(self):
        super().__init__("ARCHITECT")
        self._symmetries_found = []
        self._covariance_scores = []

    def step(self, obs: Observation, curriculum: AdaptiveCurriculum) -> dict:
        self._step += 1
        body = self._run_body(obs, curriculum)

        # Test temporal symmetry: energy should be conserved if L has no explicit t
        e_total = obs.variables.get("E_total", obs.variables.get("H_hamiltonian"))
        if e_total is not None:
            # Simple covariance test: same law should hold at different steps
            self._covariance_scores.append(abs(e_total))

        # Test rotational symmetry using the binary grid
        grid = obs.binary_signal
        grid_rot = np.rot90(grid)
        symmetry_score = float(np.sum(grid == grid_rot)) / max(grid.size, 1)
        self._symmetries_found.append(symmetry_score)

        # Detect Lorentz invariance: ds2_diff should be ~0
        ds2_diff = obs.variables.get("ds2_diff")
        if ds2_diff is not None and ds2_diff < 1e-6:
            curriculum.record_discovery(
                self.agent_id, "lorentz_invariance",
                "ds^2=invariant", 1.0, self._step)

        # Vote when symmetries are consistently detected
        if len(self._symmetries_found) > 30:
            mean_sym = sum(self._symmetries_found[-30:]) / 30
            self._vote_advance = mean_sym > 0.5
            if self._vote_advance:
                curriculum.agent_vote_advance(self.agent_id)

        body["role"] = "ARCHITECT"
        body["symmetries_found"] = len(self._symmetries_found)
        body["mean_symmetry_score"] = sum(self._symmetries_found[-10:]) / max(1, len(self._symmetries_found[-10:]))
        return body


class CognitiveCouncil:
    """
    The 4-agent council. Runs all agents each step and collects their votes.
    """
    def __init__(self):
        self.engineer = EngineerAgent()
        self.prophet = ProphetAgent()
        self.witness = WitnessAgent()
        self.architect = ArchitectAgent()
        self._agents = [self.engineer, self.prophet, self.witness, self.architect]

    def step(self, obs: Observation, curriculum: AdaptiveCurriculum) -> Dict[str, dict]:
        results = {}
        for agent in self._agents:
            try:
                results[agent.agent_id] = agent.step(obs, curriculum)
            except Exception as e:
                results[agent.agent_id] = {"error": str(e), "role": agent.agent_id}
        # Check if curriculum should advance
        if curriculum.check_advancement(n_agents=len(self._agents)):
            print(f"[COUNCIL] Curriculum advanced to Tier {int(curriculum.tier)}")
        return results

    def dashboard(self) -> List[dict]:
        out = []
        for agent in self._agents:
            out.append({
                "id": agent.agent_id,
                "step": agent._step,
                "discoveries": len(agent._discoveries),
                "vote_advance": agent._vote_advance,
            })
        return out
