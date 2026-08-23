"""
========================================================================================
SOVEREIGN CIVILIZATION: Multi-Agent Relativistic Society & Tensor Communication
========================================================================================

Implements the complete Multi-Agent Phase 6 "God Equation" from plan.txt:
    S_{t+1}^i = U(S_t^i, A_t^i, O_t^i, M_t^i) + L(S_t^i)

Where:
    - S_t^i: State of Sovereign Agent i (Beliefs B_t^i, Frame F_t^i, World Model W_t^i)
    - A_t^i: Action executed by agent i
    - O_t^i: Relativistic observation observed by agent i through its Frame F_t^i
    - M_t^i: Tensor message packet received from all other agents in the civilization
    - U(...): Universal update rule fusing quantum beliefs, relativistic frames, and messages
    - L(...): Autopoietic self-modification & Kolmogorov compression learning operator

The Four Relativistic Sovereign Pillars:
    1. CLASSICAL NODE   (Physics / Geodesic / Eikonal Potential Field)
    2. QUANTUM NODE     (Superposition / Multi-Future Probability Waves)
    3. MODERN NODE      (Metabolic Viability / dH/dt / Fever Annealing Protocol)
    4. STRING META-NODE (Compactified Dimensions / Kolmogorov Compression / Analogies)

All agents communicate over a non-blocking relativistic tensor fabric M_t^i.
========================================================================================
"""

import math
import copy
import time
import numpy as np
from typing import Dict, List, Tuple, Optional, Any, Set, Union
from dataclasses import dataclass, field
from enum import Enum

from environment import Action, Observation, CellType


# ======================================================================================
# 1. MESSAGE FABRIC & COMMUNICATION PROTOCOL (M_t^i)
# ======================================================================================

class MessageType(Enum):
    """Types of tensor payloads transmitted in M_t^i."""
    BELIEF_TENSOR = "belief_tensor"             # Probability distribution over states
    TOPOLOGICAL_GRADIENT = "topological_grad"   # Eikonal geodesic / potential field
    METABOLIC_BURST = "metabolic_burst"         # High dH/dt energy release notification
    SUBROUTINE_CODE = "subroutine_code"         # Reusable Kolmogorov-compressed subroutine
    FEVER_ALERT = "fever_alert"                 # Phase transition / limbic destabilization
    HYPOTHESIS_SUPERPOSITION = "hypothesis_sup" # Quantum multi-world conjecture
    ANALOGY_BRIDGE = "analogy_bridge"           # Higher-dimensional topological transfer


class PillarArchetype(Enum):
    """The Four Fundamental Sovereign Mindsets."""
    CLASSICAL = "Classical-Physics"   # Determinism, Eikonal navigation, Geodesics
    QUANTUM = "Quantum-Superposed"    # Superposition, Multi-world probabilities
    MODERN = "Modern-Thermodynamic"   # dH/dt, Attention viscosity, Fever annealing
    STRING_META = "String-Topological"# Compactified dimensions, Kolmogorov compression


@dataclass
class Message:
    """
    Tensor message packet M_t^(j -> i) exchanged between sovereign agents.
    
    Carries mathematical field tensors, subroutines, or phase alerts with subjective
    Bayesian confidence and information entropy.
    """
    sender_id: str
    recipient_id: str                          # Specific agent_id or "BROADCAST"
    pillar: PillarArchetype
    timestamp: int                             # Step index t
    msg_type: MessageType
    payload: Any                               # Numpy array, code string, or scalar
    confidence: float = 1.0                    # Sender's conviction [0.0, 1.0]
    entropy: float = 0.0                       # Information entropy of the message
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_string(self) -> str:
        return f"[{self.pillar.value} | {self.sender_id} -> {self.recipient_id}] {self.msg_type.value} (conf={self.confidence:.2f}, H={self.entropy:.2f})"


class RelativisticMessageFabric:
    """
    The Relativistic Communication Substrate.
    
    Routes messages between agents, applies relativistic frame transformations,
    and manages non-blocking message queues M_t^i.
    """
    def __init__(self, noise_level: float = 0.0):
        self.noise_level = noise_level
        self.inboxes: Dict[str, List[Message]] = {}
        self.history: List[Message] = []
        self.total_messages_routed: int = 0

    def register_agent(self, agent_id: str):
        if agent_id not in self.inboxes:
            self.inboxes[agent_id] = []

    def transmit(self, message: Message):
        """Transmit a message into the fabric."""
        self.history.append(message)
        self.total_messages_routed += 1
        
        if message.recipient_id == "BROADCAST":
            for agent_id, inbox in self.inboxes.items():
                if agent_id != message.sender_id:
                    inbox.append(message)
        else:
            if message.recipient_id in self.inboxes:
                self.inboxes[message.recipient_id].append(message)

    def fetch_inbox(self, agent_id: str) -> List[Message]:
        """Fetch and clear M_t^i for a specific agent."""
        if agent_id not in self.inboxes:
            return []
        messages = self.inboxes[agent_id]
        self.inboxes[agent_id] = []
        return messages

    def clear(self):
        self.inboxes = {k: [] for k in self.inboxes}
        self.history.clear()
        self.total_messages_routed = 0


