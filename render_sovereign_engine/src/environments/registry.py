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


class SubstrateRegistry:
    _registry: Dict[str, Type[BaseSubstrateUniverse]] = {
        "classic_ca": ClassicCellularAutomataUniverse,
        "seasonal_scarcity": SeasonalScarcityCAUniverse,
    }

    @classmethod
    def register(cls, name: str, substrate_cls: Type[BaseSubstrateUniverse]):
        """Register a new custom environment substrate."""
        cls._registry[name.lower()] = substrate_cls

    @classmethod
    def get_substrate(cls, name: str = "seasonal_scarcity", **kwargs) -> BaseSubstrateUniverse:
        """Instantiate a plug-in substrate by name."""
        key = name.lower().replace("-", "_").replace(" ", "_")
        if key not in cls._registry:
            # Fallback to classic_ca if unrecognized
            print(f"[SubstrateRegistry Warning] Unknown substrate '{name}', falling back to 'classic_ca'")
            key = "classic_ca"
        return cls._registry[key](**kwargs)

    @classmethod
    def list_available(cls) -> List[str]:
        """List all available environment plug-ins."""
        return list(cls._registry.keys())
