"""
========================================================================================
SOVEREIGN CIVILIZATION: Multi-Agent Relativistic Society & Tensor Communication
========================================================================================
Stand-alone module for 24/7 Render Cloud Server.
Governed by the God Equation: S_{t+1}^i = U(S_t^i, A_t^i, O_t^i, M_t^i) + L(S_t^i)
========================================================================================
"""

import copy
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from enum import Enum


class Action(Enum):
    MOVE_UP = 0
    MOVE_DOWN = 1
    MOVE_LEFT = 2
    MOVE_RIGHT = 3
    OBSERVE = 4
    WAIT = 5
    INTERACT = 6


@dataclass
class Observation:
    visible_cells: np.ndarray
    position: Tuple[int, int]
    reward: float = 0.0


class MessageType(Enum):
    BELIEF_TENSOR = "belief_tensor"
    TOPOLOGICAL_GRADIENT = "topological_grad"
    METABOLIC_BURST = "metabolic_burst"
    SUBROUTINE_CODE = "subroutine_code"
    FEVER_ALERT = "fever_alert"
    HYPOTHESIS_SUPERPOSITION = "hypothesis_sup"


class PillarArchetype(Enum):
    CLASSICAL = "Classical-Physics"
    QUANTUM = "Quantum-Superposed"
    MODERN = "Modern-Thermodynamic"
    STRING_META = "String-Topological"


@dataclass
class Message:
    sender_id: str
    recipient_id: str
    pillar: PillarArchetype
    timestamp: int
    msg_type: MessageType
    payload: Any
    confidence: float = 1.0
    entropy: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def summary(self) -> str:
        return f"[{self.pillar.value[:9]}] {self.sender_id} -> {self.recipient_id} : {self.msg_type.value} (conf={self.confidence:.2f})"


class RelativisticMessageFabric:
    def __init__(self):
        self.inboxes: Dict[str, List[Message]] = {}
        self.history: List[Message] = []
        self.total_messages_routed: int = 0

    def register_agent(self, agent_id: str):
        if agent_id not in self.inboxes:
            self.inboxes[agent_id] = []

    def transmit(self, message: Message):
        self.history.append(message)
        self.total_messages_routed += 1
        if len(self.history) > 200:
            self.history.pop(0)
            
        if message.recipient_id == "BROADCAST":
            for agent_id, inbox in self.inboxes.items():
                if agent_id != message.sender_id:
                    inbox.append(message)
        else:
            if message.recipient_id in self.inboxes:
                self.inboxes[message.recipient_id].append(message)

    def fetch_inbox(self, agent_id: str) -> List[Message]:
        if agent_id not in self.inboxes:
            return []
        messages = self.inboxes[agent_id]
        self.inboxes[agent_id] = []
        return messages


@dataclass
class SovereignState:
    agent_id: str
    pillar: PillarArchetype
    step: int = 0
    energy: float = 100.0
    dh_dt: float = 0.0
    temperature: float = 0.1
    viscosity: float = 1.0
    divergence: float = 1.0
    belief_entropy: float = 1.0
    position: Tuple[int, int] = (0, 0)
    subroutine_library: Dict[str, str] = field(default_factory=dict)
    fever_active: bool = False