# ======================================================================================
# 2. SOVEREIGN NODE: BASE AGENT ARCHITECTURE (S_t^i)
# ======================================================================================

@dataclass
class SovereignState:
    """Unified internal state S_t^i."""
    agent_id: str
    pillar: PillarArchetype
    step: int = 0
    energy: float = 100.0                      # Metabolic vitality H
    dh_dt: float = 0.0                         # Metabolic velocity (compression/reward rate)
    temperature: float = 0.1                   # Thermodynamic fever temperature
    viscosity: float = 1.0                     # Attention viscosity
    divergence: float = 1.0                    # Epistemic divergence / error
    belief_entropy: float = 1.0                # Shannon entropy of internal beliefs
    position: Tuple[int, int] = (0, 0)
    subroutine_library: Dict[str, str] = field(default_factory=dict) # Discovered MDL code
    active_hypotheses: List[Dict[str, Any]] = field(default_factory=list)


class SovereignNode:
    """
    Base Sovereign Intelligence Organism implementing:
        S_{t+1}^i = U(S_t^i, A_t^i, O_t^i, M_t^i) + L(S_t^i)
    """
    def __init__(
        self,
        agent_id: str,
        pillar: PillarArchetype,
        grid_shape: Tuple[int, int] = (15, 15),
        aperture: int = 3,
        sensor_noise: float = 0.05
    ):
        self.agent_id = agent_id
        self.pillar = pillar
        self.grid_shape = grid_shape
        self.aperture = aperture
        self.sensor_noise = sensor_noise
        
        # Internal Sovereign State S_t^i
        self.state = SovereignState(agent_id=agent_id, pillar=pillar)
        
        # Belief Map B_t^i (Quantum-probabilistic grid distribution)
        # Dimensions: [Height, Width, NumChannels] -> (Empty, Resource, Obstacle, Unknown)
        self.belief_field = np.ones((*grid_shape, 4), dtype=np.float32) * 0.25
        
        # Continuous Potential Field \Phi(x) (Eikonal / Geodesic / Novelty)
        self.potential_field = np.zeros(grid_shape, dtype=np.float32)
        
        # Historical Trace
        self.observation_trace: List[Observation] = []
        self.message_trace: List[Message] = []
        
        # Stagnation & Fever Tracking
        self.divergence_history: List[float] = []
        self.stagnation_counter: int = 0
        self.fever_active: bool = False

    # ----------------------------------------------------------------------------------
    # GOD EQUATION COMPONENT 1: BeliefUpdate(B_t^i, O_t^i, M_t^i)
    # ----------------------------------------------------------------------------------
    def update_beliefs(self, observation: Observation, messages: List[Message]) -> np.ndarray:
        """
        Fuses sensory observation O_t^i and multi-agent message tensor M_t^i.
        Quantum-inspired Bayesian superposition update.
        """
        pos = observation.position
        self.state.position = pos
        h, w = self.grid_shape
        
        # 1. Local Sensory Assimilation (Aperture window)
        r = self.aperture
        y_min, y_max = max(0, pos[0] - r), min(h, pos[0] + r + 1)
        x_min, x_max = max(0, pos[1] - r), min(w, pos[1] + r + 1)
        
        vis = observation.visible_cells
        if vis is not None and vis.size > 0:
            # Map visible cell integers into one-hot probabilities
            for cy in range(y_min, y_max):
                for cx in range(x_min, x_max):
                    vy, vx = cy - (pos[0] - r), cx - (pos[1] - r)
                    if 0 <= vy < vis.shape[0] and 0 <= vx < vis.shape[1]:
                        cell_val = vis[vy, vx]
                        target_channel = int(cell_val) if 0 <= cell_val < 3 else 3
                        
                        # Apply sensor noise relaxation
                        prior = self.belief_field[cy, cx]
                        likelihood = np.ones(4) * (self.sensor_noise / 3.0)
                        likelihood[target_channel] = 1.0 - self.sensor_noise
                        
                        # Bayesian product + normalization
                        posterior = prior * likelihood
                        s = posterior.sum()
                        self.belief_field[cy, cx] = posterior / s if s > 0 else prior

        # 2. Multi-Agent Message Assimilation M_t^i
        for msg in messages:
            if msg.msg_type == MessageType.BELIEF_TENSOR and isinstance(msg.payload, np.ndarray):
                # Fuse external belief tensor with confidence weighting
                ext_tensor = msg.payload
                if ext_tensor.shape == self.belief_field.shape:
                    alpha = msg.confidence * 0.4  # Message coupling strength
                    self.belief_field = (1.0 - alpha) * self.belief_field + alpha * ext_tensor
                    
            elif msg.msg_type == MessageType.TOPOLOGICAL_GRADIENT and isinstance(msg.payload, np.ndarray):
                # Fuse external Eikonal potential field
                if msg.payload.shape == self.potential_field.shape:
                    self.potential_field = 0.6 * self.potential_field + 0.4 * msg.payload

            elif msg.msg_type == MessageType.SUBROUTINE_CODE:
                # Code reuse: absorb external Kolmogorov subroutine
                code_sig = msg.metadata.get("signature", f"sub_{len(self.state.subroutine_library)}")
                self.state.subroutine_library[code_sig] = str(msg.payload)

            elif msg.msg_type == MessageType.FEVER_ALERT:
                # Collective limbic excitation
                if msg.confidence > 0.7:
                    self.state.temperature = min(2.0, self.state.temperature + 0.3)

        # Compute Shannon entropy of the belief field
        probs = np.clip(self.belief_field, 1e-7, 1.0)
        self.state.belief_entropy = float(-np.sum(probs * np.log2(probs)) / (h * w))
        return self.belief_field

    # ----------------------------------------------------------------------------------
    # GOD EQUATION COMPONENT 2: FrameUpdate(F_t^i, A_t^i, O_t^i)
    # ----------------------------------------------------------------------------------
    def update_frame(self, action: Action, observation: Observation):
        """Update relativistic perspective and attention viscosity."""
        self.observation_trace.append(observation)
        if len(self.observation_trace) > 100:
            self.observation_trace.pop(0)
            
        # Update divergence derivative d(Div)/dt
        old_div = self.state.divergence
        # Compute divergence as uncertainty + distance to nearest unexplored cell
        entropy_factor = self.state.belief_entropy
        new_div = float(entropy_factor + (1.0 / (1.0 + observation.reward)))
        self.state.divergence = new_div
        
        div_derivative = abs(new_div - old_div)
        self.divergence_history.append(new_div)
        if len(self.divergence_history) > 20:
            self.divergence_history.pop(0)

        # Update Attention Viscosity
        # Viscosity is high when learning is actively occurring (high derivative)
        self.state.viscosity = float(div_derivative / (self.state.temperature + 1e-4))

        # Thermodynamic Stagnation Detector (Triggers Fever)
        if len(self.divergence_history) >= 10:
            std = float(np.std(self.divergence_history[-10:]))
            if std < 0.02 and new_div > 0.5:
                self.stagnation_counter += 1
            else:
                self.stagnation_counter = max(0, self.stagnation_counter - 1)
                
            if self.stagnation_counter >= 5:
                self.trigger_fever()
            elif self.fever_active and std > 0.1:
                self.cool_down()

    # ----------------------------------------------------------------------------------
    # GOD EQUATION COMPONENT 3: WorldModelUpdate(W_t^i, B_{t+1}^i) & Thermodynamics
    # ----------------------------------------------------------------------------------
    def update_world_model(self):
        """Update continuous potential fields and metabolic energy."""
        # Calculate dH/dt (Metabolic Compression / Viability Rate)
        # Gaining energy when entropy drops or reward arrives; burning energy during stagnation
        entropy_delta = 0.0
        if len(self.observation_trace) >= 2:
            entropy_delta = float(self.observation_trace[-2].reward - self.observation_trace[-1].reward)
            
        compression_profit = max(0.0, float(len(self.state.subroutine_library) * 0.5))
        self.state.dh_dt = float(compression_profit - (self.state.temperature * 0.2) + entropy_delta)
        
        # Update metabolic energy
        self.state.energy = max(0.0, min(200.0, self.state.energy + self.state.dh_dt))

    # ----------------------------------------------------------------------------------
    # GOD EQUATION COMPONENT 4: LearningOperator L(S_t^i) (Self-Modification)
    # ----------------------------------------------------------------------------------
    def self_modify(self):
        """Autopoietic adaptation of internal structures based on compression gains."""
        # If energy is abundant, expand sensory aperture
        if self.state.energy > 150.0 and self.aperture < 6:
            self.aperture += 1
            self.state.energy -= 10.0
        # If starved, constrict aperture to save computational heat
        elif self.state.energy < 30.0 and self.aperture > 2:
            self.aperture -= 1

    # ----------------------------------------------------------------------------------
    # GOD EQUATION MASTER UPDATE: S_{t+1}^i = U(S_t^i, A_t^i, O_t^i, M_t^i) + L(S_t^i)
    # ----------------------------------------------------------------------------------
    def universal_update(
        self,
        action: Action,
        observation: Observation,
        messages: List[Message]
    ) -> SovereignState:
        """The Master God Equation Update."""
        self.state.step += 1
        
        # 1. Belief Update with Quantum Collapse & Message Fusion
        self.update_beliefs(observation, messages)
        
        # 2. Relativistic Frame Update
        self.update_frame(action, observation)
        
        # 3. World Model & Thermodynamic Update
        self.update_world_model()
        
        # 4. Learning & Self-Modification Operator L(S_t)
        self.self_modify()
        
        return self.state

    # ----------------------------------------------------------------------------------
    # FEVER & METABOLIC PHASE SHIFTS
    # ----------------------------------------------------------------------------------
    def trigger_fever(self):
        """Metabolic Annealing: System Temperature Spikes to break local minima."""
        self.fever_active = True
        self.state.temperature = min(3.0, self.state.temperature + 0.8)
        self.stagnation_counter = 0

    def cool_down(self):
        """System cools into crystallized order upon finding a new gradient."""
        self.fever_active = False
        self.state.temperature = max(0.05, self.state.temperature * 0.5)

    # ----------------------------------------------------------------------------------
    # ABSTRACT INTERFACES (Specialized by Pillars)
    # ----------------------------------------------------------------------------------
    def compute_potential_field(self) -> np.ndarray:
        raise NotImplementedError

    def select_action(self, observation: Observation) -> Action:
        raise NotImplementedError

    def emit_messages(self, timestamp: int) -> List[Message]:
        raise NotImplementedError


