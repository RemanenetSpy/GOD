"""
ARC Sovereign Living Organism (Autopoietic Survival Engine)
An embodied digital creature surviving inside ARC environments:
- Has a physical body at coordinate (r, c).
- Has metabolism & hunger: burns energy each tick.
- Starves and dies when energy <= 0.
- Eats food when placing correct pixels matching the environment's hidden physics.
- Has zero pre-coded physics rules or hypothesis templates.
- Driven by a sensory-motor connectome with Hebbian learning and Darwinian inheritance.
"""

import numpy as np
from typing import Tuple, List, Dict, Any, Optional


class SensoryMotorConnectome:
    """
    Plastic neural connectome mapping sensory observations to embodied actions.
    Reinforced by metabolic food ingestion (Hebbian reward).
    """

    def __init__(self, input_dim: int = 31, hidden_dim: int = 48, output_dim: int = 16, seed: Optional[int] = None):
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.output_dim = output_dim
        rng = np.random.default_rng(seed)

        # Synaptic weights
        self.W1 = rng.normal(0.0, 0.25, (input_dim, hidden_dim)).astype(np.float32)
        self.b1 = np.zeros(hidden_dim, dtype=np.float32)
        self.W2 = rng.normal(0.0, 0.25, (hidden_dim, output_dim)).astype(np.float32)
        self.b2 = np.zeros(output_dim, dtype=np.float32)

        # Eligibility traces for Hebbian synaptic plasticity
        self.trace_W1 = np.zeros_like(self.W1)
        self.trace_W2 = np.zeros_like(self.W2)
        self.learning_rate = 0.02

        # Last activations for trace updates
        self._last_input = None
        self._last_hidden = None
        self._last_action = None

    def forward(self, x: np.ndarray, temperature: float = 1.0) -> Tuple[int, np.ndarray]:
        """Runs forward pass and samples an action using Boltzmann exploration."""
        self._last_input = x.copy()
        # Hidden layer with tanh activation
        h = np.tanh(x @ self.W1 + self.b1)
        self._last_hidden = h.copy()

        # Output logits
        logits = h @ self.W2 + self.b2
        scaled_logits = logits / max(0.1, temperature)
        exp_logits = np.exp(scaled_logits - np.max(scaled_logits))
        probs = exp_logits / np.sum(exp_logits)

        # Sample action
        action = int(np.random.choice(len(probs), p=probs))
        self._last_action = action

        # Update synaptic eligibility traces
        self.trace_W1 *= 0.9
        self.trace_W1 += 0.1 * np.outer(x, h)
        grad_out = np.zeros(self.output_dim, dtype=np.float32)
        grad_out[action] = 1.0 - probs[action]
        self.trace_W2 *= 0.9
        self.trace_W2 += 0.1 * np.outer(h, grad_out)

        return action, probs

    def reinforce(self, reward: float):
        """Reinforces or depresses synapses based on metabolic feedback."""
        self.W1 += float(self.learning_rate * reward) * self.trace_W1
        self.W2 += float(self.learning_rate * reward) * self.trace_W2
        # Bound weights to prevent explosion
        np.clip(self.W1, -3.0, 3.0, out=self.W1)
        np.clip(self.W2, -3.0, 3.0, out=self.W2)

    def mutate(self, rate: float = 0.08, scale: float = 0.15) -> "SensoryMotorConnectome":
        """Spawns an offspring connectome with Gaussian mutation drift."""
        child = SensoryMotorConnectome(self.input_dim, self.hidden_dim, self.output_dim)
        mask1 = np.random.rand(*self.W1.shape) < rate
        child.W1 = self.W1.copy() + mask1 * np.random.normal(0.0, scale, self.W1.shape)
        mask2 = np.random.rand(*self.W2.shape) < rate
        child.W2 = self.W2.copy() + mask2 * np.random.normal(0.0, scale, self.W2.shape)
        child.b1 = self.b1.copy()
        child.b2 = self.b2.copy()
        return child

    def to_dict(self) -> Dict[str, Any]:
        return {
            "W1": self.W1.tolist(),
            "W2": self.W2.tolist(),
            "b1": self.b1.tolist(),
            "b2": self.b2.tolist(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SensoryMotorConnectome":
        c = cls()
        c.W1 = np.array(data["W1"], dtype=np.float32)
        c.W2 = np.array(data["W2"], dtype=np.float32)
        c.b1 = np.array(data["b1"], dtype=np.float32)
        c.b2 = np.array(data["b2"], dtype=np.float32)
        return c


class ArcLivingOrganism:
    """
    An embodied creature living on the ARC canvas.
    Survives by correctly predicting and painting the hidden environment.
    """

    # Action Mapping
    ACTION_MOVE_UP = 0
    ACTION_MOVE_DOWN = 1
    ACTION_MOVE_LEFT = 2
    ACTION_MOVE_RIGHT = 3
    ACTION_PAINT = 4
    ACTION_REST = 5
    # Actions 6 to 15: SELECT_COLOR 0 to 9

    def __init__(self, generation: int = 1, connectome: Optional[SensoryMotorConnectome] = None):
        self.generation = generation
        self.connectome = connectome or SensoryMotorConnectome()

        # Embodied State
        self.r: int = 0
        self.c: int = 0
        self.selected_color: int = 1
        self.energy: float = 100.0  # Max 150.0
        self.max_energy: float = 150.0
        self.is_alive: bool = True

        # Lifespan & Metabolic Stats
        self.lifespan_ticks: int = 0
        self.food_eaten: int = 0
        self.wrong_paints: int = 0
        self.puzzles_cleared: int = 0
        self.total_metabolic_reward: float = 0.0

    def reset_position(self, grid_h: int, grid_w: int):
        """Places the organism at the center of the canvas."""
        self.r = grid_h // 2
        self.c = grid_w // 2

    def perceive(self, input_canvas: np.ndarray, working_canvas: np.ndarray) -> np.ndarray:
        """
        Extracts local sensory receptive field (Tabula Rasa):
        - Local 3x3 patch around cursor on working canvas (9 values, normalized)
        - Local 3x3 patch around cursor on original input canvas (9 values, normalized)
        - Normalized body coordinates (r/H, c/W) (2 values)
        - Energy / Hunger bar (1 value)
        - One-hot encoding of currently selected color tool (10 values)
        Total dimension: 31 floats.
        """
        h, w = working_canvas.shape
        sensory = np.zeros(31, dtype=np.float32)

        # 1. Local 3x3 patch on working canvas
        idx = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nr, nc = self.r + dr, self.c + dc
                if 0 <= nr < h and 0 <= nc < w:
                    sensory[idx] = float(working_canvas[nr, nc]) / 9.0
                else:
                    sensory[idx] = -0.1  # Wall boundary signal
                idx += 1

        # 2. Local 3x3 patch on reference input canvas
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nr, nc = self.r + dr, self.c + dc
                if 0 <= nr < input_canvas.shape[0] and 0 <= nc < input_canvas.shape[1]:
                    sensory[idx] = float(input_canvas[nr, nc]) / 9.0
                else:
                    sensory[idx] = -0.1
                idx += 1

        # 3. Normalized body position
        sensory[18] = float(self.r) / max(1.0, float(h - 1))
        sensory[19] = float(self.c) / max(1.0, float(w - 1))

        # 4. Energy meter
        sensory[20] = float(self.energy) / self.max_energy

        # 5. One-hot selected color tool
        if 0 <= self.selected_color <= 9:
            sensory[21 + self.selected_color] = 1.0

        return sensory

    def step(self, sensory: np.ndarray, exploration_temp: float = 1.0) -> int:
        """Takes a metabolic breath, consults connectome, and emits an embodied action."""
        if not self.is_alive:
            return self.ACTION_REST

        self.lifespan_ticks += 1
        # Basal metabolic rate: breathing burns energy
        self.energy -= 0.15

        if self.energy <= 0.0:
            self.energy = 0.0
            self.is_alive = False
            return self.ACTION_REST

        action, _ = self.connectome.forward(sensory, temperature=exploration_temp)

        # Action-specific metabolic costs
        if action in (self.ACTION_MOVE_UP, self.ACTION_MOVE_DOWN, self.ACTION_MOVE_LEFT, self.ACTION_MOVE_RIGHT):
            self.energy -= 0.05
        elif action == self.ACTION_PAINT:
            self.energy -= 0.25
        elif action == self.ACTION_REST:
            self.energy += 0.05  # Rest slightly restores energy if not starved

        if self.energy <= 0.0:
            self.energy = 0.0
            self.is_alive = False

        return action

    def feed(self, amount: float):
        """Nutritional reward when placing a correct pixel."""
        self.energy = min(self.max_energy, self.energy + amount)
        self.food_eaten += 1
        self.total_metabolic_reward += amount
        self.connectome.reinforce(amount * 0.1)

    def punish(self, penalty: float):
        """Metabolic penalty when placing a toxic (incorrect) pixel."""
        self.energy -= penalty
        self.wrong_paints += 1
        self.total_metabolic_reward -= penalty
        self.connectome.reinforce(-penalty * 0.1)
        if self.energy <= 0.0:
            self.energy = 0.0
            self.is_alive = False

    def spawn_offspring(self) -> "ArcLivingOrganism":
        """Creates a mutated child inheriting the parent's synaptic connectome."""
        child_connectome = self.connectome.mutate()
        child = ArcLivingOrganism(
            generation=self.generation + 1,
            connectome=child_connectome
        )
        child.puzzles_cleared = self.puzzles_cleared
        return child