class SovereignNode:
    def __init__(
        self,
        agent_id: str,
        pillar: PillarArchetype,
        grid_shape: Tuple[int, int] = (25, 25),
        aperture: int = 3
    ):
        self.agent_id = agent_id
        self.pillar = pillar
        self.grid_shape = grid_shape
        self.aperture = aperture
        self.state = SovereignState(agent_id=agent_id, pillar=pillar)
        self.belief_field = np.ones((*grid_shape, 4), dtype=np.float32) * 0.25
        self.potential_field = np.zeros(grid_shape, dtype=np.float32)
        self.divergence_history: List[float] = []
        self.stagnation_counter: int = 0
        self.fever_active: bool = False
        self._last_action: Action = Action.WAIT

    def update_beliefs(self, observation: Observation, messages: List[Message]):
        pos = observation.position
        self.state.position = pos
        h, w = self.grid_shape
        r = self.aperture
        y_min, y_max = max(0, pos[0] - r), min(h, pos[0] + r + 1)
        x_min, x_max = max(0, pos[1] - r), min(w, pos[1] + r + 1)
        
        vis = observation.visible_cells
        if vis is not None and vis.size > 0:
            for cy in range(y_min, y_max):
                for cx in range(x_min, x_max):
                    vy, vx = cy - (pos[0] - r), cx - (pos[1] - r)
                    if 0 <= vy < vis.shape[0] and 0 <= vx < vis.shape[1]:
                        cell_val = vis[vy, vx]
                        target_ch = int(cell_val) if 0 <= cell_val < 3 else 3
                        prior = self.belief_field[cy, cx]
                        likelihood = np.ones(4) * 0.05
                        likelihood[target_ch] = 0.85
                        post = prior * likelihood
                        s = post.sum()
                        self.belief_field[cy, cx] = post / s if s > 0 else prior

        for msg in messages:
            if msg.msg_type == MessageType.BELIEF_TENSOR and isinstance(msg.payload, np.ndarray):
                if msg.payload.shape == self.belief_field.shape:
                    alpha = msg.confidence * 0.35
                    self.belief_field = (1.0 - alpha) * self.belief_field + alpha * msg.payload
            elif msg.msg_type == MessageType.SUBROUTINE_CODE:
                sig = msg.metadata.get("signature", f"sub_{len(self.state.subroutine_library)}")
                self.state.subroutine_library[sig] = str(msg.payload)
            elif msg.msg_type == MessageType.FEVER_ALERT:
                self.state.temperature = min(2.5, self.state.temperature + 0.4)

        probs = np.clip(self.belief_field, 1e-7, 1.0)
        self.state.belief_entropy = float(-np.sum(probs * np.log2(probs)) / (h * w))

    def update_frame(self, action: Action, observation: Observation):
        old_div = self.state.divergence
        new_div = float(self.state.belief_entropy + (1.0 / (1.0 + max(0.0, observation.reward))))
        self.state.divergence = new_div
        div_deriv = abs(new_div - old_div)
        self.divergence_history.append(new_div)
        if len(self.divergence_history) > 20:
            self.divergence_history.pop(0)

        self.state.viscosity = float(div_deriv / (self.state.temperature + 1e-4))
        
        if len(self.divergence_history) >= 8:
            std = float(np.std(self.divergence_history[-8:]))
            if std < 0.02 and new_div > 0.4:
                self.stagnation_counter += 1
            else:
                self.stagnation_counter = max(0, self.stagnation_counter - 1)
            if self.stagnation_counter >= 4:
                self.fever_active = True
                self.state.fever_active = True
                self.state.temperature = min(3.0, self.state.temperature + 0.9)
                self.stagnation_counter = 0
            elif self.fever_active and std > 0.08:
                self.fever_active = False
                self.state.fever_active = False
                self.state.temperature = max(0.1, self.state.temperature * 0.5)

    def update_world_model(self, observation: Observation):
        profit = len(self.state.subroutine_library) * 0.5
        self.state.dh_dt = float(profit + observation.reward - (self.state.temperature * 0.15))
        self.state.energy = max(0.0, min(300.0, self.state.energy + self.state.dh_dt))

    def self_modify(self):
        if self.state.energy > 180.0 and self.aperture < 6:
            self.aperture += 1
            self.state.energy -= 15.0
        elif self.state.energy < 25.0 and self.aperture > 2:
            self.aperture -= 1

    def universal_update(self, action: Action, observation: Observation, messages: List[Message]):
        self.state.step += 1
        self.update_beliefs(observation, messages)
        self.update_frame(action, observation)
        self.update_world_model(observation)
        self.self_modify()

    def select_action(self, observation: Observation) -> Action:
        raise NotImplementedError

    def emit_messages(self, timestamp: int) -> List[Message]:
        return []


