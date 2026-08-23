"""
========================================================================================
FEVER ANNEALING & VISCOUS MOMENTUM PROTOCOL (ARCHITECTURE 4)
========================================================================================
"Attention is not a while-loop. It is a potential well.
 The agent stays because physics holds it there. It leaves when the food runs out."

1. Tracks thermodynamic vitality rate dH/dt and sensory divergence Delta(t).
2. Calculates dynamic temperature tau(t) in [0.1, 3.0].
3. Viscosity Equation: Viscosity = |d(Divergence)/dt| / (SystemTemperature + 0.1).
4. Stagnation triggers limbic fever phase transition (delirium / stochastic mutation).
5. Discovery of new laws triggers cooling and crystallization.
========================================================================================
"""

import numpy as np
from collections import deque
from typing import Tuple, Dict, Any


class FeverProtocol:
    """
    Thermodynamic Temperature & Attention Viscosity State Machine.
    """
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        
        # State Variables
        self.temperature: float = 0.1         # Base cool temperature (tau)
        self.min_temperature: float = 0.1     # Crystalline ground state
        self.max_temperature: float = 3.0     # Maximum fever delirium
        self.fever_active: bool = False       # Critical phase indicator
        
        # Momentum & Viscosity
        self.viscosity: float = 1.0           # Attention viscosity
        self.stagnation_counter: int = 0      # Ticks without new discoveries
        self.divergence_history: deque = deque(maxlen=20)
        self.last_entropy: float = 1.0

    def update(
        self,
        dh_dt: float,
        current_entropy: float,
        newly_discovered_rules: int = 0
    ) -> Tuple[float, float, bool]:
        """
        Updates the metabolic temperature and attention viscosity.
        Returns: (temperature, viscosity, is_fever_active)
        """
        # 1. Measure divergence rate d(Delta)/dt
        delta_entropy = abs(current_entropy - self.last_entropy)
        self.divergence_history.append(delta_entropy)
        self.last_entropy = current_entropy
        
        mean_div_rate = float(np.mean(self.divergence_history)) if self.divergence_history else 0.01

        # 2. Check for Breakthrough / Discovery
        if newly_discovered_rules > 0:
            # Breakthrough cools the system rapidly into a crystalline ground state
            self.temperature = max(self.min_temperature, self.temperature * 0.4)
            self.stagnation_counter = 0
            self.fever_active = False
        else:
            # 3. Check for Stagnation / Trapping
            if dh_dt <= 0.1 and delta_entropy < 0.005:
                self.stagnation_counter += 1
            else:
                self.stagnation_counter = max(0, self.stagnation_counter - 1)

            # 4. Trigger Fever if stagnant for more than 15 steps
            if self.stagnation_counter >= 15:
                self.fever_active = True
                # Heat up dynamically
                self.temperature = min(self.max_temperature, self.temperature + 0.15)
            else:
                # Gradual ambient cooling
                if not self.fever_active:
                    self.temperature = max(self.min_temperature, self.temperature * 0.95)

        # 5. Compute Viscosity Equation:
        # Viscosity = |d(Div)/dt| / (Temperature + 0.1)
        self.viscosity = float(mean_div_rate / (self.temperature + 0.1))

        return (self.temperature, self.viscosity, self.fever_active)

    def force_fever(self):
        """Manual / limbic emergency trigger for phase transition."""
        self.fever_active = True
        self.temperature = min(self.max_temperature, self.temperature + 1.5)
        self.stagnation_counter = 20
