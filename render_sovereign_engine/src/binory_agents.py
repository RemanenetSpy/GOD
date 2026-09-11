"""
========================================================================================
BinoryLogy Agents — 4 Sovereign Pillars running the God Equation
========================================================================================
S_{t+1}^i = U(S_t^i, A_t^i, O_t^i, M_t^i) + L(S_t^i)

The 4 Pillars (your original mythology from civilization.py):
  1. Classical-Eikonal         — Eikonal geodesic action, strict efficiency
  2. Quantum-Superposed        — Quantum Bayesian belief, maximum exploration
  3. Modern-Thermodynamic      — Homeostasis governor, dH/dt equation
  4. String-10D-Topological    — 10-dimensional cognitive meta-agent

The physics observation stream (binory_physics_stream.py) feeds into O_t^i.
The RelativisticMessageFabric handles typed M_t^i peer messaging.

GOD/src files are NEVER modified. Imported read-only via sys.path.
========================================================================================
"""

import sys, copy, numpy as np
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional, Any

# ── GOD/src — read-only, never modified ──────────────────────────────────────────
_GOD_SRC = r"C:\Users\reman\OneDrive\Desktop\mine data\GOD\src"
if _GOD_SRC not in sys.path:
    sys.path.insert(0, _GOD_SRC)

from binory_physics_stream import Observation as PhysicsObservation
from binory_curriculum import AdaptiveCurriculum

# ── Import the 4 original GOD/src engines ────────────────────────────────────────
try:
    from quantum_belief_engine import QuantumBeliefEngine
    _HAS_BELIEF = True
except ImportError:
    _HAS_BELIEF = False
    print("[WARN] QuantumBeliefEngine missing — stub active")

try:
    from kolmogorov_engine import KolmogorovEngine, DiscoveredProgram
    _HAS_KOLMOGOROV = True
except ImportError:
    _HAS_KOLMOGOROV = False
    print("[WARN] KolmogorovEngine missing — stub active")

try:
    from fever_protocol import FeverProtocol
    _HAS_FEVER = True
except ImportError:
    _HAS_FEVER = False
    print("[WARN] FeverProtocol missing — stub active")

try:
    from string_dimensions import String10DCognitiveEngine
    _HAS_STRING = True
except ImportError:
    _HAS_STRING = False
    print("[WARN] String10DCognitiveEngine missing — stub active")


# ═══════════════════════════════════════════════════════════════════════════════════
# Engine stubs — only used when GOD/src engine is genuinely unavailable
# ═══════════════════════════════════════════════════════════════════════════════════
class _StubBeliefEngine:
    def __init__(self, grid_shape=(8, 8)):
        self.belief_tensor = np.ones((*grid_shape, 4), dtype=np.float32) * 0.25
    def update_with_observation(self, agent_pos, aperture_radius, observed_patch):
        return float(np.mean(np.abs(observed_patch - 0.5)))
    def compute_total_entropy(self):
        return float(np.mean(-self.belief_tensor * np.log(self.belief_tensor + 1e-12)))
    def get_nutrient_belief_field(self):
        return self.belief_tensor[:, :, 0]
    def get_entropy_field(self):
        return np.ones(self.belief_tensor.shape[:2]) * 0.5

class _StubKolmogorov:
    def __init__(self, agent_id="stub"):
        self.program_library = {}
    def induce_causal_laws(self, prev_obs, curr_obs, step):
        return []
    def get_library_dict(self):
        return {}

class _StubFever:
    def __init__(self, agent_id="stub"):
        self.temperature = 0.3
    def update(self, dh_dt, current_entropy, newly_discovered_rules):
        return 0.3, 0.5, False

class _StubString10D:
    def update_state(self, **kwargs): pass
    def get_summary(self): return {}


