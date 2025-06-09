from enum import Enum, auto

from deltav.spacetraders.enums import serialize_by_name


@serialize_by_name 
class TokenType(Enum):
    """

    ACCOUNT
    AGENT
    NONE
    """

    ACCOUNT = auto()
    AGENT = auto()
    NONE = auto()