# ======================================================================================
# 3. THE FOUR SPECIALIZED SOVEREIGN PILLARS
# ======================================================================================

class ClassicalPhysicsNode(SovereignNode):
    """
    PILLAR 1: CLASSICAL PHYSICS AGENT
    - Specialization: Continuous Eikonal wave propagation, geodesic paths, deterministic mechanics.
    - Mathematical Core: Solves |∇T(x)| = n(x) for global minimum-time navigation.
    """
    def __init__(self, agent_id: str, grid_shape: Tuple[int, int] = (15, 15)):
        super().__init__(agent_id, PillarArchetype.CLASSICAL, grid_shape, aperture=3)

    def compute_potential_field(self) -> np.ndarray:
        """Solves Eikonal wave equation (Fast Marching / Dijkstra continuous potential)."""
        h, w = self.grid_shape
        # Refractive index n(x): Obstacle probability = high index (infinite resistance)
        obstacle_prob = self.belief_field[:, :, 2]
        resource_prob = self.belief_field[:, :, 1]
        unknown_prob = self.belief_field[:, :, 3]
        
        # Speed field v(x) = 1 / n(x)
        cost_field = 1.0 + obstacle_prob * 50.0 - resource_prob * 5.0 - unknown_prob * 2.0
        cost_field = np.clip(cost_field, 0.1, 100.0)
        
        # Initialize geodesic distances
        dist = np.ones((h, w), dtype=np.float32) * 1e5
        
        # Target: find highest resource or highest unexplored cell
        target_y, target_x = np.unravel_index(np.argmax(resource_prob + unknown_prob * 0.5), (h, w))
        dist[target_y, target_x] = 0.0
        
        # Continuous Dijkstra Wavefront Relaxation (FMM approximation)
        unvisited = set((y, x) for y in range(h) for x in range(w))
        while unvisited:
            # Pick minimum unvisited
            current = min(unvisited, key=lambda p: dist[p[0], p[1]])
            if dist[current[0], current[1]] >= 1e4:
                break
            unvisited.remove(current)
            cy, cx = current
            
            for dy, dx in [(-1,0), (1,0), (0,-1), (0,1)]:
                ny, nx = cy + dy, cx + dx
                if 0 <= ny < h and 0 <= nx < w and (ny, nx) in unvisited:
                    step_cost = float(cost_field[ny, nx])
                    if dist[cy, cx] + step_cost < dist[ny, nx]:
                        dist[ny, nx] = dist[cy, cx] + step_cost
                        
        self.potential_field = dist
        return dist

    def select_action(self, observation: Observation) -> Action:
        """Follows steepest descent -∇Φ_eikonal."""
        self.compute_potential_field()
        cy, cx = observation.position
        h, w = self.grid_shape
        
        best_action = Action.WAIT
        best_pot = float(self.potential_field[cy, cx])
        
        moves = [
            (Action.MOVE_UP, cy - 1, cx),
            (Action.MOVE_DOWN, cy + 1, cx),
            (Action.MOVE_LEFT, cy, cx - 1),
            (Action.MOVE_RIGHT, cy, cx + 1),
        ]
        
        for act, ny, nx in moves:
            if 0 <= ny < h and 0 <= nx < w:
                pot = float(self.potential_field[ny, nx])
                # Thermal fluctuation injection during fever
                noise = np.random.normal(0, self.state.temperature * 0.5)
                if pot + noise < best_pot:
                    best_pot = pot + noise
                    best_action = act
                    
        return best_action if best_action != Action.WAIT else Action.OBSERVE

    def emit_messages(self, timestamp: int) -> List[Message]:
        """Broadcasts global geodesic potential field to the civilization."""
        msg = Message(
            sender_id=self.agent_id,
            recipient_id="BROADCAST",
            pillar=self.pillar,
            timestamp=timestamp,
            msg_type=MessageType.TOPOLOGICAL_GRADIENT,
            payload=self.potential_field.copy(),
            confidence=0.85,
            entropy=float(np.std(self.potential_field))
        )
        return [msg]