# ═══════════════════════════════════════════════════════════════════════════════════
# PillarArchetype — your original mythology, verbatim from civilization.py
# ═══════════════════════════════════════════════════════════════════════════════════
class PillarArchetype(Enum):
    CLASSICAL_EIKONAL    = "Classical-Eikonal"
    QUANTUM_SUPERPOSED   = "Quantum-Superposed"
    MODERN_THERMODYNAMIC = "Modern-Thermodynamic"
    STRING_TOPOLOGICAL   = "String-10D-Topological"


# ═══════════════════════════════════════════════════════════════════════════════════
# Action — from civilization.py
# ═══════════════════════════════════════════════════════════════════════════════════
class Action(Enum):
    OBSERVE    = 0
    MOVE_UP    = 1
    MOVE_DOWN  = 2
    MOVE_LEFT  = 3
    MOVE_RIGHT = 4


# ═══════════════════════════════════════════════════════════════════════════════════
# Message types & RelativisticMessageFabric — verbatim from civilization.py
# ═══════════════════════════════════════════════════════════════════════════════════
class MessageType(Enum):
    TOPOLOGICAL_GRADIENT = "topological_grad"
    BELIEF_TENSOR        = "belief_tensor"
    FEVER_ALERT          = "fever_alert"
    SUBROUTINE_CODE      = "subroutine_code"


@dataclass
class Message:
    sender_id:    str
    recipient_id: str
    msg_type:     MessageType
    payload:      Any
    confidence:   float
    timestamp:    int

    def summary(self) -> str:
        rec = "BROADCAST" if self.recipient_id == "BROADCAST" else self.recipient_id[:10]
        return f"[{self.sender_id[:12]}] -> {rec} : {self.msg_type.value} (conf={self.confidence:.2f})"


class RelativisticMessageFabric:
    """Non-blocking asynchronous tensor routing fabric (M_t^i) — from civilization.py."""
    def __init__(self):
        self.inboxes: Dict[str, List[Message]] = {}
        self.history: List[Message] = []
        self.total_messages_routed: int = 0

    def register_node(self, node_id: str):
        if node_id not in self.inboxes:
            self.inboxes[node_id] = []

    def unregister_node(self, node_id: str):
        self.inboxes.pop(node_id, None)

    def transmit(self, msg: Message):
        self.total_messages_routed += 1
        self.history.append(msg)
        if len(self.history) > 300:
            self.history.pop(0)
        if msg.recipient_id == "BROADCAST":
            for nid, box in self.inboxes.items():
                if nid != msg.sender_id:
                    box.append(msg)
        elif msg.recipient_id in self.inboxes:
            self.inboxes[msg.recipient_id].append(msg)

    def fetch_inbox(self, node_id: str) -> List[Message]:
        if node_id not in self.inboxes:
            return []
        msgs = self.inboxes[node_id]
        self.inboxes[node_id] = []
        return msgs


# ═══════════════════════════════════════════════════════════════════════════════════
# AgentState — from civilization.py
# ═══════════════════════════════════════════════════════════════════════════════════
@dataclass
class AgentState:
    node_id:           str
    pillar:            PillarArchetype
    position:          Tuple[int, int]   = (0, 0)
    energy:            float             = 100.0
    temperature:       float             = 0.5
    viscosity:         float             = 0.5
    dh_dt:             float             = 0.0
    fever_active:      bool              = False
    belief_entropy:    float             = 0.0
    subroutine_library: Dict[str, str]  = field(default_factory=dict)
    cognitive_10d:     Dict[str, float] = field(default_factory=dict)


