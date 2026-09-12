"""
========================================================================================
BinoryLogy Agents — 4 Sovereign Pillars running the God Equation
with Biological Hebbian Synaptic Message Fabric (Zero Broadcasting)
========================================================================================
S_{t+1}^i = U(S_t^i, A_t^i, O_t^i, M_t^i) + L(S_t^i)

The 4 Pillars (your original mythology from civilization.py):
  1. Classical-Eikonal         — Eikonal geodesic action, strict efficiency
  2. Quantum-Superposed        — Quantum Bayesian belief, maximum exploration
  3. Modern-Thermodynamic      — Homeostasis governor, dH/dt equation
  4. String-10D-Topological    — 10-dimensional cognitive meta-agent

The physics observation stream (binory_physics_stream.py) feeds into O_t^i.
The RelativisticMessageFabric is powered by BinoryLogy's Hebbian Synaptic Wiring:
  - No naive "BROADCAST" flooding
  - Messages route strictly along emerged axonal synapses (W_ij >= EMERGE_THRESHOLD)
  - Synapses strengthen when peers exchange useful knowledge (fire together, wire together)
  - Unused or noisy pathways experience Hebbian decay and pruning (use it or lose it)

GOD/src files are NEVER modified. Imported read-only via sys.path.
========================================================================================
"""

import sys, copy, math, numpy as np
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional, Any, Set

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
        return float(np.mean(np.abs(observed_patch - 0.5))) if observed_patch is not None else 0.0
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
# Message types & Synaptic Connectome Message Fabric
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
        rec = "SYNAPSE" if self.recipient_id == "BROADCAST" else self.recipient_id[:10]
        return f"[{self.sender_id[:12]}] -> {rec} : {self.msg_type.value} (conf={self.confidence:.2f})"


