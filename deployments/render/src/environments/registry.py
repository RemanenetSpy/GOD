"""
========================================================================================
SOVEREIGN SUBSTRATE REGISTRY: 7-Paradigm Plug-and-Play Multiverse Factory
========================================================================================
Enables dynamic registration and instantiation across all 7 cellular automata realms:
1. Classic Discrete CA (Conway / Wolfram)
2. Non-Stationary Seasonal Scarcity CA (Winter Famine & Stigmergy)
3. Continuous Wave Lenia (Solitons & Fluid Dynamics)
4. Reaction-Diffusion CA (Gray-Scott Turing Morphogenesis)
5. Multi-State Circuit CA (Wireworld Digital Logic & Gates)
6. Lattice Gas CA (FHP Hydrodynamics & Momentum Conservation)
7. Co-Evolutionary Ecological CA (Red Queen Predator-Prey Warfare)
========================================================================================
"""

from typing import Dict, Type, Any, List
from base_substrate import BaseSubstrateUniverse
from classic_ca import ClassicCellularAutomataUniverse
from seasonal_scarcity_ca import SeasonalScarcityCAUniverse
from lenia_substrate import LeniaContinuousUniverse
from reaction_diffusion import ReactionDiffusionUniverse
from wireworld_circuits import WireworldCircuitUniverse
from lattice_gas import LatticeGasUniverse
from red_queen import RedQueenArenaUniverse


class SubstrateRegistry:
    _registry: Dict[str, Type[BaseSubstrateUniverse]] = {
        # Realm 1: Classic Discrete CA
        "classic_ca": ClassicCellularAutomataUniverse,
        "classic": ClassicCellularAutomataUniverse,
        "conway": ClassicCellularAutomataUniverse,
        
        # Realm 2: Seasonal Scarcity CA
        "seasonal_scarcity": SeasonalScarcityCAUniverse,
        "seasonal": SeasonalScarcityCAUniverse,
        
        # Realm 3: Continuous Wave Lenia
        "lenia": LeniaContinuousUniverse,
        "continuous_lenia": LeniaContinuousUniverse,
        "lenia_waves": LeniaContinuousUniverse,
        
        # Realm 4: Reaction-Diffusion Turing Morphogenesis
        "reaction_diffusion": ReactionDiffusionUniverse,
        "turing": ReactionDiffusionUniverse,
        "gray_scott": ReactionDiffusionUniverse,
        
        # Realm 5: Multi-State Wireworld Digital Circuit
        "wireworld": WireworldCircuitUniverse,
        "circuits": WireworldCircuitUniverse,
        "digital_logic": WireworldCircuitUniverse,
        
        # Realm 6: Lattice Gas Hydrodynamics
        "lattice_gas": LatticeGasUniverse,
        "hydrodynamics": LatticeGasUniverse,
        "fhp_fluid": LatticeGasUniverse,
        
        # Realm 7: Red Queen Co-Evolution
        "red_queen": RedQueenArenaUniverse,
        "coevolution": RedQueenArenaUniverse,
        "predator_prey": RedQueenArenaUniverse,
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