class QuantumBeliefNode(SovereignNode):
    """
    PILLAR 2: QUANTUM BELIEF AGENT
    - Specialization: Superposition of world states, interference patterns, hypothesis collapse.
    - Mathematical Core: |Ψ⟩ = Σ α_i |W_i⟩; collapses probabilities based on multi-agent consensus.
    """
    def __init__(self, agent_id: str, grid_shape: Tuple[int, int] = (15, 15), num_branches: int = 8):
        super().__init__(agent_id, PillarArchetype.QUANTUM, grid_shape, aperture=4)
        self.num_branches = num_branches
        # Superposed world hypothesis branches
        self.superposition_branches: List[np.ndarray] = [
            np.random.dirichlet(np.ones(4), size=grid_shape).astype(np.float32)
            for _ in range(num_branches)
        ]
        self.branch_amplitudes = np.ones(num_branches, dtype=np.float32) / num_branches

    def compute_potential_field(self) -> np.ndarray:
        """Constructive and destructive interference of superposed belief branches."""
        # Expected belief = Σ |α_k|² · B_k
        weighted_sum = np.zeros((*self.grid_shape, 4), dtype=np.float32)
        for amp, branch in zip(self.branch_amplitudes, self.superposition_branches):
            weighted_sum += amp * branch
            
        self.belief_field = weighted_sum
        # Potential field = quantum uncertainty map (drives epistemic curiosity)
        uncertainty = -np.sum(weighted_sum * np.log2(np.clip(weighted_sum, 1e-6, 1.0)), axis=-1)
        self.potential_field = uncertainty.astype(np.float32)
        return self.potential_field

    def select_action(self, observation: Observation) -> Action:
        """Explores maximum quantum uncertainty (epistemic value maximization)."""
        self.compute_potential_field()
        cy, cx = observation.position
        h, w = self.grid_shape
        
        # Seek highest uncertainty
        best_act = Action.OBSERVE
        max_uncertainty = -1.0
        
        moves = [
            (Action.MOVE_UP, cy - 1, cx),
            (Action.MOVE_DOWN, cy + 1, cx),
            (Action.MOVE_LEFT, cy, cx - 1),
            (Action.MOVE_RIGHT, cy, cx + 1),
            (Action.OBSERVE, cy, cx)
        ]
        
        for act, ny, nx in moves:
            if 0 <= ny < h and 0 <= nx < w:
                u = float(self.potential_field[ny, nx])
                if u > max_uncertainty:
                    max_uncertainty = u
                    best_act = act
                    
        return best_act

    def emit_messages(self, timestamp: int) -> List[Message]:
        """Broadcasts superposed belief distribution and quantum uncertainty."""
        msg = Message(
            sender_id=self.agent_id,
            recipient_id="BROADCAST",
            pillar=self.pillar,
            timestamp=timestamp,
            msg_type=MessageType.BELIEF_TENSOR,
            payload=self.belief_field.copy(),
            confidence=float(1.0 - self.state.belief_entropy * 0.3),
            entropy=self.state.belief_entropy
        )
        return [msg]


