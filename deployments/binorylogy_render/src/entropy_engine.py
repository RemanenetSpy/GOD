"""
Phase 27: Entropy Engine Interface

Abstract base class for all Sovereign Engines (Universal, Zero-Point, etc.).
Ensures Plug-and-Play compatibility for safe integration.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple, Optional
from enum import Enum

class PrescriptiveAction(Enum):
    """
    Standard prescriptive actions for all engines.
    Engines may interpret these differently or add specific metadata.
    """
    CONTINUE = "CONTINUE"
    BREACH = "BREACH"       # Λ > Σ×Ω (Choked)
    REFINERY = "REFINERY"   # Ω >> Σ (Flooded)
    INJECTION = "INJECTION" # Σ >> Ω (Starved)
    DISSOLVE = "DISSOLVE"   # Ex ≈ 0 (Solved/Dead)

class EntropyEngine(ABC):
    """
    Abstract interface for managing agent entropy, metabolism, and prescriptions.
    """
    
    @abstractmethod
    def update(self, observation: Any, action: Any, reward: float) -> PrescriptiveAction:
        """
        Process observation/action/reward and return a prescriptive action.
        This is the core "heartbeat" of the engine.
        """
        pass
    
    @abstractmethod
    def get_dashboard(self) -> Dict[str, Any]:
        """
        Return a dictionary of the current engine state.
        Must include at minimum: 'sigma', 'omega', 'lambda_', 'viability_ratio'.
        """
        pass
