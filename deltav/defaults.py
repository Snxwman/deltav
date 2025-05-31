from enum import Enum

from deltav.config import CONFIG
from deltav.spacetraders.enums.faction import FactionSymbol


class Defaults(Enum):
    # Config
    EMAIL = CONFIG.email

    # Spacetraders
    FACTION = FactionSymbol.default
    