class ClassicalPhysicsNode(SovereignNode):
    def __init__(self, agent_id: str, grid_shape: Tuple[int, int] = (25, 25)):
        super().__init__(agent_id, PillarArchetype.CLASSICAL, grid_shape, aperture=3)

    def compute_potential_field(self) -> np.ndarray:
        h, w = self.grid_shape
        cost = 1.0 + self.belief_field[:, :, 2] * 40.0 - self.belief_field[:, :, 1] * 4.0
        cost = np.clip(cost, 0.1, 80.0)
        dist = np.ones((h, w), dtype=np.float32) * 1e5
        ty, tx = np.unravel_index(np.argmax(self.belief_field[:, :, 1] + self.belief_field[:, :, 3] * 0.5), (h, w))
        dist[ty, tx] = 0.0
        
        unvisited = set((y, x) for y in range(h) for x in range(w))
        while unvisited:
            curr = min(unvisited, key=lambda p: dist[p[0], p[1]])
            if dist[curr[0], curr[1]] >= 1e4:
                break
            unvisited.remove(curr)
            cy, cx = curr
            for dy, dx in [(-1,0), (1,0), (0,-1), (0,1)]:
                ny, nx = cy + dy, cx + dx
                if 0 <= ny < h and 0 <= nx < w and (ny, nx) in unvisited:
                    c = float(cost[ny, nx])
                    if dist[cy, cx] + c < dist[ny, nx]:
                        dist[ny, nx] = dist[cy, cx] + c
        self.potential_field = dist
        return dist

    def select_action(self, observation: Observation) -> Action:
        self.compute_potential_field()
        cy, cx = observation.position
        h, w = self.grid_shape
        best_act = Action.OBSERVE
        best_pot = float(self.potential_field[cy, cx])
        for act, ny, nx in [(Action.MOVE_UP, cy-1, cx), (Action.MOVE_DOWN, cy+1, cx), (Action.MOVE_LEFT, cy, cx-1), (Action.MOVE_RIGHT, cy, cx+1)]:
            if 0 <= ny < h and 0 <= nx < w:
                pot = float(self.potential_field[ny, nx]) + np.random.normal(0, self.state.temperature * 0.3)
                if pot < best_pot:
                    best_pot = pot
                    best_act = act
        return best_act

    def emit_messages(self, timestamp: int) -> List[Message]:
        return [Message(
            sender_id=self.agent_id,
            recipient_id="BROADCAST",
            pillar=self.pillar,
            timestamp=timestamp,
            msg_type=MessageType.TOPOLOGICAL_GRADIENT,
            payload=self.potential_field.copy(),
            confidence=0.85
        )]


class QuantumBeliefNode(SovereignNode):
    def __init__(self, agent_id: str, grid_shape: Tuple[int, int] = (25, 25)):
        super().__init__(agent_id, PillarArchetype.QUANTUM, grid_shape, aperture=4)

    def compute_potential_field(self) -> np.ndarray:
        unc = -np.sum(self.belief_field * np.log2(np.clip(self.belief_field, 1e-6, 1.0)), axis=-1)
        self.potential_field = unc.astype(np.float32)
        return self.potential_field

    def select_action(self, observation: Observation) -> Action:
        self.compute_potential_field()
        cy, cx = observation.position
        h, w = self.grid_shape
        best_act = Action.OBSERVE
        max_u = -1.0
        for act, ny, nx in [(Action.MOVE_UP, cy-1, cx), (Action.MOVE_DOWN, cy+1, cx), (Action.MOVE_LEFT, cy, cx-1), (Action.MOVE_RIGHT, cy, cx+1), (Action.OBSERVE, cy, cx)]:
            if 0 <= ny < h and 0 <= nx < w:
                u = float(self.potential_field[ny, nx])
                if u > max_u:
                    max_u = u
                    best_act = act
        return best_act

    def emit_messages(self, timestamp: int) -> List[Message]:
        return [Message(
            sender_id=self.agent_id,
            recipient_id="BROADCAST",
            pillar=self.pillar,
            timestamp=timestamp,
            msg_type=MessageType.BELIEF_TENSOR,
            payload=self.belief_field.copy(),
            confidence=0.80
        )]


class ModernMetabolicNode(SovereignNode):
    def __init__(self, agent_id: str, grid_shape: Tuple[int, int] = (25, 25)):
        super().__init__(agent_id, PillarArchetype.MODERN, grid_shape, aperture=2)

    def select_action(self, observation: Observation) -> Action:
        if self.fever_active or self.state.temperature > 1.2:
            return np.random.choice([Action.MOVE_UP, Action.MOVE_DOWN, Action.MOVE_LEFT, Action.MOVE_RIGHT, Action.OBSERVE])
        cy, cx = observation.position
        h, w = self.grid_shape
        best_act = Action.WAIT
        best_val = -100.0
        for act, ny, nx in [(Action.MOVE_UP, cy-1, cx), (Action.MOVE_DOWN, cy+1, cx), (Action.MOVE_LEFT, cy, cx-1), (Action.MOVE_RIGHT, cy, cx+1), (Action.INTERACT, cy, cx)]:
            if 0 <= ny < h and 0 <= nx < w:
                val = float(self.belief_field[ny, nx, 1] * 10.0 - self.belief_field[ny, nx, 2] * 8.0)
                if val > best_val:
                    best_val = val
                    best_act = act
        return best_act if best_act != Action.WAIT else Action.OBSERVE

    def emit_messages(self, timestamp: int) -> List[Message]:
        msgs = []
        if self.fever_active:
            msgs.append(Message(
                sender_id=self.agent_id,
                recipient_id="BROADCAST",
                pillar=self.pillar,
                timestamp=timestamp,
                msg_type=MessageType.FEVER_ALERT,
                payload=self.state.temperature,
                confidence=0.95
            ))
        return msgs