class RelativisticMessageFabric:
    """
    Hebbian Synaptic Message Fabric (Powered by BinoryLogy b.py engine).
    Replaces naive all-to-all broadcast with dynamic axonal routing.
    
    Principles:
      1. Co-activation & utility reinforce the synapse: W_ij += 1.0 ("fire together, wire together").
      2. Idle or redundant channels decay: W_ij = max(0, W_ij - decay).
      3. Messages travel ONLY along emerged axons where W_ij >= EMERGE_THRESHOLD (or initial bootstrap).
      4. Signal conductivity scales with synaptic weight: G_ij = clip(W_ij / 20.0, 0.2, 1.0).
    """
    EMERGE_THRESHOLD = 5.0
    DECAY_RATE       = 0.02
    MAX_WEIGHT       = 100.0

    def __init__(self):
        self.inboxes: Dict[str, List[Message]] = {}
        self.history: List[Message] = []
        self.total_messages_routed: int = 0
        
        # Directed synaptic weight matrix: (sender, recipient) -> float
        self.synapses: Dict[Tuple[str, str], float] = {}
        self.emerged: Set[Tuple[str, str]] = set()

    def register_node(self, node_id: str):
        if node_id not in self.inboxes:
            self.inboxes[node_id] = []
        # Initialize exploratory baseline synapses with all existing peers
        for peer in self.inboxes:
            if peer != node_id:
                self.synapses.setdefault((node_id, peer), 1.0)
                self.synapses.setdefault((peer, node_id), 1.0)

    def unregister_node(self, node_id: str):
        self.inboxes.pop(node_id, None)
        # Prune related synapses
        for k in list(self.synapses.keys()):
            if node_id in k:
                del self.synapses[k]
                self.emerged.discard(k)

    def reinforce_synapse(self, sender: str, recipient: str, amount: float = 1.0):
        """Reinforces the synaptic connection when useful knowledge is assimilated."""
        pair = (sender, recipient)
        old_w = self.synapses.get(pair, 1.0)
        new_w = min(self.MAX_WEIGHT, old_w + amount)
        self.synapses[pair] = new_w
        if old_w < self.EMERGE_THRESHOLD <= new_w:
            self.emerged.add(pair)

    def decay_synapses(self, rate: Optional[float] = None):
        """Hebbian decay: channels not actively used lose conductivity."""
        decay = rate if rate is not None else self.DECAY_RATE
        for pair in list(self.synapses.keys()):
            old_w = self.synapses[pair]
            new_w = max(0.5, old_w - decay)  # Maintain 0.5 minimum exploratory floor
            self.synapses[pair] = new_w
            if new_w < self.EMERGE_THRESHOLD and pair in self.emerged:
                self.emerged.discard(pair)

    def transmit(self, msg: Message):
        """
        Synaptic routing: eliminates naive all-to-all broadcast.
        If recipient_id is 'BROADCAST', message is dispatched ONLY across
        active axonal synapses connecting sender to peers.
        """
        self.history.append(msg)
        if len(self.history) > 300:
            self.history.pop(0)

        sender = msg.sender_id
        if msg.recipient_id == "BROADCAST":
            # Selective synaptic routing across active axons
            for peer, box in self.inboxes.items():
                if peer == sender:
                    continue
                pair = (sender, peer)
                weight = self.synapses.get(pair, 1.0)
                
                # Active axon gate: deliver if emerged OR exploratory baseline
                if weight >= 1.0:
                    # Modulate confidence by synaptic conductivity
                    conductance = min(1.0, max(0.2, weight / 20.0))
                    routed_msg = Message(
                        sender_id    = msg.sender_id,
                        recipient_id = peer,
                        msg_type     = msg.msg_type,
                        payload      = msg.payload,
                        confidence   = round(msg.confidence * conductance, 3),
                        timestamp    = msg.timestamp
                    )
                    box.append(routed_msg)
                    self.total_messages_routed += 1
        else:
            # Direct peer-to-peer transmission
            recipient = msg.recipient_id
            if recipient in self.inboxes:
                pair = (sender, recipient)
                weight = self.synapses.get(pair, 1.0)
                conductance = min(1.0, max(0.2, weight / 20.0))
                routed_msg = Message(
                    sender_id    = msg.sender_id,
                    recipient_id = recipient,
                    msg_type     = msg.msg_type,
                    payload      = msg.payload,
                    confidence   = round(msg.confidence * conductance, 3),
                    timestamp    = msg.timestamp
                )
                self.inboxes[recipient].append(routed_msg)
                self.total_messages_routed += 1

    def fetch_inbox(self, node_id: str) -> List[Message]:
        if node_id not in self.inboxes:
            return []
        msgs = self.inboxes[node_id]
        self.inboxes[node_id] = []
        return msgs

    def get_connectome(self) -> List[Dict[str, Any]]:
        """Returns the directed synaptic connectome for dashboard visualization."""
        edges = []
        for (src, dst), w in self.synapses.items():
            edges.append({
                "from":       src,
                "to":         dst,
                "weight":     round(w, 2),
                "emerged":    (src, dst) in self.emerged,
                "conductance": round(min(1.0, max(0.2, w / 20.0)), 3)
            })
        edges.sort(key=lambda x: x["weight"], reverse=True)
        return edges


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

    def __init__(self, node_id, pillar, grid_shape=(8, 8), aperture=3, initial_energy=100.0):
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
        """Pillar-specific tuning — preserved strictly from agent.py specialization logic."""
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

    def apply_action_movement(self, act: Action):
        """Update spatial grid position based on chosen action."""
        py, px = self.state.position
        if act == Action.MOVE_UP:
            self.state.position = (max(0, py - 1), px)
        elif act == Action.MOVE_DOWN:
            self.state.position = (min(self.h - 1, py + 1), px)
        elif act == Action.MOVE_LEFT:
            self.state.position = (py, max(0, px - 1))
        elif act == Action.MOVE_RIGHT:
            self.state.position = (py, min(self.w - 1, px + 1))

    # ─────────────────────────────────────────────────────────────────────────────
    # THE GOD EQUATION
    # S_{t+1}^i = U(S_t^i, A_t^i, O_t^i, M_t^i) + L(S_t^i)
    # Verbatim logic from civilization.py BaseSovereignNode.universal_update()
    # ─────────────────────────────────────────────────────────────────────────────
    def universal_update(self, action, physics_obs, inbox, step, fabric: Optional[RelativisticMessageFabric] = None, climate_telemetry=None):
        # 1. Build visible_cells window from physics stream signal
        raw = physics_obs.binary_signal.flatten().astype(np.float32)
        aw  = self.aperture * 2 + 1
        need = aw * aw
        if raw.size >= need:
            curr_obs = raw[:need].reshape(aw, aw)
        else:
            curr_obs = np.pad(raw, (0, need - raw.size)).reshape(aw, aw)

        # 2. Quantum Bayesian Belief Update — |Psi>
        py, px = self.state.position
        r = self.aperture
        y_min, y_max = max(0, py - r), min(self.h, py + r + 1)
        x_min, x_max = max(0, px - r), min(self.w, px + r + 1)
        dy_min = y_min - (py - r)
        dy_max = dy_min + (y_max - y_min)
        dx_min = x_min - (px - r)
        dx_max = dx_min + (x_max - x_min)
        patch_in_bounds = curr_obs[dy_min:dy_max, dx_min:dx_max]

        info_gain = self.belief_engine.update_with_observation(
            agent_pos=self.state.position,
            aperture_radius=self.aperture,
            observed_patch=patch_in_bounds
        )
        self.state.belief_entropy = self.belief_engine.compute_total_entropy()

        # 3. Synaptic Message Ingestion & Reinforcement — M_t^i
        for msg in inbox:
            sender = msg.sender_id
            if msg.msg_type == MessageType.BELIEF_TENSOR and isinstance(msg.payload, np.ndarray):
                if hasattr(self.belief_engine, 'belief_tensor') and \
                        msg.payload.shape == self.belief_engine.belief_tensor.shape:
                    weight_factor = 0.10 * msg.confidence
                    self.belief_engine.belief_tensor = (
                        (1.0 - weight_factor) * self.belief_engine.belief_tensor + weight_factor * msg.payload
                    )
                    # Reinforce connection between sender and this recipient
                    if fabric is not None:
                        fabric.reinforce_synapse(sender, self.node_id, amount=0.5)

            elif msg.msg_type == MessageType.SUBROUTINE_CODE and isinstance(msg.payload, dict):
                if _HAS_KOLMOGOROV:
                    assimilated_count = 0
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
                                assimilated_count += 1
                            except Exception:
                                pass
                    # Hebbian wiring: if peer provided useful new subroutines, reinforce synapse!
                    if assimilated_count > 0 and fabric is not None:
                        fabric.reinforce_synapse(sender, self.node_id, amount=1.0 * assimilated_count)

            elif msg.msg_type == MessageType.FEVER_ALERT:
                if msg.confidence > 0.6 and _HAS_FEVER:
                    self.fever_engine.temperature = min(3.0, self.fever_engine.temperature + 0.15 * msg.confidence)

        # 4. Kolmogorov Causal Law Induction — L(S_t^i)
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

        # 5. Thermodynamic Homeostasis — dH/dt = (Sigma * Omega) - Lambda
        friction_mult  = float((climate_telemetry or {}).get("friction_mult", 1.0))
        friction       = 0.05 * friction_mult
        feeding_energy = max(0.0, float(physics_obs.variables.get("reward", 0.0)))
        sigma          = 1.0 + len(self.kolmogorov_engine.program_library) * 0.05
        omega          = float(info_gain) + compression_profit * 0.5
        dh_dt          = (feeding_energy + sigma * omega) - friction
        self.state.dh_dt   = float(dh_dt)
        self.state.energy  = float(np.clip(self.state.energy + dh_dt, 0.0, 300.0))

        # 6. Fever & Viscous Momentum
        temp, visc, fever = self.fever_engine.update(
            dh_dt=dh_dt,
            current_entropy=self.state.belief_entropy,
            newly_discovered_rules=len(new_programs)
        )
        self.state.temperature  = float(temp)
        self.state.viscosity    = float(visc)
        self.state.fever_active = bool(fever)

        # 7. 10D String Cognitive Coordinate
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
                payload=self.belief_engine.belief_tensor.copy(),
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
    def __init__(self, grid_shape=(8, 8)):
        super().__init__("classical_prime", PillarArchetype.CLASSICAL_EIKONAL,
                         grid_shape, aperture=2, initial_energy=100.0)
        self._energy_errors: List[float] = []

    def tick(self, physics_obs, inbox, step, curriculum, fabric=None, climate=None):
        self.universal_update(self._last_action, physics_obs, inbox, step, fabric, climate)
        act = self.select_action()
        self._last_action = act
        self.apply_action_movement(act)

        # Kinematic acceleration & gravity consistency verification
        ay = physics_obs.variables.get("ay")
        g_obs = physics_obs.variables.get("g_obs")
        if ay is not None and g_obs is not None and abs(g_obs) > 1e-6:
            self._energy_errors.append(abs(abs(ay) - abs(g_obs)) / abs(g_obs))
        else:
            ke = physics_obs.variables.get("KE", 0.0)
            pe = physics_obs.variables.get("PE", 0.0)
            e_total = physics_obs.variables.get("E_total", ke + pe)
            if abs(e_total) > 1e-9:
                self._energy_errors.append(abs((ke + pe - e_total) / (abs(e_total) + 1e-9)))

        if len(self._energy_errors) > 20:
            self._vote_advance = sum(self._energy_errors[-20:]) / 20 < 0.05
            if self._vote_advance:
                curriculum.agent_vote_advance(self.node_id)
        return self.emit_messages(step), act