# ═══════════════════════════════════════════════════════════════════════════════════
# BaseSovereignNode — GOD EQUATION
# S_{t+1}^i = U(S_t^i, A_t^i, O_t^i, M_t^i) + L(S_t^i)
#
# O_t^i = physics_obs.binary_signal reshaped into a 2-D aperture window
# M_t^i = inbox from the RelativisticMessageFabric
# L(S)  = Kolmogorov causal law induction
# ═══════════════════════════════════════════════════════════════════════════════════
class BaseSovereignNode:
    """Core node. Implements the God Equation using BinoryLogy physics streams."""

    def __init__(self, node_id, pillar, grid_shape=(8,8), aperture=3, initial_energy=100.0):
        self.node_id  = node_id
        self.pillar   = pillar
        self.h, self.w = grid_shape
        self.aperture  = aperture
        self._discoveries: List[dict] = []
        self._vote_advance: bool = False

        # ── 4 original engines from BaseSovereignNode (civilization.py) ──────────
        if _HAS_BELIEF:
            try:
                self.belief_engine = QuantumBeliefEngine(grid_shape=grid_shape)
            except Exception:
                self.belief_engine = _StubBeliefEngine(grid_shape)
        else:
            self.belief_engine = _StubBeliefEngine(grid_shape)

        if _HAS_KOLMOGOROV:
            self.kolmogorov_engine = KolmogorovEngine(agent_id=node_id)
        else:
            self.kolmogorov_engine = _StubKolmogorov(agent_id=node_id)

        if _HAS_FEVER:
            self.fever_engine = FeverProtocol(agent_id=node_id)
        else:
            self.fever_engine = _StubFever(agent_id=node_id)

        if _HAS_STRING:
            self.string_10d_engine = String10DCognitiveEngine(agent_id=node_id)
        else:
            self.string_10d_engine = _StubString10D()

        self.state = AgentState(node_id=node_id, pillar=pillar, energy=initial_energy)
        self._last_action: Action = Action.OBSERVE
        self._last_obs: Optional[np.ndarray] = None

        self._apply_pillar_personality()

    def _apply_pillar_personality(self):
        """Pillar-specific tuning — from agent.py specialization logic."""
        if self.pillar == PillarArchetype.QUANTUM_SUPERPOSED:
            self.aperture = max(self.aperture, 3)
            self.exploration_bias = 1.5
        elif self.pillar == PillarArchetype.CLASSICAL_EIKONAL:
            self.aperture = max(self.aperture, 2)
            self.exploration_bias = 0.2
        elif self.pillar == PillarArchetype.MODERN_THERMODYNAMIC:
            self.aperture = max(self.aperture, 3)
            self.exploration_bias = 0.5
        elif self.pillar == PillarArchetype.STRING_TOPOLOGICAL:
            self.aperture = max(self.aperture, 4)
            self.exploration_bias = 0.8

    # ─────────────────────────────────────────────────────────────────────────────
    # THE GOD EQUATION
    # S_{t+1}^i = U(S_t^i, A_t^i, O_t^i, M_t^i) + L(S_t^i)
    # Verbatim logic from civilization.py BaseSovereignNode.universal_update()
    # ─────────────────────────────────────────────────────────────────────────────
    def universal_update(self, action, physics_obs, inbox, step, climate_telemetry=None):
        # Build visible_cells window from physics stream signal
        raw = physics_obs.binary_signal.astype(np.float32)
        aw  = self.aperture * 2 + 1
        if raw.size >= aw * aw:
            curr_obs = raw[:aw * aw].reshape(aw, aw)
        else:
            curr_obs = np.pad(raw, (0, aw * aw - raw.size)).reshape(aw, aw)

        # 1. Quantum Bayesian Belief Update — |Psi>
        info_gain = self.belief_engine.update_with_observation(
            agent_pos=self.state.position,
            aperture_radius=self.aperture,
            observed_patch=curr_obs
        )
        self.state.belief_entropy = self.belief_engine.compute_total_entropy()

        # 2. Relativistic Message Ingestion — M_t^i
        for msg in inbox:
            if msg.msg_type == MessageType.BELIEF_TENSOR and isinstance(msg.payload, np.ndarray):
                if hasattr(self.belief_engine, 'belief_tensor') and \
                        msg.payload.shape == self.belief_engine.belief_tensor.shape:
                    self.belief_engine.belief_tensor = (
                        0.90 * self.belief_engine.belief_tensor + 0.10 * msg.payload
                    )
            elif msg.msg_type == MessageType.SUBROUTINE_CODE and isinstance(msg.payload, dict):
                if _HAS_KOLMOGOROV:
                    for sig, code in msg.payload.items():
                        if sig not in self.kolmogorov_engine.program_library:
                            try:
                                prog = DiscoveredProgram(
                                    signature="assimilated_" + sig[:20],
                                    code_str=code,
                                    program_type="SHARED_PEER_RULE",
                                    compression_gain=1.5,
                                    description=f"From {msg.sender_id}",
                                    discovery_step=step
                                )
                                self.kolmogorov_engine.program_library[sig] = prog
                            except Exception:
                                pass
            elif msg.msg_type == MessageType.FEVER_ALERT:
                if msg.confidence > 0.8 and _HAS_FEVER:
                    self.fever_engine.temperature = min(3.0, self.fever_engine.temperature + 0.2)

        # 3. Kolmogorov Causal Law Induction — L(S_t^i)
        new_programs = self.kolmogorov_engine.induce_causal_laws(
            prev_obs=self._last_obs, curr_obs=curr_obs, step=step
        )
        self._last_obs = curr_obs.copy()
        compression_profit = sum(getattr(p, "compression_gain", 1.0) for p in new_programs)
        for p in new_programs:
            self._discoveries.append({
                "step":   step,
                "law":    getattr(p, "signature", str(p)),
                "gain":   getattr(p, "compression_gain", 1.0),
                "pillar": self.pillar.value
            })

        # 4. Thermodynamic Homeostasis — dH/dt = (Sigma * Omega) - Lambda
        friction_mult  = float((climate_telemetry or {}).get("friction_mult", 1.0))
        friction       = 0.05 * friction_mult
        feeding_energy = max(0.0, physics_obs.variables.get("reward", 0.5))
        sigma          = 1.0 + len(self.kolmogorov_engine.program_library) * 0.05
        omega          = float(info_gain) + compression_profit * 0.5
        dh_dt          = (feeding_energy + sigma * omega) - friction
        self.state.dh_dt   = float(dh_dt)
        self.state.energy  = float(np.clip(self.state.energy + dh_dt, 0.0, 300.0))

        # 5. Fever & Viscous Momentum
        temp, visc, fever = self.fever_engine.update(
            dh_dt=dh_dt,
            current_entropy=self.state.belief_entropy,
            newly_discovered_rules=len(new_programs)
        )
        self.state.temperature  = float(temp)
        self.state.viscosity    = float(visc)
        self.state.fever_active = bool(fever)

        # 6. 10D String Cognitive Coordinate
        self.string_10d_engine.update_state(
            pos=self.state.position,
            step=step,
            temperature=self.state.temperature,
            subroutine_count=len(self.kolmogorov_engine.program_library),
            entropy=self.state.belief_entropy,
            energy=self.state.energy,
            consensus_strength=1.0 - (self.state.belief_entropy / 2.0)
        )
        self.state.cognitive_10d      = self.string_10d_engine.get_summary()
        self.state.subroutine_library = self.kolmogorov_engine.get_library_dict()

    def select_action(self) -> Action:
        """Action selection — from BaseSovereignNode.select_action() in civilization.py."""
        # Fever → Brownian stochastic walk
        if self.state.fever_active or self.state.temperature > 1.5:
            return np.random.choice([
                Action.MOVE_UP, Action.MOVE_DOWN,
                Action.MOVE_LEFT, Action.MOVE_RIGHT, Action.OBSERVE
            ])
        if self.pillar == PillarArchetype.QUANTUM_SUPERPOSED:
            return np.random.choice([Action.MOVE_UP, Action.MOVE_DOWN,
                                     Action.MOVE_LEFT, Action.MOVE_RIGHT])
        if self.pillar == PillarArchetype.CLASSICAL_EIKONAL:
            try:
                nutrient_map = self.belief_engine.get_nutrient_belief_field()
                entropy_map  = self.belief_engine.get_entropy_field()
                cost_grid    = (1.0 - nutrient_map) * 3.0 + entropy_map * 2.0
                py, px       = self.state.position
                best_act     = Action.OBSERVE
                best_val     = cost_grid[py, px] if (0 <= py < self.h and 0 <= px < self.w) else 99.0
                for act, dy, dx in [(Action.MOVE_UP,-1,0),(Action.MOVE_DOWN,1,0),
                                    (Action.MOVE_LEFT,0,-1),(Action.MOVE_RIGHT,0,1)]:
                    ny, nx = py + dy, px + dx
                    if 0 <= ny < self.h and 0 <= nx < self.w:
                        val = cost_grid[ny, nx]
                        if val < best_val:
                            best_val = val
                            best_act = act
                return best_act
            except Exception:
                return Action.OBSERVE
        if self.pillar == PillarArchetype.MODERN_THERMODYNAMIC:
            return Action.MOVE_UP if self.state.energy > 150.0 else Action.OBSERVE
        return Action.OBSERVE  # String meta — always observes

    def emit_messages(self, step: int) -> List[Message]:
        """Emit typed relativistic messages — from civilization.py emit_messages()."""
        msgs = []
        if self.state.energy > 80.0 and hasattr(self.belief_engine, 'belief_tensor'):
            msgs.append(Message(
                sender_id=self.node_id, recipient_id="BROADCAST",
                msg_type=MessageType.BELIEF_TENSOR,
                payload=self.belief_engine.belief_tensor,
                confidence=0.85, timestamp=step
            ))
        if self.kolmogorov_engine.program_library:
            msgs.append(Message(
                sender_id=self.node_id, recipient_id="BROADCAST",
                msg_type=MessageType.SUBROUTINE_CODE,
                payload=self.kolmogorov_engine.get_library_dict(),
                confidence=0.95, timestamp=step
            ))
        if self.state.fever_active:
            msgs.append(Message(
                sender_id=self.node_id, recipient_id="BROADCAST",
                msg_type=MessageType.FEVER_ALERT,
                payload={"temperature": self.state.temperature},
                confidence=0.90, timestamp=step
            ))
        return msgs

    def vote_to_advance(self) -> bool:
        return self._vote_advance

    def snapshot(self) -> dict:
        return {
            "id":             self.node_id,
            "pillar":         self.pillar.value,
            "energy":         round(self.state.energy, 3),
            "temperature":    round(self.state.temperature, 3),
            "viscosity":      round(self.state.viscosity, 3),
            "dh_dt":          round(self.state.dh_dt, 4),
            "fever":          self.state.fever_active,
            "belief_entropy": round(self.state.belief_entropy, 4),
            "subroutines":    len(self.kolmogorov_engine.program_library),
            "discoveries":    len(self._discoveries),
            "cognitive_10d":  self.state.cognitive_10d,
            "vote_advance":   self._vote_advance,
            "last_action":    self._last_action.name,
        }