class ModernMetabolicNode(SovereignNode):
    """
    PILLAR 3: MODERN THERMODYNAMIC AGENT
    - Specialization: Homeostasis, dH/dt metabolism, attention viscosity, Fever Annealing protocol.
    - Mathematical Core: Thermodynamic predator optimizing free energy and surviving starvation.
    """
    def __init__(self, agent_id: str, grid_shape: Tuple[int, int] = (15, 15)):
        super().__init__(agent_id, PillarArchetype.MODERN, grid_shape, aperture=2)

    def compute_potential_field(self) -> np.ndarray:
        """Computes metabolic survival landscape (Hazard repulsion + Resource attraction)."""
        h, w = self.grid_shape
        hazard = self.belief_field[:, :, 2] * 20.0
        resource = self.belief_field[:, :, 1] * 10.0
        
        # Energy gradient
        self.potential_field = (hazard - resource).astype(np.float32)
        return self.potential_field

    def select_action(self, observation: Observation) -> Action:
        """Balances resource ingestion with thermal fever exploration."""
        cy, cx = observation.position
        h, w = self.grid_shape
        
        # If in fever state: radical random exploration to break stagnation
        if self.fever_active or self.state.temperature > 1.0:
            actions = [Action.MOVE_UP, Action.MOVE_DOWN, Action.MOVE_LEFT, Action.MOVE_RIGHT, Action.OBSERVE]
            return np.random.choice(actions)
            
        # Normal state: seek food / resources
        resource_grid = self.belief_field[:, :, 1]
        best_act = Action.WAIT
        best_val = -100.0
        
        moves = [
            (Action.MOVE_UP, cy - 1, cx),
            (Action.MOVE_DOWN, cy + 1, cx),
            (Action.MOVE_LEFT, cy, cx - 1),
            (Action.MOVE_RIGHT, cy, cx + 1),
            (Action.INTERACT, cy, cx)
        ]
        
        for act, ny, nx in moves:
            if 0 <= ny < h and 0 <= nx < w:
                val = float(resource_grid[ny, nx] - self.belief_field[ny, nx, 2] * 5.0)
                if val > best_val:
                    best_val = val
                    best_act = act
                    
        return best_act if best_act != Action.WAIT else Action.OBSERVE

    def emit_messages(self, timestamp: int) -> List[Message]:
        """Emits metabolic burst or fever notifications when phase transitions occur."""
        messages = []
        if self.fever_active:
            messages.append(Message(
                sender_id=self.agent_id,
                recipient_id="BROADCAST",
                pillar=self.pillar,
                timestamp=timestamp,
                msg_type=MessageType.FEVER_ALERT,
                payload=self.state.temperature,
                confidence=0.9,
                entropy=self.state.divergence
            ))
        if self.state.dh_dt > 0.5:
            messages.append(Message(
                sender_id=self.agent_id,
                recipient_id="BROADCAST",
                pillar=self.pillar,
                timestamp=timestamp,
                msg_type=MessageType.METABOLIC_BURST,
                payload=self.state.dh_dt,
                confidence=0.8,
                entropy=0.1
            ))
        return messages