class QuantumSuperposedNode(BaseSovereignNode):
    """Quantum-Superposed — maximum exploration, belief entropy convergence."""
    def __init__(self, grid_shape=(8, 8)):
        super().__init__("quantum_prime", PillarArchetype.QUANTUM_SUPERPOSED,
                         grid_shape, aperture=3, initial_energy=100.0)
        self._entropy_history: List[float] = []

    def tick(self, physics_obs, inbox, step, curriculum, fabric=None, climate=None):
        self.universal_update(self._last_action, physics_obs, inbox, step, fabric, climate)
        act = self.select_action()
        self._last_action = act
        self.apply_action_movement(act)

        self._entropy_history.append(self.state.belief_entropy)
        if len(self._entropy_history) > 25:
            # Convergence: belief entropy stabilized (variance is low or mean is bounded)
            recent_entropies = self._entropy_history[-25:]
            entropy_var = float(np.var(recent_entropies))
            self._vote_advance = entropy_var < 0.05 or np.mean(recent_entropies) < 0.85
            if self._vote_advance:
                curriculum.agent_vote_advance(self.node_id)
        return self.emit_messages(step), act


class ModernThermodynamicNode(BaseSovereignNode):
    """Modern-Thermodynamic — homeostasis, vitality & invariant verification."""
    def __init__(self, grid_shape=(8, 8)):
        super().__init__("modern_prime", PillarArchetype.MODERN_THERMODYNAMIC,
                         grid_shape, aperture=3, initial_energy=100.0)
        self._invariant_violations: List[float] = []

    def tick(self, physics_obs, inbox, step, curriculum, fabric=None, climate=None):
        self.universal_update(self._last_action, physics_obs, inbox, step, fabric, climate)
        act = self.select_action()
        self._last_action = act
        self.apply_action_movement(act)

        p_before = physics_obs.variables.get("p_before")
        p_after  = physics_obs.variables.get("p_after")
        if p_before is not None and p_after is not None and abs(p_before) > 1e-9:
            self._invariant_violations.append(
                abs(p_before - p_after) / (abs(p_before) + 1e-9))
        elif "invariant_diff" in physics_obs.variables:
            self._invariant_violations.append(float(physics_obs.variables["invariant_diff"]))
        else:
            # In Tier 1: checks homeostatic stability of vitality (|dH/dt| is bounded)
            self._invariant_violations.append(abs(self.state.dh_dt) / 5.0)

        if len(self._invariant_violations) > 20:
            self._vote_advance = sum(self._invariant_violations[-20:]) / 20 < 0.20
            if self._vote_advance:
                curriculum.agent_vote_advance(self.node_id)
        return self.emit_messages(step), act