# ═══════════════════════════════════════════════════════════════════════════════════
# The 4 Pillar subclasses — each adds specialised voting criterion on top
# ═══════════════════════════════════════════════════════════════════════════════════

class ClassicalEikonalNode(BaseSovereignNode):
    """Classical-Eikonal — governs kinematic/geometric consistency."""
    def __init__(self, grid_shape=(8,8)):
        super().__init__("classical_prime", PillarArchetype.CLASSICAL_EIKONAL,
                         grid_shape, aperture=2, initial_energy=100.0)
        self._energy_errors: List[float] = []

    def tick(self, physics_obs, inbox, step, curriculum, climate=None):
        self.universal_update(self._last_action, physics_obs, inbox, step, climate)
        act = self.select_action()
        self._last_action = act
        ke = physics_obs.variables.get("KE", physics_obs.variables.get("ke_after", 0.0))
        pe = physics_obs.variables.get("PE", physics_obs.variables.get("V_potential", 0.0))
        e_total = physics_obs.variables.get("E_total", physics_obs.variables.get("H_hamiltonian", ke + pe))
        if abs(e_total) > 1e-9:
            self._energy_errors.append(abs((ke + pe - e_total) / (abs(e_total) + 1e-9)))
        if len(self._energy_errors) > 50:
            self._vote_advance = sum(self._energy_errors[-50:]) / 50 < 0.01
            if self._vote_advance:
                curriculum.agent_vote_advance(self.node_id)
        return self.emit_messages(step), act


