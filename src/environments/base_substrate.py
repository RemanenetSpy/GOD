"""
========================================================================================
SOVEREIGN SUBSTRATE INTERFACE: Base Plug-and-Play Universe
========================================================================================
All physical environments, cellular substrates, continuous fields, and non-stationary
worlds inherit from this base class. This ensures any environment can be plugged in
or swapped out without altering agent cognitive engines or losing previous worlds.
========================================================================================
"""

from abc import ABC, abstractmethod
from typing import Dict, Tuple, Any, Optional
import numpy as np


class BaseSubstrateUniverse(ABC):
    """Abstract Base Class for all sovereign world environments."""

    def __init__(self, grid_shape: Tuple[int, int] = (25, 25), name: str = "BaseSubstrate"):
        self.grid_shape = grid_shape
        self.name = name
        self.step_count = 0

    @abstractmethod
    def reset(self, **kwargs):
        """Reset substrate to initial state."""
        pass

    @abstractmethod
    def step(self, agent_positions: Dict[str, Tuple[int, int]]) -> Dict[str, float]:
        """
        Advance substrate physics by one step.
        Returns:
            rewards: Dict[agent_id, float] thermodynamic energy yields.
        """
        pass

    @abstractmethod
    def get_observation(self, py: int, px: int, aperture: int) -> np.ndarray:
        """Extract local sensory patch centered at (py, px) with given aperture."""
        pass

    @abstractmethod
    def get_climate_telemetry(self) -> Dict[str, Any]:
        """Return real-time environmental conditions (season, temperature, scarcity)."""
        pass

    def deposit_energy_cache(self, py: int, px: int, amount: float = 10.0) -> bool:
        """Optional hook: Allow agent to deposit an energy cache/structure into the substrate."""
        return False