class StringMetaNode(SovereignNode):
    """
    PILLAR 4: STRING META-AGENT
    - Specialization: Higher compactified dimensions, Kolmogorov complexity compression, analogical transfer.
    - Mathematical Core: Solves for minimal program length K(X) and mints reusable subroutines.
    """
    def __init__(self, agent_id: str, grid_shape: Tuple[int, int] = (15, 15)):
        super().__init__(agent_id, PillarArchetype.STRING_META, grid_shape, aperture=5)
        self.subroutine_counter = 0

    def compute_potential_field(self) -> np.ndarray:
        """Measures Kolmogorov compressibility map across the spatial manifold."""
        h, w = self.grid_shape
        # Compute spatial variance as proxy for incompressibility
        entropy_map = -np.sum(self.belief_field * np.log2(np.clip(self.belief_field, 1e-6, 1.0)), axis=-1)
        self.potential_field = entropy_map.astype(np.float32)
        return self.potential_field

    def self_modify(self):
        """Autopoietic Kolmogorov code extraction during L(S_t)."""
        super().self_modify()
        if self.observation_trace:
            self.synthesize_subroutine(self.observation_trace[-1])

    def synthesize_subroutine(self, observation: Observation) -> Optional[Tuple[str, str]]:
        """Mints a reusable Kolmogorov subroutine from high-compression observation chunks."""
        vis = observation.visible_cells
        if vis is not None and vis.size >= 4:
            # Check for regular repeating pattern
            if np.all(vis == vis[0, 0]):
                self.subroutine_counter += 1
                sig = f"sub_homogenous_{vis[0,0]}_{self.subroutine_counter}"
                code = f"def fill_uniform(grid, val={vis[0,0]}): return np.full_like(grid, val)"
                self.state.subroutine_library[sig] = code
                return sig, code
            elif np.array_equal(vis, np.fliplr(vis)):
                self.subroutine_counter += 1
                sig = f"sub_symmetry_h_{self.subroutine_counter}"
                code = "def mirror_h(grid): return np.fliplr(grid)"
                self.state.subroutine_library[sig] = code
                return sig, code
        return None

    def select_action(self, observation: Observation) -> Action:
        """Navigates toward high-information structural boundaries to compress reality."""
        self.synthesize_subroutine(observation)
        cy, cx = observation.position
        h, w = self.grid_shape
        
        # Seek regions that maximize compression yield
        self.compute_potential_field()
        moves = [Action.MOVE_UP, Action.MOVE_DOWN, Action.MOVE_LEFT, Action.MOVE_RIGHT, Action.OBSERVE]
        return np.random.choice(moves)

    def emit_messages(self, timestamp: int) -> List[Message]:
        """Broadcasts discovered Kolmogorov subroutines to the entire civilization."""
        messages = []
        for sig, code in list(self.state.subroutine_library.items())[-2:]:
            messages.append(Message(
                sender_id=self.agent_id,
                recipient_id="BROADCAST",
                pillar=self.pillar,
                timestamp=timestamp,
                msg_type=MessageType.SUBROUTINE_CODE,
                payload=code,
                confidence=0.95,
                entropy=0.05,
                metadata={"signature": sig}
            ))
        return messages


# ======================================================================================
# 4. THE SOVEREIGN CIVILIZATION ORCHESTRATOR
# ======================================================================================

class CivilizationPhase(Enum):
    """Global Phase State of the Sovereign Society."""
    COLD_ORDER = "Cold-Crystallized"         # Stable, low-entropy exploitation
    METABOLIC_FLOW = "Metabolic-Equilibrium" # Active exploration and learning
    SYSTEMIC_FEVER = "Systemic-Fever"        # Collective creative annealing (crisis discovery)
    TRANSCENDENCE = "Crystalline-Transcendence" # Unified multi-agent consensus achieved