class QuantumSuperposedNode(BaseSovereignNode):
    """Quantum-Superposed — maximum exploration, belief entropy convergence."""
    def __init__(self, grid_shape=(8,8)):
        super().__init__("quantum_prime", PillarArchetype.QUANTUM_SUPERPOSED,
                         grid_shape, aperture=3, initial_energy=100.0)
        self._entropy_history: List[float] = []

    def tick(self, physics_obs, inbox, step, curriculum, climate=None):
        self.universal_update(self._last_action, physics_obs, inbox, step, climate)
        act = self.select_action()
        self._last_action = act
        self._entropy_history.append(self.state.belief_entropy)
        if len(self._entropy_history) > 30:
            self._vote_advance = sum(self._entropy_history[-30:]) / 30 < 0.05
            if self._vote_advance:
                curriculum.agent_vote_advance(self.node_id)
        return self.emit_messages(step), act


class ModernThermodynamicNode(BaseSovereignNode):
    """Modern-Thermodynamic — homeostasis, momentum invariant verification."""
    def __init__(self, grid_shape=(8,8)):
        super().__init__("modern_prime", PillarArchetype.MODERN_THERMODYNAMIC,
                         grid_shape, aperture=3, initial_energy=100.0)
        self._invariant_violations: List[float] = []

    def tick(self, physics_obs, inbox, step, curriculum, climate=None):
        self.universal_update(self._last_action, physics_obs, inbox, step, climate)
        act = self.select_action()
        self._last_action = act
        p_before = physics_obs.variables.get("p_before")
        p_after  = physics_obs.variables.get("p_after")
        if p_before is not None and p_after is not None and abs(p_before) > 1e-9:
            self._invariant_violations.append(
                abs(p_before - p_after) / (abs(p_before) + 1e-9))
        ds2_diff = physics_obs.variables.get("invariant_diff")
        if ds2_diff is not None:
            self._invariant_violations.append(float(ds2_diff))
        if len(self._invariant_violations) > 20:
            self._vote_advance = sum(self._invariant_violations[-20:]) / 20 < 0.001
            if self._vote_advance:
                curriculum.agent_vote_advance(self.node_id)
        return self.emit_messages(step), act


