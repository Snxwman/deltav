from dataclasses import dataclass
from enum import Enum, unique
from http import HTTPMethod
from string import Template
from typing import Optional

@dataclass
class EndpointDataMixin:
    path: Template
    method: HTTPMethod
    auth_required: bool
    # fields: dict

@unique
class SpaceTradersAPIEndpoint(EndpointDataMixin, Enum):
    GAME = (
        Template('/'), 
        HTTPMethod.GET,
        False
    )
    GET_AGENTS = (
        Template('/agents?page=$page&limit=$limit'), 
        HTTPMethod.GET,
        False
    )
    GET_AGENT = (
        Template('/agents/$param'), 
        HTTPMethod.GET,
        False
    )
    GET_FACTIONS = (
        Template('/factions'), 
        HTTPMethod.GET,
        False
    )
    GET_FACTION = (
        Template('/factions/$param'), 
        HTTPMethod.GET,
        False
    )
    MY_AGENT = (
        Template('/my/agent'), 
        HTTPMethod.GET,
        True
    )
    MY_CONTRACTS = (
        Template('/my/contracts'), 
        HTTPMethod.GET,
        True
    )
    MY_CONTRACT = (
        Template('/my/contracts/$param'), 
        HTTPMethod.GET,
        True
    )
    ACCEPT_CONTRACT = (
        Template('/my/contracts/$param/accept'), 
        HTTPMethod.POST,
        True
    )
    DELIVER_CONTRACT = (
        Template('/my/contracts/$param/deliver'), 
        HTTPMethod.POST,
        True
    )
    FULFILL_CONTRACT = (
        Template('/my/contracts/$param/fulfill'), 
        HTTPMethod.POST,
        True
    )
    MY_SHIPS = (
        Template('/my/ships'), 
        HTTPMethod.GET,
        True
    )
    MY_SHIP = (
        Template('/my/ships/$param'), 
        HTTPMethod.GET,
        True
    )
    # Template('/my/ships/$param/cargo')
    # Template('/my/ships/$param/chart')
    # Template('/my/ships/$param/cooldown')
    # Template('/my/ships/$param/dock')
    # Template('/my/ships/$param/extract')
    # Template('/my/ships/$param/extract/survey')
    # Template('/my/ships/$param/jettison')
    # Template('/my/ships/$param/jump')
    # Template('/my/ships/$param/mounts')
    # Template('/my/ships/$param/mounts/install')
    # Template('/my/ships/$param/mounts/remove')
    # Template('/my/ships/$param/nav')
    # Template('/my/ships/$param/navigate')
    # Template('/my/ships/$param/negotiate/contract')
    # Template('/my/ships/$param/orbit')
    # Template('/my/ships/$param/purchase')
    # Template('/my/ships/$param/refine')
    # Template('/my/ships/$param/refuel')
    # Template('/my/ships/$param/scan/ships')
    # Template('/my/ships/$param/scan/systems')
    # Template('/my/ships/$param/scan/waypoints')
    # Template('/my/ships/$param/sell')
    # Template('/my/ships/$param/siphon')
    # Template('/my/ships/$param/survey')
    # Template('/my/ships/$param/transfer')
    # Template('/my/ships/$param/warp')
    REGISTER = (
        Template('/register'), 
        HTTPMethod.POST,
        False
    )
    GET_SYSTEMS = (
        Template('/systems'), 
        HTTPMethod.POST,
        False
    )
    GET_SYSTEM = (
        Template('/systems/$param'), 
        HTTPMethod.GET,
        False
    )
    GET_WAYPOINTS = (
        Template('/systems/$param/waypoints'), 
        HTTPMethod.GET,
        False
    )
    GET_WAYPOINT = (
        Template('/systems/$param/waypoints/$param2'), 
        HTTPMethod.GET,
        False
    )
    # Template('/systems/$param/waypoints/$param2/construction')
    # Template('/systems/$param/waypoints/$param2/construction/supply')
    # Template('/systems/$param/waypoints/$param2/jump-gate')
    # Template('/systems/$param/waypoints/$param2/market')
    # Template('/systems/$param/waypoints/$param2/shipyard')

    def with_params(self, p1: Optional[str], p2: Optional[str]=None) -> str:
        return self.path.substitute(param=p1, param2=p2)

    def with_paging(self, page: int, limit: int) -> str:
        return self.path.substitute(page=page, limit=limit)