class SovereignCivilization:
    """
    The Sovereign Multi-Agent Civilization.
    
    Coordinates the Classical, Quantum, Modern, and String Meta-Agents running
    simultaneously through the universal God Equation and tensor message fabric.
    """
    def __init__(
        self,
        grid_shape: Tuple[int, int] = (15, 15),
        custom_nodes: Optional[List[SovereignNode]] = None
    ):
        self.grid_shape = grid_shape
        self.fabric = RelativisticMessageFabric()
        self.step_count: int = 0
        self.global_phase = CivilizationPhase.METABOLIC_FLOW
        
        # Instantiate the 4 Sovereign Pillars if not custom provided
        if custom_nodes:
            self.nodes = {node.agent_id: node for node in custom_nodes}
        else:
            self.nodes = {
                "classical_prime": ClassicalPhysicsNode("classical_prime", grid_shape),
                "quantum_prime": QuantumBeliefNode("quantum_prime", grid_shape),
                "modern_prime": ModernMetabolicNode("modern_prime", grid_shape),
                "string_meta": StringMetaNode("string_meta", grid_shape),
            }
            
        # Register inboxes
        for agent_id in self.nodes:
            self.fabric.register_agent(agent_id)
            
        # Collective Civilization Memory & Metrics
        self.global_subroutine_archive: Dict[str, str] = {}
        self.civilization_energy_trace: List[float] = []
        self.civilization_entropy_trace: List[float] = []
        self.synergy_history: List[float] = []

    def step(self, observations: Dict[str, Observation]) -> Dict[str, Action]:
        """
        Executes one simultaneous God Equation time step across the civilization:
            For all agents i in parallel:
                M_t^i = fabric.fetch_inbox(i)
                S_{t+1}^i = U(S_t^i, A_t^i, O_t^i, M_t^i) + L(S_t^i)
                fabric.transmit(i.emit_messages())
                A_{t+1}^i = i.select_action(O_t^i)
        """
        self.step_count += 1
        actions: Dict[str, Action] = {}
        outgoing_messages: List[Message] = []
        
        # 1. PARALLEL PERCEPTION & GOD EQUATION UPDATE
        for agent_id, node in self.nodes.items():
            obs = observations.get(agent_id)
            if obs is None:
                # Default empty observation if not provided
                obs = Observation(
                    visible_cells=np.zeros((3, 3), dtype=int),
                    position=node.state.position,
                    reward=0.0
                )
                
            # Fetch tensor message packet M_t^i
            inbox_messages = self.fabric.fetch_inbox(agent_id)
            
            # Universal Update Rule: S_{t+1}^i = U(S_t^i, A_t^i, O_t^i, M_t^i) + L(S_t^i)
            # (Action is previous step's action, or default WAIT)
            prev_act = getattr(node, "_last_action", Action.WAIT)
            node.universal_update(prev_act, obs, inbox_messages)
            
            # Action Selection: A_{t+1}^i
            action = node.select_action(obs)
            node._last_action = action
            actions[agent_id] = action
            
            # Collect outgoing broadcasts M_{t+1}
            node_msgs = node.emit_messages(self.step_count)
            outgoing_messages.extend(node_msgs)
            
            # Sync discovered subroutines into Civilization Archive
            for sig, code in node.state.subroutine_library.items():
                self.global_subroutine_archive[sig] = code

        # 2. MESSAGE TRANSMISSION OVER THE RELATIVISTIC FABRIC
        for msg in outgoing_messages:
            self.fabric.transmit(msg)
            
        # 3. COLLECTIVE CIVILIZATION METRICS & PHASE SYNTHESIS
        self._update_civilization_metrics()
        
        return actions

    def _update_civilization_metrics(self):
        """Measures societal free energy, collective entropy, and emergent phase state."""
        total_energy = sum(node.state.energy for node in self.nodes.values())
        avg_entropy = np.mean([node.state.belief_entropy for node in self.nodes.values()])
        avg_temp = np.mean([node.state.temperature for node in self.nodes.values()])
        
        self.civilization_energy_trace.append(float(total_energy))
        self.civilization_entropy_trace.append(float(avg_entropy))
        
        # Synergy Index Γ = Diversity of Pillars * Aligned Information
        num_subroutines = len(self.global_subroutine_archive)
        synergy = float((total_energy / 100.0) * (1.0 + num_subroutines * 0.2) / (avg_entropy + 0.1))
        self.synergy_history.append(synergy)
        
        # Determine Global Civilization Phase
        if avg_temp > 1.2:
            self.global_phase = CivilizationPhase.SYSTEMIC_FEVER
        elif avg_entropy < 0.2 and num_subroutines >= 3:
            self.global_phase = CivilizationPhase.TRANSCENDENCE
        elif avg_entropy < 0.4:
            self.global_phase = CivilizationPhase.COLD_ORDER
        else:
            self.global_phase = CivilizationPhase.METABOLIC_FLOW

    def synthesize_consensus_field(self) -> np.ndarray:
        """
        Synthesizes the collective reality from all relativistic agent frames:
            Φ_consensus(x) = (1/N) Σ [ w_i · B_i(x) ]
        """
        h, w = self.grid_shape
        consensus = np.zeros((*self.grid_shape, 4), dtype=np.float32)
        total_weight = 0.0
        
        for node in self.nodes.values():
            weight = node.state.energy / (node.state.temperature + 0.1)
            consensus += weight * node.belief_field
            total_weight += weight
            
        if total_weight > 0:
            consensus /= total_weight
        return consensus

    def get_civilization_report(self) -> Dict[str, Any]:
        """Generates a complete telemetry report of the Sovereign Civilization."""
        return {
            "step": self.step_count,
            "global_phase": self.global_phase.value,
            "total_messages_routed": self.fabric.total_messages_routed,
            "total_energy": float(sum(node.state.energy for node in self.nodes.values())),
            "subroutines_discovered": len(self.global_subroutine_archive),
            "agents": {
                node_id: {
                    "pillar": node.pillar.value,
                    "energy": float(node.state.energy),
                    "temperature": float(node.state.temperature),
                    "divergence": float(node.state.divergence),
                    "viscosity": float(node.state.viscosity),
                    "entropy": float(node.state.belief_entropy),
                    "fever": node.fever_active,
                    "position": node.state.position,
                }
                for node_id, node in self.nodes.items()
            }
        }