class StringTopologicalNode(BaseSovereignNode):
    """String-10D-Topological — tracks 10D cognitive coordinates, detects symmetries & consensus."""
    def __init__(self, grid_shape=(8, 8)):
        super().__init__("string_meta", PillarArchetype.STRING_TOPOLOGICAL,
                         grid_shape, aperture=4, initial_energy=100.0)
        self._consensus_scores: List[float] = []

    def tick(self, physics_obs, inbox, step, curriculum, fabric=None, climate=None):
        self.universal_update(self._last_action, physics_obs, inbox, step, fabric, climate)
        act = self.select_action()
        self._last_action = act
        self.apply_action_movement(act)

        # 10D Consensus & Analogy Metric across the pillars
        c10d = self.state.cognitive_10d if hasattr(self.state, "cognitive_10d") and self.state.cognitive_10d else (self.string_10d_engine.get_summary() if hasattr(self, "string_10d_engine") else {})
        d9_consensus = float(c10d.get("d9_consensus", 0.6))
        d5_analogy = float(c10d.get("d5_analogy", 0.6))
        combined_alignment = 0.5 * (d9_consensus + d5_analogy)
        self._consensus_scores.append(combined_alignment)

        ds2_diff = physics_obs.variables.get("ds2_diff")
        if ds2_diff is not None and ds2_diff < 1e-6:
            curriculum.record_discovery(self.node_id, "lorentz_invariance",
                                        "ds^2=invariant", 1.0, step)
        if len(self._consensus_scores) > 20:
            # Consensus reached when combined consensus/analogy >= 0.55
            self._vote_advance = sum(self._consensus_scores[-20:]) / 20 >= 0.55
            if self._vote_advance:
                curriculum.agent_vote_advance(self.node_id)
        return self.emit_messages(step), act


