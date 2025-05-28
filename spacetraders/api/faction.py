from typing import TypedDict

class FactionInfo(TypedDict):
    callsign: str
    name: str
    description: str
    headquarters: str
    traits: list[dict]
    is_recruiting: bool

class Faction:
    default: str = 'COSMIC'
    
    def __init__(self, faction_info):
        self.callsign: str