class StringTopologicalNode(BaseSovereignNode):
    """String-10D-Topological — tracks 10D cognitive coordinates, detects symmetries."""
    def __init__(self, grid_shape=(8,8)):
        super().__init__("string_meta", PillarArchetype.STRING_TOPOLOGICAL,
                         grid_shape, aperture=4, initial_energy=100.0)
        self._symmetry_scores: List[float] = []

    def tick(self, physics_obs, inbox, step, curriculum, climate=None):
        self.universal_update(self._last_action, physics_obs, inbox, step, climate)
        act = self.select_action()
        self._last_action = act
        sig = physics_obs.binary_signal.astype(np.float32)
        aw  = min(self.aperture * 2 + 1, len(sig))
        need = aw * aw
        g2d  = (sig[:need] if len(sig) >= need
                else np.pad(sig, (0, need - len(sig)))).reshape(aw, aw)
        sym  = float(np.sum(g2d == np.rot90(g2d))) / max(g2d.size, 1)
        self._symmetry_scores.append(sym)
        ds2_diff = physics_obs.variables.get("ds2_diff")
        if ds2_diff is not None and ds2_diff < 1e-6:
            curriculum.record_discovery(self.node_id, "lorentz_invariance",
                                        "ds^2=invariant", 1.0, step)
        if len(self._symmetry_scores) > 30:
            self._vote_advance = sum(self._symmetry_scores[-30:]) / 30 > 0.5
            if self._vote_advance:
                curriculum.agent_vote_advance(self.node_id)
        return self.emit_messages(step), act