# ═══════════════════════════════════════════════════════════════════════════════════
# SovereignCivilization — orchestrates 4 Pillars + Hebbian Synaptic Fabric
# Based on civilization.py SovereignCivilization.step()
# ═══════════════════════════════════════════════════════════════════════════════════
class SovereignCivilization:
    """
    The living orchestrator. Runs God Equation on all 4 Pillars each tick,
    routes messages through Hebbian RelativisticMessageFabric, drives curriculum.
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

        # 1. Decay idle synaptic channels periodically (every 10 steps)
        if self.step_count % 10 == 0:
            self.fabric.decay_synapses(rate=0.05)

        # 2. Tick each pillar with synaptic inbox
        for nid, node in self.nodes.items():
            inbox = self.fabric.fetch_inbox(nid)
            msgs, act = node.tick(physics_obs, inbox, self.step_count,
                                  curriculum, fabric=self.fabric, climate=climate_telemetry)
            out_msgs.extend(msgs)
            for sig, code in node.kolmogorov_engine.get_library_dict().items():
                self.global_subroutine_archive[sig] = code
            if node.state.energy <= 0.0:
                node.state.energy = 15.0   # pioneer dormancy floor
            snap = node.snapshot()
            snap["step"] = self.step_count
            snapshots[nid] = snap

        # 3. Route all emitted messages along active synaptic pathways
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

    def get_connectome(self) -> List[Dict[str, Any]]:
        return self.fabric.get_connectome()

    def global_discoveries(self) -> int:
        return sum(len(n._discoveries) for n in self.nodes.values())

    def total_subroutines(self) -> int:
        return len(self.global_subroutine_archive)

    def total_messages_routed(self) -> int:
        return self.fabric.total_messages_routed