class StringMetaNode(SovereignNode):
    def __init__(self, agent_id: str, grid_shape: Tuple[int, int] = (25, 25)):
        super().__init__(agent_id, PillarArchetype.STRING_META, grid_shape, aperture=5)
        self.sub_count = 0

    def synthesize_subroutine(self, observation: Observation):
        vis = observation.visible_cells
        if vis is not None and vis.size >= 4:
            if np.all(vis == vis[0, 0]):
                self.sub_count += 1
                sig = f"sub_homogenous_{vis[0,0]}_{self.sub_count}"
                self.state.subroutine_library[sig] = f"def fill_uniform(val={vis[0,0]}): pass"
            elif np.array_equal(vis, np.fliplr(vis)):
                self.sub_count += 1
                sig = f"sub_mirror_h_{self.sub_count}"
                self.state.subroutine_library[sig] = "def mirror_horizontal(): pass"

    def select_action(self, observation: Observation) -> Action:
        self.synthesize_subroutine(observation)
        return np.random.choice([Action.MOVE_UP, Action.MOVE_DOWN, Action.MOVE_LEFT, Action.MOVE_RIGHT, Action.OBSERVE])

    def emit_messages(self, timestamp: int) -> List[Message]:
        msgs = []
        for sig, code in list(self.state.subroutine_library.items())[-2:]:
            msgs.append(Message(
                sender_id=self.agent_id,
                recipient_id="BROADCAST",
                pillar=self.pillar,
                timestamp=timestamp,
                msg_type=MessageType.SUBROUTINE_CODE,
                payload=code,
                confidence=0.95,
                metadata={"signature": sig}
            ))
        return msgs


class SovereignCivilization:
    def __init__(self, grid_shape: Tuple[int, int] = (25, 25)):
        self.grid_shape = grid_shape
        self.fabric = RelativisticMessageFabric()
        self.step_count = 0
        self.nodes: Dict[str, SovereignNode] = {
            "classical_prime": ClassicalPhysicsNode("classical_prime", grid_shape),
            "quantum_prime": QuantumBeliefNode("quantum_prime", grid_shape),
            "modern_prime": ModernMetabolicNode("modern_prime", grid_shape),
            "string_meta": StringMetaNode("string_meta", grid_shape),
        }
        for aid in self.nodes:
            self.fabric.register_agent(aid)
        self.global_subroutine_archive: Dict[str, str] = {}
        self.energy_trace: List[float] = []
        self.entropy_trace: List[float] = []

    def step(self, observations: Optional[Dict[str, Observation]] = None) -> Dict[str, Action]:
        self.step_count += 1
        actions: Dict[str, Action] = {}
        out_msgs: List[Message] = []
        
        if observations is None:
            # Generate internal grid simulation
            observations = {}
            for aid, node in self.nodes.items():
                dummy_vis = np.random.choice([0, 1, 2], size=(node.aperture*2+1, node.aperture*2+1), p=[0.75, 0.20, 0.05])
                observations[aid] = Observation(visible_cells=dummy_vis, position=node.state.position, reward=np.random.choice([0.1, 1.0, 4.0]))

        for aid, node in self.nodes.items():
            obs = observations.get(aid, Observation(np.zeros((3,3)), node.state.position))
            inbox = self.fabric.fetch_inbox(aid)
            node.universal_update(node._last_action, obs, inbox)
            act = node.select_action(obs)
            node._last_action = act
            actions[aid] = act
            out_msgs.extend(node.emit_messages(self.step_count))
            for sig, code in node.state.subroutine_library.items():
                self.global_subroutine_archive[sig] = code
                
        for msg in out_msgs:
            self.fabric.transmit(msg)
            
        tot_e = sum(n.state.energy for n in self.nodes.values())
        avg_h = np.mean([n.state.belief_entropy for n in self.nodes.values()])
        self.energy_trace.append(float(tot_e))
        self.entropy_trace.append(float(avg_h))
        return actions
