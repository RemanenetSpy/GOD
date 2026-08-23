"""
========================================================================================
SOVEREIGN CIVILIZATION MASTER ENGINE: 10 UNIFIED ARCHITECTURES (100% REAL CODE)
========================================================================================
"S_{t+1}^i = U(S_t^i, A_t^i, O_t^i, M_t^i) + L(S_t^i)"

Integrates all 10 Sovereign Intelligence Architectures:
1. Thermodynamic Predator (dH/dt >= 0, Homeostasis)
2. Quantum Belief Superposition (|Psi> in R^{H x W x 4}, Shannon Entropy Field)
3. Kolmogorov Sovereign (Causal Transition Program Induction, Strict Deduplication)
4. Fever Annealing & Viscous Momentum (Limbic Phase Transition, Criticality)
5. Relativistic Multi-Agent Fabric (Non-blocking tensor bus M_t^i)
6. Manifold Navigator (Eikonal Geodesic Potential Wavefronts)
7. Autopoietic Crystal & Population Mitosis (Cell division, Mergers, Mortality)
8. String-Theory Meta-Agent (10D Compactified Cognitive State Space)
9. Gödel Self-Verification (Verified algorithmic compression gain)
10. Sovereign Civilization (The living whole organism)
========================================================================================
"""

import copy
import heapq
import numpy as np
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional, Any, Set

from kolmogorov_engine import KolmogorovEngine, DiscoveredProgram
from quantum_belief_engine import QuantumBeliefEngine
from fever_protocol import FeverProtocol
from autopoietic_mitosis import AutopoieticMitosisEngine
from string_dimensions import String10DCognitiveEngine


class Action(Enum):
    OBSERVE = 0
    MOVE_UP = 1
    MOVE_DOWN = 2
    MOVE_LEFT = 3
    MOVE_RIGHT = 4


class PillarArchetype(Enum):
    CLASSICAL_EIKONAL = "Classical-Eikonal"
    QUANTUM_SUPERPOSED = "Quantum-Superposed"
    MODERN_THERMODYNAMIC = "Modern-Thermodynamic"
    STRING_TOPOLOGICAL = "String-10D-Topological"
    HYBRID_META = "Hybrid-Meta-Agent"


class MessageType(Enum):
    TOPOLOGICAL_GRADIENT = "topological_grad"
    BELIEF_TENSOR = "belief_tensor"
    FEVER_ALERT = "fever_alert"
    SUBROUTINE_CODE = "subroutine_code"


@dataclass
class Message:
    sender_id: str
    recipient_id: str # 'BROADCAST' or specific agent ID
    msg_type: MessageType
    payload: Any
    confidence: float
    timestamp: int

    def summary(self) -> str:
        t_str = self.msg_type.value
        rec = "BROADCAST" if self.recipient_id == "BROADCAST" else self.recipient_id[:8]
        return f"[{self.sender_id[:10]}] -> {rec} : {t_str} (conf={self.confidence:.2f})"


class RelativisticMessageFabric:
    """Non-blocking asynchronous tensor routing fabric (M_t^i)."""
    def __init__(self):
        self.inboxes: Dict[str, List[Message]] = {}
        self.history: List[Message] = []
        self.total_messages_routed = 0

    def register_node(self, node_id: str):
        if node_id not in self.inboxes:
            self.inboxes[node_id] = []

    def unregister_node(self, node_id: str):
        if node_id in self.inboxes:
            del self.inboxes[node_id]

    def transmit(self, msg: Message):
        self.total_messages_routed += 1
        self.history.append(msg)
        if len(self.history) > 300:
            self.history.pop(0)

        if msg.recipient_id == "BROADCAST":
            for nid, box in self.inboxes.items():
                if nid != msg.sender_id:
                    box.append(msg)
        else:
            if msg.recipient_id in self.inboxes:
                self.inboxes[msg.recipient_id].append(msg)

    def fetch_inbox(self, node_id: str) -> List[Message]:
        if node_id not in self.inboxes:
            return []
        msgs = self.inboxes[node_id][:]
        self.inboxes[node_id].clear()
        return msgs