# ═══════════════════════════════════════════════════════════════════════════════════
# SovereignCivilization — orchestrates 4 Pillars + RelativisticMessageFabric
# Based on civilization.py SovereignCivilization.step()
# ═══════════════════════════════════════════════════════════════════════════════════
class SovereignCivilization:
    """
    The living orchestrator. Runs God Equation on all 4 Pillars each tick,
    routes messages through RelativisticMessageFabric, drives curriculum.
    """
    def __init__(self, grid_shape: Tuple[int, int] = (8, 8)):
        self.grid_shape  = grid_shape
        self.step_count  = 0
        self.fabric      = RelativisticMessageFabric()
        self.global_subroutine_archive: Dict[str, str] = {}

        self.nodes: Dict[str, BaseSovereignNode] = {
            "classical_prime": ClassicalEikonalNode(grid_shape),
            "quantum_prime":   QuantumSuperposedNode(grid_shape),
            "modern_prime":    ModernThermodynamicNode(grid_shape),
            "string_meta":     StringTopologicalNode(grid_shape),
        }
        for nid in self.nodes:
            self.fabric.register_node(nid)

    def step(self, physics_obs, curriculum, climate_telemetry=None) -> Dict[str, dict]:
        self.step_count += 1
        out_msgs: List[Message] = []
        snapshots: Dict[str, dict] = {}

        for nid, node in self.nodes.items():
            inbox = self.fabric.fetch_inbox(nid)
            msgs, act = node.tick(physics_obs, inbox, self.step_count,
                                  curriculum, climate_telemetry)
            out_msgs.extend(msgs)
            for sig, code in node.kolmogorov_engine.get_library_dict().items():
                self.global_subroutine_archive[sig] = code
            if node.state.energy <= 0.0:
                node.state.energy = 15.0   # pioneer dormancy floor
            snap = node.snapshot()
            snap["step"] = self.step_count
            snapshots[nid] = snap

        for msg in out_msgs:
            self.fabric.transmit(msg)

        if curriculum.check_advancement(n_agents=len(self.nodes)):
            print(f"[CIVILIZATION] Tier advanced — Step {self.step_count}")

        return snapshots

    def synthesize_consensus(self):
        """Weighted belief tensor consensus — from civilization.py."""
        consensus = None
        tot_w = 0.0
        for node in self.nodes.values():
            if not hasattr(node.belief_engine, "belief_tensor"):
                continue
            w = node.state.energy / (node.state.temperature + 0.1)
            if consensus is None:
                consensus = w * node.belief_engine.belief_tensor.copy()
            elif node.belief_engine.belief_tensor.shape == consensus.shape:
                consensus += w * node.belief_engine.belief_tensor
            tot_w += w
        return (consensus / tot_w) if (consensus is not None and tot_w > 0) else None

    def dashboard(self) -> List[dict]:
        out = []
        for nid, node in self.nodes.items():
            snap = node.snapshot()
            snap["step"] = self.step_count
            out.append(snap)
        return out

    def global_discoveries(self) -> int:
        return sum(len(n._discoveries) for n in self.nodes.values())

    def total_subroutines(self) -> int:
        return len(self.global_subroutine_archive)

    def total_messages_routed(self) -> int:
        return self.fabric.total_messages_routed
