from dataclasses import dataclass
from enum import Enum, auto

from textual.app import CommandCallback


class CmdCategory(Enum):
    ACCOUNT = auto()
    AGENT = auto()
    SHIP = auto()
    CONTRACT = auto()
    WAYPOINT = auto()
    SYSTEM = auto()
    MARKET = auto()
    SERVER = auto()


@dataclass
class GameCmdMixin:
    category: CmdCategory
    title: str
    desc: str
    # callback: CommandCallback


class GameCmd(GameCmdMixin, Enum):
    CREATE_ACCOUNT = (
        CmdCategory.ACCOUNT,
        'Create Account',
        'Create a new SpaceTraders account',
    )
    REGISTER_AGENT = (
        CmdCategory.AGENT,
        'Register Agent',
        'Register a new Agent',
    )
    SERVER_STATUS = (
        CmdCategory.SERVER,
        'Server Status',
        'Show the current server status',
    )