@dataclass
class Observation:
    visible_cells: np.ndarray
    position: Tuple[int, int]
    reward: float = 0.0


@dataclass
class AgentState:
    node_id: str
    pillar: PillarArchetype
    position: Tuple[int, int]
    energy: float = 100.0
    dh_dt: float = 0.0
    temperature: float = 0.1
    viscosity: float = 1.0
    belief_entropy: float = 1.0
    fever_active: bool = False
    subroutine_library: Dict[str, str] = field(default_factory=dict)
    cognitive_10d: Dict[str, Any] = field(default_factory=dict)


class BaseSovereignNode:
    """Universal Sovereign Agent governed by God Equation."""
    def __init__(
        self,
        node_id: str,
        pillar: PillarArchetype,
        grid_shape: Tuple[int, int] = (25, 25),
        aperture: int = 3,
        initial_energy: float = 120.0
    ):
        self.node_id = node_id
        self.pillar = pillar
        self.grid_shape = grid_shape
        self.h, self.w = grid_shape
        self.aperture = aperture
        
        # Core Engines
        self.belief_engine = QuantumBeliefEngine(grid_shape=grid_shape)
        self.kolmogorov_engine = KolmogorovEngine(agent_id=node_id)
        self.fever_engine = FeverProtocol(agent_id=node_id)
        self.string_10d_engine = String10DCognitiveEngine(agent_id=node_id)
        
        # State
        self.state = AgentState(
            node_id=node_id,
            pillar=pillar,
            position=(0, 0),
            energy=initial_energy
        )
        self._last_action = Action.OBSERVE
        self._last_obs: Optional[np.ndarray] = None
        self.topological_gradient: np.ndarray = np.zeros(grid_shape, dtype=np.float32)

    def universal_update(
        self,
        action: Action,
        observation: Observation,
        inbox: List[Message],
        step: int
    ):
        """
        THE GOD EQUATION OPERATOR:
        S_{t+1}^i = U(S_t^i, A_t^i, O_t^i, M_t^i) + L(S_t^i)
        """
        self.state.position = observation.position
        curr_obs = observation.visible_cells
        
        # 1. Quantum Bayesian Belief Update (|Psi>)
        info_gain = self.belief_engine.update_with_observation(
            agent_pos=self.state.position,
            aperture_radius=self.aperture,
            observed_patch=curr_obs
        )
        self.state.belief_entropy = self.belief_engine.compute_total_entropy()

        # 2. Relativistic Message Ingestion (M_t^i)
        for msg in inbox:
            if msg.msg_type == MessageType.BELIEF_TENSOR and isinstance(msg.payload, np.ndarray):
                # Fuse peer belief tensor
                if msg.payload.shape == self.belief_engine.belief_tensor.shape:
                    self.belief_engine.belief_tensor = 0.90 * self.belief_engine.belief_tensor + 0.10 * msg.payload
            elif msg.msg_type == MessageType.SUBROUTINE_CODE and isinstance(msg.payload, dict):
                # Assimilate peer subroutines
                for sig, code in msg.payload.items():
                    if sig not in self.kolmogorov_engine.program_library:
                        prog = DiscoveredProgram(
                            signature=sig,
                            code_str=code,
                            program_type="SHARED_PEER_RULE",
                            compression_gain=1.5,
                            description=f"Assimilated from {msg.sender_id}",
                            discovery_step=step
                        )
                        self.kolmogorov_engine.program_library[sig] = prog
            elif msg.msg_type == MessageType.FEVER_ALERT:
                if msg.confidence > 0.8:
                    self.fever_engine.temperature = min(3.0, self.fever_engine.temperature + 0.2)

        # 3. Kolmogorov Learning Operator L(S_t^i) - Causal Rule Induction
        new_programs = self.kolmogorov_engine.induce_causal_laws(
            prev_obs=self._last_obs,
            curr_obs=curr_obs,
            step=step
        )
        self._last_obs = curr_obs.copy() if curr_obs is not None else None
        
        # Compression profit from newly discovered unique laws
        compression_profit = sum(p.compression_gain for p in new_programs)

        # 4. Thermodynamic Homeostasis Update (dH/dt = (Sigma * Omega) - Lambda)
        friction = 0.05 # Sustainable metabolic base burn (2000 steps baseline)
        feeding_energy = max(0.0, observation.reward)
        sigma = 1.0 + len(self.kolmogorov_engine.program_library) * 0.05
        omega = info_gain + (compression_profit * 0.5)
        
        dh_dt = (feeding_energy + (sigma * omega)) - friction
        self.state.dh_dt = float(dh_dt)
        self.state.energy = float(np.clip(self.state.energy + dh_dt, 0.0, 300.0))

        # 5. Fever & Viscous Momentum Update
        temp, visc, fever = self.fever_engine.update(
            dh_dt=dh_dt,
            current_entropy=self.state.belief_entropy,
            newly_discovered_rules=len(new_programs)
        )
        self.state.temperature = float(temp)
        self.state.viscosity = float(visc)
        self.state.fever_active = bool(fever)

        # 6. 10D String Cognitive Coordinate Update
        self.string_10d_engine.update_state(
            pos=self.state.position,
            step=step,
            temperature=self.state.temperature,
            subroutine_count=len(self.kolmogorov_engine.program_library),
            entropy=self.state.belief_entropy,
            energy=self.state.energy,
            consensus_strength=1.0 - (self.state.belief_entropy / 2.0)
        )
        self.state.cognitive_10d = self.string_10d_engine.get_summary()
        self.state.subroutine_library = self.kolmogorov_engine.get_library_dict()

    def select_action(self, observation: Observation) -> Action:
        """Action selection balancing Eikonal geodesics, quantum curiosity, and Fever."""
        py, px = observation.position
        
        # High Fever: Stochastic Brownian exploration (melts rigid lock)
        if self.state.fever_active or self.state.temperature > 1.5:
            return np.random.choice([
                Action.MOVE_UP, Action.MOVE_DOWN, Action.MOVE_LEFT, Action.MOVE_RIGHT, Action.OBSERVE
            ])

        # Compute Potential Cost Matrix
        # Potential Field = (1 - Life_Belief) * 3.0 + Entropy * 2.0
        nutrient_map = self.belief_engine.get_nutrient_belief_field()
        entropy_map = self.belief_engine.get_entropy_field()
        cost_grid = (1.0 - nutrient_map) * 3.0 + entropy_map * 2.0

        # Eikonal Geodesic Action Selection (Lowest neighboring potential)
        best_act = Action.OBSERVE
        best_val = cost_grid[py, px]

        candidates = [
            (Action.MOVE_UP, py - 1, px),
            (Action.MOVE_DOWN, py + 1, px),
            (Action.MOVE_LEFT, py, px - 1),
            (Action.MOVE_RIGHT, py, px + 1),
        ]

        for act, ny, nx in candidates:
            if 0 <= ny < self.h and 0 <= nx < self.w:
                val = cost_grid[ny, nx]
                if val < best_val:
                    best_val = val
                    best_act = act

        return best_act

    def emit_messages(self, step: int) -> List[Message]:
        """Emits relativistic messages to peers."""
        msgs = []
        # Broadcast belief tensor if high certainty
        if self.state.energy > 80.0:
            msgs.append(Message(
                sender_id=self.node_id,
                recipient_id="BROADCAST",
                msg_type=MessageType.BELIEF_TENSOR,
                payload=self.belief_engine.belief_tensor,
                confidence=0.85,
                timestamp=step
            ))

        # Broadcast newly discovered subroutines
        if self.kolmogorov_engine.program_library:
            msgs.append(Message(
                sender_id=self.node_id,
                recipient_id="BROADCAST",
                msg_type=MessageType.SUBROUTINE_CODE,
                payload=self.kolmogorov_engine.get_library_dict(),
                confidence=0.95,
                timestamp=step
            ))

        # Broadcast Fever alert if in crisis
        if self.state.fever_active:
            msgs.append(Message(
                sender_id=self.node_id,
                recipient_id="BROADCAST",
                msg_type=MessageType.FEVER_ALERT,
                payload={"temperature": self.state.temperature},
                confidence=0.90,
                timestamp=step
            ))

        return msgs


