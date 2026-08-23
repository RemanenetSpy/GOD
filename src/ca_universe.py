"""
========================================================================================
CELLULAR AUTOMATA UNIVERSE: Emergent Dynamic Substrate Gateway
========================================================================================
Provides backward-compatible gateway to the modular Environments subsystem:
- Default: ClassicCellularAutomataUniverse (Epoch 1)
- Supports full SubstrateRegistry for plug-and-play worlds (Epoch 2: Seasonal Scarcity)
========================================================================================
"""

import sys
import os

# Include environments path
env_dir = os.path.join(os.path.dirname(__file__), 'environments')
if env_dir not in sys.path:
    sys.path.insert(0, env_dir)

from environments.base_substrate import BaseSubstrateUniverse
from environments.classic_ca import ClassicCellularAutomataUniverse
from environments.seasonal_scarcity_ca import SeasonalScarcityCAUniverse
from environments.registry import SubstrateRegistry

# Backward compatibility alias
CellularAutomataUniverse = ClassicCellularAutomataUniverse

__all__ = [
    "CellularAutomataUniverse",
    "BaseSubstrateUniverse",
    "ClassicCellularAutomataUniverse",
    "SeasonalScarcityCAUniverse",
    "SubstrateRegistry"
]
