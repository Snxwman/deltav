from typing import Any, TypedDict


class FactionInfo(TypedDict):
    callsign: str
    name: str
    description: str
    headquarters: str
    traits: list[dict[Any, Any]]
    is_recruiting: bool


class Faction:
    default: str = 'COSMIC'
    

    def __init__(self, faction_info: FactionInfo):
        self.callsign: str