class SovereignCivilization:
    """Master Orchestrator of the Sovereign Relativistic Multi-Agent Civilization."""
    def __init__(
        self,
        grid_shape: Tuple[int, int] = (25, 25),
        max_population: int = 10,
        enable_cyclic_pruning: bool = False
    ):
        self.grid_shape = grid_shape
        self.max_population = max_population
        self.enable_cyclic_pruning = enable_cyclic_pruning
        self.fabric = RelativisticMessageFabric()
        self.mitosis_engine = AutopoieticMitosisEngine(max_population=max_population)
        self.step_count = 0
        self.steps_since_last_discovery = 0
        self.last_archive_size = 0
        self.global_subroutine_archive: Dict[str, str] = {}
        self.pruning_events: List[str] = []
        
        # Initialize 4 Sovereign Pillars
        self.nodes: Dict[str, BaseSovereignNode] = {
            "classical_prime": BaseSovereignNode("classical_prime", PillarArchetype.CLASSICAL_EIKONAL, grid_shape=grid_shape, aperture=2),
            "quantum_prime": BaseSovereignNode("quantum_prime", PillarArchetype.QUANTUM_SUPERPOSED, grid_shape=grid_shape, aperture=3),
            "modern_prime": BaseSovereignNode("modern_prime", PillarArchetype.MODERN_THERMODYNAMIC, grid_shape=grid_shape, aperture=3),
            "string_meta": BaseSovereignNode("string_meta", PillarArchetype.STRING_TOPOLOGICAL, grid_shape=grid_shape, aperture=4),
        }
        
        for nid in self.nodes:
            self.fabric.register_node(nid)

    def _reseed_pioneers(self):
        self.nodes = {
            "classical_prime": BaseSovereignNode("classical_prime", PillarArchetype.CLASSICAL_EIKONAL, grid_shape=self.grid_shape, aperture=2, initial_energy=120.0),
            "quantum_prime": BaseSovereignNode("quantum_prime", PillarArchetype.QUANTUM_SUPERPOSED, grid_shape=self.grid_shape, aperture=3, initial_energy=120.0),
            "modern_prime": BaseSovereignNode("modern_prime", PillarArchetype.MODERN_THERMODYNAMIC, grid_shape=self.grid_shape, aperture=3, initial_energy=120.0),
            "string_meta": BaseSovereignNode("string_meta", PillarArchetype.STRING_TOPOLOGICAL, grid_shape=self.grid_shape, aperture=4, initial_energy=120.0),
        }
        for nid in self.nodes:
            self.fabric.register_node(nid)

    def step(self, observations: Optional[Dict[str, Observation]] = None) -> Dict[str, Action]:
        self.step_count += 1
        actions: Dict[str, Action] = {}
        out_msgs: List[Message] = []

        if observations is None:
            observations = {}
            for aid, node in self.nodes.items():
                dummy_vis = np.random.choice([0, 1, 2], size=(node.aperture*2+1, node.aperture*2+1), p=[0.75, 0.20, 0.05])
                observations[aid] = Observation(visible_cells=dummy_vis, position=node.state.position, reward=0.5)

        # 1. Update Each Node via Universal God Equation
        dead_nodes = []
        for aid, node in list(self.nodes.items()):
            obs = observations.get(aid, Observation(np.zeros((3, 3)), node.state.position))
            inbox = self.fabric.fetch_inbox(aid)
            
            # Universal Update
            node.universal_update(node._last_action, obs, inbox, self.step_count)
            act = node.select_action(obs)
            node._last_action = act
            actions[aid] = act
            
            # Collect messages
            out_msgs.extend(node.emit_messages(self.step_count))
            
            # Archive subroutines globally
            for sig, code in node.kolmogorov_engine.get_library_dict().items():
                self.global_subroutine_archive[sig] = code

            # Check Mortality (H <= 0) for non-pioneer offspring nodes
            is_pioneer = aid in ["classical_prime", "quantum_prime", "modern_prime", "string_meta"]
            if not is_pioneer and self.mitosis_engine.check_mortality(aid, node.state.energy):
                dead_nodes.append(aid)
            elif is_pioneer and node.state.energy <= 0.0:
                # Pioneer enters metabolic torpor / dormancy floor
                node.state.energy = 15.0

        # Remove dead offspring nodes
        for dead_id in dead_nodes:
            if dead_id in self.nodes:
                del self.nodes[dead_id]
                self.fabric.unregister_node(dead_id)

        # Genesis: If all nodes perished, re-seed the 4 pioneer pillars
        if len(self.nodes) == 0:
            self._reseed_pioneers()

        # 2. Check for Mitosis / Reproduction (H == 300.0)
        for aid, node in list(self.nodes.items()):
            spawn_info = self.mitosis_engine.check_mitosis(
                node_id=aid,
                energy=node.state.energy,
                subroutine_count=len(node.kolmogorov_engine.program_library),
                position=node.state.position,
                current_pop=len(self.nodes)
            )
            if spawn_info:
                child_id = spawn_info["offspring_id"]
                node.state.energy -= spawn_info["energy_cost"]
                
                # Spawn child inheriting parent's wisdom with mutated aperture
                child_aperture = max(2, min(5, node.aperture + np.random.choice([-1, 0, 1])))
                child_node = BaseSovereignNode(
                    node_id=child_id,
                    pillar=PillarArchetype.HYBRID_META,
                    grid_shape=self.grid_shape,
                    aperture=child_aperture,
                    initial_energy=spawn_info["energy_cost"]
                )
                # Inherit parent programs
                for sig, p in node.kolmogorov_engine.program_library.items():
                    child_node.kolmogorov_engine.program_library[sig] = copy.deepcopy(p)
                    
                self.nodes[child_id] = child_node
                self.fabric.register_node(child_id)

        # 3. Route All Messages
        for msg in out_msgs:
            self.fabric.transmit(msg)

        # 4. Saturation Tracking & Cyclic Pruning Protocol
        current_size = len(self.global_subroutine_archive)
        if current_size > self.last_archive_size:
            self.steps_since_last_discovery = 0
            self.last_archive_size = current_size
        else:
            self.steps_since_last_discovery += 1

        if self.enable_cyclic_pruning and self.global_subroutine_archive:
            # When saturated for >= 1500 steps (24 mixing cycles), prune oldest rule every 500 steps
            if self.steps_since_last_discovery >= 1500 and self.step_count % 500 == 0:
                oldest_sig = next(iter(self.global_subroutine_archive))
                del self.global_subroutine_archive[oldest_sig]
                for n in self.nodes.values():
                    if oldest_sig in n.kolmogorov_engine.program_library:
                        del n.kolmogorov_engine.program_library[oldest_sig]
                self.last_archive_size = len(self.global_subroutine_archive)
                event_msg = f"🗑️ PRUNED: [{oldest_sig}] evicted to force rediscovery (Stagnant: {self.steps_since_last_discovery} steps)"
                self.pruning_events.append(event_msg)
                if len(self.pruning_events) > 50:
                    self.pruning_events.pop(0)

        return actions

    def synthesize_consensus(self) -> np.ndarray:
        """Synthesizes collective consciousness belief tensor field."""
        consensus = np.zeros((*self.grid_shape, 4), dtype=np.float32)
        tot_w = 0.0
        for node in self.nodes.values():
            w = node.state.energy / (node.state.temperature + 0.1)
            consensus += w * node.belief_engine.belief_tensor
            tot_w += w
        return consensus / tot_w if tot_w > 0 else consensus