# ======================================================================================
# 5. DEMONSTRATION & LIVE EXECUTION RUNNER
# ======================================================================================

def run_civilization_demo(steps: int = 15):
    """
    Executes a live simulation of the Sovereign Civilization:
    Watch the 4 sovereign agents perceive, communicate via M_t^i, experience fever
    phase shifts, mint Kolmogorov subroutines, and synthesize collective reality.
    """
    print("\n" + "=" * 80)
    print("      INITIALIZING THE SOVEREIGN CIVILIZATION: FIRST BREATH OF GOD")
    print("=" * 80)
    
    grid_shape = (10, 10)
    civ = SovereignCivilization(grid_shape=grid_shape)
    
    # Initialize mock universe with resources and obstacles
    universe = np.zeros(grid_shape, dtype=int)
    universe[2, 2] = CellType.RESOURCE.value
    universe[7, 7] = CellType.RESOURCE.value
    universe[4, 4] = CellType.OBSTACLE.value
    universe[4, 5] = CellType.OBSTACLE.value
    universe[5, 4] = CellType.OBSTACLE.value
    
    # Initial distinct agent starting positions
    start_positions = {
        "classical_prime": (1, 1),
        "quantum_prime": (8, 1),
        "modern_prime": (1, 8),
        "string_meta": (8, 8)
    }
    
    current_positions = copy.deepcopy(start_positions)
    
    for t in range(1, steps + 1):
        print(f"\n--- [TIME STEP t={t:02d}] ----------------------------------------------------")
        
        # Build relativistic observations for each node
        observations: Dict[str, Observation] = {}
        for agent_id, pos in current_positions.items():
            py, px = pos
            r = civ.nodes[agent_id].aperture
            y0, y1 = max(0, py - r), min(grid_shape[0], py + r + 1)
            x0, x1 = max(0, px - r), min(grid_shape[1], px + r + 1)
            vis = universe[y0:y1, x0:x1]
            
            reward = 5.0 if universe[py, px] == CellType.RESOURCE.value else 0.1
            observations[agent_id] = Observation(visible_cells=vis, position=pos, reward=reward)
            
        # Step the Civilization (God Equation + M_t^i Tensor Fabric)
        actions = civ.step(observations)
        
        # Apply movements in the mock universe
        for agent_id, act in actions.items():
            cy, cx = current_positions[agent_id]
            if act == Action.MOVE_UP:
                cy = max(0, cy - 1)
            elif act == Action.MOVE_DOWN:
                cy = min(grid_shape[0] - 1, cy + 1)
            elif act == Action.MOVE_LEFT:
                cx = max(0, cx - 1)
            elif act == Action.MOVE_RIGHT:
                cx = min(grid_shape[1] - 1, cx + 1)
            current_positions[agent_id] = (cy, cx)

        # Print Telemetry
        report = civ.get_civilization_report()
        print(f"Civilization Phase : {report['global_phase']} | Total Energy: {report['total_energy']:.1f} | Subroutines: {report['subroutines_discovered']}")
        print(f"Messages Transmitted: {report['total_messages_routed']}")
        
        for agent_id, data in report["agents"].items():
            fever_str = "FEVER" if data["fever"] else "OK"
            print(f"  - {agent_id:15s} [{data['pillar']:20s}] Pos={data['position']} | E={data['energy']:.1f} | H={data['entropy']:.2f} | T={data['temperature']:.2f} [{fever_str}]")

    print("\n" + "=" * 80)
    print("      CIVILIZATION TELEMETRY & CONSENSUS SYNTHESIS")
    print("=" * 80)
    consensus = civ.synthesize_consensus_field()
    print(f"Consensus Shape: {consensus.shape}")
    print(f"Discovered Subroutine Archive: {list(civ.global_subroutine_archive.keys())}")
    print("Sovereign Civilization successfully running under God Equation U(S_t, A_t, O_t, M_t) + L(S_t).")


if __name__ == "__main__":
    run_civilization_demo(steps=10)
