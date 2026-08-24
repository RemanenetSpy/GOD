"""
========================================================================================
SOVEREIGN SUBSTRATE REGISTRY: Plug-and-Play Environment Factory
========================================================================================
Enables dynamic plug-in and plug-out of diverse physical substrates (Classic CA,
Seasonal Scarcity CA, Continuous Lenia, Reaction-Diffusion, Wireworld) without
modifying any core cognitive agent logic.
========================================================================================
"""

from typing import Dict, Type, Any, List
from base_substrate import BaseSubstrateUniverse
from classic_ca import ClassicCellularAutomataUniverse
from seasonal_scarcity_ca import SeasonalScarcityCAUniverse
from lenia_substrate import LeniaContinuousUniverse


class SubstrateRegistry:
    _registry: Dict[str, Type[BaseSubstrateUniverse]] = {
        "classic_ca": ClassicCellularAutomataUniverse,
        "seasonal_scarcity": SeasonalScarcityCAUniverse,
        "lenia": LeniaContinuousUniverse,
        "continuous_lenia": LeniaContinuousUniverse,
    }

    @classmethod
    def register(cls, name: str, substrate_cls: Type[BaseSubstrateUniverse]):
        """Register a new custom environment substrate."""
        cls._registry[name.lower()] = substrate_cls

    @classmethod
    def get_substrate(cls, name: str = "lenia", **kwargs) -> BaseSubstrateUniverse:
        """Instantiate a plug-in substrate by name."""
        key = name.lower().replace("-", "_").replace(" ", "_")
        if key not in cls._registry:
            print(f"[SubstrateRegistry Warning] Unknown substrate '{name}', falling back to 'lenia'")
            key = "lenia"
        return cls._registry[key](**kwargs)

    @classmethod
    def list_available(cls) -> List[str]:
        """List all available environment plug-ins."""
        return list(cls._registry.keys())
