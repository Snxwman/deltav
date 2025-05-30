from typing import TypedDict

from spacetraders.api.enums import FactionSymbol


class EndpointData(TypedDict):
    ...


class RegisterAgentData(EndpointData, closed=True):
    symbol: str
    faction: FactionSymbol
