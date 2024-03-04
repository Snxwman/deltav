from enum import Enum

from spacetraders.config import CONFIG
from spacetraders.api.faction import Faction


class Defaults(Enum):
    # Config
    EMAIL = CONFIG.email

    # Spacetraders
    FACTION = Faction.default
    
